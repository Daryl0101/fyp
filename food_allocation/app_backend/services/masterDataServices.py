from datetime import date
from itertools import chain
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import serializers
from app_backend.enums import ActionType, ActivityLevel, Gender, HalalStatus, SortOrder
from app_backend.models.master_data.family import Family
from app_backend.models.master_data.person import Person
from app_backend.models.master_data.product import Product
from app_backend.serializers.master_data.request.familyCreateUpdateRequest import (
    FamilyCreateUpdateRequest,
)
from app_backend.serializers.master_data.request.familySearchRequest import (
    FamilySearchRequest,
)
from app_backend.serializers.master_data.request.productCreateUpdateRequest import (
    ProductCreateUpdateRequest,
)
from app_backend.serializers.master_data.request.productSearchRequest import (
    ProductSearchRequest,
)
from app_backend.serializers.master_data.response.activityLevelDropdownResponse import (
    ActivityLevelDropdownResponse,
)
from app_backend.serializers.master_data.response.familyDetailResponse import (
    FamilyDetailResponse,
)
from app_backend.serializers.master_data.response.familySearchResponse import (
    FamilySearchItemResponse,
    FamilySearchResponse,
)
from app_backend.serializers.master_data.response.genderDropdownResponse import (
    GenderDropdownResponse,
)
from app_backend.serializers.master_data.response.productDetailResponse import (
    ProductDetailResponse,
)
from app_backend.serializers.master_data.response.productSearchResponse import (
    ProductSearchItemResponse,
    ProductSearchResponse,
)
from app_backend.services.systemReferenceServices import retrieveFoodCategoriesByIds
from app_backend.utils import enumToDict, isBlank, setCreateUpdateProperty


# region Products
def processSearchProducts(request):
    # region Parse request
    request_parsed = ProductSearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter
    products = Product.objects.all()

    if not isBlank(request_parsed.validated_data["product_no"]):
        products = products.filter(
            product_no__icontains=request_parsed.validated_data["product_no"]
        )

    if not isBlank(request_parsed.validated_data["product_name_or_description"]):
        products = products.filter(
            Q(
                name__icontains=request_parsed.validated_data[
                    "product_name_or_description"
                ]
            )
            | Q(
                description__icontains=request_parsed.validated_data[
                    "product_name_or_description"
                ]
            )
        )

    if request_parsed.validated_data["halal_status"] == HalalStatus.HALAL:
        products = products.filter(is_halal=True)
    elif request_parsed.validated_data["halal_status"] == HalalStatus.NON_HALAL:
        products = products.filter(is_halal=False)
    # endregion

    # region Sort
    fields = ProductSearchItemResponse().fields
    scso = "modified_at"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    products = products.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=products, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = ProductSearchResponse(
        data={
            "products": ProductSearchItemResponse(
                page.object_list, many=True, allow_null=True
            ).data,
            "total_page": paginator.num_pages,
            "current_page": page.number,
            "next_page": page.next_page_number() if page.has_next() else None,
            "previous_page": page.previous_page_number()
            if page.has_previous()
            else None,
            "total_record": paginator.count,
            "current_record": page.object_list.count(),
        }
    )
    # endregion
    return response_serializer.initial_data


def processViewProduct(request, product_id):
    if int(product_id) <= 0:
        raise serializers.ValidationError("Invalid Product ID")
    product = Product.objects.filter(id=product_id).first()
    if product is None:
        raise serializers.ValidationError("Invalid Product")
    response_serializer = ProductDetailResponse(data=product)
    return response_serializer.initial_data


@atomic
def processCreateProduct(request):
    result = False

    request_parsed = ProductCreateUpdateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    food_categories = retrieveFoodCategoriesByIds(
        ids=request_parsed.validated_data["food_categories"]
    )

    product = Product.objects.filter(
        name_iexact=request_parsed.validated_data["name"]
    ).first()
    if product is not None:
        raise serializers.ValidationError("Product already exists")

    product = Product(
        name=request_parsed.validated_data["name"],
        description=request_parsed.validated_data["description"],
        serving_size=request_parsed.validated_data["serving_size"],
        calorie=request_parsed.validated_data["calorie"],
        carbohydrate=request_parsed.validated_data["carbohydrate"],
        protein=request_parsed.validated_data["protein"],
        fat=request_parsed.validated_data["fat"],
        fiber=request_parsed.validated_data["fiber"],
        sugar=request_parsed.validated_data["sugar"],
        saturated_fat=request_parsed.validated_data["saturated_fat"],
        cholesterol=request_parsed.validated_data["cholesterol"],
        sodium=request_parsed.validated_data["sodium"],
        is_halal=request_parsed.validated_data["is_halal"],
    )
    setCreateUpdateProperty(product, request.user, ActionType.CREATE)
    product.save()

    product.food_categories.set(food_categories)
    product.product_no = "P" + str(product.id).zfill(5)
    product.save()

    result = True

    return result


def processUpdateProduct(request, product_id):
    result = False

    if product_id <= 0:
        raise serializers.ValidationError("Invalid Product ID")

    request_parsed = ProductCreateUpdateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    product = Product.objects.select_for_update().filter(id=product_id).first()
    if product is None:
        raise serializers.ValidationError("Invalid Product")

    food_categories = retrieveFoodCategoriesByIds(
        ids=request_parsed.validated_data["food_categories"]
    )

    product.name = request_parsed.validated_data["name"]
    product.description = request_parsed.validated_data["description"]
    product.serving_size = request_parsed.validated_data["serving_size"]
    product.calorie = request_parsed.validated_data["calorie"]
    product.carbohydrate = request_parsed.validated_data["carbohydrate"]
    product.protein = request_parsed.validated_data["protein"]
    product.fat = request_parsed.validated_data["fat"]
    product.fiber = request_parsed.validated_data["fiber"]
    product.sugar = request_parsed.validated_data["sugar"]
    product.saturated_fat = request_parsed.validated_data["saturated_fat"]
    product.cholesterol = request_parsed.validated_data["cholesterol"]
    product.sodium = request_parsed.validated_data["sodium"]
    product.is_halal = request_parsed.validated_data["is_halal"]
    product.food_categories.set(food_categories)
    setCreateUpdateProperty(product, request.user, ActionType.UPDATE)
    product.save()

    result = True

    return result


def processDeleteProduct(request, product_id):
    result = False

    if product_id <= 0:
        raise serializers.ValidationError("Invalid Product ID")
    product = Product.objects.filter(id=product_id).first()
    if product is None:
        raise serializers.ValidationError("Invalid Product")
    product.delete()

    result = True

    return result


def retrieveProductsByNo(product_no: str, is_validation_required: bool):
    if isBlank(product_no):
        raise serializers.ValidationError("Invalid Product No")
    products = Product.objects.filter(product_no__icontains=product_no)
    if is_validation_required:
        if products is None or len(products) <= 0:
            raise serializers.ValidationError("Invalid Products")
    return products


# endregion


# region Families
def processSearchFamilies(request):
    # region Parse request
    request_parsed = FamilySearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter
    families = Family.objects.all()

    if not isBlank(request_parsed.validated_data["family_no"]):
        families = families.filter(
            family_no__icontains=request_parsed.validated_data["family_no"]
        )

    if not isBlank(request_parsed.validated_data["family_or_person_name"]):
        members = Person.objects.filter(
            Q(
                first_name__icontains=request_parsed.validated_data[
                    "family_or_person_name"
                ]
            )
            | Q(
                last_name__icontains=request_parsed.validated_data[
                    "family_or_person_name"
                ]
            )
        )
        families = families.filter(
            Q(name__icontains=request_parsed.validated_data["family_or_person_name"])
            | Q(members__in=members)
        )

    if request_parsed.validated_data["halal_status"] == HalalStatus.HALAL:
        families = families.filter(is_halal=True)
    elif request_parsed.validated_data["halal_status"] == HalalStatus.NON_HALAL:
        families = families.filter(is_halal=False)
    # endregion

    # region Sort
    fields = FamilySearchItemResponse().fields
    scso = "modified_at"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    families = families.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=families, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = FamilySearchResponse(
        data={
            "families": FamilySearchItemResponse(
                page.object_list, many=True, allow_null=True
            ).data,
            "total_page": paginator.num_pages,
            "current_page": page.number,
            "next_page": page.next_page_number() if page.has_next() else None,
            "previous_page": page.previous_page_number()
            if page.has_previous()
            else None,
            "total_record": paginator.count,
            "current_record": page.object_list.count(),
        }
    )
    # endregion
    return response_serializer.initial_data


def processViewFamily(request, family_id):
    if family_id <= 0:
        raise serializers.ValidationError("Invalid Family ID")
    family = Family.objects.filter(id=family_id).first()
    if family is None:
        raise serializers.ValidationError("Invalid Family")
    response_serializer = FamilyDetailResponse(data=family)

    return response_serializer.initial_data


@atomic
def processCreateFamily(request):
    result = False

    request_parsed = FamilyCreateUpdateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    # members_request = request_parsed.new_members()
    # food_category_ids = [
    #     x
    #     for member_request in members_request
    #     for x in member_request["food_restrictions"]
    # ]
    food_categories = []
    if len(request_parsed.validated_data["food_restrictions"]) > 0:
        food_categories = retrieveFoodCategoriesByIds(
            ids=request_parsed.validated_data["food_restrictions"]
        )

    family = Family(
        name=request_parsed.validated_data["name"],
        is_halal=request_parsed.validated_data["is_halal"],
        household_income=request_parsed.validated_data["household_income"],
        phone_number=request_parsed.validated_data["phone_number"],
        address=request_parsed.validated_data["address"],
        calorie_discount=request_parsed.validated_data["calorie_discount"],
        total_member=len(request_parsed.new_members()),
        last_received_date=date.today(),  # TODO: Set last received date as today for now
    )
    setCreateUpdateProperty(family, request.user, ActionType.CREATE)

    family.save()

    family.family_no = "F" + str(family.id).zfill(5)

    family.food_restrictions.set(food_categories)

    family.save()

    for member_request in request_parsed.new_members():
        person = Person(
            first_name=member_request["first_name"],
            last_name=member_request["last_name"],
            gender=member_request["gender"],
            birthdate=member_request["birthdate"],
            height=member_request["height"],
            weight=member_request["weight"],
            activity_level=member_request["activity_level"],
            family=family,
        )
        setCreateUpdateProperty(person, request.user, ActionType.CREATE)

        person.save()

        # person.food_restrictions.set(
        #     [x for x in food_categories if x.id in member_request["food_restrictions"]]
        # )

        # person.save()

    result = True

    return result


@atomic
def processUpdateFamily(request, family_id):
    result = False

    if family_id <= 0:
        raise serializers.ValidationError("Invalid Family ID")
    family = Family.objects.select_for_update().filter(id=family_id).first()
    if family is None:
        raise serializers.ValidationError("Invalid Family")

    request_parsed = FamilyCreateUpdateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    # Retrieve all related food categories
    # members_request = request_parsed.validated_data["members"]
    # food_category_ids = [
    #     x
    #     for member_request in members_request
    #     for x in member_request["food_restrictions"]
    # ]
    food_categories = []
    if len(request_parsed.validated_data["food_restrictions"]) > 0:
        food_categories = retrieveFoodCategoriesByIds(
            ids=request_parsed.validated_data["food_restrictions"]
        )

    # Treat existing members
    existing_members_request = request_parsed.existing_members()
    existing_member_ids_request = set(x["id"] for x in existing_members_request)
    existing_members = family.members.select_for_update().filter(
        id__in=existing_member_ids_request
    )

    if len(existing_member_ids_request) != existing_members.count():
        raise serializers.ValidationError("Invalid member ID(s)")

    # Mapping family properties
    family.name = request_parsed.validated_data["name"]
    family.is_halal = request_parsed.validated_data["is_halal"]
    family.household_income = request_parsed.validated_data["household_income"]
    family.phone_number = request_parsed.validated_data["phone_number"]
    family.address = request_parsed.validated_data["address"]
    family.calorie_discount = request_parsed.validated_data["calorie_discount"]
    family.total_member = len(request_parsed.validated_data["members"])
    family.food_restrictions.set(food_categories)
    members_to_remove = family.members.exclude(id__in=existing_member_ids_request)
    members_to_remove.delete()
    setCreateUpdateProperty(family, request.user, ActionType.UPDATE)

    family.save()

    # Mapping existing members properties
    for existing_member in existing_members:
        existing_member_request = list(
            filter(lambda x: x["id"] == existing_member.id, existing_members_request)
        )[0]
        existing_member.first_name = existing_member_request["first_name"]
        existing_member.last_name = existing_member_request["last_name"]
        existing_member.gender = existing_member_request["gender"]
        existing_member.birthdate = existing_member_request["birthdate"]
        existing_member.height = existing_member_request["height"]
        existing_member.weight = existing_member_request["weight"]
        existing_member.activity_level = existing_member_request["activity_level"]
        # existing_member.food_restrictions.set(
        #     [
        #         x
        #         for x in food_categories
        #         if x.id in existing_member_request["food_restrictions"]
        #     ]
        # )
        setCreateUpdateProperty(existing_member, request.user, ActionType.UPDATE)

        existing_member.save()

    # Mapping new members properties
    for new_member_request in request_parsed.new_members():
        person = Person(
            first_name=new_member_request["first_name"],
            last_name=new_member_request["last_name"],
            gender=new_member_request["gender"],
            birthdate=new_member_request["birthdate"],
            height=new_member_request["height"],
            weight=new_member_request["weight"],
            activity_level=new_member_request["activity_level"],
            family=family,
        )
        setCreateUpdateProperty(person, request.user, ActionType.CREATE)

        person.save()

        # person.food_restrictions.set(
        #     [
        #         x
        #         for x in food_categories
        #         if x.id in new_member_request["food_restrictions"]
        #     ]
        # )
        # person.save()

    result = True

    return result


def processDeleteFamily(request, family_id):
    result = False

    if family_id <= 0:
        raise serializers.ValidationError("Invalid Family ID")
    family = Family.objects.filter(id=family_id).first()
    if family is None:
        raise serializers.ValidationError("Invalid Family")
    family.delete()

    result = True

    return result


def processRetrieveGenderDropdown(request):
    response_serializer = GenderDropdownResponse(data=enumToDict(Gender), many=True)
    response_serializer.is_valid()
    return response_serializer.data


def processRetrieveActivityLevelDropdown(request):
    response_serializer = ActivityLevelDropdownResponse(
        data=enumToDict(ActivityLevel), many=True
    )
    response_serializer.is_valid()
    return response_serializer.data


# endregion

# region Private Methods


# region Families
def __calculateBmi(birthdate: date, gender: Gender, height: float, weight: float):
    age = date.today().year - birthdate.year
    bmi = height / ((weight / 100) ** 2)
    pass


def __calculateCalorie():
    pass


# endregion

# endregion

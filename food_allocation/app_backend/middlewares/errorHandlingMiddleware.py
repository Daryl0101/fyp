# from email import errors
# from rest_framework import serializers
# from rest_framework.response import Response

# from app_backend.utils import baseResponseSerializerGenerator
# from app_backend.constants import SUCCESS_DICT, FAILED_DICT


# class ErrorHandlingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         response_dict = {"model": None, "errors": None, "status_name": None}
#         if response.status_code == 200:
#             response_dict["model"] = response.data
#             response_dict["status_name"] = SUCCESS_DICT["statusName"]
#         else:
#             response_dict["errors"] = response.data
#             response_dict["status_name"] = FAILED_DICT["statusName"]

#         # error_message = "Custom error message"
#         # response = JsonResponse({"error": error_message}, status=400)

#         return Response(
#             response_dict,
#             status=response.status_code,
#         )

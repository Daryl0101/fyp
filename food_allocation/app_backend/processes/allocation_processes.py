import decimal
import math
from typing import TypedDict
import numpy as np
import random
import copy
from enum import Enum
from ortools.linear_solver import pywraplp


class DataDictNutrients(TypedDict):
    calorie: int
    carbohydrate: int
    protein: int
    fat: int
    fiber: int
    sugar: int
    saturated_fat: int
    cholesterol: int
    sodium: int


class DataDictFamilies(TypedDict):
    id: int
    is_halal: bool
    food_restriction_ids: list[int]
    priority: decimal.Decimal
    nutrients: DataDictNutrients


class DataDictInventories(TypedDict):
    id: int
    qty: int
    is_halal: bool
    food_category_ids: list[int]
    max_qty_per_family: int
    nutrients: DataDictNutrients


class Inventory:
    nutrients: DataDictNutrients = {}  # Dict(nutrient, amount)

    def __init__(
        self,
        id,
        nutrients: DataDictNutrients,
        is_halal: bool,
        categories: list[int],
        quantity: int,
        max_quantity_per_family: int,
    ):
        self.id = id
        self.nutrients = nutrients
        self.is_halal = is_halal
        self.categories = categories
        self.quantity = quantity
        self.max_quantity_per_family = max_quantity_per_family
        for i in DataDictNutrients.__annotations__.keys():
            self.nutrients[i] = max(nutrients[i], 0) if i in nutrients.keys() else 0

    def get_nutrient_amount(self, nutrient: str):
        return self.nutrients[nutrient]

    def __repr__(self):
        # return str(self.__dict__)
        return str(self.id)


class Inventories:
    __inventories: list[Inventory] = []

    def __init__(self, inventories: list[Inventory]):
        self.__inventories = inventories

    def select_available_inventories(self):
        return [x for x in self.__inventories if x.quantity > 0]

    def select_all_inventories(self):
        return self.__inventories

    def available_quantity(self):
        return sum([x.quantity for x in self.select_available_inventories()])


class Beneficiary:
    nutrients: DataDictNutrients = {}  # Dict(nutrient, amount)
    allocated_inventories: dict[Inventory, int] = {}  # Dict(Inventory, qty)
    objective_value: decimal.Decimal = 0
    status_code: int

    def __init__(
        self,
        id,
        priority: decimal.Decimal,
        is_halal: bool,
        food_restrictions: list[int],
        nutrients: DataDictNutrients,
    ):
        self.id = id
        self.priority = priority
        self.is_halal = is_halal
        self.food_restrictions = food_restrictions
        self.nutrients = nutrients
        self.utility_value = priority / nutrients["calorie"]
        # for i in DataDictNutrients.__annotations__.keys():
        #     self.nutrients[i] = 0

    def __repr__(self):
        return str(self.__dict__)

    def subtract_nutrient_amount(
        self, nutrient: DataDictNutrients.__annotations__.keys, amount: decimal.Decimal
    ):
        self.nutrients[nutrient] = max(self.nutrients[nutrient] - amount, 0)


class SCIPResult(TypedDict):
    status: str  # "SUCCESS" | "FAILED"
    status_code: int
    num_of_variables: int
    num_of_constraints: int
    iterations: int
    wall_time: int
    objective_value: decimal.Decimal
    result: dict[Inventory, int]  # Dict(Inventory, qty)


class AllocationProcessResult(TypedDict):
    status: str  # "SUCCESS" | "FAILED"
    data: list[Beneficiary]
    log: str


# region Utils


# Selects item (weight / destroy_operator) with highest probability of selection
def select_highest_probability_item(dc: dict):
    max_val = max(dc.values())
    return random.choice([x for x in dc if dc[x] == max_val])


# Filters inventory candidate list based on HALAL status and food restrictions (CL)
def select_inventory_candidate_list(
    total_inventories: Inventories, is_halal: bool, food_restrictions: list[int]
):
    cl = [
        x
        for x in total_inventories.select_available_inventories()
        if not set(x.categories).intersection(set(food_restrictions))
    ]
    # Filter halal inventories only if is_halal is True
    if is_halal:
        cl = [x for x in cl if x.is_halal]
    return Inventories(cl)


def update_item_selection_probability(
    dc: dict, item_to_update, is_success: bool = True
):
    frac = dc[item_to_update].as_integer_ratio()
    new_item_probability = decimal.Decimal(frac[0] + (1 if is_success else 0)) / (
        frac[1] + 1
    )
    dc[item_to_update] = new_item_probability / (
        new_item_probability
        + sum([x[1] for x in dc.items() if x[0] is not item_to_update])
    )  # PS. this will not work if weight = 1.0 as it will not recognize 1 as 1.0, thus always make sure weight = 1


# endregion

# region Assignment Operators


def assignment_update(
    qty: int,
    inventory: Inventory,
    beneficiary: Beneficiary,
    allocated_inventories: dict[Inventory, int],
):
    inventory.quantity -= qty
    if inventory in allocated_inventories:
        allocated_inventories[inventory] += qty
    else:
        allocated_inventories[inventory] = qty
    for i in DataDictNutrients.__annotations__.keys():
        beneficiary.subtract_nutrient_amount(
            nutrient=i, amount=(int(qty) * inventory.get_nutrient_amount(i))
        )


def unassignment_update(
    inventory_candidate_list: Inventories, allocated_inventories: dict[Inventory, int]
):
    for m in list(
        set(inventory_candidate_list.select_all_inventories())
        & set(allocated_inventories.keys())
    ):
        m.quantity += allocated_inventories[m]


# endregion

# region Destroy Operators


# Remove the beneficiary with the highest demand.
def destroy_operator_1(
    served_beneficiaries: list[Beneficiary],
    tabu_beneficiaries: list[Beneficiary],
    total_inventories: Inventories,
):
    # returns if served_beneficiaries is empty
    if len(served_beneficiaries) <= 0:
        return
    choice = max(served_beneficiaries, key=lambda x: x.nutrients["calorie"])
    unassignment_update(
        inventory_candidate_list=total_inventories,
        allocated_inventories=choice.allocated_inventories,
    )
    served_beneficiaries.remove(choice)
    # tabu_beneficiaries.append(choice)


# Remove the beneficiary with the worst utility value. (highest utility value)
def destroy_operator_2(
    served_beneficiaries: list[Beneficiary],
    tabu_beneficiaries: list[Beneficiary],
    total_inventories: Inventories,
):
    # returns if served_beneficiaries is empty
    if len(served_beneficiaries) <= 0:
        return
    choice = max(served_beneficiaries, key=lambda x: x.utility_value)
    unassignment_update(
        inventory_candidate_list=total_inventories,
        allocated_inventories=choice.allocated_inventories,
    )
    served_beneficiaries.remove(choice)
    # tabu_beneficiaries.append(choice)


# Remove the beneficiary with the lowest priority. (highest priority value)
def destroy_operator_3(
    served_beneficiaries: list[Beneficiary],
    tabu_beneficiaries: list[Beneficiary],
    total_inventories: Inventories,
):
    # returns if served_beneficiaries is empty
    if len(served_beneficiaries) <= 0:
        return
    choice = max(served_beneficiaries, key=lambda x: x.priority)
    unassignment_update(
        inventory_candidate_list=total_inventories,
        allocated_inventories=choice.allocated_inventories,
    )
    served_beneficiaries.remove(choice)
    # tabu_beneficiaries.append(choice)


# Remove a random beneficiary.
def destroy_operator_4(
    served_beneficiaries: list[Beneficiary],
    tabu_beneficiaries: list[Beneficiary],
    total_inventories: Inventories,
):
    # returns if served_beneficiaries is empty
    if len(served_beneficiaries) <= 0:
        return
    choice = random.choice(served_beneficiaries)
    unassignment_update(
        inventory_candidate_list=total_inventories,
        allocated_inventories=choice.allocated_inventories,
    )
    served_beneficiaries.remove(choice)
    # tabu_beneficiaries.append(choice)


# Remove a percentage of served beneficiaries from the current solution. (Diversification)
def destroy_operator_5(
    loop_iter: int,
    served_beneficiaries: list[Beneficiary],
    tabu_beneficiaries: list[Beneficiary],
    total_inventories: Inventories,
):
    num_to_destroy = math.ceil((loop_iter / 10) * len(served_beneficiaries))
    for i in range(num_to_destroy):
        destroy_operator_4(
            served_beneficiaries=served_beneficiaries,
            tabu_beneficiaries=tabu_beneficiaries,
            total_inventories=total_inventories,
        )


# endregion


def repair_operator(
    total_beneficiaries: list[Beneficiary],
    served_beneficiaries: list[Beneficiary],
    tabu_beneficiaries: list[Beneficiary],
    total_inventories: Inventories,
    weights: dict,
) -> decimal.Decimal:
    unserved_beneficiaries = copy.deepcopy(
        [
            x
            for x in total_beneficiaries
            if x.id
            not in (
                [i.id for i in served_beneficiaries]
                + [j.id for j in tabu_beneficiaries]
            )
        ]
    )
    unserved_beneficiaries.sort(
        key=lambda x: x.utility_value, reverse=True
    )  # reverse=False to pop the lowest utility value (highest priority) from the last item in the list
    while len(unserved_beneficiaries) > 0:
        chosen_beneficiary = unserved_beneficiaries.pop()
        chosen_weight = select_highest_probability_item(dc=weights)
        # chosen_beneficiary.set_nutrient_calorie(chosen_weight)

        # Step 1
        inventory_candidate_list = select_inventory_candidate_list(
            total_inventories=total_inventories,
            is_halal=chosen_beneficiary.is_halal,
            food_restrictions=chosen_beneficiary.food_restrictions,
        )

        if inventory_candidate_list.available_quantity() > 0:
            scip_result = scip(
                flexibility=chosen_weight,
                inventories=inventory_candidate_list.select_all_inventories(),
                beneficiary=chosen_beneficiary,
            )  # Allocate this beneficiary using SCIP
            chosen_beneficiary.objective_value = decimal.Decimal(
                scip_result["objective_value"]
            )
            chosen_beneficiary.status_code = scip_result["status_code"]
            if len(scip_result["result"]) > 0:  # feasible case
                allocated_inventories = {}
                for i in scip_result["result"]:
                    assignment_update(
                        qty=scip_result["result"][i],
                        inventory=i,
                        beneficiary=chosen_beneficiary,
                        allocated_inventories=allocated_inventories,
                    )
                chosen_beneficiary.allocated_inventories = allocated_inventories
                # chosen_beneficiary.objective_value = scip_result["objective_value"]
                served_beneficiaries.append(chosen_beneficiary)
                update_item_selection_probability(
                    dc=weights, item_to_update=chosen_weight, is_success=True
                )
            else:
                update_item_selection_probability(
                    dc=weights, item_to_update=chosen_weight, is_success=False
                )  # KIV, pending testing
                tabu_beneficiaries.append(chosen_beneficiary)

    return sum([x.priority * x.objective_value for x in served_beneficiaries])


# * len(tabu_beneficiaries)


def scip(
    flexibility: decimal.Decimal, inventories: list[Inventory], beneficiary: Beneficiary
):
    solver_time_limit = 10  # Time limit in seconds.
    solver_gap_limit = 0  # .05  # Acceptable difference between the best known solution found by the solver and the optimal solution, put 0 to unset. (0 - 1)
    solver_output_enabled = True  # Enable solver output.
    nutrient_coefficients: DataDictNutrients = {
        "calorie": 3,
        "carbohydrate": 2,
        "protein": 2,
        "fat": 2,
        "fiber": 2,
        "sugar": 2,
        "saturated_fat": 2,
        "cholesterol": 1,
        "sodium": 1,
    }

    # Create the solver and naming it.
    solver = pywraplp.Solver("solver", pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
    if not solver:
        print("Could not create the solver.")
    if solver_output_enabled:
        solver.EnableOutput()

    # Set solver parameters.
    solver.set_time_limit(solver_time_limit * 1000)
    solver_params = None
    if solver_gap_limit and solver_gap_limit > decimal.Decimal(0.0):
        solver_params = pywraplp.MPSolverParameters()
        solver_params.SetDoubleParam(solver_params.RELATIVE_MIP_GAP, solver_gap_limit)

    # Declare an array to hold our variables (qty).
    foods: list[pywraplp.Variable] = [
        solver.IntVar(
            0,
            (min(inventory.quantity, inventory.max_quantity_per_family)),
            str(inventory.id),
        )
        for inventory in inventories
    ]

    slacks: list[pywraplp.Variable] = [
        solver.NumVar(
            0,
            float(beneficiary.nutrients[nutrient] * flexibility),
            f"{nutrient}_slack",
        )
        for nutrient in beneficiary.nutrients
    ]

    print("Number of variables =", solver.NumVariables())

    # Create the constraints, one per nutrient.
    constraints: list[pywraplp.Constraint] = []
    for i, nutrient in enumerate(beneficiary.nutrients):
        constraints.append(
            solver.Add(
                0
                <= sum(
                    foods[j] * float(inventory.nutrients[nutrient])
                    for j, inventory in enumerate(inventories)
                )
                + slacks[i]
                == float(beneficiary.nutrients[nutrient])
            )
        )

    constraints.append(
        solver.Add(solver.Sum(foods[j] for j in range(len(inventories))) >= 1)
    )

    print("Number of constraints =", solver.NumConstraints())

    # Create the objective function: Maximize the sum of food nutrients.
    objective: pywraplp.Objective = solver.Objective()
    for i, nutrient in enumerate(beneficiary.nutrients):
        objective.SetCoefficient(slacks[i], nutrient_coefficients[nutrient])
    objective.SetMinimization()

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve(solver_params) if solver_params else solver.Solve()

    # Check that the problem has an optimal solution.
    # if status != solver.OPTIMAL:
    #     print("The problem does not have an optimal solution!")
    #     if status == solver.FEASIBLE:
    #         print("A potentially suboptimal solution was found.")
    #     else:
    #         print("The solver could not solve the problem.")
    # else:
    #     print("Solved!")
    #     for i, food in enumerate(foods):
    #         if food.solution_value() > 0.0:
    #             print(f"{inventories[i].id}: {food.solution_value()}")

    result: SCIPResult = {
        "status": (
            "SUCCESS" if status in [solver.OPTIMAL, solver.FEASIBLE] else "FAILED"
        ),
        "status_code": status,
        "num_of_variables": solver.NumVariables(),
        "num_of_constraints": solver.NumConstraints(),
        "iterations": solver.Iterations(),
        "wall_time": solver.WallTime(),
        "objective_value": solver.Objective().Value(),
        "result": dict(
            (inventory, x.solution_value())
            for inventory, x in zip(inventories, foods)
            if x.solution_value() != 0
        ),
    }
    return result


def adaptive_heuristic(
    total_beneficiaries: list[Beneficiary],
    total_inventories: list[Inventories],
    diversification: int,
):
    solutions = []
    served_beneficiaries: list[Beneficiary] = []
    tabu_beneficiaries: list[Beneficiary] = []
    destroy_operators = {
        destroy_operator_1: decimal.Decimal(1 / 4),
        destroy_operator_2: decimal.Decimal(1 / 4),
        destroy_operator_3: decimal.Decimal(1 / 4),
        destroy_operator_4: decimal.Decimal(1 / 4),
    }
    tabu_destroy_operators = []
    weights = {
        # decimal.Decimal(0): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.1): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.2): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.3): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.4): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.5): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.6): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.7): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.8): decimal.Decimal(1 / 11),
        # decimal.Decimal(0.9): decimal.Decimal(1 / 11),
        # decimal.Decimal(1): decimal.Decimal(1 / 11),
        decimal.Decimal(1): decimal.Decimal(2 / 6),
        decimal.Decimal(0.9): decimal.Decimal(1 / 6),
        decimal.Decimal(0.8): decimal.Decimal(1 / 6),
        decimal.Decimal(0.7): decimal.Decimal(1 / 6),
        decimal.Decimal(0.6): decimal.Decimal(1 / 6),
        decimal.Decimal(0.5): decimal.Decimal(1 / 6),
    }
    inventories = Inventories(total_inventories)
    current_solution = repair_operator(
        total_beneficiaries=total_beneficiaries,
        served_beneficiaries=served_beneficiaries,
        tabu_beneficiaries=tabu_beneficiaries,
        total_inventories=inventories,
        weights=weights,
    )
    best_solution = current_solution
    solutions.append(current_solution)
    current_served_beneficiaries = copy.deepcopy(served_beneficiaries)
    for i in range(diversification - 1):  # Diversification
        destroy_operator_5(
            loop_iter=i + 1,
            served_beneficiaries=current_served_beneficiaries,
            tabu_beneficiaries=tabu_beneficiaries,
            total_inventories=inventories,
        )
        j = 0
        while j <= 4:
            chosen_destroy_operator = select_highest_probability_item(
                dc={
                    x: destroy_operators[x]
                    for x in destroy_operators
                    if x not in tabu_destroy_operators
                }
            )
            chosen_destroy_operator(
                served_beneficiaries=current_served_beneficiaries,
                tabu_beneficiaries=tabu_beneficiaries,
                total_inventories=inventories,
            )
            current_solution = repair_operator(
                total_beneficiaries=total_beneficiaries,
                served_beneficiaries=current_served_beneficiaries,
                tabu_beneficiaries=tabu_beneficiaries,
                total_inventories=inventories,
                weights=weights,
            )
            if current_solution < best_solution:  # better solution found
                best_solution = current_solution
                solutions.append(best_solution)
                served_beneficiaries = copy.deepcopy(current_served_beneficiaries)
                update_item_selection_probability(
                    dc=destroy_operators,
                    item_to_update=chosen_destroy_operator,
                    is_success=True,
                )
                tabu_destroy_operators.clear()
                j = 0
            else:
                current_solution = best_solution
                current_served_beneficiaries = copy.deepcopy(served_beneficiaries)
                if chosen_destroy_operator is not destroy_operator_4:
                    tabu_destroy_operators.append(chosen_destroy_operator)
                j += 1
            tabu_beneficiaries.clear()
    return (served_beneficiaries, best_solution, solutions)


def allocationProcess(
    # min_inventory_category,
    inventories: list[DataDictInventories],
    families: list[DataDictFamilies],
    diversification: int,
):
    inventories_data = []
    for i in inventories:
        inventories_data.append(
            Inventory(
                id=i["id"],
                nutrients=i["nutrients"],
                is_halal=i["is_halal"],
                categories=i["food_category_ids"],
                quantity=i["qty"],
                max_quantity_per_family=i["max_qty_per_family"],
            )
        )
    families_data = []
    for i in families:
        families_data.append(
            Beneficiary(
                id=i["id"],
                priority=i["priority"],
                is_halal=i["is_halal"],
                food_restrictions=i["food_restriction_ids"],
                nutrients=i["nutrients"],
            )
        )
    result: AllocationProcessResult = {"status": None, "data": None, "log": ""}
    try:
        heuristic_result, objective_value, objective_value_history = adaptive_heuristic(
            total_inventories=inventories_data,
            total_beneficiaries=families_data,
            diversification=diversification,
        )
        if len(heuristic_result) == 0:
            raise Exception("Heuristic failed to allocate inventories")
        result["status"] = "SUCCESS"
        result["data"] = heuristic_result
        result["log"] = (
            f"Objective Value: {'{0:.2f}'.format(objective_value)}\nObjective Value History: {[float(i) for i in objective_value_history]}"
        )
    except Exception as e:
        result["status"] = "FAILED"
        result["log"] = str(e)
    return result

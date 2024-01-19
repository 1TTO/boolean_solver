import math
import re

from flask_cors import CORS, cross_origin
from flask import Flask, request

not_op = ["¬", "!"]
and_op = ["∧", "&"]
or_op = ["∨", "|"]
xor_op = ["⊕", "^"]
imp_op = ["→", ">"]
bij_op = ["↔", "-"]
# The sequence of concatenating all operands regards the fact of stronger binding.
# e.g. 'not' binds stronger than or -> un_op + bin_op
# e.g. 'and' binds stronger than xor -> and_op + xor_op
bin_op = and_op + or_op + xor_op + imp_op + bij_op
un_op = not_op
all_op = un_op + bin_op
delimiter_start = ["("]
delimiter_end = [")"]

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class Assignment(object):
    def __init__(self, expression, assignment):
        self.assignment = assignment
        self.boolean_value = evaluate_boolean_expression(expression, assignment)

    def get_assigment(self):
        return self.assignment

    def get_boolean_value(self):
        return self.boolean_value

    @staticmethod
    def get_boolean_value_by_assigment(assignments, assignment):
        for assignment_obj in assignments:
            if assignment_obj.get_assigment() == assignment:
                return assignment_obj.get_boolean_value()

        return None


def evaluate_boolean_expression(expression, assigment):
    operation = get_first_operation_and_operands(expression)

    if operation[1] is None and operation[2] is None:
        return assigment[operation[0]]
    elif operation[1] in not_op:
        return False if evaluate_boolean_expression(operation[0], assigment) else True

    first_ev_ex = evaluate_boolean_expression(operation[0], assigment)
    second_ev_ex = evaluate_boolean_expression(operation[2], assigment)

    if operation[1] in and_op:
        return True if first_ev_ex and second_ev_ex else False
    elif operation[1] in or_op:
        return True if first_ev_ex or second_ev_ex else False
    elif operation[1] in xor_op:
        return True if first_ev_ex != second_ev_ex else False
    elif operation[1] in imp_op:
        return False if first_ev_ex and not second_ev_ex else True
    elif operation[1] in bij_op:
        return True if first_ev_ex == second_ev_ex else False
    else:
        raise ValueError("Unknown operator")


def get_first_operation_and_operands(expression):
    if len(expression) == 1:
        return [expression[0], None, None]
    elif expression[0] in un_op:
        return [expression[1:len(expression)] if expression[1] not in delimiter_start
                else expression[2:len(expression) - 1], expression[0], None]
    else:
        index = 0
        delimiter_count = 0

        while index != 0 and delimiter_count != 0 or (index < len(expression) and (index == 0 or (expression[index].isalpha() and index == 1))):
            if expression[index] in delimiter_start:
                delimiter_count += 1
            elif expression[index] in delimiter_end:
                delimiter_count -= 1

            index += 1

        if index == len(expression):
            return get_first_operation_and_operands(expression[1:len(expression) - 1])

        first_operand = expression[0:index] if expression[0] not in delimiter_start else expression[1:index - 1]
        second_operand = expression[index + 1:len(expression)] if expression[index + 1] not in delimiter_start else expression[index + 2:len(expression) - 1]

        return [first_operand, expression[index], second_operand]


def get_assignments_of_all_combinations(expression, variables):
    assignments = []

    for i in range(0, 2 ** len(variables)):
        combination = dict()
        binary_counter = bin(i).replace("0b", "")
        binary_counter = ("0" * (len(variables) - len(binary_counter))) + binary_counter

        for j, variable in enumerate(variables):
            combination[variable] = binary_counter[j] == '1'

        assignments.append(Assignment(expression, combination))

    return assignments


def get_truth_table(variables, assignments, only_true, only_false):
    truth_table = [variables + ["="]]

    for assignment_obj in assignments:
        if (only_true and assignment_obj.get_boolean_value()) or (not only_true and not only_false) \
                or (only_false and not assignment_obj.get_boolean_value()):
            assigment_values = [1 if assignment_obj.get_assigment()[var] else 0 for var in variables]
            truth_table.append(assigment_values + [1 if assignment_obj.get_boolean_value() else 0])

    return truth_table


def get_kv_binary_var_assignments(variables_amount):
    kv_var_assignments = ["01"] if variables_amount >= 1 else []

    for i in range(1, variables_amount):
        for j, kv_assignment in enumerate(kv_var_assignments):
            kv_var_assignments[j] = kv_assignment + kv_assignment[::-1]

        new_kv_var_assignment = "0" * 2**i
        new_kv_var_assignment = new_kv_var_assignment + "1" * 2**i

        kv_var_assignments.append(new_kv_var_assignment)

    return kv_var_assignments


def get_kv_diagram(variables, assignments, custom_kv_h_var_seq=None, custom_kv_v_var_seq=None):
    horizontal_variables = variables[:math.ceil(len(variables) / 2)] if custom_kv_h_var_seq is None else custom_kv_h_var_seq
    vertical_variables = variables[math.ceil(len(variables) / 2):] if custom_kv_v_var_seq is None else custom_kv_v_var_seq
    horizontal_kv_var_assignments = get_kv_binary_var_assignments(len(horizontal_variables))
    vertical_kv_var_assignments = get_kv_binary_var_assignments(len(vertical_variables))
    kv_diagram = [[-1 for _ in range(2**len(horizontal_variables))] for _ in range(2 ** len(vertical_variables))]

    for v_index in range(0, 2**len(vertical_variables)):
        for h_index in range(0, 2**len(horizontal_variables)):
            current_assignment = dict()

            for i, hor_var in enumerate(horizontal_variables):
                current_assignment[hor_var] = int(horizontal_kv_var_assignments[i][h_index])

            for i, vert_var in enumerate(vertical_variables):
                current_assignment[vert_var] = int(vertical_kv_var_assignments[i][v_index])

            kv_diagram[v_index][h_index] = 1 if Assignment.get_boolean_value_by_assigment(assignments, current_assignment) else 0

    return kv_diagram


def set_operation_brackets(expression):
    for op in all_op:
        edited = True
        continue_index = 0

        while edited and continue_index < len(expression):
            edited = False

            for i in range(continue_index, len(expression)):
                if expression[i] == op:
                    j = i + 1
                    opened_delimiter = 0

                    while j < len(expression):
                        if expression[j] in delimiter_start:
                            opened_delimiter += 1
                        elif expression[j] in delimiter_end and opened_delimiter > 0:
                            opened_delimiter -= 1
                        elif opened_delimiter == 0 and j != i + 1 and expression[j - 1] not in un_op:
                            break
                        j += 1

                    continue_index = i + 2
                    edited = True
                    expression = expression[0:j] + delimiter_end[0] + expression[j:len(expression)]

                    if expression[i] in un_op:
                        expression = expression[0:i] + delimiter_start[0] + expression[i:len(expression)]
                    else:
                        j = i - 1
                        while j > 0:
                            if expression[j] in delimiter_start and opened_delimiter < 0:
                                opened_delimiter += 1

                                if opened_delimiter == 0:
                                    break
                            elif expression[j] in delimiter_end:
                                opened_delimiter -= 1
                            elif opened_delimiter == 0:
                                break
                            j -= 1

                        expression = expression[0:j] + delimiter_start[0] + expression[j:len(expression)]
                    break

    return expression


@app.route('/', methods=['POST'])
@cross_origin()
def run():
    try:
        data = request.get_json()
        result = {"error": "", "truthTable": "", "kvDiagram": ""}
        expression = data["expression"]
        only_true = bool(data["onlyTrue"])
        only_false = bool(data["onlyFalse"])
        custom_var_seq = None if data["customVarSeq"][0] == '' else data["customVarSeq"]
        custom_kv_h_var_seq = None if data["horizontalVars"][0] == '' else data["horizontalVars"]
        custom_kv_v_var_seq = None if data["verticalVars"][0] == '' else data["verticalVars"]

        if custom_var_seq is None:
            variables = list(set(re.sub(r"[^a-zA-Z]", "", expression)))
            variables.sort()
        else:
            expression_variables = list(set(re.sub(r"[^a-zA-Z]", "", expression)))
            if all(v in custom_var_seq for v in expression_variables):
                variables = custom_var_seq
            else:
                return {"error": "Custom-variables are not included in term-variables!"}

        if len(variables) > 10:
            return {"error": "You are not allowed to use more than 10 variables"}

        expression = set_operation_brackets(expression)
        assignments = get_assignments_of_all_combinations(expression, variables)
        result["truthTable"] = get_truth_table(variables, assignments, only_true, only_false)

        if custom_kv_h_var_seq is not None and custom_kv_v_var_seq is not None and \
                set(variables) != set(custom_kv_h_var_seq + custom_kv_v_var_seq):
            result["error"] = "Custom-variables and term-variables of the KV-diagram are not equal!"
        else:
            if custom_kv_v_var_seq is None or custom_kv_h_var_seq is None and not (custom_kv_h_var_seq is None and custom_kv_v_var_seq is None):
                custom_kv_h_var_seq = None
                custom_kv_v_var_seq = None

            result["kvDiagram"] = get_kv_diagram(variables, assignments, custom_kv_h_var_seq, custom_kv_v_var_seq)

        return result
    except Exception:
        return {"error": "Check your input: Make sure you put the right brackets, used only allowed operands and " +
                         "that you have chosen your variables as single char (no word, only one char)"}


if __name__ == '__main__':
    app.run()

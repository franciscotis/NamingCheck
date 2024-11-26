import sys
from typing import List

from constants import (
    RESERVED_WORDS,
    FUNCTION_DECLARATION_TYPES,
    VARIABLE_DECLARATION_TYPES,
    PRE_DECLARATION_TYPES,
)

VERSION = '1.0.0'


def rule_initialized_all_variables(declaration: str) -> bool:  
    variables = declaration.replace(";", "").split(",")
    declarations = set()

    for variable in variables:
        declarations.add(True if "=" in variable else False)

    return len(declarations) == 1


def pointers_should_not_be_declared_with_non_pointers(declaration: str) -> bool:  
    variables = declaration.replace(";", "").split(",")
    declarations = set()

    for variable in variables:
        declarations.add(True if "*" in variable else False)

    return len(declarations) == 1


def all_constants_should_be_declared_in_uppercase(declaration: str) -> bool:  
    line = declaration.replace("#define", "").replace(";", "").split(" ")
    for variable in line:
        if variable != "" and variable != " " and variable != "\t":
            return variable.isupper()


def enums_should_be_capitalized(declaration: str) -> bool:  
    line = declaration.replace("enum", "").split(" ")
    for variable in line:
        if variable != "" and variable != " " and variable != "\t":
            return variable.istitle()


def functions_should_be_lower_cased(declaration: str) -> bool:  
    line = declaration.split(" ")
    function_name_position = 1
    for pre_declaration_type in PRE_DECLARATION_TYPES:
        if line[0] == pre_declaration_type:
            function_name_position += 1
            break
    if line[0] == "struct":
        function_name_position += 1
    function_name = line[function_name_position].split("(")[0].replace(" ", "")
    return True if function_name.islower() else False


def variables_should_be_lower_cased(declaration: str) -> bool:  
    variables = "".join(declaration.replace(";", "").split(" ")[1:]).split(",")
    for variable in variables:
        variable = variable.split("[")[0]
        if not variable.islower():
            return False
    return True


def variables_should_have_length_greater_than_one(declaration: str) -> bool:  
    variables = declaration.replace(";", "").split(",")
    variables[0] = variables[0].split(" ")[1]
    for variable in variables:
        if len(variable.replace(" ", "")) == 1:
            return False
    return True


def struct_declaration_should_be_in_lower_case(
    declaration: str, struct_types: List[str]
) -> bool or None:
    line = declaration.split(" ")
    struct_name = ""
    if line[0] == "typedef":
        if 2 < len(line):
            struct_name = line[2]
        else:
            return None
    elif line[0] == "struct":
        struct_name = line[1]
    struct_name = struct_name.replace(" ", "")
    struct_types.append(struct_name)
    return struct_name.islower()


def struct_typedef_name_should_be_in_lower_case(
    declaration: str, struct_types: List[str]
) -> bool:  
    line = declaration.replace("}", "").replace(" ", "")
    struct_types.append(line)
    return True if line.islower() else False


def has_numbers(input_string: str):
    return any(char.isdigit() for char in input_string)


def is_variable_declaration(line: str, struct_types: List[str]) -> bool:
    can_be_variable_declaration = False
    if "{" in line:
        return False
    for reserved_word in RESERVED_WORDS:
        if reserved_word in line:
            return False
    contents = line.split(" ")
    if len(contents) <= 1:
        return False

    variable_type = line.strip().split(" ")[0]
    if variable_type in struct_types or variable_type in VARIABLE_DECLARATION_TYPES:
        can_be_variable_declaration = True

    if (
        can_be_variable_declaration
        and "return" not in contents[0]
        and not has_numbers(contents[0])
        and contents[1] is not None
            and contents[1] != ""
    ):
        return True


def is_function_declaration(line: str) -> bool:
    lines = line.split(" ")
    can_be_function = False
    return_function_type_index = 0
    for pre_declaration_type in PRE_DECLARATION_TYPES:
        if lines[0].strip() == pre_declaration_type:
            return_function_type_index += 1
            break
    return_name = lines[return_function_type_index].replace(" ", "")
    if len(return_name) == 0:
        return False
    pointers_count = return_name.count("*")
    pointer_in_front = return_name[0] == "*"

    for function_type in FUNCTION_DECLARATION_TYPES:
        function_type_with_pointer = (
            function_type
            if pointers_count == 0
            else (
                "*" * pointers_count + function_type
                if pointer_in_front
                else function_type + "*" * pointers_count
            )
        )
        if return_name == function_type_with_pointer:
            can_be_function = True
            break
    if not can_be_function:
        return False
    return True if can_be_function and ("(" in line and ")" in line) else False


def is_struct_declaration(line: str) -> bool:
    return True if "struct" in line and ";" not in line else False


def is_comment(declaration):
    line = declaration.strip()
    if len(line) < 2:
        return False
    return (
        True
        if (line[0] == line[1] == "/")
        or (line[0] == "/" and line[1] == "*")
        or (line[0] == "*")
        or (line[0] == "*" and line[1] == "/")
        else False
    )

def c_analyzer(code):
    current_line = 1
    warnings = []
    struct_types = []
    is_watching_struct = False
    for line in code:
        if is_comment(line):
            continue
        if is_watching_struct:
            if "}" in line:
                is_watching_struct = False
                warning = not struct_typedef_name_should_be_in_lower_case(
                    line, struct_types
                )
                if warning:
                    warning_message = f"WARN: [{current_line}] Structs should be declared in lowercase."
                    warnings.append(warning_message)
        if "enum" in line:
            warning = not enums_should_be_capitalized(line)
            if warning:
                warning_message = (
                    f"WARN: [{current_line}] Enums declaration should be capitalized"
                )
                warnings.append(warning_message)
        if "#define" in line:
            warning = not all_constants_should_be_declared_in_uppercase(line)
            if warning:
                warning_message = f"WARN: [{current_line}] All constants should be declared in uppercase."
                warnings.append(warning_message)
        if is_struct_declaration(line):
            warning = struct_declaration_should_be_in_lower_case(line, struct_types)
            if warning is not None:
                if not warning:
                    warning_message = f"WARN: [{current_line}] Structs should be declared in lowercase."
                    warnings.append(warning_message)
            else:
                is_watching_struct = True
        if is_function_declaration(line):
            warning = not functions_should_be_lower_cased(line)
            if warning:
                warning_message = (
                    f"WARN: [{current_line}] Functions names should be lower cased."
                )
                warnings.append(warning_message)
        if is_variable_declaration(line, struct_types):
            warning = not rule_initialized_all_variables(line)
            if warning:
                warning_message = f"WARN: [{current_line}] If you initialize one variable, you should initialize the others"
                warnings.append(warning_message)

            warning = not pointers_should_not_be_declared_with_non_pointers(line)
            if warning:
                warning_message = f"WARN: [{current_line}] Pointers variables should not be declared with no pointers variables"
                warnings.append(warning_message)

            warning = not variables_should_be_lower_cased(line)
            if warning:
                warning_message = (
                    f"WARN: [{current_line}] Variables names should be lower cased"
                )
                warnings.append(warning_message)

            warning = not variables_should_have_length_greater_than_one(line)
            if warning:
                warning_message = f"WARN: [{current_line}] Variables names should have length greater than one."
                warnings.append(warning_message)

        current_line += 1

    return warnings


def py_analyzer():
    pass


def start():
    args = sys.argv

    if len(args) == 1:
        raise Exception("No input file was provided")

    input_file = args[1]

    warnings = []

    with open(input_file, "r") as file:
        code = file.read().splitlines()

    if input_file.endswith(".c"):
        warnings = c_analyzer(code)
    elif input_file.endswith(".py"):
        raise Exception("Unsupported")

    for warning in warnings:
        print(warning)


if __name__ == "__main__":
    start()

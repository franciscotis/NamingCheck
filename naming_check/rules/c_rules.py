import re 
from typing import List
from constants import PRE_DECLARATION_TYPES


def rule_initialized_all_variables(declaration: str) -> bool:  
    """
    Determines if all variables in a given declaration are either initialized or uninitialized.

    Args:
        declaration (str): A string representing variable declarations separated by commas,
                           with optional initialization (e.g., "x=1, y, z=2").

    Returns:
        bool: True if all variables are consistently either initialized or uninitialized;
              False otherwise.
    """
    variables = declaration.replace(";", "").split(",")
    declarations = set()

    for variable in variables:
        declarations.add(True if "=" in variable else False)

    return len(declarations) == 1


def pointers_should_not_be_declared_with_non_pointers(declaration: str) -> bool:  
    """
    Checks if all variables in a given declaration are either pointers or non-pointers.

    Args:
        declaration (str): A string representing variable declarations separated by commas,
                           where pointers are denoted by an asterisk (*) 
                           (e.g., "int *p, x, *q").

    Returns:
        bool: True if all variables are consistently either pointers or non-pointers;
              False otherwise.
    """
    variables = declaration.replace(";", "").split(",")
    declarations = set()

    for variable in variables:
        declarations.add(True if "*" in variable else False)

    return len(declarations) == 1


def all_constants_should_be_declared_in_uppercase(declaration: str) -> bool:  
    """
    Verifies if all constants in a given declaration are written in uppercase.

    Args:
        declaration (str): A string representing a constant declaration, typically in the form
                           of a `#define` directive (e.g., "#define MAX_VALUE 100").

    Returns:
        bool: True if the constant name is in uppercase; False otherwise.
    """
    line = declaration.replace("#define", "").replace(";", "").split(" ")
    for variable in line:
        if variable != "" and variable != " " and variable != "\t":
            return variable.isupper()


def enums_should_be_pascal_case(declaration: str) -> bool:  
    """
    Checks if the enum declaration follows the Pascal case naming convention.

    Args:
        declaration (str): The declaration string containing the enum.

    Returns:
        bool: True if the enum name is in Pascal case, False otherwise.
        
    """
    line = declaration.replace("enum", "").split(" ")
    pascal_case_regex = r'^[A-Z][a-zA-Z0-9]*$'
    for variable in line:
        if variable != "" and variable != " " and variable != "\t":
            return bool(re.match(pascal_case_regex, variable))


def functions_should_be_lower_cased(declaration: str) -> bool:  
    """
    Verifies if a function name in the given declaration is written in lowercase.

    Args:
        declaration (str): A string representing a function declaration, which may include
                           pre-declaration types (e.g., "static int my_function()").

    Returns:
        bool: True if the function name is entirely lowercase; False otherwise.
    """    
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


def variables_should_be_snake_cased(declaration: str) -> bool:  
    """
    Checks if all variables in a given declaration are written in snake_case.

    Args:
        declaration (str): A string representing a variable declaration, which may include
                           multiple variables separated by commas (e.g., "int test, variable, my_array[10];").

    Returns:
        bool: True if all variable names are entirely snake_case; False otherwise.
    """
    variavel_regex = r'\b(?:int|float|double|char|long|short|unsigned|signed|void|const)\s+([a-zA-Z_][a-zA-Z0-9_]*)(?=\s*(?:,|=|\s*;))'
    variaveis = re.findall(variavel_regex, declaration)
    snake_case_regex = r'^[a-z]+(_[a-z0-9]+)*$'
    for variavel in variaveis:
        if not re.match(snake_case_regex, variavel):
            return False
    return True


def variables_should_have_length_greater_than_one(declaration: str) -> bool:  
    """
    Checks if all variable names in a given declaration have a length greater than one.

    Args:
        declaration (str): A string representing a variable declaration, which may include
                           multiple variables separated by commas (e.g., "int x, yVar, z;").

    Returns:
        bool: True if all variable names have a length greater than one; False otherwise.
    """
    variables = declaration.replace(";", "").split(",")
    variables[0] = variables[0].split(" ")[1]
    for variable in variables:
        if len(variable.replace(" ", "")) == 1:
            return False
    return True


def struct_declaration_should_be_in_lower_case(
    declaration: str, struct_types: List[str]
) -> bool:
    """
    Checks if a struct name in the given declaration is written in lowercase and 
    appends the struct name to a list of struct types.

    Args:
        declaration (str): A string representing a struct declaration, either with or 
                           without a `typedef` keyword (e.g., "typedef struct my_struct" 
                           or "struct my_struct").
        struct_types (List[str]): A list to which the struct name will be appended.

    Returns:
        bool: True if the struct name is entirely lowercase; False otherwise.
        None: If the declaration is invalid or does not provide a struct name.
    """
    line = declaration.split(" ")
    struct_name = ""
    if line[0] == "typedef":
        if 2 < len(line) and line[2] is not "{":
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
    """
    Checks if a `typedef` name for a struct in the given declaration is written in lowercase 
    and appends the typedef name to a list of struct types.

    Args:
        declaration (str): A string representing a `typedef` declaration for a struct
                           (e.g., "typedef struct { ... } my_struct;").
        struct_types (List[str]): A list to which the typedef name will be appended.

    Returns:
        bool: True if the typedef name is entirely lowercase; False otherwise.
    """
    line = declaration.replace("}", "").replace(" ", "")
    struct_types.append(line)
    return True if line.islower() else False
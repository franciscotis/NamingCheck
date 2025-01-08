import re 
def rule_names_should_be_snake_case(variable: str) -> bool:
    """
    Checks if the given variable name follows the snake_case naming convention.

    Args:
        variable (str): A string representing the variable name to be checked.

    Returns:
        bool: True if the variable name is in snake_case; False otherwise.
    """
    snake_case_pattern = r'^[a-z]+(_[a-z0-9]+)*$'
    return bool(re.match(snake_case_pattern, variable))

def rule_variable_names_should_have_length_greater_than_one(variable: str, line: str) -> bool:
    """
    Checks if the variable name has more than one character, except for the specific case 
    where the variable name is within a for loop.

    Parameters:
    variable (str): The name of the variable to be checked.
    line (str): The line of code where the variable is declared, used to exclude the "for" case.

    Returns:
    bool: Returns True if the variable name has more than one character or if it is "for".
          Returns False if the variable name has exactly one character, except its within the for loop
    """
    return len(variable) == 1 and not line.startswith("for")
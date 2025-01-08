import re 
from typing import List

from constants import FUNCTION_DECLARATION_TYPES, PRE_DECLARATION_TYPES, RESERVED_WORDS, VARIABLE_DECLARATION_TYPES
from rules.c_rules import all_constants_should_be_declared_in_uppercase, enums_should_be_pascal_case, functions_should_be_lower_cased, pointers_should_not_be_declared_with_non_pointers, rule_initialized_all_variables, struct_declaration_should_be_in_lower_case, struct_typedef_name_should_be_in_lower_case, variables_should_be_snake_cased, variables_should_have_length_greater_than_one

class CAnalyzer:
    """
    A class responsible for analyzing C code to detect style violations and coding standard issues.

    This class provides methods to check for warnings related to variable and function naming conventions,
    struct and enum declarations, pointer and variable initialization, constants, and other
    predefined coding rules.
    
    """
    def __init__(self, code):
        self.code = code
        self.current_line = 1
        self.warnings = []
        self.struct_types = []
        self.is_watching_struct = False
        
    def analyze(self):
        """
        Analyzes the code for style and coding standard violations.

        This method triggers the process of checking for warnings and returns a list of detected warnings.

        Returns:
            list: A list of warning messages related to code style violations.
        """
        self.check_warnings()
        return self.warnings
    
    def check_warnings(self):
        """
        Checks the code for various warnings related to coding standards and style guidelines.

        This method iterates through each line of code and applies different style checks, such as:
        - Comment checks
        - Struct declaration checks
        - Enum capitalization checks
        - Constant uppercase checks
        - Function name casing checks
        - Variable initialization checks
        - Pointer declaration checks

        Any violations of the guidelines result in warning messages being added to the `warnings` list.
        """
        for line in self.code:
            if self.is_comment(line):
                self.current_line+=1
                continue
            if self.is_watching_struct:
                self.struct_typedef_handler(line)
            if "enum" in line:
                self.enum_handler(line)
            if "#define" in line:
                self.constant_handler(line)
            if self.is_struct_declaration(line):
                self.struct_handler(line)
            if self.is_function_declaration(line):
                self.function_handler(line)
            if self.is_variable_declaration(line, self.struct_types):
                self.variable_handler(line)
            self.current_line += 1
            
    def struct_typedef_handler(self, line) -> None:
        """
        Checks a line of code for potential struct typedef-related issues and appends relevant warnings.

        Args:
            line (str): The line of code to be checked for struct typedef-related conventions.
    """
        if "}" in line:
            self.is_watching_struct = False
            warning = not struct_typedef_name_should_be_in_lower_case(
                line, self.struct_types
            )
            if warning:
                self.append_warning("Structs should be declared in lower case.")
            
    def enum_handler(self, line) -> None:
        """
            Checks a line of code for potential enum-related issues and appends relevant warnings.

            Args:
                line (str): The line of code to be checked for enum-related conventions.
        """
        warning = not enums_should_be_pascal_case(line)
        if warning:
            self.append_warning("Enums declaration should be in pascal case.")
            
    def constant_handler(self, line) -> None:
        """
            Checks a line of code for potential constant-related issues and appends relevant warnings.

            Args:
                line (str): The line of code to be checked for constant-related conventions.
        """
        warning = not all_constants_should_be_declared_in_uppercase(line)
        if warning:
            self.append_warning("All constants should be declared in uppercase.")
            
    def struct_handler(self, line) -> None:
        """
            Checks a line of code for potential struct-related issues and appends relevant warnings.

            Args:
                line (str): The line of code to be checked for struct-related conventions.
        """
        warning = struct_declaration_should_be_in_lower_case(line, self.struct_types)
        if warning is not None:
            if not warning:
                self.append_warning("Structs should be declared in lowercase.")
        else:
            self.is_watching_struct = True

    def function_handler(self, line) -> None:
        """
            Checks a line of code for potential function-related issues and appends relevant warnings.

            Args:
                line (str): The line of code to be checked for function-related conventions.
        """
        warning = not functions_should_be_lower_cased(line)
        if warning:
            self.append_warning("Functions names should be declared in snake case.")
        
    def variable_handler(self, line) -> None:
        """
            Checks a line of code for potential variable-related issues and appends relevant warnings.

            Args:
                line (str): The line of code to be checked for variable-related conventions.
        """
        warning = not rule_initialized_all_variables(line)
        if warning:
            self.append_warning("If you initialize one variable, you should initialize the others.")
        warning = not pointers_should_not_be_declared_with_non_pointers(line)
        if warning:
            self.append_warning("Pointers variables should not be declared with no pointers variables.")
        warning = not variables_should_be_snake_cased(line)
        if warning:
            self.append_warning("Variables names should be declared in snake case.")
        warning = not variables_should_have_length_greater_than_one(line)
        if warning:
            self.append_warning("Variables names should have length greater than one.")

    def append_warning(self, warning_message) -> None:
        """
            Appends a warning message to the list of warnings with the current line number.

            Args:
                warning_message (str): The warning message to be appended.
        """
        message = f"WARN: [{self.current_line}] {warning_message}"
        self.warnings.append(message)

    def has_numbers(self, input_string: str) -> bool:
        """
        Checks if the given string contains any numeric digits.

        Args:
            input_string (str): A string to be checked for numeric characters.

        Returns:
            bool: True if the string contains any digits; False otherwise.
        """
        return any(char.isdigit() for char in input_string)

    def contains_reserved_words(self, line) -> bool:
        """
            Checks if the given line contains any reserved words.

            Args:
                line (str): The line of code to check for reserved words.

            Returns:
                bool: True if the line contains any reserved words, False otherwise.
        """
        pattern = rf'\b(?:{"|".join(map(re.escape, RESERVED_WORDS))})\b'
        return bool(re.search(pattern, line))
    
    def is_variable_declaration(self, line: str, struct_types: List[str]) -> bool:
        """
        Determines if the given line is a valid variable declaration.

        Args:
            line (str): A string representing a line of code to be checked.
            struct_types (List[str]): A list of types representing structs in the code.

        Returns:
            bool: True if the line is a valid variable declaration (with valid type and variable name);
                False otherwise.
        """
        can_be_variable_declaration = False
        if "{" in line:
            return False
        
        if self.contains_reserved_words(line):
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
            and not self.has_numbers(contents[0])
            and contents[1] is not None
                and contents[1] != ""
        ):
            return True


    def is_function_declaration(self, line: str) -> bool:
        """
        Determines if the given line is a valid function declaration.

        Args:
            line (str): A string representing a line of code to be checked.

        Returns:
            bool: True if the line matches a valid function declaration pattern (including return type, function name, and parentheses);
                False otherwise.]
    """
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


    def is_struct_declaration(self, line: str) -> bool:
        """
        Checks if the given line represents a struct declaration.

        Args:
            line (str): A string representing a line of code to be checked.

        Returns:
            bool: True if the line contains a struct declaration (indicated by the keyword "struct" and no semicolon);
                False otherwise.
         """
        return True if "struct" in line and ";" not in line else False


    def is_comment(self,declaration):
        """
        Checks if the given declaration is a comment, supporting both single-line and multi-line comments.

        Args:
            declaration (str): A string representing the line of code or declaration to be checked.

        Returns:
            bool: True if the declaration is a comment (single-line or multi-line); False otherwise.
        """
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
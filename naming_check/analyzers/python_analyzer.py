import re

from naming_check.rules.py_rules import rule_names_should_be_snake_case, rule_variable_names_should_have_length_greater_than_one 
class PythonAnalyzer:
    """
    A class responsible for analyzing Python code to detect style violations and coding standard issues.

    This class provides methods to check for warnings related to variable and function naming conventions.
    
    """
    def __init__(self, code):
        self.warnings = []
        self.code = code
        self.multiline_string = False
        self.current_variable = None
        self.current_function = None
        self.current_line = 1
    
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
        Analyzes the code for style violations, specifically focusing on variable and function name patterns.

        This method checks each line of code for potential issues, including:
        - Ensuring variable names follow the snake_case pattern.
        - Ensuring function names follow the snake_case pattern.

        Any violations are added as warning messages to the `warnings` list.

        """
        for code in self.code:
            if self.is_comment(code):
                self.current_line+=1
                continue
            line = code.strip()
            if self.is_variable_declaration(line):
                self.variable_handler(line)
            # if self.is_function_declaration(line):
            #     self.function_handler()
            self.current_line+=1
            
            
    def variable_handler(self, line) -> None:
        """
            Checks the current variable name for snake_case naming convention and appends a warning if necessary.
        """
        # warning = not rule_names_should_be_snake_case(self.current_variable)
        # if(warning):
        #     self.append_warning("Variables names should be declared in snake case.")
        warning = rule_variable_names_should_have_length_greater_than_one(self.current_variable, line)
        if warning:
            self.append_warning("Variables names should have length greater than one.")
        self.current_variable = None
        
    def function_handler(self) -> None:
        """
            Checks the current function name for snake_case naming convention and appends a warning if necessary.
        """
        warning = not rule_names_should_be_snake_case(self.current_function)
        if(warning):
            self.append_warning("Functions names should be declared in snake case.")
        self.current_function = None
        
    def is_comment(self, line: str) -> bool:
        """
        Checks if the given line is a comment or part of a multiline comment in Python.

        Args:
            line (str): A string representing a line of code to be checked.

        Returns:
            bool: True if the line is a comment (either single-line or part of a multiline comment); False otherwise.
            
        Side Effects:
            Toggles the `multiline_string` attribute if a multiline comment is encountered.
        """
        line = line.strip()
        if(line.startswith("#")):
            return True
        if '"""' in line or "'''" in line:
            self.multiline_string = not self.multiline_string
            return True
        if self.multiline_string:
            return True
        return False
    
    def is_variable_declaration(self, line: str) -> bool:
        """
        Determines if the given line is a valid variable declaration with an assignment in Python.

        Args:
            line (str): A string representing a line of code to be checked.

        Returns:
            bool: True if the line matches a variable declaration with an assignment; False otherwise.
            
        Side Effects:
            Sets the `current_variable` attribute to the variable name if a match is found.
        """
        variable_pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[^=]'
        match = re.match(variable_pattern, line.strip())
        if match:
            self.current_variable = match.group(1)
        return match
        
    def is_function_declaration(self, line: str) -> bool:
        """
        Determines if the given line is a valid function declaration in Python.

        Args:
            line (str): A string representing a line of code to be checked.

        Returns:
            bool: True if the line matches a function declaration pattern; False otherwise.
            
        Side Effects:
            Sets the `current_function` attribute to the function name if a match is found.
         """
        function_pattern = r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*\)\s*:'
        match = re.match(function_pattern, line.strip())
        if match:
            self.current_function = match.group(1)
        return match
    
    def append_warning(self, warning_message) -> None:
        """
            Appends a warning message to the list of warnings with the current line number.

            Args:
                warning_message (str): The warning message to be appended.
        """
        message = f"WARN: [{self.current_line}] {warning_message}"
        self.warnings.append(message)
import re 
class PythonAnalyzer:
    def __init__(self, code):
        self.warnings = []
        self.code = code
        self.multiline_string = False
        self.current_variable = None
        self.current_function = None
        self.current_line = 1
    
    def analyze(self):
        self.check_warnings()
        return self.warnings
                
                
    def check_warnings(self):
        for code in self.code:
            
            if self.is_comment(code):
                self.current_line+=1
                continue
            line = code.strip()
            if self.is_variable_declaration(line):
                warning = not self.rule_names_should_be_snake_case(self.current_variable)
                if(warning):
                    warning_message = (f"WARN: [{self.current_line}] Variables names should be in snake case pattern")
                    self.warnings.append(warning_message)
                self.current_variable = None
            if self.is_function_declaration(line):
                warning = not self.rule_names_should_be_snake_case(self.current_function)
                if(warning):
                    warning_message = (f"WARN: [{self.current_line}] Functions names should be in snake case pattern")
                    self.warnings.append(warning_message)
                self.current_function = None
            self.current_line+=1
            
                
    def is_comment(self, line):
        line = line.strip()
        if(line.startswith("#")):
            return True
        if '"""' in line or "'''" in line:
            self.multiline_string = not self.multiline_string
            return True
        if self.multiline_string:
            return True
        return False
    
    def is_variable_declaration(self, line):
        variable_pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[^=]'
        match = re.match(variable_pattern, line.strip())
        if match:
            self.current_variable = match.group(1)
        return match
        
    def is_function_declaration(self, line):
        function_pattern = r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*\)\s*:'
        match = re.match(function_pattern, line.strip())
        if match:
            self.current_function = match.group(1)
        return match
    
    def rule_names_should_be_snake_case(self, variable):
        snake_case_pattern = r'^[a-z]+(_[a-z0-9]+)*$'
        return bool(re.match(snake_case_pattern, variable))
    
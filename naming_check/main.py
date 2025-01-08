import sys

from analyzers.c_analyzer import CAnalyzer
from analyzers.python_analyzer import PythonAnalyzer


def c_analyzer(code):
    """
    Analyzes C code and returns a list of warnings related to coding style and conventions.

    Args:
        code (List[str]): A list of strings representing the lines of C code to analyze.

    Returns:
        List[str]: A list of warning messages found during the analysis.
    """
    analyzer = CAnalyzer(code)
    return analyzer.analyze()
    


def py_analyzer(code):
    """
    Analyzes Python code and returns a list of warnings related to coding style and conventions.

    Args:
        code (List[str]): A list of strings representing the lines of Python code to analyze.

    Returns:
        List[str]: A list of warning messages found during the analysis.
    """
    analyzer = PythonAnalyzer(code)
    return analyzer.analyze()


def start():
    """
    Starts the analysis process by reading the input file and running the appropriate analyzer based on the file type.

    The function performs the following steps:
    1. Checks if an input file was provided as a command-line argument.
    2. Reads the content of the input file into a list of code lines.
    3. Determines the file type (C or Python) based on the file extension.
    4. Runs the corresponding analyzer (CAnalyzer for `.c` files, PythonAnalyzer for `.py` files).
    5. Prints any warnings generated during the analysis.

    Raises:
        Exception: If no input file is provided via command-line arguments.
    """
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
        warnings = py_analyzer(code)

    for warning in warnings:
        print(warning)


if __name__ == "__main__":
    start()

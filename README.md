
# NamingCheck
A static analyzer tool for checking naming conventions in C and Python.


## Install

For command line use, you can install using the following command:

```bash
  pip install naming_check
```


    
## How to use

You can start using the analyzer by providing the relative path of the code that you want to analyze:


```python
  naming_check C:\Documents\Codes\my_code.c
```

The analyzer will check all variables and functions and provide a feedback about their declaration such as:

> WARN: [30] All constants should be declared in uppercase.

- Warn means that the feedback is a warning
- [30] means that the warning is happening on line 30

### List of warnings

The following list presents all the warnings that can be presented by the analyzer:

- Structs should be declared in lowercase.
- Enums declaration should be pascalcase.
- All constants should be declared in uppercase.
- Functions names should be declared in snakecase.
- If you initialize one variable, you should initialize the others
- Pointers variables should not be declared with no pointers variables
- Variables names should be declared in snake case.
- Variables names should have length greater than one.


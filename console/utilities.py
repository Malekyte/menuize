import os
from re import Pattern, compile
from types import NoneType

def clear_console():
    '''
    Clears console screen.

    Arguments:
        None

    Returns:
        None

    Version:
        v1; 2024-04-23
    '''
    
    os.system('cls' if os.name == 'nt' else 'clear')

def varg(input, *args, varname:str = None) -> bool:
    '''
    Determines if an input argument is a valid data type from the array of
    *args data types.

    Arguments:
              input: (obj) Input object to be validated.
               args: (array) Array of type objects, or list of type objects.
            varname: (str) Variable input name for raising error callout.
        raise_error: (bool) Raise error on invalid input.

    Return:
        bool: Validity of arg to data types.
    '''
    # v: 2024-07-07

    # bypass empty arguments
    if input == None:
        return True

    # validate inputs
    if not isinstance(varname, str | NoneType):
        raise TypeError(f"Invalid data type for varname. Expected {type(str())}, got {type(varname)}.")
    
    # iterate over args
    valid = False
    for a in args:
        # special case - RegEx pattern
        if a == Pattern:
            try:
                compile(input)
                valid = True
            except:
                pass
        # direct instancing
        elif isinstance(input, a):
            valid = True

    # raise error if optioned
    if varname != None and not valid:
        raise TypeError(f"Invalid data type for {varname}. Expected {args}, got {type(input)}.")
    return valid
        

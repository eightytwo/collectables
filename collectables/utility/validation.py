# General validation

def is_integer(s):
    """
    Checks if a given value is an integer.
    """
    try:
        int(s)
        return True
    except:
        return False

def is_float(s):
    """
    Checks if a given value is a float.
    """
    try:
        float(s)
        return True
    except:
        return False

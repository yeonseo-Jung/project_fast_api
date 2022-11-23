def isInt_nonegative(x: any) -> bool:
    try:
        x = int(x)
        if x >= 0:
            return True
        else:
            return False
        
    except ValueError:
        return False
    
def isNatural(x: any) -> bool:
    try:
        x = int(x)
        if x > 0:
            return True
        else:
            return False
        
    except ValueError:
        return False
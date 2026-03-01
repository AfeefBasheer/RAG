def require_str(data: str, *, name: str = "value") -> str:

    if not isinstance(data,str): #handling non string inputs
        raise TypeError(f"Type error at {name}: expected str, received {type(data).__name__}")
    return data
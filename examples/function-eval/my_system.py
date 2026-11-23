"""The 'system under evaluation': any Python callable taking an example's input."""


def add(inp: dict) -> float:
    return inp["a"] + inp["b"]


def buggy_add(inp: dict) -> float:
    if inp["a"] < 0:
        raise ValueError("negative inputs not supported")
    return inp["a"] + inp["b"] + (1 if inp["a"] > 50 else 0)

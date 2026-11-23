"""The code under evaluation. Swap `add` for `add_v2` in evals/config.yaml to see a regression."""


def add(inp: dict) -> float:
    return inp["a"] + inp["b"]


def add_v2(inp: dict) -> float:
    # A plausible-looking "optimization" that breaks negative inputs and large numbers.
    if inp["a"] < 0:
        raise ValueError("negative inputs not supported")
    return inp["a"] + inp["b"] + (1 if inp["a"] > 50 else 0)

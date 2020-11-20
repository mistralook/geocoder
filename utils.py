def make_criteria(**kwargs) -> str:
    return " and ".join([f'{key} = {value}'
                         for key, value in kwargs.items()])

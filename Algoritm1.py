
def calculate_algorithm1(x1, x2) -> int:
    if (float(x1) < float(x2)) and (float(x1) > float(1.5)) and ((float(x2) - float(x1)) > 0.9):
        return 1
    return 0


def compute_form(s1: str) -> float:
    residual = 1
    form = 0
    list_string = [*s1][::-1]

    for i in list_string:
        ratio = 0.18
        coefficient = ratio * residual
        residual -= coefficient

        if i.lower() == 'W'.lower():
            form += coefficient * 2
        elif i.lower() == 'D'.lower():
            form += coefficient * 1
        else:
            form += coefficient * 0

    return form / 2  # interval 0-2 moved to 0-1

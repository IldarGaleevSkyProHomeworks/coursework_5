from src.utils.console_color import FG_YELLOW, FG_RESET


def user_choice(choice_list: list[str]) -> int:
    """
    User choice dialog
    :param choice_list: strings for choice list
    :return: chosen index or -1 if error
    """
    try:
        choice_list = '\n'.join([f' {i + 1}: {FG_YELLOW}{a}{FG_RESET}' for i, a in enumerate(choice_list)])
        print(f"Выберите дальнейшее действие:\n{choice_list}\n")
        return int(input("> "))
    except ValueError:
        return -1

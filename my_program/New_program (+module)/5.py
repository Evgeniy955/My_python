from module_in import my_input


def paired_unpaired():
    lines = my_input(0, "Enter the number: ", "You entered not an integer.", True)
    y = [print(i, "Is EVEN") if i % 2 == 0 else print(i, "Is ODD") for i in range(lines)]

paired_unpaired()
from module_in import my_input


def chr_tree():
    lines = my_input(0, "Enter the number: ", "You entered not an integer.", True)
    tree = [print("*" * i) for i in range(1, lines + 1)]


chr_tree()
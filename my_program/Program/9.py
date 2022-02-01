from module_in import my_input


def coffee_cup():
    cup = my_input(0, "Enter the number of coffee cups: ", "You entered not an integer.", True)
    bonus = cup // 6
    print(f"You have {bonus} free cups of coffee.")


coffee_cup()

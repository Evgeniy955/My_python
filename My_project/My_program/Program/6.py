from module_in import my_input

def total():
    int_number = my_input(0, "Enter the number: ", "You entered not an integer.", True)
    total = 0
    for i in range(int_number):
        if i % 3 == 0 or i % 5 == 0:
            total += i
    print(total)

total()
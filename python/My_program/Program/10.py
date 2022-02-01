from module_in import my_input

def animal(animal_naming):
    int_number = my_input(0, f"Enter the number of {animal_naming}: ", "You entered not an integer.", True)
    return int_number

chickens = animal('Chickens')
pigs = animal('Pigs')
cows = animal('Cows')

sum_legs = chickens * 2 + cows * 4 + pigs * 4
print(f"Animals have {sum_legs} legs")

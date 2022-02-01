print(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])

card_to_weight = {
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    '6': 1,
    '7': 0,
    '8': 0,
    '9': 0,
    '10': -1,
    'J': -1,
    'Q': -1,
    'K': -1,
    'A': -1
}

current_hand = []

def card():
    while True:
        s = input("Enter one of the characters or press enter: ")
        if s.upper() in card_to_weight.keys():
            current_hand.append(s.upper())
        elif s == '':
            break
        else:
            print("Sorry, you entered an invalid character")
            continue
    x = [card_to_weight[i] for i in current_hand if i in card_to_weight]
    print(current_hand)
    print(x)
    print(sum(x))

card()
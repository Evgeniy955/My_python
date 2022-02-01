def total_sum(x, y):
    joined_list = []
    for i in range(10):
        if x[i] % 2 == 0:
            joined_list.append(x[i])
        if y[i] % 2 != 0:
            joined_list.append(y[i])
    print(sum(joined_list))


list1 = [1, 31, 42, 5, 6, 7, 8, 24, 56, 88]
list2 = [2, 54, 78, 99, 44, 22, 10, 65, 66, 18]

total_sum(list1, list2)


def total_sum(list1, list2):
    joined_list = [i for i in list1 if i % 2 == 0] + [i for i in list2 if i % 2 != 0]
    print(sum(joined_list))


x = [1, 31, 42, 5, 6, 7, 8, 24, 56, 88]
y = [2, 54, 78, 99, 44, 22, 10, 65, 66, 18]

total_sum(x, y)

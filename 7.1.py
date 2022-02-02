def total_sum(list1, list2):
    joined_list = [i for i in list1 if i % 2 == 0] + [i for i in list2 if i % 2 != 0]
    print(sum(joined_list))


list_x = [1, 21, 42, 5, 6, 7, 8, 21, 56, 88]
list_y = [2, 23, 78, 99, 44, 22, 8, 26, 66, 18]


total_sum(list_x, list_y)

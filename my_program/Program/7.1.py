def total_sum(list1, list2):
    joined_list = [i for i in list1 if i % 2 == 0] + [i for i in list2 if i % 2 != 0]
    print(sum(joined_list))


list_1 = [1, 31, 18, 5, 6, 7, 8, 24, 56, 84]
list_2 = [2, 54, 78, 99, 40, 32, 10, 65, 66, 60]

total_sum(list_1, list_2)

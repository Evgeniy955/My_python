def my_input(min_int, msg, ex_msg, logic_flag: True):
    while True:
        try:
            res = int(input(msg))
            if logic_flag:
                if res > min_int:
                    return res
            elif not logic_flag:
                if res >= min_int:
                    return res
        except ValueError:
            print(ex_msg)

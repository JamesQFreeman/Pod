

def print_tuple(the_tuple, context, count_ex, setting_ex_no):
    level = the_tuple[0]
    content = the_tuple[1]
    refleshed_context = level
    refleshed_count_ex = count_ex
    if refleshed_context != 10:
        refleshed_count_ex = 0
    if level == 1:
        context = level
        print(content)
    elif level == 2:
        context = level
        print('|--->' + content)
    elif level == 3:
        context = level
        print('      |--->' + content)
    elif level == 5:
        context = level
        print('            |--->' + content)
    elif level == 10:
        refleshed_count_ex += 1
        print('               |(ex%d)%s' % (refleshed_count_ex, content)
    return refleshed_context, refleshed_count_ex


def main(the_dict, setting_ex_no=3):
    # it is a variable you will maintain, it record where you are working at
    context=0
    count_ex=0
    for index, content in the_dict.items():
        context, count_ex=print_tuple(
            content, context, count_ex, setting_ex_no)

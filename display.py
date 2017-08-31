def display_dict(the_dict):
    # print(the_dict)
    for index, content in the_dict.items():
        if content[0] == 1:
            print(content[1])
        elif content[0] == 2:
            print('|----' + content[1])
        elif content[0] == 3:
            print('     |----' + content[1])
        elif content[0] == 5:
            print('          |----'+content[1])

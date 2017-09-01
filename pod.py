import sys
import core
import display

def dict_loop():
    while 1:
        word = input('Please type the word/phrase you want to look up:')
        if word[-4:] is not 'fuck':
            test.test_901(word)
        else:
            exit()


def main():
    print(sys.argv)
    is_arg = sys.argv[1][0]
    if is_arg == '-':
        if sys.argv[1] == '-l':
            display.display_dict(core.lookup('test'))


if __name__ == '__main__':
    main()

import sys
import core
import display


def dict_loop():
    import test
    while 1:
        word = input('\n#Please type the word/phrase you want to look up:')
        if word[-4:] != 'fuck':
            display.main(core.lookup(word))
        else:
            exit()


def main():
    if len(sys.argv) < 2:
        dict_loop()
    else:
        is_arg = sys.argv[1][0]
        if is_arg == '-':
            if sys.argv[1] == '-l':
                display.main(core.lookup(' '.join(sys.argv[2:])))
            if sys.argv[1] == '-d':
                display.main(core.lookup(' '.join(sys.argv[2:])))
                dict_loop()
        else:
            display.main(core.lookup(' '.join(sys.argv[1:])))


if __name__ == '__main__':
    main()

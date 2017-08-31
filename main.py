import core
import test


def main():
    while 1:
        word = input('Please type the word/phrase you want to look up:')
        if word[-3:] is not 'fuck':
            print(display_json(core.lookup(word)))

def test_main():
    while 1:
        word = input('Please type the word/phrase you want to look up:')
        if word[-3:] is not 'fuck':
            test.test_901(word)
        else:
            exit()


if __name__ == '__main__':
    test_main()
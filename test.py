import urllib.request


def test1():
    with urllib.request.urlopen('https://en.oxforddictionaries.com/definition/test') as response:
        open('test.html', 'w').write(response.read().decode('utf-8'))


def test2():
    while True:
        test_word = input('fuck me: ')
        if test_word[-4:] != 'fuck':
            print(test_word[-4:])
            print(test_word)


def test_find(s, p='entryWrapper'):
    begin = s.find('<div class=')
    length = len(s)
    end = length - (s[::-1].find('>vid/<'))
    open('logger5.log', 'a').write(str(begin) + ' and ' + str(end) + '\n')
    if s[0:27] != '<div class="entryWrapper">':
        return test_find(s[begin:end], p)
    else:
        return s


from html.parser import HTMLParser


class htmlParser(HTMLParser):
    buffer = ''

    def handle_starttag(self, tag, attrs):
        self.buffer += ("Start tag:%s\n" % tag)
        for attr in attrs:
            self.buffer += ("     attr:" + str(attr) + '\n')

    def handle_endtag(self, tag):
        self.buffer += ("End tag:%s\n" % tag)

    def handle_data(self, data):
        self.buffer += ("Data:%s\n" % data)

    def __del__(self):
        f = open('fuck.log', 'w')
        f.write(self.buffer)


def ugly_solution(html):
    begin = html.find('<div class="entryWrapper">')
    end = html.find('<div class="comments">')
    html = html[begin:end]
    import re
    c = re.compile(
        '''<div class="social.+?</div>|<div class="examples"><div class="moreInfo"><button data-behaviour="ga-event" data-value="[a-zA-Z ]*">[a-zA-Z ]*</button></div>|<section class="pronSection etym">.+?</section>''')
    # html = re.sub('<div class="social.+?</div>', '', html)
    # html = re.sub('<div class="examples"><div class="moreInfo"><button data-behaviour="ga-event" data-value="[a-zA-Z ]*">[a-zA-Z ]*</button></div>', '', html)
    # html = re.sub('<section class="pronSection etym">.+?</section>', '', html)
    return html


def test_parser():
    p = htmlParser()
    p.feed(open('test_main.html').read())


def test_find_1():
    s = open('test.html', 'r').read()
    s = ugly_solution(s)
    open('test_main.html', 'w').write(s)


def test_830():
    import core
    open('test_main.html', 'w').write(core.lookup('purple'))
    main_html = open('test_main.html').read()
    core._get_all_level_1(main_html)
    core._get_all_level_2(main_html)
    core._get_all_level_3(main_html)


def test_901(the_word):
    import core
    the_dick = core.lookup(the_word)
    import display
    display.main(the_dick)

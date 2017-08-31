import urllib.request
import re
import copy


def _find_main_ugly(html):
    begin = html.find('<div class="entryWrapper">')
    end = html.find('<div class="comments">')
    html = html[begin:end]
    c = re.compile(
        '''<div class="social.+?</div>|<div class="examples"><div class="moreInfo"><button data-behaviour="ga-event" data-value="[a-zA-Z ]*">[a-zA-Z ]*</button></div>|<section class="pronSection etym">.+?</section>''')
    html = re.sub(c, '', html)
    return html


def _get_dict(url):
    return _find_main_ugly(urllib.request.urlopen(url).read().decode('utf-8'))


def _get_all_level_1(main_html):
    pattern = re.compile(
        '<span class="hw" data-headword-id="[\w ]*">[\w ]*(<sup>[1-9]</sup>)?</span>')
    raw_data = re.finditer(pattern, main_html)

    def get_content(s):
        m = re.search(re.compile('>[\w ]*<'), s)
        n = re.search('[1-9]', s)
        if not n:
            return s[m.start() + 1:m.end() - 1]
        else:
            return s[m.start() + 1:m.end() - 1] + '_' + n.group()

    def get_the_dic(i):
        return (i.start() - 20, (1, get_content(i.group())))

    tuple_data = [get_the_dic(i) for i in raw_data]
    # print('the level 1 is: ', dict((x, y) for x, y in tuple_data))
    return (dict((x, y) for x, y in tuple_data))


def _get_all_level_2(main_html):
    pattern = re.compile('<h2( class="[\w ]*")?><[\w= "-]*>[\w ]*</[\w]*>')
    raw_data = re.finditer(pattern, main_html)

    def get_content(s):
        m = re.search(re.compile('>[\w ]+<'), s)
        return s[m.start() + 1:m.end() - 1]

    def get_the_dic(i):
        return (i.start(), (2, get_content(i.group())))

    tuple_data = [get_the_dic(i) for i in raw_data]
    # print('the level 2 is: ', dict((x, y) for x, y in tuple_data))
    return (dict((x, y,) for x, y in tuple_data))


def _get_all_level_3(main_html):
    pattern = re.compile(
        '<h3( class="[\w ]*")?><(span class="[\w ]*"|strong)>[\w ]*</(span|strong)></h3>')
    raw_data = re.finditer(pattern, main_html)

    def get_content(s):
        m = re.search(re.compile('>[\w ]+<'), s)
        return s[m.start() + 1:m.end() - 1]

    def get_the_dic(i):
        return (i.start(), (3, get_content(i.group())))

    tuple_data = [get_the_dic(i) for i in raw_data]
    # print('the level 3 is: ', dict((x, y) for x, y in tuple_data))
    return (dict((x, y,) for x, y in tuple_data))


def _get_all_level_4(main_html):
    pattern = re.compile(
        '<h3( class="[\w ]*")?><(span class="[\w ]*"|strong)>[\w ]*</(span|strong)></h3>')
    raw_data = re.finditer(pattern, main_html)

    def get_content(s):
        m = re.search(re.compile('>[\w ]+<'), s)
        return s[m.start() + 1:m.end() - 1]

    def get_the_dic(i):
        return (i.start(), (4, get_content(i.group())))

    tuple_data = [get_the_dic(i) for i in raw_data]
    print('the level 4 is: ', dict((x, y) for x, y in tuple_data))
    return (dict((x, y,) for x, y in tuple_data))


def _get_all_level_5(main_html):
    pattern = re.compile(
        '<span class="ind">[\w \.,]*</span>')
    raw_data = re.finditer(pattern, main_html)

    def get_content(s):
        m = re.search(re.compile('>[\w \.,]+<'), s)
        return s[m.start() + 1:m.end() - 1]

    def get_the_dic(i):
        return (i.start(), (5, get_content(i.group())))

    tuple_data = [get_the_dic(i) for i in raw_data]
    # print('the level 5 is: ', dict((x, y) for x, y in tuple_data))
    return (dict((x, y,) for x, y in tuple_data))
    pass


def lookup(word):
    url = 'https://en.oxforddictionaries.com/definition/%s' % word
    main_html = _get_dict(url)
    level_1 = _get_all_level_1(main_html)
    level_2 = _get_all_level_2(main_html)
    level_3 = _get_all_level_3(main_html)
    # level_4=_get_all_level_4(main_html)
    level_5=_get_all_level_5(main_html)
    import collections
    gathered = ({**level_1, **level_2, **level_3,**level_5})
    ordered=collections.OrderedDict(sorted(gathered.items()))
    # print(ordered)
    return ordered

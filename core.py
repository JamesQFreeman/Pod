import urllib.request
import re


def _find_main_ugly(html):
    begin = html.find('<div class="entryWrapper">')
    end = html.find('<div class="comments">')
    html = html[begin:end]
    c = re.compile(
        '''<div class="social.+?</div>|<div class="examples"><div class="moreInfo"><button data-behaviour="ga-event" data-value="[a-zA-Z ]*">[a-zA-Z ]*</button></div>|<section class="pronSection etym">.+?</section>''')
    html = re.sub(c, '', html)
    return html


def lookup(word):
    url = 'https://en.oxforddictionaries.com/definition/%s' % word
    html_string = urllib.request.urlopen(url).read().decode('utf-8')
    main_html = _find_main_ugly(html_string)

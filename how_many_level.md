
# static

| level   | regex expression                         |
| ----------------- | ---------------------------------------- |
| 1(subsense)                | ```<span class="hw" data-headword-id="the word">test<sup>[1-9]</sup></span>``` |
| 2(the word/usage) | ```<h2( class="[\w ]*")?><[\w= "-]*>[\w ]*</[\w]*>``` |
| 3(noun/verb/exclamation/Phase/Phase verbs/Origin) | ```<h3 class="[\w ]*"><(span class="[\w ]*"|strong)>[\w ]*</(span|strong)></h3>``` |
| 4()

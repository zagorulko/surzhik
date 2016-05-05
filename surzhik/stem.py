"""
Russian stemming algorithm provided by Dr Martin Porter (snowball.tartarus.org):
http://snowball.tartarus.org/algorithms/russian/stemmer.html

Algorithm implementation in PHP provided by Dmitry Koterov (dklab.ru):
http://forum.dklab.ru/php/advises/HeisticWithoutTheDictionaryExtractionOfARootFromRussianWord.html

Algorithm implementation adopted for Drupal by Algenon (4algenon@gmail.com):
https://drupal.org/project/ukstemmer

Algorithm implementation in Python by Zakharov Kyrylo
https://github.com/Amice13

Algorithm implementation adopted for Python 3 by Vlad Zagorulko (zagovlad@gmail.com)
"""
import re

VOWEL = '[аеиоуюяіїє]' # http://uk.wikipedia.org/wiki/Голосний_звук
PFGROUND = '(ив|ивши|ившись|ыв|ывши|ывшись((?<=[ая])(в|вши|вшись)))$'
REFLEXIVE = '(с[яьи])$' # http://uk.wikipedia.org/wiki/Рефлексивне_дієслово
ADJECTIVE = '(ими|ій|ий|а|е|ова|ове|ів|є|їй|єє|еє|я|ім|ем|им|ім|их|іх|ою|йми|іми|у|ю|ого|ому|ої)$'  # http://uk.wikipedia.org/wiki/Прикметник + http://wapedia.mobi/uk/Прикметник
PARTICIPLE = '(ий|ого|ому|им|ім|а|ій|у|ою|ій|і|их|йми|их)$'  # http://uk.wikipedia.org/wiki/Дієприкметник
VERB = '(сь|ся|ив|ать|ять|у|ю|ав|али|учи|ячи|вши|ши|е|ме|ати|яти|є)$'  # http://uk.wikipedia.org/wiki/Дієслово
NOUN = '(а|ев|ов|е|ями|ами|еи|и|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я|і|ові|ї|ею|єю|ою|є|еві|ем|єм|ів|їв|ю)$'  # http://uk.wikipedia.org/wiki/Іменник
DERIVATIONAL = '[^аеиоуюяіїє][аеиоуюяіїє]+[^аеиоуюяіїє]+[аеиоуюяіїє].*(?<=о)сть?$'

def substitute(rvl, fr, to=''):
    orig = rvl[0]
    rvl[0] = re.sub(fr, to, rvl[0])
    return orig != rvl[0]

def stem_word(word):
    word = word.lower()
    if not re.search(VOWEL,word):
        return word

    p = re.search(VOWEL,word)
    rvl = [word[p.span()[1]:]]

    # Step 1
    if not substitute(rvl,PFGROUND):
        substitute(rvl,REFLEXIVE)
    if substitute(rvl,ADJECTIVE):
        substitute(rvl,PARTICIPLE)
    elif not substitute(rvl,VERB):
        substitute(rvl,NOUN)

    # Step 2
    substitute(rvl,'и$')

    # Step 3
    if re.search(DERIVATIONAL,rvl[0]):
        substitute(rvl,'ость$')

    # Step 4
    if substitute(rvl,'ь$'):
        substitute(rvl,'ейше?$')
    substitute(rvl,'нн$','н')

    return word[0:p.span()[1]] + rvl[0]

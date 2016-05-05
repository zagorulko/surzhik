#!/usr/bin/env python3
import json
import os
from glob import glob

from surzhik import Stats

ss = Stats('data/dict/uk_UA.txt','data/dict/word_list.txt')

news = {}
with open('data/news/tsn.txt','r') as fin:
    news = json.load(fin)

output = {}

for link,text in news.items():
    if 'ru.tsn.ua' in link:
        continue

    print(link)

    st = ss.stats_text(text,heur_fp=False)

    print('+ %i words' % st['total'])
    if st['count']:
        print('+ %i occurences detected' % st['count'])
        output[link] = st

with open('data/news/stats-tsn.txt', 'w') as fout:
    json.dump(output, fout, indent=4, sort_keys=True, ensure_ascii=False)

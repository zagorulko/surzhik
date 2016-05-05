#!/usr/bin/env python3
import json
import os
from glob import glob

from surzhik import Stats

ss = Stats('data/dict/uk_UA.txt','data/dict/word_list.txt')

output = {}

for author in os.listdir('data/lit/books'):
    author_path = 'data/lit/books/'+author+'/'
    output[author] = {}

    for path in sorted(glob(author_path+'*.txt')):
        book = path[len(author_path):-4]
        print('%s: %s' % (author,book))

        st = ss.stats_file(path)

        print('+ %i words' % st['total'])
        if st['count']:
            print('+ %i occurences detected' % st['count'])

        output[author][book] = st

with open('data/lit/stats-books.txt', 'w') as fout:
    json.dump(output, fout, indent=4, sort_keys=True, ensure_ascii=False)

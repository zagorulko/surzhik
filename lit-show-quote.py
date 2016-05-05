#!/usr/bin/env python3
import os
from glob import glob

from surzhik import Stats

path_all = []
for author in os.listdir('data/lit/books'):
    author_path = 'data/lit/books/'+author+'/'
    for path in sorted(glob(author_path+'*.txt')):
        path_all.append(path)

filt = input('Where: ').lower()
path_var = [v for v in path_all if filt in v.lower()]

if not path_var:
    print('No books found')
    exit(1)

path = ''
if len(path_var) == 1:
    path = path_var[0]
else:
    for i,v in enumerate(path_var):
        print('%i: %s' % (i+1,v))
    ch = int(input('[1-%i]: ' % len(path_var)))
    path = path_var[ch-1]

ss = Stats('data/dict/uk_UA.txt','data/dict/word_list.txt')
st = ss.stats_file(path,quote=True)

print('%i/%i' % (st['count'],st['total']))
for word,quotes in st['where'].items():
    for quote in quotes:
        print('[%s] %s' % (word,quote[1]))

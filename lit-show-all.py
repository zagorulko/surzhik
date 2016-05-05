#!/usr/bin/env python3
import json
from collections import defaultdict

from tabulate import tabulate

data = {}
with open('data/lit/stats-books.txt','r') as fin:
    data = json.load(fin)

table = []
headers = ['Автор','Твір','Слів']

for author,books in data.items():
    for book,stats in books.items():
        if stats['count']:
            table.append([author,book,stats['count']])

table = sorted(table)

print(tabulate(table,headers,tablefmt='psql'))

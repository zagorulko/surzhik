#!/usr/bin/env python3
import json
from collections import defaultdict

import pygal
from tabulate import tabulate

data = {}
with open('data/lit/stats-books.txt','r') as fin:
    data = json.load(fin)

def top_books(data, chart_path, abs=True, bound=30):
    top = []
    for author,books in data.items():
        for book,stats in books.items():
            rate = stats['count']
            if abs:
                pass
            else:
                rate /= stats['total']
                rate *= 100.
            top += [(rate,author,book)]
    top = sorted(top, reverse=True)

    table = []
    headers = ['#','Вх.' if abs else 'Вх., %','Автор','Твір']

    for i in range(min(bound,len(top))):
        s = ('%i' if abs else '%.2f') % top[i][0]
        table.append([i+1,s,top[i][1],top[i][2]])

    print('За творами (%s):' % ('абсолютно' if abs else 'відносно'))
    print(tabulate(table,headers,tablefmt='psql'))
    print()

    chart = pygal.Bar(style = pygal.style.DarkGreenBlueStyle,
        truncate_legend=50, width=1000, height=700)

    chart.title = 'Знайдені випадки вживання суржику в українській літературі (%s):' % (
        'абсолютно' if abs else 'відносно розміру твору')

    for i in range(min(bound,len(top))):
        s = ('%i' if abs else '%.2f%%') % top[i][0]
        chart.add('%i. %s - %s (%s)' % (i+1,top[i][1],top[i][2],s),[top[i][0]])

    chart.render_to_png(chart_path)

def top_authors(data, chart_path, bound=30):
    top_a = defaultdict(int)
    for author,books in data.items():
        for book,stats in books.items():
            top_a[author] += stats['count']

    table = []
    headers = ['#','Вх.','Автор']

    top = [(v,k) for k,v in top_a.items()]
    top = sorted(top, reverse=True)
    for i in range(min(bound,len(top))):
        table.append([i+1,top[i][0],top[i][1]])

    print('За авторами:')
    print(tabulate(table,headers,tablefmt='psql'))
    print()

    chart = pygal.Bar(style = pygal.style.DarkGreenBlueStyle,
        truncate_legend=50, width=1000, height=700)

    chart.title = 'Знайдені випадки вживання суржику різними авторами:'

    for i in range(min(bound,len(top))):
        chart.add('%i. %s (%i)' % (i+1,top[i][1],top[i][0]),[top[i][0]])

    chart.render_to_png(chart_path)

def top_words(data, bound=30):
    top_w = defaultdict(int)
    for author,books in data.items():
        for book,stats in books.items():
            for word in stats['where']:
                top_w[word] += len(stats['where'][word])

    table = []
    headers = ['#','Повторень','Випадок']

    top = [(v,k) for k,v in top_w.items()]
    top = sorted(top, reverse=True)
    for i in range(min(bound,len(top))):
        table.append([i+1,top[i][0],top[i][1]])

    print('За випадками:')
    print(tabulate(table,headers,tablefmt='psql'))
    print()

top_books(data,'report/lit/abs.png')
top_books(data,'report/lit/rel.png',abs=False)
top_authors(data,'report/lit/author.png')
top_words(data)

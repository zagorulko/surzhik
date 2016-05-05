#!/usr/bin/env python3
import os
import re
from collections import defaultdict

from .stem import stem_word

class Stats:
    def __init__(self, exceptions_dict, surzhik_dict, ex_base=[]):
        self.stem_cache = {}

        self.stem_exceptions = set([
            'прийшл','сам','прив','прин'
        ]+ex_base)
        with open(exceptions_dict) as fin:
            for l in fin.read().splitlines():
                stem = stem_word(l)
                self.stem_exceptions.add(stem)

        self.route = {}
        with open(surzhik_dict) as fin:
            for entry in [self._stem(l) for l in fin.read().splitlines()]:
                if entry and entry[0] != '#':
                    self._route_insert(self.route,entry.split(' '))

    def _stem(self, word):
        if word not in self.stem_cache:
             stem = stem_word(word)
             if stem in self.stem_exceptions:
                 stem = word
             self.stem_cache[word] = stem
        return self.stem_cache[word]
        #return word.lower()

    def _route_insert(self, route, path):
        if not path: return
        base = self._stem(path.pop(0))
        route[base] = {}
        self._route_insert(route[base],path)

    def _is_surzhik(self, words, i, route=None):
        if route == None:
            route = self.route
        if i >= len(words):
            return False
        s = self._stem(words[i])
        if s not in route:
            return False
        if len(route[s]):
            sub = self._is_surzhik(words,i+1,route[s])
            return False if not sub else words[i].lower()+' '+sub
        return words[i].lower()

    def stats_text(self, text, quote=False, heur_fp=True):
        pos, count = 0, 0
        cases, where =  defaultdict(int), defaultdict(list)

        for sentence in [s.strip() for s in text.split('.')]:
            delims = [re.escape(d) for d in ['\n', ' ', ',', '?', '!', ':']]
            words = re.split('|'.join(delims), sentence)
            for i in range(len(words)):
                pos += 1
                case = self._is_surzhik(words,i)
                if not case:
                    continue
                count += 1
                cases[case] += 1
                where[case].append((pos,sentence) if quote else pos)

        # heuristic to reduce false positives
        if heur_fp and (count < 20 or len(cases) < 3):
            count, cases, where = 0, {}, {}

        return {
            'total': pos,
            'count': count,
            'cases': cases,
            'where': where
        }

    def stats_file(self, path, quote=False, heur_fp=True):
        with open(path,'r') as fin:
            return self.stats_text(fin.read(),quote,heur_fp)

if __name__ == '__main__':
    ss = SurzhikStats('data/uk_UA.txt','data/word_list.txt')
    print(ss.route)

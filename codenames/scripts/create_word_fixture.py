#!/usr/bin/env python
'''Usage:
    python create_word_fixture.py /path/to/word_list.txt > word_fixture.json
Turns a plain newline separated list of words in a text file into
a json file that can be loaded as a base of words:
    ./manage.py loaddata word_fixture.json
'''
import sys
import json

word_file = sys.argv[1]
fixtures = []

with open(word_file, 'rb') as f:
    for line in f:
        word = line.strip('\n')
        fixtures.append({"fields": {"text": word}, "model": "codenames.word"})

print json.dumps(fixtures)

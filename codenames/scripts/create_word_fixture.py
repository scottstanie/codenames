#!/usr/bin/env python
'''Usage:
    python create_word_fixture.py /path/to/word_list.txt my_word_set > word_fixture.json
Turns a plain newline separated list of words in a text file into
a json file that can be loaded as a base of words:
    ./manage.py loaddata word_fixture.json
'''
import sys
import json

if len(sys.argv) < 3:
    print("Usage: python create_word_fixture WORD_FILE.TXT MY_WORD_SET")
    sys.exit(1)

word_file = sys.argv[1]
word_set = sys.argv[2]
fixtures = []

with open(word_file, 'rb') as f:
    for line in f:
        word = line.strip('\n')
        fixtures.append({"fields": {"text": word, "word_set": word_set}, "model": "codenames.word"})

print(json.dumps(fixtures))

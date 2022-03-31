#!/usr/bin/env python3
import sys
import re

def count_things (file, word, number):
    word_regex = "[^A-Za-z]+"
    number_regex = "(-|)[0-9]+"
    special_number_regex = "[^-|^0-9]"
    f = open(file, "r")
    for i in f.readlines():
        t_word = 0
        t_number = 0
        line = i.strip().split()
        for j in range(len(line)):
            if re.search(word_regex, line[j]) is None:
                t_word += 1
            if re.search(number_regex, line[j]) is not None:
                if re.search(special_number_regex,re.search(number_regex, line[j]).string) is None:
                    t_number +=1
        word += t_word
        number += t_number

    f.close()
    return word, number

def main():
    word = 0
    number = 0
    file = sys.argv[1]
    word, number = count_things(file, word, number)
    print("In the file %s, there are %d words and %d numbers" % (file, word, number))

main()

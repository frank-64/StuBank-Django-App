#!/usr/bin/python
# -*- coding: utf-8 -*-
# by ..:: crazyjunkie ::.. 2014
# If you need a Good Wordlist ====> http://uploaded.net/folder/j7gmyz

"""
gencc: A simple program to generate credit card numbers that pass the
MOD 10 check (Luhn formula).
Usefull for testing e-commerce sites during development.
by ..:: crazyjunkie ::.. 2014
"""

from random import Random
import copy
import datetime

from django.utils import timezone

StuBankPrefix = [['2', '0', '0', '2']]



def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):

            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    return ''.join(ccnumber)


def credit_card_number(rnd, length, howMany):

    result = []

    while len(result) < howMany:

        ccnumber = copy.copy(rnd.choice(StuBankPrefix))
        result.append(completed_number(ccnumber, length))
    return result

generator = Random()
generator.seed()        # Seed from current time

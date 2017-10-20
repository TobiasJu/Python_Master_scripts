#!/usr/bin/env python
# -*- coding: utf-8 -*-

# script for generating an IOTA seed, or private key

from random import SystemRandom
alphabet = u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ'
generator = SystemRandom()
print(u''.join(generator.choice(alphabet) for _ in range(81)))


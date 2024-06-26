#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   learn_argparse.py
@time    :   2024/06/26 21:31:23
@author  :   xiongkouqin 
@Email   :   xiongkouqin413@gmail.com
@description   :   I created this script to get familiar with module argparse
'''


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()
print(args.echo)
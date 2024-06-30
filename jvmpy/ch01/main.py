#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   main.py
@time    :   2024/06/26 00:57:16
@author  :   xiongkouqin 
@email   :   xiongkouqin413@gmail.com
@description   :   主程序
'''

import argparse
from my_cmd import MyCmd

def main():
    parser = argparse.ArgumentParser(prog="jvmpy")
    parser.add_argument("-v", '--version', action="store_true", help="print version and exit.", dest="version_flag")
    parser.add_argument("-cp", "--classpath", action="store", type=str, help="specify your java classpath.", dest="cp_option")
    parser.add_argument("args", nargs='*')
    args = parser.parse_args()
    cmd = MyCmd(args)
    if cmd.version_flag:
        cmd.print_version()
    else:
        print("start jvm")
        start_JVM(cmd=cmd)
        
def start_JVM(cmd):
    print(f"classpath = {cmd.classpath}, classname = {cmd.classname}, args = [{' '.join(cmd.args)}]")
    

if __name__  == "__main__":
    main()


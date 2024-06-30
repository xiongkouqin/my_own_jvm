#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   main.py
@time    :   2024/06/26 00:57:16
@author  :   xiongkouqin 
@Email   :   xiongkouqin413@gmail.com
@description   :   主程序
'''

import argparse
from ch02.my_cmd import MyCmd
from ch02.my_classpath.classpath import Classpath

def main():
    parser = argparse.ArgumentParser(prog="jvmpy")
    parser.add_argument("-v", '--version', action="store_true", help="print version and exit.", dest="version_flag")
    parser.add_argument("-cp", "--classpath", action="store", type=str, help="specify your java classpath.", dest="cp_option")
    parser.add_argument("args", nargs='+', help='Specify your main class and arguments')
    parser.add_argument("-Xjre", action="store", type=str, help="specify your jre location", dest="xjre_option")
    args = parser.parse_args()
    cmd = MyCmd(args)
    if cmd.version_flag:
        cmd.print_version()
    else:
        print("start jvm")
        start_JVM(cmd=cmd)
        
def start_JVM(cmd:MyCmd):
    cp = Classpath.parse(cmd.xjre_option, cmd.classpath)
    print(f'classpath: {cmd.classpath}, class:{cmd.classname}, args: {cmd.args}')
    
    # 这里有一点不懂 等下debug看下内部吧
    main_class_name = cmd.classname.replace('.', '/')
    class_data, _, error = cp.read_class(main_class_name)
    if error:
        print(f'Could not find or load main class{main_class_name}, error occurred: {error}')
        exit(0)
    # print data read
    print(f'data read from main class {[int(hex(d), 16) for d in class_data]}')
    

if __name__  == "__main__":
    import os  
    print(os.getcwd())
    main()


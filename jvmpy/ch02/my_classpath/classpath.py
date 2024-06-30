#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   classpath.py
@time    :   2024/06/30 14:29:23
@author  :   xiongkouqin 
@email   :   xiongkouqin413@gmail.com
@description   :   {to be filled}

这个类有三个字段：用于存放三种类路径
'''

import os

from ch02.my_classpath.entry import Entry


class Classpath:
    
    def __init__(self) -> None:
        # 启动类路径 
        self.boot_classpath = None 
        # 扩展类路径
        self.ext_classpath = None 
        # 用户类路径
        self.user_classpath = None 
        
    
    # 解析类路径，并且返回一个ClassPath实例，感觉有点像工厂模式？
    @staticmethod
    def parse(jre_option, cp_option):
        cp = Classpath()
        cp.parse_boot_and_ext_classpath(jre_option)
        cp.parse_user_classpath(cp_option)
        return cp 
    
    
    def parse_boot_and_ext_classpath(self, jre_option):
        # jre options might be None,
        # if it's None, we try to find it from env?
        jre_dir = self.__get_jre_dir(jre_option)
        jre_lib = os.path.join(jre_dir, 'lib', '*')
        self.boot_classpath = Entry.new_entry(jre_lib)
        jre_ext = os.path.join(jre_dir, 'lib','ext', '*')
        self.ext_classpath = Entry.new_entry(jre_ext)
    
    def parse_user_classpath(self, cp_option):
        if not cp_option:
            cp_option = '.'
        self.user_classpath = Entry.new_entry(cp_option)
    
    def read_class(self, class_name):
        class_name = class_name + '.class'
        data, entry, error = None, None, None 
        if self.boot_classpath:
            data, entry, error = self.boot_classpath.read_class(class_name)
        if not data and self.ext_classpath:
            data, entry, error = self.ext_classpath.read_class(class_name)
        if not data and self.user_classpath:
            data, entry, error =  self.user_classpath.read_class(class_name)
        return data, entry, error
        
        
    def __get_jre_dir(self,jre_option):
        if jre_option  and os.path.isdir(jre_option):
            return jre_option
        java_home = os.environ.get('JAVA_HOME')
        if java_home:
            return os.path.join(java_home, 'jre')
        raise RuntimeError('Failed to find jre location')
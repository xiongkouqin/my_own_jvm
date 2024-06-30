#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   entry.py
@time    :   2024/06/29 16:13:44
@author  :   xiongkouqin 
@Email   :   xiongkouqin413@gmail.com
@description   :   Entry接口, Python3 abc模块提供了抽象基类的支持。
ABC: abstract base class
'''

from abc import ABC, abstractmethod


class Entry(ABC):
    # 获得当前操作系统路径分隔符号
    # path_list_separator = os.path.sep
    path_list_separator = ':' # 我自己定义一个吧 哈哈
    
    # 寻找和加载class文件，接口的方法，实现类应该自己去定义
    @abstractmethod
    def read_class(self, class_name):
        pass
    
    # 静态方法，根据指定的path来确认返回某一种类型的Entry
    # 返回的Entry调用自己实现的read_class来完成类加载
    @staticmethod
    def new_entry(path:str):
        from ch02.my_classpath.composite_entry import CompositeEntry
        from ch02.my_classpath.wildcard_entry import WildcardEntry
        from ch02.my_classpath.dir_entry import DirEntry
        from ch02.my_classpath.zip_entry import ZipEntry
        if Entry.path_list_separator in path:
            return CompositeEntry(path)
        elif path.endswith('*'):
            return WildcardEntry(path)
        elif path.endswith('.jar') or path.endswith('.JAR') or path.endswith('.zip') or path.endswith('.ZIP'):
            return ZipEntry(path)
        else:
            return DirEntry(path)        

#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   dir_entry.py
@time    :   2024/06/29 16:19:51
@author  :   xiongkouqin 
@email   :   xiongkouqin413@gmail.com
@description   :   表示目录形式的类路径
'''

from ch02.my_classpath.entry import Entry
import os 

class DirEntry(Entry):
    
    # 传进来的未必是绝对路径
    # 我们把它转化一下再保存  
    def __init__(self, path) -> None:
        # super().__init__() 
        self.abs_dir = os.path.abspath(path)
        
    def read_class(self, class_name):
        file_name = os.path.join(self.abs_dir, class_name)
        data, error = None, None 
        try: 
            with open(file_name, 'rb') as file: # with保证文件被正常关闭 无论是否发生异常
                data = file.read()
        except IOError as e:
            error = e 
        return data, self, error 
    
    def __str__(self) -> str:
        return f'DirEntry(abs_dir={self.abs_dir})'
    
    def __repr__(self) -> str:
        return f'DirEntry(abs_dir={self.abs_dir})'
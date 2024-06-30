#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   zip_entry.py
@time    :   2024/06/29 16:20:44
@author  :   xiongkouqin 
@email   :   xiongkouqin413@gmail.com
@description   :   从zip/jar 文件中读取指定的class file
JAR（Java Archive）文件本质上是一个ZIP文件
'''

from ch02.my_classpath.entry import Entry
import os 
import zipfile

class ZipEntry(Entry):
    def __init__(self, path) -> None:
        # super().__init__() 
        self.abs_dir = os.path.abspath(path)
        
    def read_class(self, class_name):
        data, error = None, None
        try:
            with zipfile.ZipFile(self.abs_dir, 'r') as zip_ref:
                if class_name in zip_ref.namelist():
                    data = zip_ref.read(class_name)
                else:
                    raise FileExistsError(f'{class_name} not exists in {self.abs_dir}')
        except FileNotFoundError as e:
            error = e 
        except zipfile.BadZipFile as e:
            error = e 
        return data, self, error 
    
    def __str__(self) -> str:
        return f'ZipEntry({self.abs_dir})'
    
    def __repr__(self) -> str:
        return f'ZipEntry({self.abs_dir})'
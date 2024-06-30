#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   composite_entry.py
@time    :   2024/06/29 16:19:16
@author  :   xiongkouqin 
@email   :   xiongkouqin413@gmail.com
@description   :   指定了多个路径，对每个路径去构造一个Entry存储在list中
'''

from ch02.my_classpath.entry import Entry

class CompositeEntry(Entry):
    
    def __init__(self, path_list:str) -> None:
        self.composition_entry_list = []
        
        if path_list.find(Entry.path_list_separator) > 0:
            for path in path_list.split(Entry.path_list_separator):
                entry = Entry.new_entry(path)
                self.composition_entry_list.append(entry)
    
    def read_class(self, class_name):
        for entry in self.composition_entry_list: 
            data, entry_, error = entry.read_class(class_name)
            if data:
                return data, entry_, error
        return None, None, f"Error on Looking for {class_name}"
    
    
    def __str__(self) -> str:
        return str.join(Entry.path_list_separator, self.composition_entry_list)



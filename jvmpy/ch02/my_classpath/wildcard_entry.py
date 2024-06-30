#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   wildcard_entry.py
@time    :   2024/06/29 16:20:19
@author  :   xiongkouqin 
@Email   :   xiongkouqin413@gmail.com
@description   :   /dir/* 形式，所以本质上也是 一个 CompositeEntry, 但是注意通配符路径不能提柜匹配子目录下的jar文件
因此 简单来说，直接去继承 CompositeEntry
然后调用super().__init__()
这里因为不会有 path_seprator所以init里面只会初始化list

'''

from ch02.my_classpath.composite_entry import CompositeEntry
from ch02.my_classpath.zip_entry import ZipEntry
import os 

class WildcardEntry(CompositeEntry):
    
    def __init__(self, path: str) -> None:
        super().__init__(path)
        base_dir = path[:-1] # 去掉最后面的星号
        # for root, dirs, files in os.walk(base_dir): 
        # 这个walk会递归便利subdir 这里按照需求应该是不想要这样
        for item in os.listdir(base_dir):
            if item.endswith('.jar') or item.endswith('.JAR'):
                jar_entry = ZipEntry(os.path.join(base_dir, item))
                self.composition_entry_list.append(jar_entry)
         
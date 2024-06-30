#! /usr/bin/env python
# encoding: utf-8
'''
@file    :   cmd.py
@time    :   2024/06/26 00:56:17
@author  :   xiongkouqin 
@Email   :   xiongkouqin413@gmail.com
@description   :   命令行类
'''

class MyCmd:   
  
    def __init__(self, args_obj): 
        self._version_flag = None
        self._classpath = None
        self._classname = None
        self._args = None
        self._xjre_option = None
        # 检查并设置实例属性  
        if hasattr(args_obj, 'version_flag') and args_obj.version_flag:
            self._version_flag = args_obj.version_flag
        if hasattr(args_obj, 'cp_option') and args_obj.cp_option:  
            self._classpath = args_obj.cp_option    
        if hasattr(args_obj, 'args') and args_obj.args:  
            self._classname = args_obj.args[0]
            self._args = args_obj.args[1:]
        if hasattr(args_obj, "xjre_option") and args_obj.xjre_option:
            self._xjre_option = args_obj.xjre_option
            
    @property
    def version_flag(self):
        return self._version_flag
            
    @property
    def classpath(self):
        return self._classpath
    
    @property
    def classname(self):
        return self._classname
    
    @property
    def args(self):
        return self._args
    
    @property
    def xjre_option(self):
        return self._xjre_option
    
    def print_version(self):
        print('version 0.0.1')
    
    
    
    
    
            

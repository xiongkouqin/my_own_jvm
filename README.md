# Python实现JVM记录

## CH01. 命令行工具

## 0. 总体逻辑

1. 定义一个类叫Cmd，表示命令行
2. 使用`os.Args`来获取命令行参数，但是自己去处理这里面的变量要写很多代码，因此可以用一个包`flag`来帮助处理命令行选项
3. 上面这个所谓的`flag`包主要是来解析比如里面有没有表示help, version, cpOption的参数
4. 如果没有的话，那么就打印usage说明用户输入的参数不能被正确解析，告诉用户usage是什么
5. 总体流程
	1. 如果有versionFlag， 打印版本信息
	2. 如果有helpFlag打印帮助信息，或者class为空也是帮助信息
	3. 否则启动jvm

### 1. Python文件开头的!#

- `!#`叫Sha-bang, 用于指明这个脚本的解释器，如果某个脚本有执行权限就可以不用指定解释器直接运行。
- 相比/usr/bin/python 写 /usr/bin/env更好。
- \# encoding: utf-8 指定编码格式

### 2. ArgParse

> [Doc](https://docs.python.org/zh-cn/3.13/howto/argparse.html)
>
> I didn't use the optparse because the it has been deprecated

- module for command line parsing - decides the behavior of your program on the given options

- `-h` or `--help`is the only option you got for free

- `arg_parse()` specify which command-line options the program is willing to accept

- `args = parser.parse_args()` parse the arguments, so we can get them from args

- we can do more

	```python
	# it's call positional argument
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("square", help="display a square of a given number",
	                    type=int)
	args = parser.parse_args()
	print(args.square**2)
	```

- `parser.add_argument("--verbosity", help="increase output verbosity")` works when `python prog.py --verbosity 1`

	```python
	# optional arguments
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--verbosity", help="increase output verbosity")
	args = parser.parse_args()
	if args.verbosity:
	    print("verbosity turned on")
	```

- but after, all it's a flag, because we use if, so we can do more to assign true to it as long as the flag presents

- `parser.add_argument("--verbosity", help="increase output verbosity", action="store_true")`

- Short options: `parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")`

- restrain the value can be accepted: `parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")`



## CH02. 搜索class文件

### 2.1 类路径

Java虚拟机没有规定虚拟机从哪里寻找类，Oracle的虚拟机实现如下：按照搜索先后顺序

- 启动类路径 bootstrap classapth 
	- 默认对应jre/lib
	- Java标准库
- 扩展类路径 extension classpath 
	- 默认在jre/lib/ext
- 用户类路径 user classpath 
	- 默认当前目录
	- -cp来指定
	- 可以指定多个 java -cp path/to/classes:lib/b

### 2.2 准备工作

1. 指定jre目录的位置
	- -Xjre

### 2.3 实现类路径

类路径由三个小的路径构成，因此可以使用`组合模式`来实现类路径。

#### 2.3.1 Entry接口

有两个方法

```java
[]byte, Entry, error readClass(String className){
  // 参数是class文件的相对路径，文件名有.class后缀
  // 比如读取java.lang.Object, 传入的参数是java/lang/Object.class 
  
  // 返回值
  // byte: 读到的字节数据
  // Entry: 最终定位到class文件的Entry ??? 不确定是什么
  // error 错误信息
}

toString()
```

另外有一个 newEntry方法

- 根据参数创建不同类型的Entry实例
- Entry接口有四个实现 
	- DirEntry
	- ZipEntry
	- CompositeEntry
	- WildcardEntry



**下面就不单独写了，总结一下大概的逻辑吧！**

1. `cmd`去parse参数，拿到用户指定的jre和自定义的classpath, 以及启动类

2. 用jre_option和classpath去构造`Classpath`类

	```python
	cp = Classpath.parse(cmd.xjre_option, cmd.classpath)
	
	# Classpath有一个静态方法
	# 里面根据参数来构造上面说的三种路径的Entry
	# 最后返回构造完的Classpath实例
	@staticmethod
	    def parse(jre_option, cp_option):
	        cp = Classpath()
	        cp.parse_boot_and_ext_classpath(jre_option)
	        cp.parse_user_classpath(cp_option)
	        return cp 
	```

3. 上面的parse主要做的是，对每个路径，解析出完整的路径，返回一个`Entry`，Entry里面有`read_class`方法来真正进行读取

4. `Entry`是一个抽象类，类似接口，然后有四种实现，本身定一个`new_entry`方法，根据参数来返回对应的实现类

	```python
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
	        if Entry.path_list_separator in path: # /dir1:/dir2 的形式
	            return CompositeEntry(path)
	        elif path.endswith('*'): # /dir/* 的形式
	            return WildcardEntry(path)
	        elif path.endswith('.jar') or path.endswith('.JAR') or path.endswith('.zip') or path.endswith('.ZIP'):
	            return ZipEntry(path)
	        else:
	            return DirEntry(path)  # 普通的/dir
	```

5. 讲讲每个Entry实现类

	1. DirEntry 

		- 参数形式对应的是/dir/xxx
		- 直接在/dir/xxx 下面找对应的文件，比如java.lang.Object, 就是看/dir/xxx/java/lang/Object.class能不能读到

	2. ZipEntry

		- 参数形式是/dir/xxx.zip or .jar

		- ```python
			with zipfile.ZipFile(self.abs_dir, 'r') as zip_ref:
			                if class_name in zip_ref.namelist(): # 递归的返回全部存在的文件和目录
			```

		- 所以本质上，我觉得和上面的dir是一样的，压缩包也可以看成一个特殊的目录嘛

	3. CompositeEntry

		- 参数形式是/dir/xxx:/dir/xxx/*
		- 对参数中的每一个路径去调用Entry.new_entry,得到相应的

	4. WildcardEntry

		- 参数形式是/dir/xxx/*
		- 本质上是一个CompositeEntry
		- 然后不递归，就是说我这样写了之后（假设program.jar里面有object那个类）
			- /dir/xxx/program.jar 可以被找到
			- 但是/dir/xxx/yyy/program.jar不行？

6. 以上，三种路径每个都有自己的entry, 加载一个类的时候就按照顺序读取

	```python
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
	```



> ⚠️
>
> 这里遇到了ModuleImportError 
>
> 解决的办法是，查看一下sys.path是什么，里面的目录假设是/xxx
>
> 那么我import的时候 ch02.entry.. 这个ch02必须存在在xxx内
>
> 然后可以自己在环境变量增加pythonpath
>
> ```bash
> export PYTHONPATH="/Users/xiongkouqin/dev/my_own_jvm/jvmpy:$PYTHONPATH"
> ```


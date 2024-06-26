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

- 


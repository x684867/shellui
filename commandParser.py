#!/usr/bin/env python
#
# commandParser.py
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Sam Caldwell.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from logger import logger

class commandParser:
	__command=''
	__parameter=''
	__arguments=[]
	__log=None
	
	@property
	def command(self):
		return self.__command
	
	@property
	def parameter(self):
		return self.__parameter
	
	@property
	def arguments(self):
		return self.__arguments
	
	@command.setter
	def command(self,c):
		self.__command=c
	
	@parameter.setter
	def parameter(self,p):
		self.__parameter=p
		
	@arguments.setter
	def arguments(self,a):
		if typeof(a) is list:
			self.__arguments=a
		else:
			raise Exception( \
				"parsedCommandClass::arguments.setter failed.  " + \
				"Type mismatch (expected <list>)" \
			)

	def __init__(self):
		self.__log=logger('commandParser')
		self.__log.write("commandParser::__init__()")
	
	def __del__(self):
		self.__log.write("commandParser::__del__()")
	
	def hasCommand(self):
		return (self.__command =='')
	
	def parse(commandString):
		#
		# command
		# command <parameter>
		# command --recipe <recipeName> --account <accountName> [--verbose]
		# command <parameter> [--recipe <recipeName>] [--account <accountName>] [--verbose]
		#
		PARSE_ITEM_NONE=0
		PARSE_ITEM_ARG=1
		PARSE_ITEM_VALUE=2
		#
		try:
			if typeof(commandString) is str:
				arrCmd=re.sub(' +',' ',commandString).split(' ')
			else:
				raise Exception("commandString not type <string>")
			# start parsing for the <command>
			if len(arrCmd) == 0:
				self.__command=""
				self.__parameter=""
				self.__arguments=[]
			elif len(arrCmd) >=1:
				#A command exists.
				self.__command=arrCmd.pop(0)
				#Check for a parameter.		
				if (len(arrCmd) >0) and (arrCmd[0][0:2] != "--"):
					self.__parameter=arrCmd.pop(0)
				#Check for arguments.
				lastItem=PARSE_ITEM_NONE
				a=''
				v=''
				while len(arrCmd) >0:
					item=arrCmd(0)
					if item[0:2] == "--":
						a=item[2:]
						lastItem=PARSE_ITEM_ARG
					else:
						if lastItem==PARSE_ITEM_ARG:
							v=item
							lastItem=PARSE_ITEM_VALUE
						else:
							raise Exception("syntax error.  Expected --<argName>")
					self.__arguments.append({a:v})
			else:
				raise Exception("unexpected internal error.")
		except Exception as err:
			self.__log.write("commandParser::parse() ERROR:"+str(err))
			
			
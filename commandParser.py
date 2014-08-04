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

import re
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
	
	def __del__(self):
		pass
		
	def hasCommand(self):
		return (len(self.__command)!=0)
	
	def parse(self,commandString):
		#
		# cmd
		# cmd <param>
		# cmd <param> [--recipe <recipe>] [--account <acctName>] [--verbose]
		# cmd --recipe <recipe> --account <acctName> [--verbose]
		#
		try:
			try:
				if type(commandString) is str:
					arrCmd=re.sub(' +',' ',commandString).split(' ')
				else:
					raise Exception(
						"commandString not type <string> type:" + \
						str(type(commandString))
					)
			except Exception as err:
				raise Exception(str(err))

			if len(arrCmd) == 0:
				(self.__command,self.__parameter,self.__arguments)=("","",[])
			elif len(arrCmd) >=1:
				try:
					# start parsing for the <command>
					try:
						self.__command=arrCmd.pop(0)
					except Exception as err:
						raise Exception("failed to pop command ["+str(err)+"]")
						
					#Check for an optional parameter.		
					if (len(arrCmd) >0) and (arrCmd[0][0:2] != "--"):
						try:
							self.__parameter=arrCmd.pop(0)
						except Exception as err:
							raise Exception("failed to pop parameter ["+str(err)+"]")
						
					#Check for arguments.
					if arrCmd[0][0:2] == "--":
						#We have an argument.
						try:
							i=0					
							while len(arrCmd) >0:
								(a,v)=('','')
								item=arrCmd.pop(0)
								if item[0:2] == "--":
									a=item[2:]
									if arrCmd[0][0:2] != "--":
										v=arrCmd.pop(0)
									else:
										raise Exception("Syntax error.  Expected --<argName>")	
									self.__log.write(str(i)+":arg:  " +str(a))
								#
								self.__arguments.append({a:v})
								i+=1
						except Exception as err:
							raise Exception("failed to parse args ["+str(err)+"]")
					else:
						raise Exception("Syntax Error.  Expected --<argName>")	
				except Exception as err:
					raise Exception(str(err))
			else:
				raise Exception("unexpected internal error.")
		except Exception as err:
			raise Exception(str(err))




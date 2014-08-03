#!/usr/bin/env python
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
import sys
import curses
from logger import logger
from shellUIinput import shellUIinput
from commandParser import commandParser


class shellUI(shellUIinput):
	__parser=commandParser()
	__log=None
	__uiRow=0
	
	def __init__(self,motd="Message of the Day"):
		self.__log=logger('shellUI')
		try:
			shellUIinput.__init__(self,motd)	
			self.__uiRow=self.getRow()
		except Exception as err:
			self.__log.write("__init__(): error:"+str(err))

	def __del__(self):
		self.__log.write("__del__()")
		pass
	
	def getCommand(self):
		try:
			try:
				commandString=self.getInput(self.__uiRow)
				self.__uiRow+=1
			except Exception as err:
				raise Exception("shellUI failed to get command string.  " + str(err))

			self.__log.write("COMMANDLINE["+str(self.__uiRow)+"]: " + str(commandString))
			
			if self.__parser.hasCommand():
				try:
					self.__parser.parse(commandString)
				except Exception as err:
					raise Exception(err)
			
			self.__log.write(
				"\ncommand: 	" + self.__parser.command + "\n" + \
				"parameter:	" + self.__parser.parameter + "\n" + \
				"arguments: " + str(self.__parser.arguments) + "\n" \
			)
			return ( \
					self.__parser.command, \
					self.__parser.parameter, \
					self.__parser.arguments \
			)
		except Exception as err:
			self.__log.write(str(err))				
	
	
if __name__=="__main__":
	ui=shellUI()
	(c,p,a)=ui.getCommand()
	sys.exit(0)
	
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
import locale
from shellUIbase import shellUIbase
#
# command <parameter>
#
# command --recipe <recipeName> --account <accountName> [--verbose]
#
# command <parameter> [--recipe <recipeName>] [--account <accountName>] [--verbose]
#
class shellUI(shellUIbase):
	#parser properties.
	command=""
	parameter=""
	arguments=[]
	
	#command history.
	history=[]
	max_history=10

	def parse(self,commandString):
		self.log.write("shellUI::parse()")
		try:
			arrCmd=re.sub(' +',' ',commandString).split(' ')
			self.command=arrCmd[0]
			if len(arrCmd) > 1:
				#
				# get the command
				#
				arrCmd.remove(self.command)
				#
				# If the first argument is not
				# an optional argument, then it
				# is a "parameter" of the command.
				#
				if(arrCmd[0][0:2]!="--"):
					self.parameter=arrCmd[0]
					arrCmd.remove(self.parameter)
				#
				# Iterate through the remaining 
				# arguments and their optional
				# associated values.
				#
				while len(arrCmd) > 0:
					print "starting loop.  queue:"+str(arrCmd)
					arg=''
					value=''
					try:
						if arrCmd[0][0:2] == "--":
							# Encountered an argument --<argName>
							#print "queue: " + str(arrCmd)
							arg=arrCmd.pop(0)[2:]
							#print "queue: " + str(arrCmd)

							#print "we have an arg ["+arg + "] & a  value [" + str(arrCmd[0])+"]"
							if arrCmd[0] == "--":
								#print "null value."
								value=''
							else:
								# argument is followed by a value.
								# pop the value and move on.
								value=arrCmd.pop(0)
								#print "store value: "+ value
							# update the last item encountered.
							#print "update last"
						else:
							raise Exception("Expected --<argName> [<value>]")
					except IndexError as err:
						pass
					except Exception as err:
						raise err
					if arg!='':
						#print "appending arguments"
						self.arguments.append({arg:value})
					else:
						#print "empty arg."
						pass
			else:
				self.parameter=""
				self.arguments=[]
		except Exception as err:
			self.status.write("Syntax Error.  Check usage with -h or --help.  " + str(err))
		return (self.command,self.parameter,self.arguments)

	def interact(self,prompt="#"):
		self.log.write("shellUI::__interact__()")
		buffer=''
		return self.parse(self.__getInput__())
	
if __name__=="__main__":
	ui=shellUI()
	ui.log.write("\n-------------------")
	ui.log.write("start test...")
	ui.log.write("-------------------\n")
	(c,p,a)=ui.interact()
	ui.log.write("command:  " + c)
	ui.log.write("parameter:" + p)
	ui.log.write("argumetnt:" + str(a))
	ui.log.write("tests complete.")
	sys.exit(0)
	
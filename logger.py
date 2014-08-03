#!/usr/bin/env python
#
# logger.py
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
# Purpose:
#
#	This file provides a class for file-based logging.
#
# Todo:
#	(1) Define log timestamps
#	(2) Define log levels
#
import datetime

class logger:
	logFile="logger.log"
	channel=''
	fh=None
	def __init__(self,ch="undeclared_log"):
		self.channel=str(ch)
		try:
			self.fh=open(str(self.logFile),'a',0)
		except Exception as err:
			raise Exception("logger failed to open file: " + str(self.logFile))
		self.write(""+"-"*40)
		self.write("    "+str(self.logFile)+"["+str(self.channel)+"]")
		self.write("    Start: "+str(datetime.datetime.utcnow()))
	
	def __del__(self):
		self.fh.close()
	
	def write(self,m):
		try:
			ts=str(datetime.datetime.utcnow())[:-7]
			self.fh.write(ts+":"+self.channel+":"+str(m)+"\n")
			self.fh.flush()
		except Exception as err:
			raise Exception("logger failed to write ["+self.logFile+"]["+self.channel+"]")
		

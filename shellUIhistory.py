#!/usr/bin/env python 
#
# shellUIhistory.py
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
# This file provides a class that tracks
# command history from the shellUIinput
# class and returns the last command in
# a LIFO fashion on request.
#
# The history is currently non-persistent
# and has a maximum size defined by the
# class constructor.
#
from logger import logger

class shellUIhistory:
	__minSize=1
	__maxSize=0
	__buffer=[]
	__log=None
	__historyFile=None

	def __init__(self,bufSize=10):
		self.__log=logger('shellUIhistory')
		try:
			if bufSize > self.__minSize:
				self.__maxSize=bufSize
			else:
				self.__maxSize=self.__minSize
		except Exception as err:
			raise err
		try:
			self.__historyFile=open('shellUIhistory','a')
		except Exception as err:
			raise Exception(str(err))
	
	def __del__(self):
		self.__log=None
		try:
			for item in self.__buffer:
				self.__historyFile.write(str(item)+"\n")
			self.__historyFile.close()
		except Exception as err:
			pass

	def __pruneBuffer__(self):
		try:
			if len(self.__buffer) >= self.__maxSize:
				self.__historyFile.write(str(self.__buffer.pop(0))+"\n")
		except Exception as err:
			raise err
			
	def size(self):
		return len(self.__buffer)	
		
	def push(self,commandString):
		try:
			self.__pruneBuffer__()
			self.__buffer.append(commandString)
		except Exception as err:
			raise err
		
	def pop(self):
		try:
			top=len(self.__buffer)-1
			if top == 0:
				return ""
			else:
				return self.__buffer.pop(top)
		except Exception as err:
			raise err

#
# UNIT TESTS...
#
def unitTest(szTest=0,szBuff=0):
	testSize=0
	testData=[]
	ui=None
	
	if (type(szTest) is int) and (type(szBuff) is int):
		testSize=szTest
	else:	
		raise Exception("Expected integer test size and buffer size values")
	
	print "     preparing testData.  Size="+str(testSize)
	for i in range(testSize):
			testData.append("test" + str(i))
	
	print "     testData("+str(len(testData))+")="+str(testData)
	print "     test starting"

	print "     instantiating ui buffer("+str(szBuff)+")"
	ui=shellUIhistory(szBuff)
	print "          ui buffer declared("+str(ui.size())+")"
	
	print "     shellUIhistory instantiated."
	print "     loading data("+str(testSize)+")..."
	for test in testData:
		ui.push(test)
	print "     data loaded.  Starting validation test."
	
	testData.reverse()
	counter=0
	for rhs in testData:
		if (testSize > 0) and (counter < szBuff):
			lhs=ui.pop()
			if lhs != rhs:
				raise Exception("Test failed.  lhs:"+str(lhs)+" != "+str(rhs))
			else:
				print "row passed: " + str(lhs)
		else:
			print "testSize reached."
			break;
		counter+=1
		
	print "     test complete."
#
# Main body that executes the unit tests if run directly.
#
if __name__ == "__main__":
	import sys
	print "test starting"
	print "test #1: default-size tests."
	try:
		unitTest(10)
	except Exception as err:
		print "test failed."
		sys.exit(1)
	print "test #2: variable-size test."
	try:
		for i in range(1000):
			try:
				print "test #2-"+str(i)+": variable-size test"
				unitTest(i)
			except Exception as err:
				print "test ("+str(i)+") failed.  err: " +str(err)
				sys.exit(1)
			print " "
	except Exception as err:
		print "test failed.  Err:"+str(err)
	print "test complete."
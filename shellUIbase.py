#!/usr/bin/env python
#
# shellUIbase.py
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
# 			This is the base class for the terminal-based user-interface called
#			shellUIwindow which provides curses-based window management.
#
# 			The base class only initalizes and destroys the UI windows via curses
# 			and provides certain minimum curses functionality.
#
import curses
import locale
from logger import logger

class shellUIbase:
	#terminal
	__terminal=None
	__curses=None
	__encoding=None
	
	__errors=0
	__errBuff=[]
	
	__log=None
		
	def __crashSafe__(self,m):
		self.__errors+=1
		self.__log.write(''+str(m))
	
	def errorCount(self):
		return self.__errors
	
	def getErrors(self):
		return self.__errBuff
	
	def __init__(self,logFile="shellUIbase"):
		try:
			self.__log=logger(logFile)
			locale.setlocale(locale.LC_ALL,'')
			self.__encoding=locale.getpreferredencoding()
			self.__terminal=curses.initscr()
			self.__curses=curses
			self.__curses.noecho()
			self.__curses.cbreak()
			self.__curses.nonl()
			#self.__curses.curs_set(0)
			self.__terminal.keypad(1)
		except Exception as err:
			self.__crashSafe__('shellUIbase::__init__()  Err:'+str(err))
	
	def __getLogger__(self):
		return self.__log
	
	def __del__(self):
		try:
			if self.__terminal is not None:
				self.__terminal.keypad(0); 
			else:
				self.__log.write('__del__(): self.__terminal not initialized.')
			if self.__curses is not None:
				self.__curses.cbreak(); 
				self.__curses.echo()
				self.__curses.endwin()
				self.__curses.nl()
				self.__curses.curs_set(1)
			else:
				self.__log.write('__del__(): self.__curses not initialized.')
		except Exception as err:
			self.__crashSafe__('__del__()  Err:'+str(err))
			
	def __createWindow__(self,sRow,sCol,szRows,szCols):
		if not type(sRow) is int:
			raise Exception("shellUIbase::createWindow() sRow type mismatch (expect int)")
		if not type(sCol) is int:
			raise Exception("shellUIbase::createWindow() sCol type mismatch (expect int)")
		if not type(szRows) is int:
			raise Exception("shellUIbase::createWindow() szRows type mismatch (expect int)")
		if not type(szCols) is int: 
			raise Exception("shellUIbase::createWindow() szCols type mismatch (expect int)")
		if (szRows < 1):
			raise Exception("shellUIbase::createWindow() szRows out of range (1...n)")
		if (szCols < 1):
			raise Exception("shellUIbase::createWindow() szCols out of range (1...n)")
		if (sRow<0) or (sRow >= szRows):
			raise Exception("shellUIbase::createWindow() sRow out of range (0...szRows)")
		if (sCol<0) or (sCol >= szCols):
			raise Exception("shellUIbase::createWindow() sCol out of range (0...szCols)")
		
		thisWindow=self.__curses.newwin(szRows,szCols,sRow,sCol)
		thisWindow.refresh()
		return thisWindow
	
	def getch(self):
		return self.__terminal.getch()
#
# Unit tests
#
def unit_test():
	ui=shellUIbase()
	if ui.errorCount() > 0:
		print "shellUIbase unit test error count: " + str(ui.errorCount())
		print "shellUIbase unit test errors:"+str(ui.getErrors())
		raise Exception("Unit test had one or more errors")	
	else:
		print "No errors"
#
# Main body (executes unit tests if run directly).
#
if __name__ == "__main__":
	import sys
	try:
		unit_test()
	except Exception as err:
		print "Unit test failed."
		sys.exit(1)
	print "unit test passed."
	sys.exit(0)


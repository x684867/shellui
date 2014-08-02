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
# This class will define a curses window
# of the given dimensions based on the
# functionality provided by the base
# class.
#
# It then provides extended functionality
# for user I/O to write() to and clear()
# the window screen.
#
import curses
from shellUIbase import shellUIbase

class shellUIwindow(shellUIbase):
	__window=None
	__name=""
	__row=0
	__col=0
	__szRows=0
	__szCols=0
	
	__log=None
	
	def clear(self):
		self.__log.write("shellUIwindow::clear() starting...")
		try:
			self.__window.clear()
			self.__window.refresh()
		except Exception as err:
			self.__crashSafe__(
				'shellUIwindow::clear()' + \
				'\nErr:'+str(err))
		finally:
			self.__log.write("shellUIwindow::clear() done")

	def writeBlink(self,r,c,cursor):
		self.__window.addstr(r,c,cursor,curses.A_BLINK)
		self.__window.refresh()
	
	def write(self,m):
		try:

			nChars=abs(self.__szCols-self.__col)-1
			self.__window.addnstr(self.__row,self.__col,str(m),nChars)
			self.__window.refresh()

		except Exception as err:
			self.__crashSafe__("write()[addnstr()] encountered error.\nErr:"+str(err))

	def move(self,row,col):
		try:
		
			#Bounds-check:rows
			if (row >= 0) and (row < self.__szRows):
				self.__row=row
			else:
				if row < 0:
					self.__row=0
					raise Exception("row out of range ("+str(row)+") <0")
				else:
					self.__row=self.szRows-1
					raise Exception("row out of range ("+str(row)+") >="+str(self.__szRows))
			
			#Bounds-check:cols
			if (col >= 0) and (col < self.__szCols):
				self.__col=col
			else:
				if col < 0:
					self.__col=0
					raise Exception("col out of range ("+str(col)+") <0")
				else:
					self.__col=self.__szCols-1
					raise Exception("col out of range ("+str(col)+") >="+str(self.__szCols))
			try:
				self.__window.move(self.__row,self.__col)
			except Exception as err:
				raise Exception("cursor move failed.  Err:"+str(err))
			try:
				self.__window.refresh()
			except Exception as err:
				raise Exception("window refresh failed.  Err:" + str(err))
		
		except Exception as err:
			self.__crashSafe__("shellUIwindow::move(): " + str(err))
			curses.beep()
		return (row,col)
	
	def __init__(self,n="undefined",sRow=0,sCol=0,szRows=25,szCols=80):
		#initialize the base class.
		try:
			try:
				shellUIbase.__init__(self,"shellUIwindow_"+n)
			except Exception as err:
				raise Exception('Error calling baseclass constructor. Err:'+str(err))
			try:
				self.__log=shellUIbase.__getLogger__(self)	
			except Exception as err:
				raise Exception('Error getting baseclass logger.  Err:'+str(err))
			#Set the internal properties.
			self.__row=sRow
			self.__col=sCol
			self.__szRows=szRows
			self.__szCols=szCols
			self.__name=n
			try:
				self.__log.write('creating window ['+str(n)+']')
				self.__window=self.__createWindow__(sRow,sCol,szRows,szCols)
				(self.__sRow,self.__sCol)=self.__window.getyx()
			except Exception as err:
				raise Exception('shellUIwindow::__init__(): Err:'+str(err))
		except Exception as err:
			self.__crashSafe__("shellUIwindow::__init__(): " + str(err))
		self.__log.write("shellUIwindow::__init__(): Done")
		
		
	def __del__(self):
		self.__log.write('shellUIwindow::__del__()['+str(self.__name)+'] starting')
		if self.__window is not None:
			try:
				del self.__window
			except Exception as err:
				self.__crashSafe__('__del__()\nErr:'+str(err))
		else:
			pass
		try:
			shellUIbase.__del__(self)
		except Exception as err:
			self.__crashSafe__(
				'shellUIwindow::__init__() Error calling baseclass destructor.' + \
				'\nERROR:'+str(err)+'\n' \
			)
		self.__log.write('shellUIwindow::__del__()['+str(self.__name)+'] done')
		self.__log=None

# Unit tests
#
def unit_test():
	import time
	f=open('unitTest.log','a')
	f.write('unit_test(): starting unit test.\n')
	try:
		f.write('>>test instantiation of shellUIwindow\n')
		try:
			ui=shellUIwindow("unit_test",0,0,25,80)
		except Exception as err:
			raise Exception("shellUIwindow failed instantiation.\nErr:"+str(err))
		f.write('>>test clear()\n')
		try:
			ui.clear()
		except Exception as err:
			raise Exception("clear() failed.\nErr:"+str(err))
		f.write(">>test write()\n")
		try:
			ui.write("WRITE TEST!")
			time.sleep(1)
		except Exception as err:
			raise Exception("write() failed.\nErr:"+str(err))
		f.write(">>test move(1,1)\n")
		try:
			ui.move(1,1)
		except Exception as err:
			raise Exception("move() failed.\nErr:"+str(err))
		f.write(">>test errorCount()\n")
		if ui.errorCount() > 0:
			f.write("shellUIwindow unit test error count: " + str(ui.errorCount())+'\n')
			f.write("shellUIwindow unit test errors:"+str(ui.getErrors())+'\n')
			raise Exception("Unit test had one or more errors\n")	
		else:
			f.write("Error-check test passes.\n")
		f.write(">>destruction test.\n")
		try:
			del ui
		except Exception as err:
			raise Exception("Failed to destroy ui\n")
		f.write(">>Destruction test passes\n")
	except Exception as err:
		f.write("unit_test(): " + str(err)+"\n")
		raise err
	f.close()
#
# Main body (executes unit tests if run directly).
#
if __name__ == "__main__":
	import sys
	try:
		unit_test()
	except Exception as err:
		print "Unit test failed. \nErr:"+str(err)
		sys.exit(1)
	print "unit test passed."
	sys.exit(0)


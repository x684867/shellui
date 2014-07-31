#!/usr/bin/env python
#
# shellUIinput.py
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
# This script creates a class to add interactive functionality
# to the shellUI.  This class will instantiate a history class,
# a status window and a main window and orchestrate the user
# interactions with the two windows while maintaining a user
# history log for 'up-arrow' history retrieval.
#
import curses
from logger import logger
from shellUIwindow import shellUIwindow
from shellUIhistory import shellUIhistory

class shellUIinput:
	__history=None
	__log=None
	
	__window=None
	__status=None
	__statusLine=''
	
	__wRow=0
	__wCol=0
	__buffer=''

	def __init__(self):
		self.__log=logger('shellUIinput')
		self.__log.write('shellUIinput::__init__() start.')
		self.__history=shellUIhistory(10)
		self.__status=shellUIwindow(n="status",sRow=0,sCol=0,szRows=1,szCols=80)
		self.__window=shellUIwindow(n="window",sRow=self.__wRow,sCol=self.__wCol,szRows=20,szCols=80)
		(self.__wRow,self.wCol)=self.__window.move(0,0)
		self.__statusLine="Starting..."
		self.repaint()
		self.__log.write('shellUIinput::__init__() done.')

	def __del__(self):
		self.__log=None
		self.__history=None
		self.__window=None
		self.__status=None

	def __updateStatus__(self,m):
		try:
			if m!="":
				self.__statusLine=m
			self.__status.move(0,0)
			self.__status.write( \
					"Row:"+str(self.__wRow) + "," + \
					"Col:"+str(self.__wCol) + "," + \
					"Status:"+str(self.__statusLine)[0:(80-self.__wCol-len(self.__statusLine))] \
			)
			self.__window.move(self.__wRow,self.__wCol)
		except Exception as err:
			self.__log.write("shellUIinput::__updateStatus__(): " + str(err))
		return m

	def repaint(self,prompt="#"):
		fillString=" " * (80-len(self.__buffer)-2)
		lineString=prompt+self.__buffer+fillString
		(self.__wRow,self.wCol)=self.__window.move(self.__wRow,0)
		self.__window.write(lineString)
		(self.__wRow,self.__wCol)=self.__window.move(self.__wRow,len(self.__buffer)+1)
		self.__updateStatus__("")
				
	def __actionBackspace__(self):
		self.__log.write("shellUIinput::__actionBackspace__():")
		try:
			self.__buffer=self.__buffer[0:len(self.__buffer)-1]
			self.repaint()
		except Exception as err:
			raise Exception('on Backspace: '+str(err))	

	def __actionKeyRight__(self):
		self.__log.write("shellUIinput::getInput(): KeyPress (RIGHT")
		curses.beep()

	def __actionKeyDown__(self):
		self.__log.write("shellUIinput::getInput(): KeyPress (DOWN)")		
		try:
			self.__log.write('on KeyDown: not implemented')
			pass
		except Exception as err:
			raise Exception('on KeyDown: ' + str(err))	

	def __actionKeyUp__(self):
		self.__log.write("shellUIinput::getInput(): KeyPress (UP)")					
		try:
			lastLine=self.__history.pop().strip()
			if lastLine=="":
				curses.beep()
			else:
				self.__buffer=lastLine
				self.repaint(self.__buffer)
				self.__log.write("shellUIinput::actionKeyUp() history:"+str(lastLine))
		except Exception as err:
			curses.beep()
	
	def __actionKeyEnter__(self):
		self.__log.write("shellUIinput::getInput(): KeyPress (ENTER)")
		try:
			self.__history.push(self.__buffer.strip())
			self.__log.write("shellUIinput::getInput()[saveHistory size]:"+str(self.__history.size()))
			(self.__wRow,self.__wCol)=self.__window.move(self.__wRow+1,0)
			self.__buffer=''
			self.repaint("")
			return (self.__wRow,self.__buffer)
		except Exception as err:
			raise Exception('on KeyEnter: ' + str(err))

	def __actionKeyCapture__(self,ascii):
		try:
			try:
				self.__buffer+=chr(ascii)
			except Exception as err:
				raise Exception('appending self.__buffer '+str(err))
			self.repaint()
		except Exception as err:
			raise Exception('on anyKey: ' + str(err))

	
	def getInput(self,startRow):
		(self.__wRow,self.__wCol)=self.__window.move(startRow,0)
		self.__log.write('shellUIinput::getInput() start')
		self.__buffer=''
		try:
			self.repaint(self.__buffer)
			while True:
				self.__log.write('(wRow:'+str(self.__wRow)+',wCol:'+str(self.__wCol)+'):'+self.__buffer)
				self.__updateStatus__("Waiting...")
				try:
					ascii=self.__window.getch()
				except Exception as err:
					raise Exception('failed to get char from terminal.  Err:'+str(err))
				self.__updateStatus__("Typing...")
				try:
					if (ascii==curses.KEY_LEFT) or (ascii==127):
						self.__actionBackspace__()
					elif ascii==curses.KEY_RIGHT:
						self.__actionKeyRight__()
					elif ascii==curses.KEY_DOWN:
						self.__actionKeyDown__()
					elif ascii==curses.KEY_UP:
						self.__actionKeyUp__()
					elif ascii==13:
						self.__actionKeyEnter__()
					else:
						self.__actionKeyCapture__(ascii)
				except Exception as err:
					raise Exception('in eval char.  Err:'+str(err))

			self.__log.write('shellUIbase::getInput() stop')	
		except Exception as err:
			self.__log.write("shellUIbase::getInput() Err:"+str(err))
		self.__log.write('shellUIbase::getInput() done.')

#
# Unit Testing
#
if __name__ == "__main__":
	f=open('shellUIinput.log','a')
	f.write("Unit Test starting\n")
	ui=shellUIinput()
	f.write("ui instantiated.\n")
	f.write("ui.getInput() called.\n")
	row=1
	while True:
		(row,dataString)=ui.getInput(row)
		if dataString=="q":
			break
	f.write("ui.getInput() returned.\n")
	f.write("Test complete\n")
	f.close()
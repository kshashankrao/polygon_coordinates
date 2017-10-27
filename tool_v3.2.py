#install pyqt4, pexpect, opencv
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui, uic #imp
import cv2
import os
#import json
import pexpect 

qtCreatorFile = "tool_v3_GUI.ui" # Enter file here.
a = []

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
	        Ui_MainWindow.__init__(self)
	        self.setupUi(self)
		#self.load.clicked.connect(self.get_input)
		self.centerOnScreen()
		self.browse.clicked.connect(self.get_browse)
		self.load.clicked.connect(self.get_load)
		self.upload.clicked.connect(self.file_upload)
		
   	def centerOnScreen (self):
        
		resolution = QtGui.QDesktopWidget().screenGeometry()
		self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
		          (resolution.height() / 2) - (self.frameSize().height() / 2)) 

	def file_upload(self):
		
		source = 'Output.csv'
		username = str(self.usrname.text())
		password = str(self.pwd.text())
		ipaddr =str( self.ipaddress.text())
		tdir = str(self.tardir.text())	
		child = pexpect.spawn("scp " +source+' '+username+'@'+ipaddr+':'+tdir)	
		child.logfile = open("mylog.txt", "w")		
		
		 
		try:
			e = child.expect(username+'@'+ipaddr+"'s password:")
			child.sendline(password)
			child.expect(pexpect.EOF, timeout=5) 
			
		except: pass
		
		
		
		w = QWidget()
		if "Output.csv" and "100%" in open("mylog.txt").read():
			#print 'success'
			result = QMessageBox.warning(w, "Message", "File successfully transferred")	
		elif "Are you sure you want to continue connecting (yes/no)?"  in open("mylog.txt").read():
			print "Network Error or Check IP address"
			result = QMessageBox.warning(w, "Message", "Error! Check the IP address and try again")
		elif "Permission denied" in  open("mylog.txt").read():
			print "Username or Password or Target directory is incorrect"
			result = QMessageBox.warning(w, "Message", "Error! Username or Password or Target directory is incorrect")
		else:
			print "Network error or check the parameters again ! "
			result = QMessageBox.warning(w, "Message", " Error! Check for Network connection or the parameters and try again !")
		
		
	
	def get_browse(self):
		filePath = QtGui.QFileDialog.getOpenFileName(self, 'Single File',"~/Desktop/",'*.jpg')
		print filePath
		self.textbox.setText(filePath)        	
		
        def get_load(self):
		
		filePath = self.textbox.text()
			
		def click_and_crop(event, x, y, flags, param):
			
			global a,length
			if event == cv2.EVENT_LBUTTONDBLCLK and len(a) < 5:
				cv2.circle(image,(x,y),4,(0,0,255),-1,cv2.LINE_AA)
				print (x,y)
				
				a.append([x,y])	
				
						
				get_line(a)
			
									
			else:pass
					
		def get_line(a):			
			length = len(a) - 1
			if length > 0:
				cv2.line(image,(a[length - 1][0],a[length - 1 ][1]),((a[length][0],a[length][1])),(0,0,255),2,cv2.LINE_AA)


		global a
		length= 0		
		path = str(filePath)
		print path	
		image = cv2.imread(path)
		
		#resolution = QtGui.QDesktopWidget().screenGeometry()
		#cv2.namedWindow('image')
		#cv2.moveWindow('image',(resolution.width() / 2) - (self.frameSize().width() / 2),(resolution.height() / 2) - (self.frameSize().height() / 2))
		cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
		
		
		cv2.imshow('image',image)
		clone = image.copy()
		cv2.namedWindow("image")
		cv2.setMouseCallback("image", click_and_crop)


		while True:
			
			cv2.imshow("image", image)
			key = cv2.waitKey(1) & 0xFF
			# if the 'c' key is pressed, save and exit from the loop
			if key == ord("s"):
				
				w = QWidget()
				result = QMessageBox.warning(w, "Message", "Coordinates Saved to Output.csv")
				f = open("Output.csv", "a")
				f.write("%d,%d \n" % (int(a[0][0]) ,  int(a[0][1])) )
				f.write("%d,%d \n" % (int(a[1][0]) ,  int(a[1][1])) )
				f.write("%d,%d \n" % (int(a[3][0]) ,  int(a[3][1])) )
				f.write("%d,%d \n" % (int(a[2][0]) ,  int(a[2][1])) )
				f.close()
				a = []
				
				break

			# if the 'x' key is pressed,exit from the loop
			elif key == ord("x"):
				a = []	
				break
		 
			# if the 'r' key is pressed, reset the cropping region
			if key == ord("r"):
				a = []
				image = clone.copy()

		cv2.destroyAllWindows()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
sys.exit(app.exec_())

#install pyqt4, pexpect, opencv
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui, uic #imp
import cv2
import os
import sys, paramiko

curr_dir = os.getcwd()

qtCreatorFile = curr_dir + "/GUI.ui" # Enter file here.
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

		source = curr_dir + '/Output.csv'
		username = str(self.usrname.text())
		password = str(self.pwd.text())
		ipaddr =str( self.ipaddress.text())
		tdir = str(self.tardir.text())

		port = 22
		w = QWidget()
		#hostname = sys.argv[1]
		#password = sys.argv[2]

		#t = paramiko.Transport(('192.168.1.151', port))

		try:
			t = paramiko.Transport((ipaddr, port))
			t.connect(username=username, password=password)
			sftp = paramiko.SFTPClient.from_transport(t)
			sftp.put(source, tdir)
			t.close()
			result = QMessageBox.warning(w, "Message", "File successfully transferred")
		except:
			#print('Error')
			result = QMessageBox.warning(w, "Message", "Error! \nCheck Parameter Again")






	def get_browse(self):
		filePath = QtGui.QFileDialog.getOpenFileName(self, 'Single File',"~/Desktop/",'*.jpg')
		#print filePath
		self.textbox.setText(filePath)

	def get_load(self):

		filePath = self.textbox.text()

		def click_and_crop(event, x, y, flags, param):

			global a,length
			if event == cv2.EVENT_LBUTTONDBLCLK and len(a) < 5:
				cv2.circle(image,(x,y),4,(0,0,255),-1)
				print (x,y)

				a.append([x,y])


				get_line(a)


			else:pass

		def get_line(a):
			length = len(a) - 1
			if length > 0:
				cv2.line(image,(a[length - 1][0],a[length - 1 ][1]),((a[length][0],a[length][1])),(0,0,255),2)


		global a
		length= 0
		path = str(filePath)
		#print path
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
				#result = QMessageBox.warning(w, "Message", "Coordinates Saved to Output.csv")
				f = open(curr_dir + "/Output.csv", "a")
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

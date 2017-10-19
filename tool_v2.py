import sys
from PyQt4 import QtCore, QtGui, uic
import cv2

qtCreatorFile = "untitled.ui" # Enter file here.
a = []

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
	        Ui_MainWindow.__init__(self)
	        self.setupUi(self)
		self.load.clicked.connect(self.get_input)
		self.centerOnScreen()

   	def centerOnScreen (self):
        
		resolution = QtGui.QDesktopWidget().screenGeometry()
		self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
		          (resolution.height() / 2) - (self.frameSize().height() / 2)) 
	
	
	def get_input(self):
				
		
		def click_and_crop(event, x, y, flags, param):
			
			global a,length
			if event == cv2.EVENT_LBUTTONDBLCLK:
				cv2.circle(image,(x,y),4,(255,0,0),-1)
				print (x,y)
				a.append([x,y])	
				print ('hey',a[0][0])
				
				get_line(a)					
				
						
				
						
		def get_line(a):			
			length = len(a) - 1
			if length > 0:
				cv2.line(image,(a[length - 1][0],a[length - 1 ][1]),((a[length][0],a[length][1])),(255,0,0),1)
		



		global a
		length= 0		
		path = str(self.input_path.toPlainText())
		print path
		image = cv2.imread(path)
		cv2.imshow('image',image)
		clone = image.copy()
		cv2.namedWindow("image")
		cv2.setMouseCallback("image", click_and_crop)


		while True:
			
			cv2.imshow("image", image)
			key = cv2.waitKey(1) & 0xFF
			# if the 'c' key is pressed, save and exit from the loop
			if key == ord("c"):
				print (a[0])
				a = []
				text_file = open("Output.txt", "w")
				text_file.write(a[0])
				text_file.close()
				break

			# if the 'c' key is pressed,exit from the loop
			elif key == ord("x"):	
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

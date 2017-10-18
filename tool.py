# import the necessary packages
import argparse
import cv2

a = [] 

 
def click_and_crop(event, x, y, flags, param):
	global a,b	
	if event == cv2.EVENT_LBUTTONDBLCLK:
		cv2.circle(image,(x,y),4,(255,0,0),-1)
		print (x,y)
		a.append([x,y])
		#b = b.append([y])
		
		
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
 
# if there are two reference points, then crop the region of interest
# from teh image and display it
'''
	if len(refPt) == 2:
		roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
		cv2.imshow("ROI", roi)
		cv2.waitKey(0)
''' 
print (a)

# close all open windows
cv2.destroyAllWindows()

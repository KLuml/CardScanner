#Kevin Lumley
#AI PROJECT
#COMPUTER VISION


# Building a card Scanner App using Python, OpenCV, and Computer VisionPython
#finds the 4 corners and applies the top-down view for skewed images
from pyimagesearch.transform import four_point_transform 
import argparse #cmd line arguments
import cv2 #Computer vision library. used majority of time.
import imutils #image resizing
import pytesseract #OCR (Optical Character Recognition)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
'''
	Name: edged
	Parameters: None
	Function: Image from CMD arg is copied, resized, converted 
  to greyscale and edge detection is run on it. displays original image
  and edged results
  
  Return: Original image, Edged image, copy of original image, and ratio
'''
def edged():
   # load the image and compute the ratio of the old height
  # to the new height, clone it, and resize it
  image = cv2.imread(args["image"])
  ratio = image.shape[0] / 500.0
  orig = image.copy()
  image = imutils.resize(image, height = 500)

  # convert the image to grayscale, blur it, and find edges
  # in the image
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray,(5,5), 0)
  edged = cv2.Canny(gray, 75, 200)

  # show the original image and the edge detected image
  cv2.imshow("Image", image)
  cv2.imshow("Edged", edged)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  # cv2.imwrite('edged.png',edged)
  return image,orig,edged,ratio

  
'''
	Name: drawContours
	Parameters: img - copy of original image 
		    edgedImg - used to draw contours
	Function: calculate the contours of the edged image and apply it to
  a copy of the original image
  Return: Contours - array of contour shape.
'''  
def drawContours(img,edgedImg):
  # find the contours in the edged image, keeping only the
  # largest, and initialize the screen contour
  screenContours = cv2.findContours(edgedImg.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  screenContours = imutils.grab_contours(screenContours)
  screenContours = sorted(screenContours, key = cv2.contourArea, reverse = True)[:1] #store largest contour
   
  # loop over the contours
  for c in screenContours:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # approx = cv2.approxPolyDP(c, 0.025 * peri, True)
    # if  approximated contour has four points, then we
    #  assume found the card
    if len(approx) == 4:
      contours = approx
      cv2.drawContours(img, [contours], -1, (0, 255, 0), 2)
  
  # show the contour (outline) of the card
  #The reason to use the copy made in edging is because
  #contour functions are considered destructive AKA permanent
  cv2.drawContours(img, [contours], -1, (0, 255, 0), 2)
  cv2.imshow("Outline", img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  # cv2.imwrite('contours.png',img)
  return contours

  
'''
	Name: extractCard
	Parameters: img - copy of original image 
		          contours - used for card position in image to crop
              ratio - Size of card img
	Function: use the contours from draw contours to crop the 
  assumed card. Use the four_point_transform to give a top-down
  view of the card if it's not positioned right.
  Return: card - cropped image of card from original image
'''    
def extractCard(Image, contours,ratio):
  # top-down view from four_point_transform
  card = four_point_transform(Image, contours.reshape(4, 2) * ratio)
  # show the contoured card with a top-down view
  cv2.imshow("extracted Card", imutils.resize(card, height = 650))

  # cv2.imwrite('extracted.png',card)
  return card

# images loaded with opencv are numpy arrays in HxWxC format
# This helps us crop the images with an easy format
  #ROI:Region of Interest
'''
	Name: cropName
	Parameters: image - copy of original image 
		    
	Function: resize image and crop it at approximate average location
  of name.
  Return: cropName - cropped image of card's name from card image
'''    
def cropName(image):
  image = cv2.resize(image,(500,700))
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  #Img[ymin:ymax,xmin:xmax,:]
  cropName = gray[15:100,15:380]
  cv2.imshow('Name', cropName)
  return cropName

'''
	Name: cropSymbol
	Parameters: image - copy of original image 
		    
	Function: resize image and crop it at approximate average location
  of name.
  Return: cropName - cropped image of card's name from card image
'''    
def cropSymbol(image):
  image = cv2.resize(image,(500,700))
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
  #Img[ymin:ymax,xmin:xmax,:]  
  cropSymbol = gray[390:435,420:480]
  cv2.imshow('Symbol', cropSymbol)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
def main():
  image,ogImg, edgedImg,ratio = edged()
  screenContours = drawContours(image,edgedImg)
  card = extractCard(ogImg,screenContours, ratio)
  cardName = cropName(card)
  cardSymbol = cropSymbol(card)
  text = pytesseract.image_to_string(cardName)
  print("\n\nCard Name: " + text)
  

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
  help = "Path to the image to be scanned")
args = vars(ap.parse_args())
main()

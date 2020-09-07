Kevin Lumley


*This program is meant to scan an image for a Magic The Gathering Card and return the name and set. Then it was to be sent to an online database to upload a stores inventory automatically.*

*Can find the card and return the card's name with a certain. Heavily dependent on image quality.*
*TODO: Add symbol Recognition*


Prequisites to run program-

    the document-scanner folder has an unzipped document-scanner folder. Put this in python lib folder. 
    

    Modules you may need to pip install-

        opencv
        imutils
        pillow
        pytesseract
        scikit-image

    Downloads-
     
        https://github.com/tesseract-ocr/
        Where ever the download is located on your machine
        copy and paste that path to the tesseract.exe file at line 8
          EX-  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


    How to run-
      
      STEP1
        py scan.py --image (Image Name)
          py scan.py --image card.jpg
          py scan.py --image card0.jpg
          py scan.py --image card10.jpg
          
        
        
        Preloaded images in folder include
          card.jpg
          card#.jpg(0-4) (10-12) 
              First5 images work pretty well finding the cards and extracting the text name.
              10 and above work with less accuracy.
              
      STEP2
        While running, images will load to the screen. Pressing arrow keys should
        advance you through displays of the following.
        
        1- ORIGINAL IMAGE && EDGED VERSION
        2- ORIGINAL IMAGE WITH CONTOURS AROUND CARD
        3- CARD CROPPED ORIGINAL IMAGE AND DISPLAYED 
        4- NAME CROPPED FROM 3
        5- SYMBOL CROPPED FROM 3
        6- Terminal DISPLAYS CARD NAME FROM 4 ***  


Design -
  
    find/crop card
      use OpenCV, imutils, and a special four point transform function to
      import card, convert to greyscale, shape, edge, find corners, draw contours
      around corners, extract(crop) the card image from the original image. Convert it to
      top-down view(can lose a lot of quality from this) and use estimated coordinates to
      crop the card name and the card symbol
    
    crop name/symbol from card image AKA ROI:Region of Interest
      OpenCV images are stored as numpy arrays in HxWxC format. I simply had to find an image size
      that returned a decent picture and use the x/y coordinates to crop the name/symbol
      Img[ymin:ymax,xmin:xmax,:] <-- cropping method
    
    Print name of card
      Run Pytesseract on cropped card name for text parsing from image.

    Possible methods for Symbol Recognition
      
      Haars Cascade-
        I had originally wanted to use this method to train for symbol matching.
        having a library of negatives and positives approx 100's for each. positives
        being images with the symbol and negatives without the symbol. I decided against
        using this method, because it did seem like overkill. First storing 100's of images
        (the suggested number was about a thousand) of negatives and positives for over 100 symbols
        was a bit much. We can I find this dataset!?!?!?
        
      
      Template matching for the symbol? vs
      Zernike moments?
        using an array of template symbol images that are
        completely whited out, take the current card symbol and 
        overlap it with template images. The image with the least 
        amount of empty space inside symbol, and least amount of 
        full space outside template symbol will return a suggested possible
        correct symbol for card.
        
      Brute force and various methods-
        I tried to run a few different algorithms before I found the template matching/zernike moments
          these include fast corner, harris corner, homography brute force.
          these were looking for individual pixels or points that matched in another image. Which led me to
          the question "how can I convert a whole symbol into a feature/point to be compared???" which led me to Zernike Moments

      
      
Challenges-
    OCR-
      1-Card names can be written in a format alien to the tesseract OCR returning
      bad results or no results at all.
      
      2-Because the image never returns consistent contours(ALWAYS around entire card)
      estimates were made and I have to leave a little space so the name is ALWAYS found.
      This leads to the creature art being in the pytesseract to_string function sometimes and can return 
      characters or symbols. Even the card art and rounded curve left of the name can be found
      as a left paren (.
    
      3-Importing pytesseract and then downloading tesseract-ocr and finding that line of code 8.
      Spent a great many of hours finding that line to get it to work. I started with the pytesseract.
      Then moved to OpenCV.
    
    Cropping-  
      1-I can never get precision when the card is cropped from the image.
      Sometimes it does the whole card's border other times the art border and sometimes it's a skewed contour.
      This doesn't give me an exact position everytime. 
      The symbol crop is estimates with extra space around the image.
      My understanding if that it places the images ontop and sees how much*white space*
      is left over. After iterating over every symbol the one with the least white space
      would be the suggested symbol. Every example I saw had precise crops that made each image
      look identical. Where as my symbol would sometimes be exactly middle or right/left side of image
      
      2-contouring inconsistencies has negative impacts on both OCR and symbol matching.
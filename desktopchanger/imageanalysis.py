"""
    The ImageAnalysis class is used to arbitrary information about an
    image.
    Including:
        * hues
        * dark/light balance
"""

import logging
import numpy as np
import cv2

##### Functions
#####

##### Classes
#####
class ImageAnalysis:
    """
        Image Analysis class collates lower level image analysis based
        upon a higher level business requirements. I.E.
            * reading the important hsv values
    """

    def __init__(self, path):
        """
            Reads in the image path and set up an image.
        """
        logging.debug("Image Analysis: Analyse path: %s", path)
        self.image = Image(path)

    def analyse_hsv(self):
        """
            Convert the RGB image to HSV and return the red, green, blue/
            colours and dark/light balance of the image.
        """
        self.image.convert_hsv()
        blue, green, red = self.image.primary_hues()
        light, dark = self.image.value_gradient()
        logging.debug("HSV values: \n red: {0:.5f}, \
            blue: {1:.5f}, green: {2:.5f}  \
            \n light: {3:.5f}, dark: {4:.5f} \
            ".format(blue, green, red, light, dark))
        return blue, green, red, light, dark

class Image:
    """
        Represents a single image.
    """
    def __init__(self, path):
        """
            Read in the file path and load the file as an opencv numpy.
        """
        try:
            self.img = cv2.imread(path)
            self.hsv = []
            if self.img is None:
                raise FileNotFoundError
        except FileNotFoundError:
            print("Could not load image. \n")
            raise

    def convert_hsv(self):
        """
            Converts the rgb self.img into the HSV scheme
        """
        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

    def primary_hues(self):
        """
            Returns the fraction of primary colours represented in the image.
            Note this number won't necessarily add to 1.
            Takes in the hue channel information and returns
            red, green, blue fracions
        """
        # lower and upper bound blue
        lower_blue = np.array([104, 80, 80])
        upper_blue = np.array([134, 255, 255])
        blue_hsv = cv2.inRange(self.hsv, lower_blue, upper_blue)

        # lower and upper bound green
        lower_green = np.array([44, 80, 80])
        upper_green = np.array([74, 255, 255])
        green_hsv = cv2.inRange(self.hsv, lower_green, upper_green)

        # lower and upper bound red on the low value hsv half-circle
        lower_red_low = np.array([0, 80, 80])
        upper_red_low = np.array([14, 255, 255])
        # lower and upper bound red on the high value hsv half-circle
        lower_red_high = np.array([164, 80, 80])
        upper_red_high = np.array([179, 255, 255])
        red_hsv_low = cv2.inRange(self.hsv, lower_red_low, upper_red_low)
        red_hsv_high = cv2.inRange(self.hsv, lower_red_high, upper_red_high)
        red_hsv = cv2.bitwise_or(red_hsv_low, red_hsv_high)

        blue = cv2.countNonZero(blue_hsv)
        green = cv2.countNonZero(green_hsv)
        red = cv2.countNonZero(red_hsv)
        height, width, _ = self.img.shape
        size = height*width
        return blue/size, green/size, red/size

    def value_gradient(self):
        """
            Measuring the lightness and darkness of an image based upon
            the value channel from hsv. Returning the lightness and darkness
            of the image based upon the number of pixels in the top and bottom
            third of the value gradient.
            Returns light, dark fractional values
        """

        # lower and upper bound brightnesss
        lower_blue = np.array([0, 0, 170])
        upper_blue = np.array([255, 255, 255])
        light_hsv = cv2.inRange(self.hsv, lower_blue, upper_blue)

        # lower and upper bound darkness
        lower_blue = np.array([0, 0, 0])
        upper_blue = np.array([255, 255, 80])
        dark_hsv = cv2.inRange(self.hsv, lower_blue, upper_blue)

        light = cv2.countNonZero(light_hsv)
        dark = cv2.countNonZero(dark_hsv)
        height, width, _ = self.img.shape
        size = height*width
        return light/size, dark/size

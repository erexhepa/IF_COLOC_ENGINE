global __name__
__name__= 'define_im_descriptors'

# import opencv

import numpy as np
import cv2

class ColourHistogram:

    # Class constructor definings number of bins to be extracted during the histogram construction and which cannels
    # to be used to extract the bins
    def __init__(self, bins, channelIDs):
        self.bins = bins
        self.channelIds = channelIDs


    # histogram in the RGB color space
    def describeRGB(self, image):
        # compute a multidimensional histogram in the RGB colorspace using information from informaiton defined
        # channels which index is defined by the variable channelIds. Then normalize the histogram so that images
        # with the same content, but either scaled larger or smaller will have (roughly) the same histogram

        if(self.channelIds.shape[0]==1):
            hist = cv2.calcHist([image], self.channelIds,
               None, self.bins, [0, 256])
            hist = cv2.normalize(hist)

        elif(self.channelIds.shape[0]==2):
            hist = cv2.calcHist([image], self.channelIds,
                None, self.bins, [0, 256, 0, 256])
            hist = cv2.normalize(hist)

        elif(self.channelIds.shape[0]==3):
            hist = cv2.calcHist([image], self.channelIds,
                None, self.bins, [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist)
        else:
            print "WARNING: number of channels must be greate or equal to 1"
            hist = np.zeros([8,1])

        # return out 3D histogram as a flattened array
        return hist.flatten()


    # extract histogram in the L*a*b* color space
    def describeLAB(self, image):
            lab_colRep      = cv2.cvtColor( image, cv2.COLOR_RGB2HSV_FULL)
            hist = cv2.calcHist([lab_colRep], [1, 2],
                None, self.bins, [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist)


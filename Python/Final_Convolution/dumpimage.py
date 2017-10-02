#
# Print out a NumPy 1D array as an image with specified rows and columns
#
# Simon D. Levy        CSCI 315         8 April 2016
#

import sys
import numpy as np

def dumpimage(image, rows, cols, binary=True):
    print(' ' + '-'*cols)
    for j in range(rows):
        sys.stdout.write('|')
        for k in range(cols):
            value = image[j*cols+k]
            s = ('*' if value else ' ') if binary else '%0.1f ' % value 
            sys.stdout.write(s)
        print('|')
    print(' ' + '-'*cols)

if __name__ == '__main__':
    '''
    random test
    '''

    W = 30
    H = 20

    dumpimage(np.random.rand(W*H) > 0.5, H, W)

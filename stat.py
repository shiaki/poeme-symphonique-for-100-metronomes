
import os, sys, glob, json
from collections import OrderedDict
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

if __name__ == '__main__':

    fp = fits.open('TNS-MasterCatalog-2019.fits')
    cat = fp[1].data


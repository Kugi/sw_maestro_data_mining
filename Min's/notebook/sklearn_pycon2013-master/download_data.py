"""
Run this script to make sure data is cached in the appropriate
place on your computer.

The data are only a few megabytes, but conference wireless is
often not very reliable...
"""
import os
import sys
from sklearn import datasets

#------------------------------------------------------------
# Faces data: this will be stored in the scikit_learn_data
#             sub-directory of your home folder
faces = datasets.fetch_olivetti_faces()
print "Successfully fetched olivetti faces data"

#------------------------------------------------------------
# SDSS galaxy data: this will be stored in notebooks/datasets/data
sys.path.append(os.path.abspath('notebooks'))
from datasets import fetch_sdss_galaxy_mags
colors = fetch_sdss_galaxy_mags()
print "Successfully fetched SDSS galaxy data"


#------------------------------------------------------------
# SDSS filters & vega spectrum: stored in notebooks/figures/downloads
from figures.sdss_filters import fetch_filter, fetch_vega_spectrum
spectrum = fetch_vega_spectrum()
print "Successfully fetched vega spectrum"

filters = [fetch_filter(f) for f in 'ugriz']
print "Successfully fetched SDSS filters"

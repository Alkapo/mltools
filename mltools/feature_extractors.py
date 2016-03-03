"""
What: Contains various feature extraction functions.
Authors: Carsten Tusk, Kostas Stamatiou, Nathan Longbotham
Contact: kostas.stamatiou@digitalglobe.com
"""

from __future__ import division
import numpy as np


def spectral_angles(data, members):
    """Pass in a numpy array of the data and a numpy array of the spectral
       members to test against.
    
       Args: 
           data (numpy array): Array of shape (n,x,y) where n is band number.
           members (numpy array): Array of shape (m,n) where m is member number
                                  and n is the number of bands.

       Returns: Spectral angle vector (numpy array)
                                      
    """

    # if members is one-dimensional, convert to horizontal vector 
    if len(members.shape) ==1:
        members.shape = (1, len(members))

    # Basic test that the data looks ok before we get going.
    assert members.shape[1] == data.shape[0], 'Dimension conflict!'

    # Calculate sum of square for both data and members
    dnorm = np.linalg.norm(data,ord=2,axis=0)
    mnorm = np.linalg.norm(members,ord=2,axis=1)

    # Run angle calculations
    a = np.zeros((members.shape[0], data.shape[1], data.shape[2]))
    for m in xrange(len(mnorm)):
        num = np.sum(data*members[m,:][:,np.newaxis,np.newaxis],axis=0)
        den = dnorm*mnorm[m]
        with np.errstate(divide='ignore', invalid='ignore'):
            a[m,:,:] = num/den  #Float both from __future__ and dnorm/mnorm
            a[m,:,:] = np.arccos(np.clip(a[m,:,:],-1,1))
            a[m,:,:][den == 0] = 0

    return a


def vanilla_features(data):
    """The simplest feature extractor.

       Args:
           data (numpy array): Pixel data vector.

       Yields:
           A vector with the mean, std and variance of data.
    """
    
    yield [ np.mean(data), np.std(data), np.var(data) ]
    

def pool_features(data, raster_file):
    """Feature extractor for swimming pool detection.

       Args:
           data (numpy array): Pixel data vector.
           raster_file (str): Image filename.

       Yields:
           Feature vector (numpy array).
    """

    # get signatures from raster_file; this needs to be acomped
    # this is hard-coded for the time being
    pool_sig = np.array([1179, 2295, 2179, 759, 628, 186, 270, 110])
    
    pool_data = spectral_angles(data, pool_sig)
    band26_ratio = (data[1,:,:] - data[5,:,:])/(data[1,:,:] + data[5,:,:])
    band36_ratio = (data[2,:,:] - data[5,:,:])/(data[2,:,:] + data[5,:,:])
    
    return [np.max(band26_ratio), np.max(band36_ratio), np.min(pool_data)]
    
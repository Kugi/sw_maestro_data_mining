__author__ = 'kugi'

import pickle

import pandas
from sklearn.datasets import load_svmlight_file


class Loadmanager(object):


    @staticmethod
    def loadDat(filename):
        '''
        load '.dat' files
        ret: tuple, it can be translated into (csr_matrix, csr_matrix) shape.
        '''
        temp_tuple = load_svmlight_file(filename)
        return temp_tuple


    @staticmethod
    def loadDf(filename):
        '''
        load '.df' files
        ret: DataFrame
        '''
        temp_pickle = pandas.load(filename)
        print temp_pickle
        return temp_pickle


    @staticmethod
    def loadPkl(filename):
        '''
        load '.pkl' files
        ret: dict
        '''
        temp_pickle = pickle.load(file(filename))
        print temp_pickle
        return temp_pickle

__author__ = 'jeongmingi'

import pickle

import pandas
from sklearn.externals import joblib

from pandas import DataFrame


class Savemanager(object):


    @staticmethod
    def saveModel(data, filename):
        '''
        save Model files(studied files)
        If Model is used, n_features must be remembered, and input it likely..
        '''

        saved_model = joblib.dump(data, filename, compress=9)
        print saved_model


    @staticmethod
    def saveDf(data, filename):
        '''
        save *.df files
        : DataFrame
        '''

        saved_df = DataFrame.save(data, filename)
        print saved_df


    @staticmethod
    def savePkl(data, filename):
        '''
        save *.pkl files
        !!! update for overwright, newwirght, ...
        '''
        fout = file(filename,"w")
        saved_pickle = pickle.dump(data,fout)

        print saved_pickle


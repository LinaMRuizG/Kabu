import pandas as pd
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import datetime
import numpy as np

class curves:

    def __init__(self,dataframe,datesName,casesName,kernel,plotName,outFolder):
        
        #database
        self.df = dataframe
        # in this frst version the database is a DataFrame with 2 columns 
        # But it could be for more columns or curves.
        # the dates could be strings or datetimes

        #column names variable
        self.dN = datesName
        self.cN = casesName
        
        #parameters
        self.kernel = kernel # is the same kernel for both smoothing

        #to fit
        self.plotName = plotName
        self.outFolder = outFolder
    
    
    def stansardizingDates(self):

        """It converts the dates in a Timestamp object"""

        df = self.df
        df[self.dN] = pd.to_datetime(df[self.dN]) 
        #this should be improved to standardize even when they are already Timestamp.. 

    
    def curveNormalization(self, inputNormalization, outputNormalization):

        """It normalizes (i.e., dividing by the maximum value) a column in the dataframe.
        The result is a new column in the dataframe"""

        df = self.df
        df[outputNormalization] = df[inputNormalization]/df[inputNormalization].abs().max()
        #print(df)


    def __gettingKernel(self):

        kInfo = self.kernel
        
        if isinstance(self.kernel,(int,float)):
            k = self.kernel/2
        else:
            df = kInfo[0]
            c1 = kInfo[1]
            v1 = kInfo[2]
            c2 = kInfo[3]
            k = df[df[c1]==v1][c2]
        return int(k.iloc[0])/2



    def curveSmoothing(self,inputToSmooth,outputSmoothed):

        """It makes a Gaussian filter of any column in the dataframe using the
        gaussian_filter function """

        kernel = self.__gettingKernel()
        df = self.df
        df[outputSmoothed] = gaussian_filter(df[inputToSmooth], kernel)

    
    def curveSmoothing2(self,inputToSmooth,outputSmoothed):
        
        """It makes a Gaussian filter of any column in the dataframe using the equation 
        of gaussian filter"""

        kernel = self.__gettingKernel()
        smoothed_cases = []
        df = self.df
        
        for date in sorted(df[self.dN]):
            df['gaussian'] = np.exp( - (((df[self.dN] - date).apply(lambda x: x.days)) ** 2) / (2 * (kernel ** 2)))
            df['gaussian'] /= df['gaussian'].sum()
            smoothed_cases.append((df[inputToSmooth] * df['gaussian']).sum())     
        df[outputSmoothed] = smoothed_cases
      
    
    def discreteDerivative(self,inputToDerivate,outputDerivate):
        
        """It makes a discrete derivate of any column in the dataframe"""
        
        df = self.df
        df[outputDerivate] = df[inputToDerivate].rolling(2).agg(lambda x : x.iloc[1]-x.iloc[0])
    
    
    def plottingTheCurveNormalized(self):

        """It makes a plot of the Normalized Cases"""

        df = self.df

        plt.figure(figsize=(12,6))
        
        plt.plot(df[self.dN],df["NormalizedCases"], color = "gray", label ="Raw Cases")
        plt.plot(df[self.dN],df["SmoothedNCases"], color="red", label ="Smoothed Cases")
        plt.ylabel("Normalized Cases")
        plt.xlabel("Time")
        plt.title(self.plotName)
        plt.legend()

    def plottingTheCurveNoNormalized(self):

        """It makes a plot of the No-Normalized Cases"""

        df = self.df

        plt.figure(figsize=(12,6))
        
        plt.plot(df[self.dN],df[self.cN], color = "gray", label ="Raw Cases")
        plt.plot(df[self.dN],df["SmoothedCases"], color="red", label ="Smoothed Cases")
        plt.ylabel("Cases")
        plt.xlabel("Time")
        plt.title(self.plotName)
        plt.legend()

    

    def run(self):

        """It run all the class methods in the correct order"""

        self.stansardizingDates()

        self.curveNormalization(self.cN,"NormalizedCases")
        
        self.curveSmoothing2("NormalizedCases","SmoothedNCases")
        self.curveSmoothing2(self.cN,"SmoothedCases")
    
        
        self.discreteDerivative("SmoothedNCases","FirstDerivate")
        self.curveSmoothing2("FirstDerivate","FirstDerivateSmoothed")
        
        
        self.discreteDerivative("FirstDerivateSmoothed","SecondDerivate")
        
    def run2(self):
        
        self.run()
        self.plottingTheCurveNormalized()
        self.plottingTheCurveNoNormalized()
        plt.show()


















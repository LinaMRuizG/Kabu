import pandas as pd
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import datetime
import numpy as np

class curves:
    
    """curves is the class from kabu module in the EpidemicKabu library.⁄n
    The main workflow of this class is to normalize the epidemic curve, 
    smooth it with a Gaussian kernel, and estimate the first and second derivative 
    of the smoothed curveThe main workflow of this class is to normalize, smooth with 
    a Gaussian kernel, and estimate the first and second derivative of the epidemic curve. 
    A draw of this workflow in ***LINK****
     """

    def __init__(self,dataframe,datesName,casesName,kernel,plotName,dfName,outFolderPlot = "./plots/",outFolderDF="./dataframes/"):

        """The arguments to make an instance are:
         1. dataframe: DataFrame with the dates and the number of cases by date
         2. datesName: Name of the column with the dates which are strings 
         3. casesName: Name of the column with the cases by each date
         4. kernel: value of the parameters to apply the Gaussian kernel.
         The kernel could be a int or it could be a list with [df,column1,value,column2], where
         df is a dataframe with a column1 (i.e., name of this coulmn1) with the values (i.e., name of this value to filter)
         to select from column2 (i.e., name of this coulmn2) an specific kernel value. In this way you 
         could use a configuration file with the kernels as in ***LINK****
         5. plotName: The name for the output plot and file of the plot
         5. dfName: The name for the output dataframe. This dataframe has the inital
         dates and number of cases and it is added a column for the normalized values
         and smoothed values
         6. outFolderPlot: The directory to put the output plot. The default is ./plots/, be sure of create it
         7. outFolderDF: The directory to put the output dataframe. The default is ./dataframes/, be sure of create it""" 
        
        #database
        self.df = dataframe
        #column names 
        self.dN = datesName
        self.cN = casesName
        #parameters
        self.kernel = kernel # is the same kernel for both smoothing
        #to customize
        self.plotName = plotName
        self.dfName = dfName
        self.outFolderPlot = outFolderPlot
        self.outFolderDF = outFolderDF

    
    def stansardizingDates(self):

        """It converts the dates of the column datesName in a Timestamp object with to_date() function from pandas"""

        df = self.df
        df[self.dN] = pd.to_datetime(df[self.dN])

    
    def curveNormalization(self, inputNormalization, outputNormalization):

        """It normalizes (i.e., dividing by the maximum value) a column (i.e., inputNormalization) in the dataframe.
        The result is a new column (i.e., outputNormalization) in the dataframe"""

        df = self.df
        df[outputNormalization] = df[inputNormalization]/df[inputNormalization].abs().max()


    def __gettingKernel(self):

        """It gets the kernel value. The kernel could be a int or it could be a list with [df,column1,value,column2], where
         df is a dataframe with a column1 (i.e., name of this c1) with the values (i.e., name of this v1 to filter)
         to select from column2 (i.e., name of this c2) an specific kernel value. In this way you 
         could use a configuration file with the kernels as in ***LINK****"""

        kInfo = self.kernel
        
        if isinstance(self.kernel,(int,float)):
            k = self.kernel
        else:
            df = kInfo[0]
            c1 = kInfo[1]
            v1 = kInfo[2]
            c2 = kInfo[3]
            k = int(df[df[c1]==v1][c2].iloc[0])
        return k/2


    def curveSmoothing(self,inputToSmooth,outputSmoothed):

        """It smooths any column (i.e.,inputToSmooth) in the dataframe using gaussian_filter 
        function. The result is a new column (i.e., outputSmoothed) in the dataframe """

        kernel = self.__gettingKernel()
        df = self.df
        df[outputSmoothed] = gaussian_filter(df[inputToSmooth], kernel)

    
    def curveSmoothing2(self,inputToSmooth,outputSmoothed):
        
        """It smooths any column (i.e.,inputToSmooth) in the dataframe using a Gaussian kernel
        function. The result is a new column (i.e., outputSmoothed) in the dataframe """

        kernel = self.__gettingKernel()
        smoothed_cases = []
        df = self.df
        
        for date in sorted(df[self.dN]):
            df['gaussian'] = np.exp( - (((df[self.dN] - date).apply(lambda x: x.days)) ** 2) / (2 * (kernel ** 2)))
            df['gaussian'] /= df['gaussian'].sum()
            smoothed_cases.append((df[inputToSmooth] * df['gaussian']).sum())     
        df[outputSmoothed] = smoothed_cases
      
    
    def discreteDerivative(self,inputToDerivate,outputDerivate):
        
        """It makes a discrete derivate of any column (i.e., inputToDerivate) in the dataframe. The result is a new column (i.e., outputDerivate)
          in the dataframe"""
        
        df = self.df
        df[outputDerivate] = df[inputToDerivate].rolling(2).agg(lambda x : x.iloc[1]-x.iloc[0])
    
    
    def plottingTheCurveNormalized(self):

        """It makes a temporal plot of the Normalized and Smoothed cases"""

        df = self.df

        plt.figure(figsize=(12,6))
        
        plt.plot(df[self.dN],df["NormalizedCases"], color = "gray", label ="Raw Cases")
        plt.plot(df[self.dN],df["SmoothedNCases"], color="red", label ="Smoothed Cases")
        plt.ylabel("Normalized Cases")
        plt.xlabel("Time")
        plt.title(self.plotName)
        plt.legend()

    def plottingTheCurveNoNormalized(self):

        """It makes a temporal plot of the No-Normalized and Smoothed cases"""

        df = self.df

        plt.figure(figsize=(12,6))
        
        plt.plot(df[self.dN],df[self.cN], color = "gray", label ="Raw Cases")
        plt.plot(df[self.dN],df["SmoothedCases"], color="red", label ="Smoothed Cases")
        plt.ylabel("Cases")
        plt.xlabel("Time")
        plt.title(self.plotName)
        plt.legend()


    def run(self):

        """It run all the class methods in the correct order to make the main workflow of this class.
        It creates the output variables that will be part of the a dataframe to be used in the kabuWaves 
        and kabuPeakValleys modules"""

        self.stansardizingDates()

        self.curveNormalization(self.cN,"NormalizedCases")
        
        self.curveSmoothing2("NormalizedCases","SmoothedNCases")
        self.curveSmoothing2(self.cN,"SmoothedCases")
    
        
        self.discreteDerivative("SmoothedNCases","FirstDerivate")
        self.curveSmoothing2("FirstDerivate","FirstDerivateSmoothed")
        
        
        self.discreteDerivative("FirstDerivateSmoothed","SecondDerivate")


    def runAndPlot(self):
        
        """If builds the plot and a dataframe of the plot"""

        self.run()
        
        self.plottingTheCurveNormalized()
        plt.savefig(self.outFolderPlot+self.plotName+"N.png")
        self.plottingTheCurveNoNormalized()
        plt.savefig(self.outFolderPlot+self.plotName+"NoN.png")
        
        df = self.df[[self.dN,self.cN,"NormalizedCases","SmoothedCases"]]
        df.to_csv(self.outFolderDF + self.dfName + ".csv")


















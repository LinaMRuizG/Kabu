from kabuWaves import *

class peaksValleys(waves):

    def __init__(self,dataframe,datesName,casesName,kernel,plotName,dfName,outFolderPlot = "./plots/",outFolderDF="./dataframes/",thresholdPV=0):
        
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
         7. outFolderDF: The directory to put the output dataframe. The default is ./dataframes/, be sure of create it
         8. thresholdPV: It is used to filter the peaks and valleys""" 
        
        super().__init__(dataframe,datesName,casesName,kernel,plotName,dfName,outFolderPlot,outFolderDF,thresholdW=None)
        self.thresholdPV = thresholdPV

    def idenCutPoints(self,inputToFindCuts,outputName): 

        """For a column (i.e.,inputToFindCuts), it identifies the positions (i.e., rows) with a 
        positive value for each consecutive pair of positive-negative values (+/-) and negative value for 
        each consecutive pair of negative-positive values (-/+)"""

        df = self.df

        df[outputName] = (df[inputToFindCuts].rolling(2).agg(lambda x : True if (x.iloc[0]<0 and x.iloc[1]>0) or (x.iloc[0]>0 and x.iloc[1]<0) else False)).fillna(False)

       
    def thresholdNeg(self):

        """It selects those cutDates below the threshold"""
        
        thresholdN = self.thresholdPV
        df = self.df
             
        cutDatesDF = df[df[self.dN].isin(self.cutDates)].reset_index(drop = True)
        cutDatesDF = cutDatesDF[self.dN]
        select = cutDatesDF.groupby(cutDatesDF.index//2).agg(lambda x : x if  min(df[(df[self.dN]>=x.iloc[0]) & (df[self.dN]<=x.iloc[1])]["SecondDerivate"]) < thresholdN else [])
        dates = pd.to_datetime(select.explode())
        self.cutDates = dates[~np.isnat(dates)]


    def run(self):
       
        """It run all the class methods in the correct order and builds the plot and a dataframe of the plot"""
        
        #those are the methods of curves class
        self.stansardizingDates()
        self.curveNormalization(self.cN,"NormalizedCases")
        self.curveSmoothing2("NormalizedCases","SmoothedNCases")
        self.curveSmoothing2(self.cN,"SmoothedCases")
        self.discreteDerivative("SmoothedNCases","FirstDerivate")
        self.curveSmoothing2("FirstDerivate","FirstDerivateSmoothed")
        self.discreteDerivative("FirstDerivateSmoothed","SecondDerivate")

        #those are the methods from this class
        self.idenCutPoints("SecondDerivate","rollingSD")
        
        #those are the methods from detecting waves class
        self.idenPreviousDates("rollingSD","SecondDerivate")
        
        #those are the methods from this class
        self.thresholdNeg()

        #creating and saving the output dataframe
        self.df["cutDates"] = self.df[self.dN].isin(self.cutDates).astype(int)
        df = self.df[[self.dN,self.cN,"SmoothedCases","cutDates"]]
        df.to_csv(self.outFolderDF + self.dfName + ".csv")
        
        self.plottingTheCurveNormalized()
        self.plottingTheCurveNoNormalized()
    






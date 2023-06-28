from kabuWaves import *

class peaksValleys(waves):

    def __init__(self,dataframe,datesName,casesName,kernel,plotName,dfName,outFolder = "./plots/",outFolder2="./dataframes/",thresholdPV=0):
        super().__init__(dataframe,datesName,casesName,kernel,plotName,dfName,outFolder,outFolder2,thresholdW=None)
        self.thresholdPV = thresholdPV

    def idenCutPoints(self,columnToFindCuts,outputName): 

        """This identifies the positions of the Negative values in the consecutive pair Negative/Positive 
        and Positive values in the consecutive pair Positive/Negative
        """

        df = self.df

        df[outputName] = (df[columnToFindCuts].rolling(2).agg(lambda x : True if (x.iloc[0]<0 and x.iloc[1]>0) or (x.iloc[0]>0 and x.iloc[1]<0) else False)).fillna(False)

    
    
    def thresholdNeg(self):

        """It selects those cutDays below the threshold"""
        
        thresholdN = self.thresholdPV
        df = self.df
        
        
        cutDayDF = df[df[self.dN].isin(self.cutDays)].reset_index(drop = True)
        cutDayDF = cutDayDF[self.dN]
        select = cutDayDF.groupby(cutDayDF.index//2).agg(lambda x : x if  min(df[(df[self.dN]>=x.iloc[0]) & (df[self.dN]<=x.iloc[1])]["SecondDerivate"]) < thresholdN else [])
        dates = pd.to_datetime(select.explode())
        self.cutDays = dates[~np.isnat(dates)]
        

    
    def run(self):
       
        """It run all the class methods in the correct order"""
        
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
        self.df["CutDays"] = self.df[self.dN].isin(self.cutDays).astype(int)
        df = self.df[[self.dN,self.cN,"SmoothedCases","CutDays"]]
        df.to_csv(self.outFolder2 + self.dfName + ".csv")
        
        self.plottingTheCurveNormalized()
        self.plottingTheCurveNoNormalized()
    






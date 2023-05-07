from kabu import *

class waves(curves):
        
    def __init__(self,databasePath,datesName,casesName,kernel,thresholdW):
        super().__init__(databasePath,datesName,casesName,kernel)
        self.thresholdW = thresholdW
    
    
    def idenCutPoints(self,inputToFindCuts,outputCuts):

        """It identifies the positions with a Positive value for each consecutive pair
        positive / negative (+/-)."""

        df = self.df

        df[outputCuts]= (df[inputToFindCuts].rolling(2).agg(lambda x : True if x.iloc[0]<0 and x.iloc[1]>0 else False)).fillna(False)

        #print(df)


    def idenPreviousDates(self,inputCuts,inputToFindCuts):#column name from where the rolling comes from

        """It identifies the missing value of the consecutive pairs (+/- or -/+) of the CutPoints and also 
        concatenates them in a unique list. After that, it select one values/position by each
        consecutive pair for the final cutDays list"""

        df = self.df
       
        positions1 = df[df[inputCuts]==True][[self.dN,inputToFindCuts]].reset_index(drop=True)
       
        positions2 = df[df[self.dN].isin(list(positions1[self.dN] - datetime.timedelta(days=1)))][[self.dN,inputToFindCuts]].reset_index(drop=True)
        positions2.rename(columns={self.dN:self.dN+"1",inputToFindCuts:inputToFindCuts+"1"},inplace=True)
        
        positions = pd.concat([positions1, positions2], axis=1)

        self.cutDays = list(positions.agg(lambda x : x[self.dN] if abs(x[inputToFindCuts])<abs(x[inputToFindCuts+"1"])  else x[self.dN+"1"], axis=1))
        
        
    def thresholdPos(self):

        """It selects those cutDays above the threshold"""
        
        thresholdW = self.thresholdW
        df = self.df

        self.cutDays = df[df[self.dN].isin(self.cutDays)].reset_index(drop = True)
        self.cutDays = self.cutDays.agg(lambda x : x[self.dN] if  x["SecondDerivate"] > thresholdW else [],axis=1)
        self.cutDays = pd.to_datetime(self.cutDays.explode())
        self.cutDays = self.cutDays[~np.isnat(self.cutDays)]



    def plottingTheCurveNormalized(self):

        """It adds to the plot the CutDays"""
        
        super().plottingTheCurveNormalized()
        df = self.df
        cases = df["NormalizedCases"]
        
        for date in self.cutDays:
            plt.axvline(x=date, color='black', ymax= max(cases), linestyle='--', linewidth=.91)
        plt.show()

        
    def plottingTheCurveNoNormalized(self):

        """It adds to the plot the CutDays"""
        
        super().plottingTheCurveNoNormalized()
        df = self.df
        cases = df[self.cN]
        
        for date in self.cutDays:
            plt.axvline(x=date, color='black', ymax= max(cases), linestyle='--', linewidth=.91)
        plt.show()


    def run(self):
       
        """It run all the class methods in the correct order"""
        
        super().run()
        self.idenCutPoints("FirstDerivateSmoothed","rollingFDS")
        self.idenPreviousDates("rollingFDS","FirstDerivateSmoothed")
        self.thresholdPos()
        self.plottingTheCurveNormalized()
        self.plottingTheCurveNoNormalized()

    
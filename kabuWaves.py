from kabu import *

class waves(curves):

    """waves is the class from kabuWaves module in the EpidemicKabu library. It is a child class of 
    curves class from module kabu. Its workflow is to identify the cut points that delimites the start
    and the end of a wave using the methods idenCutPoints() and idenPreviousDates(). And filter those cut 
    points according to a threshold with the method idenPreviousDates(). A draw of this workflow in ***LINK****
     """
        
    def __init__(self,dataframe,datesName,casesName,kernel,plotName,dfName,outFolderPlot = "./plots/",outFolderDF="./dataframes/",thresholdW=0):
        
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
         8. thresholdW: It is used to filter the waves""" 
        
        super().__init__(dataframe,datesName,casesName,kernel,plotName,dfName,outFolderPlot,outFolderDF)     
        self.thresholdW = thresholdW
    
    
    def idenCutPoints(self,inputToFindCuts,outputCuts):

        """For a column (i.e.,inputToFindCuts), it identifies the positions (i.e., rows) with a 
        positive value for each consecutive pair of positive-negative values (+/-)."""

        df = self.df

        df[outputCuts]= (df[inputToFindCuts].rolling(2).agg(lambda x : True if x.iloc[0]<0 and x.iloc[1]>0 else False)).fillna(False)


    def idenPreviousDates(self,inputCuts,inputToFindCuts):

        """Using the columns (i.e.,inputCuts and inputToFindCuts) from the dataframe, it identifies 
        the positions (i.e., rows) with a negative value for each consecutive pair of positive-negative values (+/-)
        or a positive value for each consecutive pair of negative-positive values (-/+). It filters with these positions
        the dates and the values of inputToFindCuts (i.e., the column used to indentify the cut points ***LINK***). 
        Then, it selects the dates associated to the lowest absolute value of each consecutive pair of positive-negative or 
        negative-positive (i.e., ensuring to select the date associate to the value closest to zero or when the values
        of the column cut the axis in the temporal plot ***LINK***)"""

        df = self.df
       
        positions1 = df[df[inputCuts]==True][[self.dN,inputToFindCuts]].reset_index(drop=True)
       
        positions2 = df[df[self.dN].isin(list(positions1[self.dN] - datetime.timedelta(days=1)))][[self.dN,inputToFindCuts]].reset_index(drop=True)
        positions2.rename(columns={self.dN:self.dN+"1",inputToFindCuts:inputToFindCuts+"1"},inplace=True)
        
        positions = pd.concat([positions1, positions2], axis=1)

        self.cutDates = list(positions.agg(lambda x : x[self.dN] if abs(x[inputToFindCuts])<abs(x[inputToFindCuts+"1"])  else x[self.dN+"1"], axis=1))
        
          
    def thresholdPos(self):

        """It selects those cutDates above the threshold"""
        
        thresholdW = self.thresholdW
        df = self.df

        self.cutDates = df[df[self.dN].isin(self.cutDates)].reset_index(drop = True)
        self.cutDates = self.cutDates.agg(lambda x : x[self.dN] if  x["SecondDerivate"] > thresholdW else [],axis=1)
        self.cutDates = pd.to_datetime(self.cutDates.explode())
        self.cutDates = self.cutDates[~np.isnat(self.cutDates)]


    def plottingTheCurveNormalized(self):

        """It adds the cutDates to the temporal plot of the Normalized and Smoothed cases"""
        
        super().plottingTheCurveNormalized()
        df = self.df
        cases = df["NormalizedCases"]
        
        for date in self.cutDates:
            plt.axvline(x=date, color='black', ymax= max(cases), linestyle='--', linewidth=.91)
        plt.savefig(self.outFolderPlot+self.plotName+"N.png")

        
    def plottingTheCurveNoNormalized(self):

        """It adds the cutDates to the temporal plot of the No-Normalized and Smoothed cases"""
        
        super().plottingTheCurveNoNormalized()
        df = self.df
        cases = df[self.cN]
        
        for date in self.cutDates:
            plt.axvline(x=date, color='black', ymax= max(cases), linestyle='--', linewidth=.91)
        plt.savefig(self.outFolderPlot+self.plotName+"NoN.png")


    def run(self):
       
        """It run all the class methods in the correct order and builds the plot and a dataframe of the plot"""
        
        super().run()
        
        self.idenCutPoints("FirstDerivateSmoothed","rollingFDS")
        self.idenPreviousDates("rollingFDS","FirstDerivateSmoothed")
        self.thresholdPos()
        
        self.df["cutDates"] = self.df[self.dN].isin(self.cutDates).astype(int)
        df = self.df[[self.dN,self.cN,"SmoothedCases","cutDates"]]
        df.to_csv(self.outFolderDF + self.dfName + ".csv")

        self.plottingTheCurveNormalized()
        self.plottingTheCurveNoNormalized()

    

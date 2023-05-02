from kabu import *

if __name__ == "__main__":
    
    databasePath = "/Users/linaruiz/Documents/projectEpidemicCurve/data/database.csv"
    datesName = "Date_reported"
    casesName = "New_cases"
    kernel = 28
    thresholdW = 2.5*10**-5
    thresholdPV = 2.5*10**-5

    test = curves(databasePath,datesName,casesName,kernel,thresholdW,thresholdPV)
    
    test.stansardizingDates()

    #All these names for the variables are fixed, the only one changing (between users) are: datesName and casesName
    test.curveNormalization("New_cases","NormalizedCases")#New_cases must be changed by self.cN
    test.curveSmoothing("NormalizedCases","SmoothedNCases")
    test.curveSmoothing("New_cases","SmoothedCases")
   
    test.discreteDerivative("SmoothedNCases","FirstDerivate")
    test.curveSmoothing("FirstDerivate","FirstDerivateSmoothed")
    test.discreteDerivative("FirstDerivateSmoothed","SecondDerivate")
   
    test.idenNegatPositCuts("rollingFDS","FirstDerivateSmoothed")
    test.idenPreviousDates("rollingFDS","FirstDerivateSmoothed")
    
    #test.plottingTheCurveNormalized()
    test.plottingTheCurveNoNormalized()

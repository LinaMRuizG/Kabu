from kabu import curves

if __name__ == "__main__":
    
    databasePath = "/Users/linaruiz/Documents/projectEpidemicCurve/data/database.csv"
    datesName = "Date_reported"
    casesName = "New_cases"
    kernel = 28
    thresholdW = 2.5*10**-5
    thresholdPV = 2.5*10**-5

    #print(database)

    test = curves(databasePath,datesName,casesName,kernel,thresholdW,thresholdPV)
    test.curveNormalization()
    test.curveSmoothing("NormalizedCases","SmoothedNCases")
    test.discreteDerivative("SmoothedNCases","FirstDerivate")
    test.curveSmoothing("FirstDerivate","FirstDerivateSmoothed")
    test.discreteDerivative("FirstDerivateSmoothed","SecondDerivate")
    #test.plottingCurves()
    test.idenNegatPositCuts("rollingFDS","FirstDerivateSmoothed")
    test.idenPreviousDates("rollingFDS","FirstDerivateSmoothed")

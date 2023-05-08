from kabu import curves
from kabuWaves import waves
from kabuPeaksValleys import peaksValleys

if __name__ == "__main__":
    
    databasePath = "/Users/linaruiz/Documents/projectEpidemicCurve/data/database.csv"
    datesName = "Date_reported"
    casesName = "New_cases"
    kernel = 28
    thresholdW = 2.5*10**-5
    thresholdPV = -2.5*10**-5
    plotName = "Italy"

    #for curves class
    #test = curves(databasePath,datesName,casesName,kernel,plotName)
    #test.run2()
    
    #for waves class
    #test = waves(databasePath,datesName,casesName,kernel,plotName,thresholdW)
    #test.run() 

    #for peaksValleys class
    test = peaksValleys(databasePath,datesName,casesName,kernel,plotName,thresholdPV)
    test.run()   
    
    

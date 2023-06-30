from kabu import curves
from kabuWaves import waves
from kabuPeaksValleys import peaksValleys
import pandas as pd

if __name__ == "__main__":
    
    database = pd.read_csv("/Users/linaruiz/Documents/projectEpidemicCurve/data/database.csv")
    datesName = "Date_reported"
    casesName = "New_cases"
    kernel = 28
    plotName = "Epidemic curve for Italy"
    dfName = "Epidemic_curve_Italy"
    outFolderPlot = "/Users/linaruiz/Documents/projectEpidemicCurve/kabu/Kabu/plots/"
    outFolderDF = "/Users/linaruiz/Documents/projectEpidemicCurve/kabu/Kabu/dataframes/"
    thresholdW = 0
    thresholdPV = 0

    #for curves class
    test = curves(database,datesName,casesName,kernel,plotName,dfName,outFolderPlot,outFolderDF)
    test.runAndPlot()
    
    #for waves class
    #test = waves(database,datesName,casesName,kernel,plotName,dfName,outFolder,outFolderPlot,outFolderDF)
    #test.run() 
    #test2 = waves(database,datesName,casesName,kernel,plotName,dfName)
    #test2.run() 

    #for peaksValleys class
    #test = peaksValleys(database,datesName,casesName,kernel,plotName,dfName,outFolder,outFolderPlot,outFolderDF)
    #test.run() 
    #test2 = peaksValleys(database,datesName,casesName,kernel,plotName,dfName)
    #test2.run() 
    
    
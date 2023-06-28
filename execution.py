from kabu import curves
from kabuWaves import waves
from kabuPeaksValleys import peaksValleys
import pandas as pd

if __name__ == "__main__":
    
    kernel = 28
    #kernel could be a list with the [datafram, column with the value to select the row, 
    # value of the row, and column of the kernel]
    #configFile= pd.read_csv("/Users/linaruiz/Documents/projectEpidemicCurve/kabu/Kabu/ConfigFile.csv")
    #kernel = [configFile,"Code","IT","kernel1"]
    
    database = pd.read_csv("/Users/linaruiz/Documents/projectEpidemicCurve/data/database.csv")
    datesName = "Date_reported"
    casesName = "New_cases"
    kernel = 28
    plotName = "Epidemic curve for Italy2"
    dfName = "Epidemic curve for Italy2"
    outFolder = "/Users/linaruiz/Documents/projectEpidemicCurve/kabu/Kabu/plots/"
    outFolder2 = "/Users/linaruiz/Documents/projectEpidemicCurve/kabu/Kabu/dataframes/"
    thresholdW = 0
    thresholdPV = 0

    #for curves class
    #test = curves(database,datesName,casesName,kernel,plotName)
    #test.run2()
    
    #for waves class
    #test = waves(database,datesName,casesName,kernel,plotName,dfName,outFolder,outFolder2,thresholdW)
    #test.run() 
    #test2 = waves(database,datesName,casesName,kernel,plotName,dfName)
    #test2.run() 

    #for peaksValleys class
    test = peaksValleys(database,datesName,casesName,kernel,plotName,dfName,outFolder,outFolder2,thresholdPV)
    test.run() 
    #test2 = peaksValleys(database,datesName,casesName,kernel,plotName,dfName)
    #test2.run() 
    
    

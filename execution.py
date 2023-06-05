from kabu import curves
from kabuWaves import waves
from kabuPeaksValleys import peaksValleys
import pandas as pd

if __name__ == "__main__":
    
    #kernel = 28
    #kernel could be a list with the [datafram, column with the value to select the row, 
    # value of the row, and column of the kernel]
    configFile= pd.read_csv("/Users/linaruiz/Documents/projectEpidemicCurve/kabu/Kabu/ConfigFile.csv")
    kernel = [configFile,"Code","IT","kernel1"]
    
    database = pd.read_csv("/Users/linaruiz/Documents/projectEpidemicCurve/data/database.csv")
    datesName = "Date_reported"
    casesName = "New_cases"
    thresholdW = 2.5*10**-5
    thresholdPV = -2.5*10**-5
    plotName = "Epidemic curve for Italy"
    outFolder = "/Users/linaruiz/Documents/projectEpidemicCurve/kabu/Kabu/plots/"

    #for curves class
    #test = curves(database,datesName,casesName,kernel,plotName,outFolder)
    #test.run2()
    
    #for waves class
    #test = waves(database,datesName,casesName,kernel,plotName,outFolder,thresholdW)
    #test.run() 

    #for peaksValleys class
    test = peaksValleys(database,datesName,casesName,kernel,plotName,outFolder,thresholdPV)
    test.run()   
    
    

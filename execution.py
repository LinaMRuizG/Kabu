from kabu import curves
from kabuWaves import waves
from kabuPeaksValleys import peaksValleys
import pandas as pd

if __name__ == "__main__":
    
    database = pd.read_csv("/Users/linaruiz/Documents/EpidemicKabu_project/dataGeneral/databaseExampleItaly.csv")
    datesName = "Date_reported"
    casesName = "New_cases"
    kernel = 28
    plotName = "Epidemic curve for Italy "
    dfName = "Epidemic_curve_Italy_"
    outFolderPlot = "/Users/linaruiz/Documents/EpidemicKabu_project/EpidemicKabu/plots/"
    outFolderDF = "/Users/linaruiz/Documents/EpidemicKabu_project/EpidemicKabu/dataframes/"
    thresholdW = 0
    thresholdPV = 0

    #for curves class
    test = curves(database,datesName,casesName,kernel,plotName,dfName,outFolderPlot,outFolderDF)
    test.runAndPlot()
    
    #for waves class
    test = waves(database,datesName,casesName,kernel,plotName + "W",dfName +"W",outFolderPlot,outFolderDF)
    test.run() 
    #test = waves(database,datesName,casesName,kernel,plotName + "W",dfName +"W")
    #test.run() 

    #for peaksValleys class
    test = peaksValleys(database,datesName,casesName,kernel,plotName + "PV",dfName + "PV",outFolderPlot,outFolderDF)
    test.run() 
    #test = peaksValleys(database,datesName,casesName,kernel,plotName + "PV",dfName + "PV")
    #test.run() 
    
    
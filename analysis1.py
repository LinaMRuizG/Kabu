# Here we analyze the size of the waves
from kabu import curves
from kabuWaves import waves
from kabuPeaksValleys import peaksValleys

class sizes:

    def __init__(self,database, datesName,casesName, popuName):
        self.df = database
        self.dN = datesName
        self.cN = casesName
        self.pN = popuName
    
    
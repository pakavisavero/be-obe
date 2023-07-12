import  jpype     
import  asposecells     
jpype.startJVM() 
from asposecells.api import Workbook
workbook = Workbook("trial.xlsx")
workbook.save("Output.pdf")
jpype.shutdownJVM()

import sys
import clr # Connecting with .NET (PI Database)

import pandas as pd
import numpy as np

sys.path.append(r'C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0')  
clr.AddReference('OSIsoft.AFSDK')

from OSIsoft.AF import *
from OSIsoft.AF.PI import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *
from OSIsoft.AF.UnitsOfMeasure import *

print("Welcome to PIthon!!")

# PI Data Archive
piServers = PIServers()
piServer = piServers.DefaultPIServer;

def Pull_PI_Data(pitag, start, end, freq, timestampcalc = AFTimestampCalculation.MostRecentTime, summarytype = AFSummaryTypes.Maximum):
    '''Creates dataframe of historical max hourly values for a single PI point'''
    piServers = PIServers()
    piServer = piServers.DefaultPIServer
    pt = PIPoint.FindPIPoint(piServer, pitag)
    timerange = AFTimeRange(start,end)
    span = AFTimeSpan.Parse(freq)
    summaries = pt.Summaries(timerange, span, summarytype, AFCalculationBasis.TimeWeighted, timestampcalc)

    # Loop through and make list
    times = []
    vals = []
    for summary in summaries:
        for event in summary.Value:
            times.append(str(event.Timestamp.LocalTime))
            if type(event.Value) is PIException:
                vals.append(None)
            else:
                vals.append(event.Value)
    # Create dataframe
    df = pd.DataFrame(data = {pitag: vals}, index=times)
    df.index = pd.to_datetime(df.index)
    
    return df

def Pull_Multi_PIData(pitags, start, end, freq, timestampcalc = AFTimestampCalculation.MostRecentTime, complete_cases = False, summarytype = AFSummaryTypes.Maximum):
    '''Creates a dataframe with historical data for multiple points'''
    mult_df = pd.DataFrame()
    
    for tag in pitags:    
        df = Pull_PI_Data(tag, start, end, freq, timestampcalc=timestampcalc, summarytype=summarytype)
        mult_df = pd.concat([mult_df, df], axis=1, join = 'outer')
        mult_df.index = pd.to_datetime(mult_df.index)
        
    if complete_cases:
        mult_df = mult_df.dropna(axis=0, how='any')
    return mult_df


def rename_forecast_cols(df):
    new_colnames = []
    for col in df.columns:
        new_colnames.append((col.split(".")[0]))
    df.columns = new_colnames
    return df

def Store_Preds(df, valuecol, pointname):
    '''Function for storing values from a dataframe back into PI. Index of the dataframe needs to be in 
    datetime format'''
    df.rename(columns = {valuecol:'vals'}, inplace = True)
    df.head()
    piServer = piServers.DefaultPIServer
    writept = PIPoint.FindPIPoint(piServer,pointname)
    writeptname = writept.Name.lower()
    
    for row in df.itertuples():
        val = AFValue()
        val.Value = float(row.vals)
        time = AFTime(str(row.Index))
        val.Timestamp = time
        writept.UpdateValue(val, AFUpdateOption.Replace, AFBufferOption.BufferIfPossible)
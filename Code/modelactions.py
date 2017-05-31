from Code import OSI as osi
from Code import featureengineering as fe

from Code import pipeline as pipe

from sklearn.externals import joblib
import pandas as pd
import numpy as np
import time
from datetime import datetime

import os

import logging

logging.basicConfig(level=logging.INFO, 
                    filename='./LoadForecast.log', # log to this file
                    format='%(asctime)s %(message)s') # include timestamp


def build_and_save_models(load_tags, 
                          weather_tags = ['NWS_KDCA_DewPoint_F','NWS_KDCA_Temperature_F','NWS_KDCA_WindSpeed_mph'],
                         start ='Jan 1 2010',
                          end = '*',
                          freq = '1h',
                         summarytype = osi.AFSummaryTypes.Average):
    # Set starttime
    file_path = './models/'

    start_time = time.time()
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Create and all tags list
    all_tags = load_tags + weather_tags

    print("Starting process to build models for the following points:")
    print(*load_tags, sep='\n')
    # Pull all weather and historic tags
    print("Pulling PI data for the weather points:")
    print(*weather_tags, sep='\n')
    df_weather = osi.Pull_Multi_PIData(weather_tags, start, end, freq, complete_cases=False, summarytype=summarytype)
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": Done pulling weather data taking " + str(round(time.time() - start_time)) + " seconds")
    # Loop through each load tag
    for load in load_tags:
        print("Pulling data for: "+str(load))
        df_load = osi.Pull_Multi_PIData([load], start, end, freq, complete_cases=False, summarytype=summarytype)
        print("Joining Weather and Load Data")

        # Join load with weather
        df_combined = df_load.join(df_weather, how='inner')
        # Make it only complete cases
        df_combined = df_combined.dropna(axis=0, how='any')
        
        # Create X and y variables
        X = df_combined.drop([load], axis = 1)
        y = pd.DataFrame(df_combined[load])
        y_log = np.log(y)
        
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": Fitting Model for: " + str(load) )
        # Fit the model
        pipe.pipeline.fit(X, y_log.values.ravel())
        
        # Save model as file
        filename = file_path+str(load)+'.sav'
        print("Saving fitted model for: " + str(load) + " with filename: " + str(filename))
        print("So far this script has been running for: " + str(round(time.time() - start_time)) + " seconds")
        joblib.dump(pipe.pipeline, filename)


def predict_and_store(points):
    
    logging.info("==== STARTING THE PREDICT AND STORE SCRIPT =====")

    X_future = osi.Pull_Multi_PIData(
        pitags = ['NWS_KDCA_DewPoint_F.Forecast','NWS_KDCA_Temperature_F.Forecast','NWS_KDCA_WindSpeed_mph.Forecast'], 
        start= 't-14d',
        end = '*+7d',
        freq = '1h',
        complete_cases=True,
        summarytype=osi.AFSummaryTypes.Average)
  

    X_future = osi.rename_forecast_cols(X_future)

    
    for model in points:
        filename = str(model)+'.sav'
        file_path = './models/'
        try:
            loaded_model = joblib.load(file_path+filename)
            fut_predictions = pd.DataFrame(np.exp(loaded_model.predict(X_future)), index=X_future.index, columns=['Future_Predictions'])
            storepoint = str(model)[:-2]+'Forecast'

            # Log that we are storing forecast
            print("Storing forecast for: " + str(storepoint))
            logging.info("Storing forecast for: " + str(storepoint))
            
            osi.Store_Preds(fut_predictions, valuecol='Future_Predictions',pointname=storepoint)
        except FileNotFoundError:
            print("Could not store predictions for " + str(model) + ". Check to make sure model SAV file exists.")
            logging.info("Could not store predictions for " + str(model) + ". Check to make sure model SAV file exists.")

            
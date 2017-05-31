# LOAD FORECAST WITH OSISOFT PI USING PYTHON
Readme.txt

The scripts in this folder are used to:
	- Pull historic load from PI
	- Build and store machine learning models for the points
	- Predict and store forecast based on future weather conditions
	- Store results in PI under the name `Tagname+.Forecast`

## Files:

build_points.csv - A list of points for the `BuildModels.py` script to build for
predict_points.csv - A list of points for the `PredictandStore.py` script to predict and store for
BuildModels.py - Run this script to build models for the list of points in the build_points.csv file. Saves model file in the /models folder
PredictandStore.py - Run this script to predict and store results for the points in the predict_points.csv file
/models - Folder containing the model files
/Code - Folder containing code for pulling PI tags, building model and storing reults
LoadForecast.log - Logs the timestamp and results of the BuildModels.py and PredictandStore.py scripts. Use for debugging.

## How to use:
- To Build New Models
	- Open the build_points.csv and add the point names you want to predict. Each point on its own line, no commas.
	- open a powershell of command prompt.
	- cd to the directory containing the scripts
	- run the script
	  `>> python BuildModels.py`


- To Predict and Store Reults in PI
	- Open the predict_points.csv and add the point names you want to predict. Each point on its own line, no commas.
	- open a powershell of command prompt.
	- cd to the directory containing the scripts
	- run the script
	  `>> python PredictandStore.py`

## Questions? Contact Rob Mulla - rob.mulla@gmail.com



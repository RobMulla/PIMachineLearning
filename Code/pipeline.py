# For modeling and pipeline
from sklearn.pipeline import Pipeline

# For preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from .featureengineering import *

# Models
from sklearn.pipeline import FeatureUnion
from sklearn.neighbors import KNeighborsRegressor 
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import PassiveAggressiveRegressor
from sklearn.linear_model import ElasticNet
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.ensemble import AdaBoostRegressor

import pandas as pd
import numpy as np


pipeline = Pipeline([
        
    ('features', FeatureUnion(
                transformer_list=[
                ('Hour of Day', HourOfDayTransformer()),
                ('Day of Week', DayofWeekTransformer()),
                ('Month_of_year', MonthTransformer()),
                ('Day_of_month', DayofMonthTransformer()),
                ('Year', YearTransformer()),
                ('hour dummies',HourDummies()),
                ('month dummies',MonthDummies()),
                ('weekday dummies',WeekdayDummies()),
                ('square temp', SquareTemp()),
                ('square windspeed', SquareWindspeed()),
                ('Weekday weekend', WeekdayWeekend()),
                ('Holiday Binary', HolidayBinary()),
                ('StandardScaler', StandardScaler()),
                ('Temp Change Last', TempChangeLast()),
                ('Temp Change Next', TempChangeNext())
            ])
     ),
        ('estimator', RandomForestRegressor(n_estimators=300))
    ])
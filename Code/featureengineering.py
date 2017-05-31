#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.base import BaseEstimator, TransformerMixin

import pandas as pd
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

class PipelineEstimator(BaseEstimator, TransformerMixin):
    """Define the necessary methods"""

    def __init__(self):
        pass
    
    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        return X

    
class YearTransformer(PipelineEstimator):
    """Parse datetime and pull year"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        self.earliest_date = np.min(X.index.date)
        return self

    def transform(self, X, y = None):
        year = pd.DataFrame(X.index.year)
        return year
    
class MonthTransformer(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        self.earliest_date = np.min(X.index.date)
        return self

    def transform(self, X, y = None):
        moy = pd.DataFrame(X.index.month)
        return moy

class DayofMonthTransformer(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        self.earliest_date = np.min(X.index.date)
        return self

    def transform(self, X, y = None):
        dom = pd.DataFrame(X.index.day)
        return dom
    
class HourOfDayTransformer(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        self.earliest_date = np.min(X.index.date)
        return self

    def transform(self, X, y = None):
        hod = pd.DataFrame(X.index.hour)
        return hod

class DayofWeekTransformer(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        self.earliest_date = np.min(X.index.date)
        return self

    def transform(self, X, y = None):
        dow = pd.DataFrame(X.index.weekday)
        return dow
    
class HourDummies(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        self.earliest_date = np.min(X.index.date)
        return self

    def transform(self, X, y = None):
        """Create Dummy Variables."""
        cat = pd.Categorical(X.index.hour, categories=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
        hourdummies = pd.get_dummies(pd.DataFrame({"cat":cat}),prefix='hour', drop_first=True)
        return hourdummies
    
class MonthDummies(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        self.earliest_date = np.min(X.index.date)
        return self

    def transform(self, X, y = None):
        """Create Dummy Variables."""
        cat = pd.Categorical(X.index.hour, categories=[0,1,2,3,4,5,6,7,8,9,10,11])
        monthdummies = pd.get_dummies(pd.DataFrame({"cat":cat}),prefix='month', drop_first=True)
        return monthdummies
    
class WeekdayDummies(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        self.earliest_date = np.min(X.index.date)
        return self

    def transform(self, X, y = None):
        """Create Dummy Variables."""
        cat = pd.Categorical(X.index.weekday, categories=[0,1,2,3,4,5,6])
        weekdaydummies = pd.get_dummies(pd.DataFrame({"cat":cat}),prefix='weekday', drop_first=True)
        return weekdaydummies

class SquareTemp(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        """Create Squared Variables."""
        return pd.DataFrame(np.square(X['NWS_KDCA_Temperature_F']))
    
class SquareWindspeed(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        """Create Squared Variables."""
        return pd.DataFrame(np.square(X['NWS_KDCA_WindSpeed_mph']))
    
    
class WeekdayWeekend(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        """Create Squared Variables."""
        weekendweekday = ((pd.DatetimeIndex(X.index).dayofweek) // 5 == 1).astype(float)
        weekendweekday = pd.DataFrame(weekendweekday)
        return weekendweekday

class HolidayBinary(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        """Create Squared Variables."""
        cal = calendar()
        holidays = cal.holidays(start='2000-01-01', end='2050-01-01')
        holiday_bin_temp = pd.DataFrame(X.index.date, index=X.index, columns=['date'])
        holiday_bin = holiday_bin_temp['date'].astype('datetime64').isin(holidays)
        holiday_bin = pd.DataFrame(holiday_bin)
        del holiday_bin_temp
        return holiday_bin

class TransformedDetails(PipelineEstimator):
    """Parse datetime into its component parts"""

    def __init__(self):
        self.earliest_date = None

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        """Create Squared Variables."""
        X = pd.DataFrame(X)
        print(X.shape)
        print(X.describe())
        return
    
class FeatureStats(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def transform(self, X, y=None):
        print("size = ", X.shape[1])
        return X

    def fit(self, X, y=None):
        return self
    
class TempChangeLast(PipelineEstimator):
    def __init__(self, use = True):
        pass

    def transform(self, X, y = None):
        
        temp_change_bk = (X['NWS_KDCA_Temperature_F'].shift() - X['NWS_KDCA_Temperature_F']).fillna(0)
        return pd.DataFrame(temp_change_bk)

class TempChangeNext(PipelineEstimator):
    def __init__(self, use = True):
        pass
        
    def transform(self, X, y = None):
        temp_change_fwd = (X['NWS_KDCA_Temperature_F'].shift(-1) - X['NWS_KDCA_Temperature_F']).fillna(0)
        return pd.DataFrame(temp_change_fwd)
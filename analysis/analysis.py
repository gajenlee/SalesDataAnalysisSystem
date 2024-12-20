from abc import ABC, abstractmethod
import pandas as pd
from multipledispatch import dispatch

class Analysis(ABC):

    @abstractmethod
    def display_analysis(self):
        raise NotImplementedError

    @abstractmethod
    def save_analysis(self):
        raise NotImplementedError
    
    @abstractmethod
    def data_graph(self):
        raise NotImplementedError
    
    @abstractmethod
    def corr_graph(self):
        raise NotImplementedError

    @dispatch(dict)
    def _clear_data(self, data:dict) -> pd.DataFrame:
        dataFrame = pd.DataFrame(data)
        dataFrame.dropna(inplace=True)
        dataFrame.drop_duplicates(inplace=True)
        return dataFrame

    @dispatch(list, list)
    def _clear_data(self, row: list, columns: list)-> pd.DataFrame:
        dataFrame = pd.DataFrame(row, columns=columns)
        dataFrame.dropna(inplace=True)
        dataFrame.drop_duplicates(inplace=True)
        return dataFrame
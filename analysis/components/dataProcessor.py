from abc import ABC, abstractmethod

class DataProcessor(ABC):

    @abstractmethod
    def _load_sales_data(self, source: str) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def _save_sales_data(self, output: str, data: list, header: list) -> None:
        raise NotImplementedError
    
    

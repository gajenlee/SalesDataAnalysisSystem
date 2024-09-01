from abc import ABC, abstractmethod

class Analysis(ABC):

    @abstractmethod
    def display_analysis(self):
        raise NotImplementedError

    @abstractmethod
    def save_analysis(self):
        raise NotImplementedError
    
    @abstractmethod
    def display_graph(self):
        raise NotImplementedError

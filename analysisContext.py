from analysis.analysis import Analysis

class AnalysisContext:
    
    def __init__(self, strategy: Analysis):
        if strategy is not None: 
            self._strategy = strategy
    
    def set_strategy(self, strategy: Analysis):
        self._strategy = strategy
    
    def perform_analysis(self):
        try:
            self._strategy.display_analysis()
            return True
        except Exception as e:
            print(e)
            return False
    
    def perform_graph_analysis(self):
        try:
            self._strategy.data_graph()
            return True
        except Exception as e:
            print(e)
            return False
            
    
    def perform_corr_analysis(self, fun=None):
        try:
            if fun is None: self._strategy.corr_graph()
            self._strategy.corr_graph(fun)
            return True
        except Exception as e:
            print(e)
            return False
    
    def perform_save_analysis(self, file_name:str):
        try:
            self._strategy.save_analysis(file_name)
            return True
        except Exception as e:
            print(e)
            return False
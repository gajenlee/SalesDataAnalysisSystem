from analysis.analysis import Analysis

class AnalysisContext:
    
    def __init__(self, strategy: Analysis):
        self._strategy = strategy
    
    def set_strategy(self, strategy: Analysis):
        self._strategy = strategy
    
    def perform_analysis(self):
        self._strategy.display_analysis()
    
    def perform_graph_analysis(self):
        self._strategy.data_graph()
    
    def perform_corr_analysis(self, fun=None):
        if fun is None: self._strategy.corr_graph()
        self._strategy.corr_graph(fun)
    
    def perform_save_analysis(self, file_name:str):
        self._strategy.save_analysis(file_name)
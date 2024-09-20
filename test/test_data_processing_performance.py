import timeit

def test_data_processing_performance():
    setup = "from analysis.monthlySalesAnalysis import MonthlySalesAnalysis;\
        from analysisContext import AnalysisContext;"
    
    stmt = "context = AnalysisContext(MonthlySalesAnalysis('D:/sales_data.csv'));\
        context.perform_analysis();"
    
    execution_time = timeit.timeit(stmt, setup=setup, number=1)
    assert execution_time < 2

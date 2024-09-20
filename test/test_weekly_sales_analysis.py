from analysis.weeklySalesAnalysis import WeeklySalesAnalysis
from analysisContext import AnalysisContext

data_file = r'test\sample_data\sales_data.csv'

# Test Weekly Sales Analysis

# Analysis
def test_weekly_sales_analysis():
    context = AnalysisContext(WeeklySalesAnalysis(data_file))
    assert context.perform_analysis() == True

# Save Analysis
def test_weekly_sales_analysis_save():
    context = AnalysisContext(WeeklySalesAnalysis(data_file))
    assert context.perform_save_analysis("./test_weekly_sales_analysis.csv") == True

# Grap Analysis
def test_weekly_sales_analysis_graph():
    context = AnalysisContext(WeeklySalesAnalysis(data_file))
    context.perform_graph_analysis()

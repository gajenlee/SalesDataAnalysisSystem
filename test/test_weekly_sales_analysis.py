from analysis.weeklySalesAnalysis import WeeklySalesAnalysis
from analysisContext import AnalysisContext


# Test Weekly Sales Analysis

# Analysis
def test_weekly_sales_analysis():
    context = AnalysisContext(WeeklySalesAnalysis('./sample_data/sales_data.csv'))
    assert context.perform_analysis() == True

# Save Analysis
def test_weekly_sales_analysis_save():
    context = AnalysisContext(WeeklySalesAnalysis('./sample_data/sales_data.csv'))
    assert context.perform_save_analysis("./test_weekly_sales_analysis.csv") == True

# Grap Analysis
def test_weekly_sales_analysis_graph():
    context = AnalysisContext(WeeklySalesAnalysis('./sample_data/sales_data.csv'))
    context.perform_graph_analysis()

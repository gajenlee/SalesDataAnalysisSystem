from analysis.monthlySalesAnalysis import MonthlySalesAnalysis
from analysisContext import AnalysisContext

# Test Monthly Sales Analysis

# Analysis
def test_monthly_analysis_all_branch():
    context = AnalysisContext(MonthlySalesAnalysis("D:/sales_data.csv"))
    assert context.perform_analysis() == True

def test_monthly_analysis_branch():
    context = AnalysisContext(MonthlySalesAnalysis("D:/sales_data.csv", branch_name='colombo'))
    assert context.perform_analysis() == True


# Save Analysis
def test_monthly_analysis_all_branch_save():
    context = AnalysisContext(MonthlySalesAnalysis("D:/sales_data.csv"))
    assert context.perform_save_analysis("C:/Users/gajen/OneDrive/Desktop/test_monthly_analysis_all_branch.csv") == True

def test_monthly_analysis_branch_save():
    context = AnalysisContext(MonthlySalesAnalysis("D:/sales_data.csv", branch_name='colombo'))
    assert context.perform_save_analysis("C:/Users/gajen/OneDrive/Desktop/test_monthly_analysis_branch.csv") == True

# Garph Analysis
def test_monthly_analysis_all_branch_graph():
    context = AnalysisContext(MonthlySalesAnalysis("D:/sales_data.csv"))
    assert context.perform_graph_analysis() == True

def test_monthly_analysis_branch_graph():
    context = AnalysisContext(MonthlySalesAnalysis("D:/sales_data.csv", branch_name='colombo'))
    assert context.perform_graph_analysis() == True

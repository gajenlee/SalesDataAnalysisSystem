from analysis.priceAnalysis import PriceAnalysis
from analysisContext import AnalysisContext


# Test Price Analysis

# Analysis
def test_price_analysis_all_product():
    context = AnalysisContext(PriceAnalysis("D:/sales_data.csv"))
    assert context.perform_analysis() == True

def test_price_analysis_product():
    context = AnalysisContext(PriceAnalysis("D:/sales_data.csv", product='bread'))
    assert context.perform_analysis() == True

# Save Analysis
def test_price_analysis_all_product_save():
    context = AnalysisContext(PriceAnalysis("D:/sales_data.csv"))
    assert context.perform_save_analysis("C:/Users/gajen/OneDrive/Desktop/test_price_analysis_all_product.csv") == True

def test_price_analysis_product_save():
    context = AnalysisContext(PriceAnalysis("D:/sales_data.csv", product='bread'))
    assert context.perform_save_analysis("C:/Users/gajen/OneDrive/Desktop/test_price_analysis_product.csv") == True

# Graph Analysis
def test_price_analysis_all_product_graph():
    context = AnalysisContext(PriceAnalysis("D:/sales_data.csv"))
    assert context.perform_graph_analysis() == True

def test_price_analysis_product_graph():
    context = AnalysisContext(PriceAnalysis("D:/sales_data.csv", product='bread'))
    assert context.perform_graph_analysis() == True

from analysisContext import AnalysisContext
from analysis.prodectPreferenceAnalysis import ProdectPreferenceAnalysis

data_file = r'test\sample_data\sales_data.csv'
# Test Prodect Preference Analysis

# Analysis
def test_product_preference_analysis():
    context = AnalysisContext(ProdectPreferenceAnalysis(data_file))
    assert context.perform_analysis() == True

# Save Analysis
def test_product_preference_analysis_save():
    context = AnalysisContext(ProdectPreferenceAnalysis(data_file))
    assert context.perform_save_analysis("./test_product_preference_analysis.csv") == True

# Graph Analysis
def test_product_preference_analysis_graph():
    context = AnalysisContext(ProdectPreferenceAnalysis(data_file))
    assert context.perform_graph_analysis() == True


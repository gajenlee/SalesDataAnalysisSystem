from analysisContext import AnalysisContext
from analysis.analysisOfDistribution import AnalysisOfDistribution

# Test Distribution Analysis

# Analysis
def test_distribution_analysis():
    context = AnalysisContext(AnalysisOfDistribution('./sample_data/sales_data.csv'))
    assert context.perform_analysis() == True

# Save Analysis
def test_distribution_analysis_save():
    context = AnalysisContext(AnalysisOfDistribution('./sample_data/sales_data.csv'))
    assert context.perform_save_analysis("./test_distribution_analysis.csv") == True

# Graph Analysis
def test_distribution_analysis_graph():
    context = AnalysisContext(AnalysisOfDistribution('./sample_data/sales_data.csv'))
    assert context.perform_graph_analysis() == True

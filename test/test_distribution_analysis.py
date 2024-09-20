from analysisContext import AnalysisContext
from analysis.analysisOfDistribution import AnalysisOfDistribution

data_file = r'test\sample_data\sales_data.csv'

# Test Distribution Analysis

# Analysis
def test_distribution_analysis():
    context = AnalysisContext(AnalysisOfDistribution(data_file))
    assert context.perform_analysis() == True

# Save Analysis
def test_distribution_analysis_save():
    context = AnalysisContext(AnalysisOfDistribution(data_file))
    assert context.perform_save_analysis("./test_distribution_analysis.csv") == True

# Graph Analysis
def test_distribution_analysis_graph():
    context = AnalysisContext(AnalysisOfDistribution(data_file))
    assert context.perform_graph_analysis() == True

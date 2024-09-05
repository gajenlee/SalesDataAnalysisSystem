from .components.csv_processor import *
from tabulate import tabulate
from .analysis import Analysis

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

import numpy as np

class AnalysisOfDistribution(CSVProcessor, Analysis):
    __distribution_analysis_data = None
    __file_name = None

    def __init__(self, file_name):
        super().__init__(file_name)
        self.__file_name = file_name
        self.__distribution_analysis_data = self.__distribution_analysis(file_name)
    
    def __distribution_analysis(self, file_name):
        sales_data = self._load_sales_data(file_name)

        common_element_branch = list(set(self._global_fieldname) & set(self._branch))
        common_element_amount = list(set(self._global_fieldname) & set(self._amount))

        if common_element_branch:
            total_sales = sum( row[common_element_amount[0]] for row in sales_data)
            distribution = defaultdict(float)
            for row in sales_data:
                if row[common_element_branch[0]] in distribution:
                    distribution[row[common_element_branch[0]]] = {
                        "amount": distribution[row[common_element_branch[0]]][common_element_amount[0]] + row[common_element_amount[0]],
                        "percentage": (distribution[row[common_element_branch[0]]][common_element_amount[0]] / total_sales) * 100
                    }
                else:
                    distribution[row[common_element_branch[0]]] = {
                        "amount": row[common_element_amount[0]],
                        "percentage": (row[common_element_amount[0]] / total_sales) * 100
                    }
        
        return self._clear_data(distribution).to_dict()

    def display_analysis(self):
        # Extract headers
        headers = ['Branch', 'Amount', 'Percentage']        

        # Extract rows
        rows = [
            [branch, f"{data['amount']:,.2f}", f"{data['percentage']:.2f}%"]
            for branch, data in self.__distribution_analysis_data.items()
        ]

        # Print the table
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def save_analysis(self, file_name):
        headers = ['Branch', 'Amount', 'Percentage']
        rows = [
            { 
                "Branch": branch, 
                "Amount":float(f"{data['amount']:.2f}"), 
                "Percentage":f"{data['percentage']:.2f}%"
            } 
            for branch, data in self.__distribution_analysis_data.items()]
        self._save_sales_data(file_name, rows, headers)

    def data_graph(self):
        plt.subplots_adjust(bottom=0.487, left=0.127)
        rows = [[branch, float(f"{data['amount']:.3f}")] for branch, data in self.__distribution_analysis_data.items()]
        x = [row[0] for row in rows]
        y = [round(row[-1]) for row in rows]
        plt.plot(x, y, marker='o')

        # Apply the formatter to the y-axis
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(self.__millions))

        # Rotate x-axis labels to prevent overlap
        plt.xticks(rotation=45, ha='right')  # Rotate by 45 degrees, align to the right

        plt.title('Distribution Analysis')
        plt.xlabel('Branch')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.show()
    
    def corr_graph(self):
        rows = [
            {"branch": branch, "amount": data['amount'], 'percentage': data['percentage']}
            for branch, data in self.__distribution_analysis_data.items()
        ]
        dataFrame = pd.DataFrame(rows)
        correlation_analysis = dataFrame[['amount', 'percentage']].corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_analysis, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.show()

        sns.clustermap(correlation_analysis, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
        plt.title('Correlation Clustermap')
        plt.tight_layout()
        plt.show()
    
    # Define a custom format function
    def __millions(self, x, pos):
        """
        Convert to millions and add 'M'

        """

        return f'{x * 1e-6:.1f}M' 
        
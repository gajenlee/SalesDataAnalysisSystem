from .components.fileData import *
from tabulate import tabulate
from .analysis import Analysis

class AnalysisOfDistribution(FileData, Analysis):
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
        
        return distribution

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
        rows = [{ "Branch": branch, "Amount":float(f"{data['amount']:.2f}"), "Percentage":f"{data['percentage']:.2f}%"} for branch, data in self.__distribution_analysis_data.items()]
        self._save_sales_data(file_name, rows, headers)
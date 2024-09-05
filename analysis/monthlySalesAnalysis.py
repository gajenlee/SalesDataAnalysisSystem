from .components.csv_processor import *
from tabulate import tabulate
from .analysis import Analysis


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors
import seaborn as sns


import numpy as np

class MonthlySalesAnalysis(CSVProcessor, Analysis):
    __branch_sales_analysis = defaultdict(float)
    __file_name = None
    __branch_name = None
    __headers = ['Branch', "Month",  'Sales']

    def __init__(self, file_name, branch_name = None):
        super().__init__(file_name)
        self.__file_name = file_name
        self.__branch_name = branch_name
        if branch_name == None:
            self.__branch_sales_analysis = self.__monthly_sales_all_branch(file_name)
        else:
            self.__branch_sales_analysis = self.__monthly_sales_branch(branch_name, file_name)


    def __monthly_sales_all_branch(self, file_name):
        sales_data = self._load_sales_data(file_name)
        montly_sales = defaultdict(float)

        common_element_date = list(set(self._global_fieldname) & set(self._date))
        common_element_branch = list(set(self._global_fieldname) & set(self._branch))
        common_element_amount = list(set(self._global_fieldname) & set(self._amount))

        for row in sales_data:
            if common_element_branch:
                branch_name = row[common_element_branch[0]] + "-" + row[common_element_date[0]].strftime('%Y/%m')
                try:
                    montly_sales[branch_name] += row[common_element_amount[0]]
                except:
                    montly_sales[branch_name] = row[common_element_amount[0]]
        
        rows = [
            [branch.split('-')[0], branch.split('-')[-1], sales]
            for branch, sales in montly_sales.items()
        ]

        return self._clear_data(rows, self.__headers).to_dict()

    def __monthly_sales_branch(self, branch, file_name):
        sales_data = self._load_sales_data(file_name)
        montly_sales = defaultdict(float)

        common_element_date = list(set(self._global_fieldname) & set(self._date))
        common_element_branch = list(set(self._global_fieldname) & set(self._branch))
        common_element_amount = list(set(self._global_fieldname) & set(self._amount))

        for row in sales_data:
            if common_element_branch:
                branch_name = row[common_element_branch[0]] + "-" + row[common_element_date[0]].strftime('%Y/%m')
                if row[common_element_branch[0]].lower() == branch.lower():            
                    try:
                        montly_sales[branch_name] += row[common_element_amount[0]]
                    except Exception as e:
                        montly_sales[branch_name] = row[common_element_amount[0]]

        rows = [
            [branch.split('-')[0], branch.split('-')[-1], sales]
            for branch, sales in montly_sales.items()
        ]

        return self._clear_data(rows, self.__headers).to_dict()

    def display_analysis(self):

        # Extract rows
        rows = [[branch[-1], month[-1], sale[-1]] for branch, month, sale in zip(
                        self.__branch_sales_analysis[self.__headers[0]].items(),
                        self.__branch_sales_analysis[self.__headers[1]].items(),
                        self.__branch_sales_analysis[self.__headers[-1]].items())]

        rows.sort()
        # Print the table
        print(tabulate(rows, headers=self.__headers, tablefmt="grid"))
    
    def save_analysis(self, file_name):
        
        rows = [
            { 
                "Branch": branch[-1], 
                "Month":datetime.strptime(month[-1], "%Y/%m").date(), 
                "Sales": float(f"{sales[-1]:.2f}")
            } 
            for branch, month, sales in zip(self.__branch_sales_analysis[self.__headers[0]].items(),
                                     self.__branch_sales_analysis[self.__headers[1]].items(),
                                     self.__branch_sales_analysis[self.__headers[-1]].items())
        ]


        rows.sort(key=lambda x : x['Branch'])
        self._save_sales_data(file_name, rows, self.__headers)
    
    def data_graph(self):

        rows = [
            [ 
                datetime.strptime(month[-1], "%Y/%m").date(), 
                float(f"{sales[-1]:.2f}"),
                branch[-1]
            ] 
            for branch, month, sales in zip(self.__branch_sales_analysis[self.__headers[0]].items(),
                                     self.__branch_sales_analysis[self.__headers[1]].items(),
                                     self.__branch_sales_analysis[self.__headers[-1]].items())
        ]
        
        x_value = [x[0] for x in rows] # Month
        y_value = [y[1] for y in rows] # Sales Amounts
        branches = [br[2] for br in rows] # branch Names

        unique_branches = list(set(branches))
        color_map = {
            branch: color for branch, color in zip(unique_branches, plt.cm.get_cmap('tab10', len(unique_branches)).colors)
        }

        colors = [color_map[branch] for branch in branches]


        fig, ax = plt.subplots()
        scatter = ax.scatter(x_value, y_value, color=colors, marker='o')
        
        # Apply the formatter to the y-axis
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(self.__millions))

        ax.set_xticks(x_value)
        ax.set_xticklabels([date.strftime("%Y-%m") for date in x_value], rotation=45, ha='right')

        # Create legend entries
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[branch], markersize=10, label=branch) for branch in unique_branches]
        ax.legend(handles=legend_handles, title="Branches", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

        cursor = mplcursors.cursor(scatter, hover=True)

    
        @cursor.connect("add")
        def on_add(am):
            index = am.index

            branch_name =branches[index]
            amount = y_value[index]
            month = x_value[index]

            am.annotation.set(
                text=f"Branch: {branch_name}\nMonth: {month.strftime('%Y-%m')}\nAmount: {amount:,.2f}", 
                color=color_map[branch_name], 
                fontsize=10)
        
        plt.title("Monthly Sales Analysis")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    def corr_graph(self):
        rows = [
            { 
                "branch": branch[-1],
                "sales": float(f"{sales[-1]:.2f}"),
                "month": datetime.strptime(month[-1], "%Y/%m").date(), 
            } 
            for branch, month, sales in zip(self.__branch_sales_analysis[self.__headers[0]].items(),
                                     self.__branch_sales_analysis[self.__headers[1]].items(),
                                     self.__branch_sales_analysis[self.__headers[-1]].items())
        ]
        dataFrame = pd.DataFrame(rows)
        dataFrame['month'] = pd.to_datetime(dataFrame['month'], format='%Y/%m').map(pd.Timestamp.toordinal)
        correlation_analysis = dataFrame[['sales', 'month']].corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_analysis, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.show()

    # Define a custom format function
    def __millions(self, x, pos):
        """
        Convert to millions and add 'M'

        """

        return f'{x * 1e-6:.1f}M' 
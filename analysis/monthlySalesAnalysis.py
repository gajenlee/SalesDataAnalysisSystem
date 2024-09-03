from .components.fileData import *
from tabulate import tabulate
from .analysis import Analysis


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors


import numpy as np

class MonthlySalesAnalysis(FileData, Analysis):
    __branch_sales_analysis = defaultdict(float)
    __file_name = None
    __branch_name = None

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
        return montly_sales


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
        return montly_sales

    def display_analysis(self):
        # Extract headers
        headers = ['Branch-Month', "Month",  'Sales']

        # Extract rows
        rows = [
            [branch.split('-')[0], branch.split('-')[-1], f"{sales:,.2f}"]
            for branch, sales in self.__branch_sales_analysis.items()
        ]
        rows.sort()

        # Print the table
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def save_analysis(self, file_name, all=False):
        print(self.__file_name)
        if all == False and self.__branch_name:
            rows = [
                { 
                    "Branch": branch.split("-")[0], 
                    "Month":datetime.strptime(branch.split("-")[-1], "%Y/%m").date(), 
                    "Sales": float(f"{sales:.2f}")
                } 
                for branch, sales in self.__monthly_sales_branch(self.__branch_name, self.__file_name).items()
            ]

        else:
            rows = [
                { 
                    "Branch": branch.split("-")[0], 
                    "Month":datetime.strptime(branch.split("-")[-1], "%Y/%m").date(), 
                    "Sales": float(f"{sales:.2f}")
                } 
                for branch, sales in self.__monthly_sales_all_branch(self.__file_name).items()
            ]

        rows.sort(key=lambda x : x['Branch'])

        headers = ['Branch', "Month",  'Sales']
        self._save_sales_data(file_name, rows, headers)
    
    def display_graph(self, all=False):
        if all:
            rows = [
                [ 
                    datetime.strptime(branch.split("-")[-1], "%Y/%m").date(),
                    float(f"{sales:.2f}"),
                    branch.split("-")[0]
                ]
                for branch, sales in self.__monthly_sales_all_branch(self.__file_name).items()
            ]
        else:
            rows = [
                [ 
                    datetime.strptime(branch.split("-")[-1], "%Y/%m").date(),
                    float(f"{sales:.2f}"),
                    branch.split("-")[0]
                ]
                for branch, sales in self.__monthly_sales_branch(self.__branch_name, self.__file_name).items()
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

    # Define a custom format function
    def __millions(self, x, pos):
        """
        Convert to millions and add 'M'

        """

        return f'{x * 1e-6:.1f}M' 
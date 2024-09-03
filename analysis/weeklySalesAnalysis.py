from .components.fileData import *
from tabulate import tabulate
from .analysis import Analysis


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors

class WeeklySalesAnalysis(FileData, Analysis):
    
    __weekly_sales_analysis_data = None
    __file_name = None

    def __init__(self, file_name):
        super().__init__(file_name)
        self.__file_name = file_name
        self.__weekly_sales_analysis_data = self.__weekly_sales_analysis(file_name)

    def __weekly_sales_analysis(self, file_name):
        sales_data = self._load_sales_data(file_name)
        weekly_sales = defaultdict(float)

        common_element_date = list(set(self._global_fieldname) & set(self._date))
        common_element_amount = list(set(self._global_fieldname) & set(self._amount))
        
        for row in sales_data:
            if common_element_date:
                week = row[common_element_date[0]].strftime('%Y/%U')
                weekly_sales[week] += row[common_element_amount[0]]
        return weekly_sales

    def display_analysis(self):
        # Prepare the data for tabulate
        headers = ["Week", "Sales"]
        rows = [(week, f"{sales:,.2f}") for week, sales in self.__weekly_sales_analysis_data.items()]
        rows.sort()

        # Print the table
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def save_analysis(self, file_name):
        headers = ["Week", "Sales"]
        rows = [
            { 
                "Week": datetime.strptime(week + "/1", "%Y/%W/%w").date(), 
                "Sales":float(f"{sales:.2f}")
            } 
            for week, sales in self.__weekly_sales_analysis(self.__file_name).items()
        ]
        rows.sort(key=lambda x:x["Week"])
        self._save_sales_data(file_name, rows, headers)
    
    def display_graph(self):
        rows = [
            [ 
                datetime.strptime(week + "/1", "%Y/%W/%w").date(), 
                float(f"{sales:.2f}")
            ] 
            for week, sales in self.__weekly_sales_analysis(self.__file_name).items()
        ]
        x_values = [row[0] for row in rows]
        y_values = [row[1] for row in rows]

        fig, ax = plt.subplots()
        scatter = ax.scatter(x_values, y_values, marker='o')

        # Apply the formatter to the y-axis
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(self.__millions))

        cursor = mplcursors.cursor(scatter, hover=True)

        @cursor.connect('add')
        def on_add(mousePoint):
            index = int(mousePoint.index)
            mousePoint.annotation.set(text=f"Week: {x_values[index]}\nSale: {y_values[index]:,.2f}", fontsize=10)

        plt.title("Weekly Sales Analysis")
        plt.xlabel("Week (Count)")
        plt.ylabel("Sales (Amount)")
        plt.grid(True)
        plt.xticks(rotation=45, ha="right")
        plt.subplots_adjust(bottom=0.22)
        plt.show()

    # Define a custom format function
    def __millions(self, x, pos):
        """
        Convert to millions and add 'M'

        """

        return f'{x * 1e-6:.1f}M' 

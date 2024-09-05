from .components.csv_processor import *
from tabulate import tabulate
from .analysis import Analysis


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors
import seaborn as sns

class WeeklySalesAnalysis(CSVProcessor, Analysis):
    
    __weekly_sales_analysis_data = None
    __file_name = None
    __headers = ["Week", "Sales"]

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

        rows = [
            [ 
                datetime.strptime(week + "/1", "%Y/%W/%w").date(), 
                float(f"{sales:.2f}")
            ] 
            for week, sales in weekly_sales.items()
        ]
        return self._clear_data(rows, self.__headers).to_dict()

    def display_analysis(self):
        # Prepare the data for tabulate
        rows = [(week[-1], f"{sales[-1]:,.2f}") for week, sales in zip(
            self.__weekly_sales_analysis_data[self.__headers[0]].items(),
            self.__weekly_sales_analysis_data[self.__headers[-1]].items()
            )]
        rows.sort()

        # Print the table
        print(tabulate(rows, headers=self.__headers, tablefmt="grid"))
    
    def save_analysis(self, file_name):
        rows = [
            { 
                "Week": week[-1], 
                "Sales":float(f"{sales[-1]:.2f}")
            } 
            for week, sales in zip(
            self.__weekly_sales_analysis_data[self.__headers[0]].items(),
            self.__weekly_sales_analysis_data[self.__headers[-1]].items()
            )
        ]
        rows.sort(key=lambda x:x["Week"])
        self._save_sales_data(file_name, rows, self.__headers)
    
    def data_graph(self):
        rows = [
            [ 
                week[-1], 
                float(f"{sales[-1]:.2f}")
            ] 
            for week, sales in zip(
            self.__weekly_sales_analysis_data[self.__headers[0]].items(),
            self.__weekly_sales_analysis_data[self.__headers[-1]].items()
            )
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

    def corr_graph(self):
        rows = [
            { 
                self.__headers[0]: week[-1], 
                self.__headers[-1]: float(f"{sales[-1]:.2f}")
            } 
            for week, sales in zip(
            self.__weekly_sales_analysis_data[self.__headers[0]].items(),
            self.__weekly_sales_analysis_data[self.__headers[-1]].items()
            )
        ]
        data_frame = pd.DataFrame(rows)
        data_frame[self.__headers[0]] = pd.to_datetime(data_frame[self.__headers[0]], format='%Y/%m/%d').map(pd.Timestamp.toordinal)
        correlation_analysis = data_frame[[self.__headers[0], self.__headers[-1]]].corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_analysis, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.show()

        sns.clustermap(correlation_analysis, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
        plt.title('Correlation Clustermap')
        plt.tight_layout()
        plt.show()
        
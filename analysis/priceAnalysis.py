from tabulate import tabulate
from .components.csv_processor import *
from .analysis import Analysis

import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import seaborn as sns
import numpy as np

class PriceAnalysis(CSVProcessor, Analysis):
    
    __analysis_data = None
    __file_name = None
    __product_name = None
    __headers = ['Product', "Average Price", "Total Quantity"]

    def __init__(self, file_name, product=None):
        super().__init__(file_name)
        self.__file_name = file_name
        self.__product_name = product
        if product == None:
            self.__analysis_data = self.__price_analysis_all(file_name)
        else:
            self.__analysis_data = self.__price_analysis(file_name, product)

    def __price_analysis_all(self, file_name):
        sales_data = self._load_sales_data(file_name)
        analysis_data = defaultdict(float)
        prices_list = defaultdict(float)
        qty_list = defaultdict(float)

        common_element_product = list(set(self._global_fieldname) & set(self._product))
        common_element_amount = list(set(self._global_fieldname) & set(self._amount))
        common_element_qty = list(set(self._global_fieldname) & set(self._quantity))

        for row in sales_data:
            if common_element_product:
                if row[common_element_product[0]] in prices_list:
                    prices_list[row[common_element_product[0]]].append(row[common_element_amount[0]] / row[common_element_qty[0]])
                    qty_list[row[common_element_product[0]]].append(row[common_element_qty[0]])
                else:
                    prices_list[row[common_element_product[0]]] = [row[common_element_amount[0]]/row[common_element_qty[0]]]
                    qty_list[row[common_element_product[0]]] = [row[common_element_qty[0]]]
        
        for product in prices_list:
            analysis_data[product] = [sum(prices_list[product]) / len(prices_list[product]), sum(qty_list[product])]

        rows = [
            [product, list_val[0], list_val[1]]
            for product, list_val in analysis_data.items()
        ]

        return self._clear_data(rows, self.__headers).to_dict() 

    def __price_analysis(self, file_name, product):
        analysis_data = defaultdict(float)
        sales_data = self._load_sales_data(file_name)
        prices = [row['amount'] / row['quantity'] for row in sales_data if row['product'].lower() == product.lower()]
        qty = [row['quantity'] for row in sales_data if row['product'].lower() == product.lower()]
        if prices:
            analysis_data[product] = [sum(prices) / len(prices), sum(qty)]
            
        else:
            analysis_data[product] = [0, 0]
        
        rows = [
            [product, list_val[0], list_val[1]]
            for product, list_val in analysis_data.items()
        ]

        return self._clear_data(rows, self.__headers).to_dict() 

    def display_analysis(self):

        # Extract rows
        rows = [
            [product[-1], f"{avg[-1]:,.2f}", f"{tot[-1]:,}"]
            for product, avg, tot in zip(
                self.__analysis_data[self.__headers[0]].items(),
                self.__analysis_data[self.__headers[1]].items(),
                self.__analysis_data[self.__headers[2]].items())
        ]
        rows.sort()

        # Print the table
        print(tabulate(rows, headers=self.__headers, tablefmt="grid"))

    def save_analysis(self, file_name):
        # Extract rows
        rows = [
            { 
                self.__headers[0]: product[-1], 
                self.__headers[1]: float(f"{avg[-1]:.2f}"),
                self.__headers[2]: tot[-1]
            }
            for product, avg, tot in zip(
                self.__analysis_data[self.__headers[0]].items(),
                self.__analysis_data[self.__headers[1]].items(),
                self.__analysis_data[self.__headers[2]].items())
        ]
        rows.sort(key=lambda x : x[self.__headers[0]])
        self._save_sales_data(file_name, rows, self.__headers)
    
    def data_graph(self):
        rows = [
            [ 
                product[-1], 
                float(f"{avg[-1]:.2f}"),
                tot[-1]
            ]
            for product, avg, tot in zip(
                self.__analysis_data[self.__headers[0]].items(),
                self.__analysis_data[self.__headers[1]].items(),
                self.__analysis_data[self.__headers[2]].items())
        ]
        
        x_value = [row[0] for row in rows]
        y_value = [row[1] for row in rows]
        qty = [row[2] for row in rows]

        fig, ax = plt.subplots()
        scatter = ax.plot(x_value, y_value, marker='o')

        cursor = mplcursors.cursor(scatter, hover=True)

        @cursor.connect("add")
        def on_add(sl):
            index = int(sl.index)
            sl.annotation.set(text=f"Product: {x_value[index]}\nAVG Price: {y_value[index]}\nTotal Qty: {qty[index]}", fontsize=10)

        plt.subplots_adjust(bottom=0.22)
        plt.title("Price Analysis")
        plt.xlabel("Products")
        plt.ylabel("Average Prices")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.show()
        
    def corr_graph(self, corr_fun=None):
        rows = [
            { 
                self.__headers[0]: product[-1], 
                self.__headers[1]: float(f"{avg[-1]:.2f}"),
                self.__headers[2]: tot[-1]
            }
            for product, avg, tot in zip(
                self.__analysis_data[self.__headers[0]].items(),
                self.__analysis_data[self.__headers[1]].items(),
                self.__analysis_data[self.__headers[2]].items())
        ]
        if len(rows) <= 1:
            if corr_fun != None: corr_fun()
        else:
            dataFrame = pd.DataFrame(rows)
            dataFrame[self.__headers[1]] = dataFrame[self.__headers[1]].map(lambda x : float(x) )
            dataFrame[self.__headers[-1]] = dataFrame[self.__headers[-1]].map(lambda x : int(x) )
            correlation_analysis = dataFrame[[self.__headers[1], self.__headers[-1]]].corr()
            
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_analysis, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Correlation Matrix')
            plt.show()
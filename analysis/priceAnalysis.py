from tabulate import tabulate
from .components.fileData import *
from .analysis import Analysis

import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

class PriceAnalysis(FileData, Analysis):
    
    __analysis_data = None
    __file_name = None
    __product_name = None

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

        common_element_product = list(set(self._global_fieldname) & set(self._product))
        common_element_amount = list(set(self._global_fieldname) & set(self._amount))
        common_element_qty = list(set(self._global_fieldname) & set(self._quantity))

        for row in sales_data:
            if common_element_product:
                if row[common_element_product[0]] in prices_list:
                    prices_list[row[common_element_product[0]]].append(row[common_element_amount[0]] / row[common_element_qty[0]])
                else:
                    prices_list[row[common_element_product[0]]] = [row[common_element_amount[0]]/row[common_element_qty[0]]]
        
        for product in prices_list:
            analysis_data[product] = sum(prices_list[product]) / len(prices_list[product])
        return analysis_data 
        

    def __price_analysis(self, file_name, product):
        analysis_data = defaultdict(float)
        sales_data = self._load_sales_data(file_name)
        prices = [row['amount'] / row['quantity'] for row in sales_data if row['product'].lower() == product.lower()]
        if prices:
            average_price = sum(prices) / len(prices)
            analysis_data[product] = average_price
            
        else:
            average_price = 0
            analysis_data[product] = average_price

        return analysis_data

    def display_analysis(self):
        # Extract headers
        headers = ['Product', "Average Price"]

        # Extract rows
        rows = [
            [product, f"{avg:,.2f}"]
            for product, avg in self.__analysis_data.items()
        ]
        rows.sort()

        # Print the table
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def save_analysis(self, file_name, all=False):
        if all and self.__product_name:
            rows = [
                { 
                    "Product": product, 
                    "Average Price":float(f"{price:.2f}")
                } 
                for product, price in self.__price_analysis(self.__file_name, self.__product_name).items()
            ]
        else:
            rows = [
                { 
                    "Product": product, 
                    "Average Price":float(f"{price:.2f}")
                } for product, price in self.__price_analysis_all(self.__file_name).items()
            ]

        headers = ["Product", "Average Price"]
        self._save_sales_data(file_name, rows, headers)
    
    def display_graph(self, all=False):
        if all:
            rows = [
                [ 
                    product, 
                    float(f"{price:.2f}")
                ] for product, price in self.__price_analysis_all(self.__file_name).items()
            ]
        else:
            rows = [
                [ 
                    product, 
                    float(f"{price:.2f}")
                ] 
                for product, price in self.__price_analysis(self.__file_name, self.__product_name).items()
            ]
        
        x_value = [x[0] for x in rows]
        y_value = [y[1] for y in rows]

        fig, ax = plt.subplots()
        scatter = ax.plot(x_value, y_value, marker='o')

        cursor = mplcursors.cursor(scatter, hover=True)

        @cursor.connect("add")
        def on_add(sl):
            index = sl.index
            sl.annotation.set(text=f"Product: {x_value[index]}\nAVG Price: {y_value[index]}", fontsize=10)

        plt.subplots_adjust(bottom=0.22)
        plt.title("Price Analysis")
        plt.xlabel("Products")
        plt.ylabel("Average Prices")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.show()
        

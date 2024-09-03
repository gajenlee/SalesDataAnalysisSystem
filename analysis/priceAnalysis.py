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
    __headers = ['Product', "Average Price"]

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

        rows = [
            [product, avg]
            for product, avg in analysis_data.items()
        ]

        return self._clear_data(rows, self.__headers).to_dict() 
        

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
        
        rows = [
            [product, avg]
            for product, avg in analysis_data.items()
        ]

        return self._clear_data(rows, self.__headers).to_dict() 

    def display_analysis(self):

        # Extract rows
        rows = [
            [product[-1], f"{avg[-1]:,.2f}"]
            for product, avg in zip(
                self.__analysis_data[self.__headers[0]].items(),
                self.__analysis_data[self.__headers[-1]].items())
        ]
        rows.sort()

        # Print the table
        print(tabulate(rows, headers=self.__headers, tablefmt="grid"))

    def save_analysis(self, file_name):
        # Extract rows
        rows = [
            { 
                "Product": product[-1], 
                "Average Price":float(f"{avg[-1]:.2f}")
            }
            for product, avg in zip(
                self.__analysis_data[self.__headers[0]].items(),
                self.__analysis_data[self.__headers[-1]].items())
        ]
        rows.sort(key=lambda x : x[self.__headers[0]])
        self._save_sales_data(file_name, rows, self.__headers)
    
    def display_graph(self):
        rows = [
            [ 
                product[-1], 
                float(f"{avg[-1]:.2f}")
            ]
            for product, avg in zip(
                self.__analysis_data[self.__headers[0]].items(),
                self.__analysis_data[self.__headers[-1]].items())
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
        

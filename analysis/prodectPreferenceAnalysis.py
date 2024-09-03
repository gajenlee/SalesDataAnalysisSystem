from .components.fileData import *
from tabulate import tabulate
from .analysis import Analysis


import pandas as pd
import matplotlib.pyplot as plt
import mplcursors


class ProdectPreferenceAnalysis(FileData, Analysis):
    
    __prodect_preference_analysis_data = None
    __file_name = None

    def __init__(self, file_name):
        super().__init__(file_name)
        self.__file_name = file_name
        self.__prodect_preference_analysis_data = self.__prodect_preference_analysis(file_name)

    
    def __prodect_preference_analysis(self, file_name):
        sales_data = self._load_sales_data(file_name)
        product_sales = defaultdict(float)

        common_element_product = list(set(self._global_fieldname) & set(self._product))
        common_element_qty = list(set(self._global_fieldname) & set(self._quantity))

        for row in sales_data:
            if common_element_product:
                product_sales[row[common_element_product[0]]] += row[common_element_qty[0]]
        return product_sales

    def display_analysis(self):

        # Extract headers
        headers = ['Product', "Quantity"]

        # Extract rows
        rows = [
            [product, qty]
            for product, qty in self.__prodect_preference_analysis_data.items()
        ]
        rows.sort()

        # Print the table
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def save_analysis(self, file_name):
        headers = ['Product', "Quantity"]
        rows = [
            { 
                "Product": product, 
                "Quantity":int(qty)
            } 
            for product, qty in self.__prodect_preference_analysis(self.__file_name).items()
        ]
        self._save_sales_data(file_name, rows, headers)
    
    def display_graph(self):
        rows = [
            [ 
                product, 
                int(qty)
            ] 
            for product, qty in self.__prodect_preference_analysis(self.__file_name).items()
        ]

        x_values = [x[0] for x in rows]
        y_values = [y[1] for y in rows]

        fig, ax = plt.subplots()
        plot = ax.plot(x_values, y_values, marker='o')

        cursor = mplcursors.cursor(plot, hover=True)

        @cursor.connect("add")
        def on_add(sl):
            index = int(sl.index)
            sl.annotation.set(text=f"Product: {x_values[index]}\nQuantity: {y_values[index]}", fontsize=10)

        plt.title("Product Perference Analysis")
        plt.xlabel("Products")
        plt.ylabel("Quantity")
        plt.grid(True)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
        
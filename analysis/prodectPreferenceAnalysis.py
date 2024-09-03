from .components.fileData import *
from tabulate import tabulate
from .analysis import Analysis


import pandas as pd
import matplotlib.pyplot as plt
import mplcursors


class ProdectPreferenceAnalysis(FileData, Analysis):
    
    __prodect_preference_analysis_data = None
    __file_name = None
    __headers = ['Product', "Quantity"]

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
        
        rows = [
            [product, qty]
            for product, qty in product_sales.items()
        ]
        rows.sort()

        return self._clear_data(rows, self.__headers).to_dict()

    def display_analysis(self):

        # Extract rows
        rows = [
            [product[-1], qty[-1]]
            for product, qty in zip(self.__prodect_preference_analysis_data[self.__headers[0]].items(),
                                    self.__prodect_preference_analysis_data[self.__headers[1]].items())
        ]
        rows.sort()

        # Print the table
        print(tabulate(rows, headers=self.__headers, tablefmt="grid"))
    
    def save_analysis(self, file_name):
        rows = [
            { 
                "Product": product[-1], 
                "Quantity":int(qty[-1])
            } 
            for product, qty in zip(self.__prodect_preference_analysis_data[self.__headers[0]].items(),
                                    self.__prodect_preference_analysis_data[self.__headers[1]].items())
        ]
        self._save_sales_data(file_name, rows, self.__headers)
    
    def display_graph(self):
        rows = [
            [ 
                product[-1], 
                int(qty[-1])
            ] 
            for product, qty in zip(self.__prodect_preference_analysis_data[self.__headers[0]].items(),
                                    self.__prodect_preference_analysis_data[self.__headers[1]].items())
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
        
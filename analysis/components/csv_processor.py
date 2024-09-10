import csv
from collections import defaultdict
from datetime import datetime
from .dataProcessor import DataProcessor

class CSVProcessor(DataProcessor):

    _global_fieldname = []
    _amount = ["amount", "rs.", "rs", "revenue", "profit"]
    _quantity = ["qty", "quantity", "volume"]
    _date = ["date", "duration"]
    _no = ["no", "id"]
    _product  = ["product"]
    _branch = ['branch']

    def __init__(self, file_name):
        try:
            self._global_fieldname = self.__get_csv_keys(file_name)
        except FileNotFoundError as e:
            self._global_fieldname = []
            print("The file not found!")
    
    
    def _load_sales_data(self, file_name:str) -> list:

        """
            Arguments: 
                file_name: it should be a CSV file path.

            Return: List type data.

            It used to load the data from the CSV file.
        """


        sales_data = []
        try:
            with open(r"{}".format(file_name), mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.__process_keys(self._global_fieldname, row)
                    sales_data.append(row)

        except FileNotFoundError as e:
            print("The file not found... ")
        
        except Exception as e:
            print(e)

        return sales_data
            
    
    def _save_sales_data(self, file_name:str, sales_date:list, header=None):

        """
            Arguments: 
                file_name: it should be a CSV file path.
                sales_data: it should be list type data.
                header: it should be list type and it used to header of the data rows.

            Return: List type data

            It used to save data into the CSV file.
        
        """

        try:
            with open(r"{}".format(file_name), mode='w', newline='') as file:
                if header:
                    writer = csv.DictWriter(file, fieldnames=header)
                else:
                    writer = csv.DictWriter(file, fieldnames=self._global_fieldname)
                writer.writeheader()
                for row in sales_date:
                    writer.writerow(row)
        
        except csv.Error as e:
            print(e)
    
    def __get_csv_keys(self, file_name:str) -> list:
        key_list = []
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key_list = list(row.keys())
        return key_list

    def __process_keys(self, key_list:list, row:dict) -> list:
        for i in range(len(key_list)):
            if key_list[i].lower() in self._amount:
                row[key_list[i]] = float(row[key_list[i]])
            elif key_list[i].lower() in self._quantity or key_list[i] in self._no:
                row[key_list[i]] = int(row[key_list[i]])
            elif key_list[i].lower() in self._date:
                row[key_list[i]] = datetime.strptime(row[key_list[i]], "%Y/%m/%d")
            
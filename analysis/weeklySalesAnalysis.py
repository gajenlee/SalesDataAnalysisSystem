from .components.fileData import *
from tabulate import tabulate
from .analysis import Analysis


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
        rows = [{ "Week": datetime.strptime(week + "/1", "%Y/%W/%w").date(), "Sales":float(f"{sales:.2f}")} for week, sales in self.__weekly_sales_analysis(self.__file_name).items()]
        rows.sort(key=lambda x:x["Week"])
        self._save_sales_data(file_name, rows, headers)

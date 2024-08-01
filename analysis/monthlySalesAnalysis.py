from .components.fileData import *
from tabulate import tabulate

class MonthlySalesAnalysis(FileData):
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
        if all and self.__branch_name:
            rows = [{ "Branch": branch.split("-")[0], "Month":datetime.strptime(branch.split("-")[-1], "%Y/%m").date(), "Sales": float(f"{sales:.2f}")} for branch, sales in self.__monthly_sales_branch(self.__branch_name, self.__file_name).items()]
        else:
            rows = [{ "Branch": branch.split("-")[0], "Month":datetime.strptime(branch.split("-")[-1], "%Y/%m").date(), "Sales": float(f"{sales:.2f}")} for branch, sales in self.__monthly_sales_all_branch(self.__file_name).items()]
        rows.sort(key=lambda x : x['Branch'])

        headers = ['Branch', "Month",  'Sales']
        self._save_sales_data(file_name, rows, headers)
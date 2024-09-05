from analysis.priceAnalysis import PriceAnalysis
from analysis.analysisOfDistribution import AnalysisOfDistribution
from analysis.monthlySalesAnalysis import MonthlySalesAnalysis
from analysis.prodectPreferenceAnalysis import ProdectPreferenceAnalysis
from analysis.weeklySalesAnalysis import WeeklySalesAnalysis
from cli_ui import *

from colorama import Fore
import sys, re


class Main(InterfaceOfConsole):
    
    def __init__(self):
        super().__init__()
    
    def __chech_csv_file(self, file_name):
        folder_location = file_name.split("\\")
        csv_pattern = re.compile(r".*\.csv$", re.IGNORECASE)
        file = [file for file in folder_location if csv_pattern.match(file)]
        if file:
            return True
        return False
    
    def __monthly_sales_analysis(self, csv_file, all=False):
        branch_name = None
        monthly_sales = None

        if all:
            monthly_sales = MonthlySalesAnalysis(csv_file)
        else:
            branch_name = str(self._input("Enter the branch name > "))
            monthly_sales = MonthlySalesAnalysis(csv_file, branch_name)
        print()

        self._view_analysis()
        val = int(self._input())
        if val == 1:
            
            monthly_sales.display_analysis()

            if self._user_to_ask():
                if branch_name:
                    path = str(self._input("Enter save location (X:\\folder name\\) > "))
                    path = self.__location_replacer(path, f"Monthly-Sales-Analysis[{branch_name}].csv")
                    if path:
                        monthly_sales.save_analysis(path)
                    else:
                        self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                        input("\nPress enter to continue....")
                else:
                    path = str(self._input("Enter save location (X:\\folder name\\) > "))
                    path = self.__location_replacer(path, "Monthly-Sales-Analysis.csv")
                    if path:
                        monthly_sales.save_analysis(path)
                    else:
                        self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                        input("\nPress enter to continue....")
        
        elif val == 2:
            self._view_graph()
            inp = int(self._input())

            if inp == 1:
                monthly_sales.data_graph()
            elif inp == 2:
                monthly_sales.corr_graph()
            else:
                pass
            
        else:
            pass

    def __price_analysis(self, csv_file, corr_fun=None, all=False):
        product_name = None

        if all:
            price = PriceAnalysis(csv_file)
        else:
            product_name = str(self._input("Enter the product name > "))
            price = PriceAnalysis(csv_file, product_name)

        self._view_analysis()
        val = int(self._input())

        if val == 1:
            print()
            price.display_analysis()
            if self._user_to_ask():
                if product_name:
                    path = str(self._input("Enter save location (X:\\folder name\\) > "))
                    path = self.__location_replacer(path, f"Price-Analysis[{product_name}].csv")
                    if path:
                        price.save_analysis(path)
                    else:
                        self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                        input("\nPress enter to continue....")
                else:
                    path = str(self._input("Enter save location (X:\\folder name\\) > "))
                    path = self.__location_replacer(path, "Price-Analysis.csv")
                    if path:
                        price.save_analysis(path)
                    else:
                        self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                        input("\nPress enter to continue....")
        elif val == 2:
            self._view_graph()
            inp = int(self._input())

            if inp == 1:
                price.data_graph()
            elif inp == 2:
                price.corr_graph(corr_fun)
            else:
                pass

        else:
            pass
    
    def __weekly_sales_analysis(self, csv_file):
        weekly_analysis = WeeklySalesAnalysis(csv_file)
        self._view_analysis()
        val = int(self._input())

        if val == 1:
            print()
            weekly_analysis.display_analysis()
            if self._user_to_ask():
                path = str(self._input("Enter save location (X:\\folder name\\) > "))
                path = self.__location_replacer(path, "Weekly-Sales-Analysis.csv")
                if path:
                    weekly_analysis.save_analysis(path)
                else:
                    self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                    input("\nPress enter to continue....")
        elif val == 2:
            self._view_graph()
            inp = int(self._input())

            if inp == 1:
                weekly_analysis.data_graph()
            elif inp == 2:
                weekly_analysis.corr_graph()
            else:
                pass

        else:
            pass

    def __product_perference_analysis(self, csv_file):
        product_per = ProdectPreferenceAnalysis(csv_file)
        self._view_analysis()
        val = int(self._input())
        if val == 1:
            print()
            product_per.display_analysis()
            if self._user_to_ask():
                path = str(self._input("Enter save location (X:\\folder name\\) > "))
                path = self.__location_replacer(path, "Product-Perference-Analysis.csv")
                if path:
                    product_per.save_analysis(path)
                else:
                    self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                    input("\nPress enter to continue....")
        elif val == 2:
            self._view_graph()
            inp = int(self._input())

            if inp == 1:
                product_per.data_graph()
            elif inp == 2:
                product_per.corr_graph()
            else:
                pass

        else:
            pass

    def __distribution_analysis(self, csv_file):
        distribution = AnalysisOfDistribution(csv_file)
        print()

        self._view_analysis()
        val = int(self._input())
        if val == 1:
            distribution.display_analysis()
        
            if self._user_to_ask():
                path = str(self._input("Enter save location (X:\\folder name\\) > "))
                path = self.__location_replacer(path, "DistributioAnalysis.csv")
                if path:
                    distribution.save_analysis(path)
                else:
                    self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                    input("\nPress enter to continue....")
        
        elif val == 2:
            self._view_graph()
            inp = int(self._input())

            if inp == 1:
                distribution.data_graph()
            elif inp == 2:
                distribution.corr_graph()
            else:
                pass
        
        else:
            pass

    def __location_replacer(self, path, file_name):
        folder_location = path.split("\\")
        csv_pattern = re.compile(r".*\.csv$", re.IGNORECASE)
        file = [file for file in folder_location if csv_pattern.match(file)]
        if file == []:
            return path + file_name
        return None
    
    def __help(self):
        text = """
1. Location of the CSV data file must be the field names are includes 
    
    1. Amount   -> amount, rs., rs, revenue, profit
    2. Quantity -> qty, quantity, volume
    3. Date     -> date, duration
    4. No       -> no, id
    5. Product  -> product
    6. Branch   -> branch

2. The save loaction of the file seems like this:

    Ex -> Drive_Name:\\Folder_name\\
        - The final slash is imported
"""
        self._print(text, alignment="left", color=Fore.GREEN)
        input("Enter to exit the help... ")

    def runMainLoop(self):
        runner = True
        while runner:
            self._clear()
            self._main_opening_menu()
            val = int(self._input())
            if val == 1:
                inner_runner = True
                while inner_runner:
                    self._clear()
                    self._monthly_analysis_menu()
                    val = int(self._input())
                    
                    if val == 1:
                        csv_file = str(self._input("\nEnter the CSV file path to process the data > "))
                        if self.__chech_csv_file(csv_file):
                            self.__monthly_sales_analysis(csv_file)
                        else:
                            self._print("The CSV file is not found !", alignment='center', color=Fore.RED)
                            input("\nPress enter to continue....")


                    elif val == 2:
                        csv_file = str(self._input("\nEnter the CSV file path to process the data > "))
                        if self.__chech_csv_file(csv_file):
                            self.__monthly_sales_analysis(csv_file, True)
                        else:
                            self._print("The CSV file is not found !", alignment='center', color=Fore.RED)
                            input("\nPress enter to continue....")


                    elif val == 3:
                        inner_runner = False
                    else:
                        inner_runner = False
                        sys.exit()

            elif val == 2:
                inner_runner = True
                while inner_runner:
                    self._clear()
                    self._price_analysis_menu()
                    val = int(self._input())

                    if val == 1:
                        csv_file = str(self._input("\nEnter the CSV file path to process the data > "))
                        if self.__chech_csv_file(csv_file):
                            self.__price_analysis(csv_file, corr_fun=self._userInformationCorr)
                        else:
                            self._print("The CSV file is not found !", alignment='center', color=Fore.RED)
                            input("\nPress enter to continue....")
                        
                    elif val == 2:
                        csv_file = str(self._input("\nEnter the CSV file path to process the data > "))
                        if self.__chech_csv_file(csv_file):
                            self.__price_analysis(csv_file, all=True)
                        else:
                            self._print("The CSV file is not found !", alignment='center', color=Fore.RED)
                            input("\nPress enter to continue....")

                    elif val == 3:
                        inner_runner = False
                    else:
                        inner_runner = False
                        exit()

            elif val == 3:
                csv_file = str(self._input("\nEnter the CSV file path to process the data > "))
                if self.__chech_csv_file(csv_file):
                    self.__weekly_sales_analysis(csv_file)
                else:
                    self._print("The CSV file is not found !", alignment='center', color=Fore.RED)
                    input("\nPress enter to continue....")

            elif val == 4:
                csv_file = str(self._input("\nEnter the CSV file path to process the data > "))
                if self.__chech_csv_file(csv_file):
                    self.__product_perference_analysis(csv_file)
                else:
                    self._print("The CSV file is not found !", alignment='center', color=Fore.RED)
                    input("\nPress enter to continue....")

            elif val == 5:
                csv_file = str(self._input("\nEnter the CSV file path to process the data > "))
                if self.__chech_csv_file(csv_file):
                    self.__distribution_analysis(csv_file)
                else:
                    self._print("The CSV file is not found !", alignment='center', color=Fore.RED)
                    input("\nPress enter to continue....")

            elif val == 6:
                self.__help()

            elif val == 7:
                runner = False

            else:
                self._print("Invalid number pleacse check the number", alignment='center', color=Fore.RED)
                continue


    

if __name__ == "__main__":
    main = Main()
    main.runMainLoop()
from analysis.priceAnalysis import PriceAnalysis
from analysis.analysisOfDistribution import AnalysisOfDistribution
from analysis.monthlySalesAnalysis import MonthlySalesAnalysis
from analysis.prodectPreferenceAnalysis import ProdectPreferenceAnalysis
from analysis.weeklySalesAnalysis import WeeklySalesAnalysis

from colorama import init, Fore, Style
import sys, os, re

class InterfaceOfConsole:

    __opening_header = """
                     █████  ███    ██  █████  ██      ██    ██ ███████ ██ ███████ 
                    ██   ██ ████   ██ ██   ██ ██       ██  ██  ██      ██ ██      
                    ███████ ██ ██  ██ ███████ ██        ████   ███████ ██ ███████ 
                    ██   ██ ██  ██ ██ ██   ██ ██         ██         ██ ██      ██ 
                    ██   ██ ██   ████ ██   ██ ███████    ██    ███████ ██ ███████"""
    def __init__(self):
        init()
    
    def _print(self, text, alignment='center', width=80, color=Fore.WHITE):
        """
        Print text in a beautiful format with specified alignment and color.

        Parameters:
        text (str): The text to print.
        alignment (str): The alignment of the text ('left', 'center', 'right').
        width (int): The width of the console.
        color (colorama.Fore): The color of the text.
        """
        if alignment == 'center':
            formatted_text = text.center(width)
        elif alignment == 'left':
            formatted_text = text.ljust(width)
        elif alignment == 'right':
            formatted_text = text.rjust(width)
        else:
            raise ValueError("Alignment must be 'left', 'center', or 'right'")
        print(color + formatted_text + Style.RESET_ALL)
    
    def _opening_header(self):
        self._print(self.__opening_header, alignment='center', color=Fore.GREEN, width=100)
    
    def _monthly_analysis_menu(self):
        self._opening_header()
        text =  """
\n1. Monthly Analysis For A Branch
2. Monthly Analysis For All Branch
3. Back
        """
        self._print(" *** Monthly Sales Analysis *** ", alignment='center', color=Fore.GREEN, width=100)
        self._print(text, alignment='left')
    
    def _price_analysis_menu(self):
        self._opening_header()
        text = """
\n1. Price Analysis For A Product
2. Price Analysis For All Product
3. Back
        """
        self._print(" *** Price Analysis *** ", alignment='center', color=Fore.GREEN, width=100)
        self._print(text, alignment='left')

    def _view_analysis(self):
        self._opening_header()
        text = """
\n1. Table View
2. Graph View
3. Back
"""
        self._print(" *** Data View *** ", alignment='center', color=Fore.GREEN, width=100)
        self._print(text, alignment="left")
    
    def _main_opening_menu(self):
        self._opening_header()
        text = """
\n1. Monthly Sales Analysis
2. Price Analysis
3. Weekly Sales Analysis Of Supermarket Network
4. Product Preference Analysis
5. Analysis Of The Distribution Of Total Sales Amount Of Purchases
6. Help
7. Exit
        """
        self._print(" *** Main Menu ***", alignment='center', color=Fore.GREEN, width=100)
        self._print(text, alignment='left')

    def _input(self, text=None):
        if text == None:
            val = input("Choice > ")
        else:
            val = input(text)
        return val
    
    def _clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    def _user_to_ask(self):
        self._print("Do you want to save the results into new CSV file?", alignment='left')
        val = str(self._input("Yes (y) or No (n) > "))
        if val.lower() == 'y':
            return True
        return False
    

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
                        monthly_sales.save_analysis(path, all=True)
                    else:
                        self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                        input("\nPress enter to continue....")
        
        elif val == 2:
            if branch_name:
                monthly_sales.display_graph()
            else:
                monthly_sales.display_graph(all=True)
        
        else:
            pass

    def __price_analysis(self, csv_file, all=False):
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
                        price.save_analysis(path, all=True)
                    else:
                        self._print("The loaction is not found !", alignment='center', color=Fore.RED)
                        input("\nPress enter to continue....")
        elif val == 2:
            if product_name:
                price.display_graph()
            else:
                price.display_graph(all=True)

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
            weekly_analysis.display_graph()
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
            product_per.display_graph()
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
            distribution.display_graph()
        
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
                            self.__price_analysis(csv_file)
                        else:
                            self._print("The CSV file is not found !", alignment='center', color=Fore.RED)
                            input("\nPress enter to continue....")
                        
                    elif val == 2:
                        csv_file = str(self._input("\nEnter the CSV file path to process the data > "))
                        if self.__chech_csv_file(csv_file):
                            self.__price_analysis(csv_file, True)
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
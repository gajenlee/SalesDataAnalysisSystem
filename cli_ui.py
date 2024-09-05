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
        self._clear()
        self._opening_header()
        text = """
\n1. Table View
2. Graph View
3. Back
"""
        self._print(" *** Data View *** ", alignment='center', color=Fore.GREEN, width=100)
        self._print(text, alignment="left")
    
    def _view_graph(self):
        self._clear()
        self._opening_header()
        text = """
\n1. Data Graph View
2. Correlation Matrix Graph View
3. Back
"""
        self._print(" *** Graph View *** ", alignment='center', color=Fore.GREEN, width=100)
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

    def _userInformationCorr(self):
        self._print(
            "To calculate a meaningful correlation, you need at least two data points, and ideally many more.",
            alignment="center", color=Fore.RED)
        print("Continue... ")
        input()
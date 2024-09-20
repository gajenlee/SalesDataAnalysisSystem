from analysis.components.csv_processor import CSVProcessor

class csv_processor(CSVProcessor):

    def __init__(self, file_name):
        super().__init__(file_name)
        self.file_name = file_name
    
    def load_data(self):
        return self._load_sales_data(self.file_name)
    
    def save_data(self, file_name, data, header):
        return self._save_sales_data(file_name, data, header)

def test_load_date():
    csv = csv_processor('./sample_data/sales_data.csv')
    assert len(csv.load_data()) > 0

def test_save_data():
    csv = csv_processor('./sample_data/sales_data.csv')
    data = csv.load_data()
    header = ["branch", "product", "quantity", "amount", "date"]

    assert csv.save_data("./test_data.csv", data, header) == True

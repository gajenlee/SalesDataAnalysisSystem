import csv
import random
from datetime import datetime, timedelta

branches = [
    "Colombo", "Kandy", "Galle", "Jaffna", "Negombo", "Batticaloa", "Moratuwa",
    "Trincomalee", "Anuradhapura", "Dambulla", "Dehiwala-Mount Lavinia", "Gampaha",
    "Sri Jayewardenepura Kotte", "Badulla", "Kalutara", "Katunayake", "Matale",
    "Nuwara Eliya", "Ratnapura", "Matara", "Ampara", "Ella", "Hambantota", "Kaduwela"
]

products = ["Apples", "Oranges", "Bananas", "Milk", "Bread", "Eggs", "Chicken", "Rice", "Pasta", "Sugar"]

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def generate_sales_data(filename, num_records):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    fieldnames = ["branch", "product", "quantity", "amount", "date"]

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for _ in range(num_records):
            branch = random.choice(branches)
            product = random.choice(products)
            quantity = random.randint(1, 20)
            price_per_unit = random.uniform(10.0, 500.0)
            amount = round(quantity * price_per_unit, 2)
            date = random_date(start_date, end_date).strftime('%Y/%m/%d')
            
            writer.writerow({
                "branch": branch,
                "product": product,
                "quantity": quantity,
                "amount": amount,
                "date": date
            })

generate_sales_data("sales_data.csv", 100000)

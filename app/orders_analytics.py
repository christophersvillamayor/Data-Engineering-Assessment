import pandas as pd

class OrdersAnalytics:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.orders_df = pd.read_csv(self.csv_path)

    def calculate_profit_by_order(self):
        "Calculate profit for each order in the DataFrame"

        # return orders_df
        return

    def calculate_most_profitable_region(self):
        "Calculate the most profitable region and its profit"
    
        return

    def find_most_common_ship_method(self):
        "Find the most common shipping method for each Category"
        
        return 

    def find_number_of_order_per_category(self):
        "find the number of orders for each Category and Sub Category"

        return
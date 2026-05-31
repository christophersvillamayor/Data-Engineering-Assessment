import pandas as pd

class OrdersAnalytics:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.orders_df = pd.read_csv(self.csv_path)

    def calculate_profit_by_order(self, order: pd.Series):
        "Calculate profit for an order in the DataFrame"
        # FIXME: get expected values from series, handle missing values accordingly
        actual_price = order['List Price'] * (1 - order['Discount Percent']/100)
        profit = (actual_price - order['cost price']) * order['Quantity']
        return profit

    def calculate_most_profitable_region(self):
        "Calculate the most profitable region and its profit"

        regions: pd.arrays.StringArray = self.orders_df['Region'].unique()
        max_profit = 0
        most_profitable_region = None
        for region in regions:
            orders: pd.DataFrame = self.orders_df.loc[self.orders_df['Region'] == region]
            total_profit = 0
            for _, row in orders.iterrows():
                profit = self.calculate_profit_by_order(row)
                total_profit += profit
            if total_profit > max_profit:
                max_profit = total_profit
                most_profitable_region = region
                
        return most_profitable_region, max_profit

    def find_most_common_ship_method(self):
        "Find the most common shipping method for each Category"
        
        return 

    def find_number_of_order_per_category(self):
        "find the number of orders for each Category and Sub Category"

        return
import logging
import os

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

class OrdersAnalytics:
    def __init__(self, csv_path: str):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper()))

        self.csv_path = csv_path
        self.orders_df = pd.read_csv(self.csv_path)

    def calculate_profit_by_order(self, order: pd.Series):
        "Calculate profit for an order in the DataFrame"
        
        self.logger.info(f"Calculating profit for order id: {order['Order Id']}")

        # FIXME: handle missing values accordingly
        list_price = order['List Price']
        discount_percent = order['Discount Percent'] / 100
        cost_price = order['cost price']
        quantity =  order['Quantity']

        actual_price = list_price * (1 - discount_percent)
        profit = (actual_price - cost_price) * quantity

        self.logger.debug(f"Got the following values:")
        self.logger.debug(f"   List Price: {list_price}")
        self.logger.debug(f"   Discount Percent: {discount_percent}")
        self.logger.debug(f"   Actual Price: {actual_price}")
        self.logger.debug(f"   Cost Price: {cost_price}")
        self.logger.debug(f"   Quantity: {quantity}")
        self.logger.debug(f"   Profit: {profit}")

        return profit

    def calculate_most_profitable_region(self):
        "Calculate the most profitable region and its profit"

        self.logger.info(f"Calculating most profitable region")

        regions: pd.arrays.StringArray = self.orders_df['Region'].unique()
        max_profit = 0
        most_profitable_region = None
        for region in regions:
            self.logger.info(f"Calculating profit for region: {region}")
            
            orders: pd.DataFrame = self.orders_df.loc[self.orders_df['Region'] == region]
            total_profit = 0
            for _, row in orders.iterrows():
                profit = self.calculate_profit_by_order(row)
                total_profit += profit
            
            self.logger.debug(f"Total profit for region {region}: {total_profit}")
            if total_profit > max_profit:
                self.logger.debug(f"Previous Most Profitable Region: {most_profitable_region}, {max_profit}")
                max_profit = total_profit
                most_profitable_region = region
                self.logger.info(f"Latest Most Profitable Region: {region}, {total_profit}")
                
        return most_profitable_region, max_profit

    def find_most_common_ship_method(self):
        "Find the most common shipping method for each Category"

        mode = self.orders_df['Ship Mode'].mode()
        return mode[0]

    def find_number_of_order_per_category(self):
        "find the number of orders for each Category and Sub Category"

        return
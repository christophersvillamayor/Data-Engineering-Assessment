import logging
import os

import pandas as pd
from pandas import Series
from pandas.arrays import StringArray

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

    def calculate_profit_by_order(self, order: Series):
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

        self.logger.info("Calculating most profitable region")

        self.orders_df['Profit'] = self.orders_df.apply(self.calculate_profit_by_order, axis=1)
        most_profitable_region = (
            self.orders_df.groupby('Region', as_index=False)['Profit']
                .sum()
                .sort_values('Profit', ascending=False)
                .head(1)
        )

        return most_profitable_region

    def find_most_common_ship_method_per_category(self):
        "Find the most common shipping method for each Category"

        self.logger.info("Finding most common shipping method for each category")
        
        shipping_counts = (
            self.orders_df.groupby(['Category', 'Ship Mode'])
            .size()
            .reset_index(name='Order Count')
        )
        most_common_shipping = (
            shipping_counts.loc[
                shipping_counts.groupby('Category')['Order Count'].idxmax()
            ]
        )

        return most_common_shipping

    def find_number_of_orders_per_category(self):
        "Find the number of orders for each Category and Sub Category"

        self.logger.info("Finding number of orders by category and subcategory")

        orders_per_category = (
            self.orders_df.groupby(['Category', 'Sub Category'])
                .size()
                .reset_index(name='Order Count')
                .sort_values(['Category', 'Order Count'], ascending=[True, False])
        )

        return orders_per_category

    def get_reporting_period(self):
        "Get the reporting period from earliest order date to latest order date"
        start_date = self.orders_df["Order Date"].min().strftime("%Y-%m-%d")
        end_date = self.orders_df["Order Date"].max().strftime("%Y-%m-%d")
        return start_date, end_date

    def generate_output_csvs(self):
        start_date, end_date = self.get_reporting_period()
        reporting_period_label = f"{start_date}_to_{end_date}"
        


import logging
import os
from typing import Tuple
from pathlib import Path

import boto3
import pandas as pd
from pandas import DataFrame, Series

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

    def calculate_profit_by_order(self, order: Series) -> int:
        "Calculate profit for an order in the DataFrame"
        
        self.logger.debug(f"Calculating profit for order id: {order['Order Id']}")

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

    def calculate_most_profitable_region(self) -> DataFrame:
        "Calculate the most profitable region and its profit"

        self.logger.info("Calculating most profitable region")

        self.orders_df['Profit'] = self.orders_df.apply(self.calculate_profit_by_order, axis=1)
        profits_per_region = self.orders_df.groupby('Region', as_index=False)['Profit'].sum()

        self.logger.debug(f"Profits per region: \n{profits_per_region}")

        most_profitable_region = profits_per_region.sort_values('Profit', ascending=False).head(1)

        return most_profitable_region

    def find_most_common_ship_method_per_category(self) -> DataFrame:
        "Find the most common shipping method for each Category"

        self.logger.info("Finding most common shipping method for each category")
        
        shipping_counts = (
            self.orders_df.groupby(['Category', 'Ship Mode'])
            .size()
            .reset_index(name='Order Count')
        )

        self.logger.debug(f"Shipping method by category: \n{shipping_counts}")

        most_common_shipping = (
            shipping_counts.loc[
                shipping_counts.groupby('Category')['Order Count'].idxmax() # FIXME: There might be a tie sometimes
            ]
        )

        return most_common_shipping

    def find_number_of_orders_per_category(self) -> DataFrame:
        "Find the number of orders for each Category and Sub Category"

        self.logger.info("Finding number of orders by category and subcategory")

        orders_per_category = (
            self.orders_df.groupby(['Category', 'Sub Category'])
                .size()
                .reset_index(name='Order Count')
                .sort_values(['Category', 'Order Count'], ascending=[True, False])
        )

        self.logger.debug(f"Number of orders per category/subcategory: \n{orders_per_category}")

        return orders_per_category

    def get_reporting_period(self) -> Tuple[str, str]:
        "Get the reporting period from earliest order date to latest order date"

        start_str = self.orders_df["Order Date"].min()
        end_str = self.orders_df["Order Date"].max()

        return start_str, end_str

    def generate_output_csvs(self) -> Path:
        "Generate the output csvs"

        self.logger.info("Generating output csvs")

        s3_client = boto3.client('s3')

        start_str, end_str = self.get_reporting_period()
        reporting_period_label = f"{start_str}_to_{end_str}"
        output_folder = Path('/tmp/output/')
        output_folder.mkdir(exist_ok=True)

        self.logger.info("Gathering required csvs")

        files = [
            self.calculate_most_profitable_region(),
            self.find_most_common_ship_method_per_category(),
            self.find_number_of_orders_per_category()
        ]

        filenames = [
            f"most_profitable_region_{reporting_period_label}.csv",
            f"shipping_method_by_category_{reporting_period_label}.csv",
            f"orders_by_category_subcategory_{reporting_period_label}.csv"
        ]

        output_bucket = os.environ['OUTPUT_BUCKET']

        for df, filename in zip(files, filenames):
            local_path = output_folder / filename
            df.to_csv(local_path, index=False)

            self.logger.info(
                f"Uploading {filename} to s3://{output_bucket}/results/"
            )

            s3_client.upload_file(
                str(local_path),
                output_bucket,
                f"results/{filename}"
            )

        return filenames

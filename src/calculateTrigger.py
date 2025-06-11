#This program is using trigger price(the price from where an instrument has moved minimum 5%).
# this is calculating differene between current price and the trigger prices
# then it is finding the percentage of price different wrt to current price.
# if the percentage is between -2 to 2 percent this means the current price is near to trigger price and i can aspect a 5% move again.
# this need to run daily after fundamentallyStrongStock.csv file is created in result folder
import pandas as pd
import os

fundamental_instruments_file = "/Users/rohitkumar/Trades/NSE/BhavCopy/result/fundamentallyStrongStocks.csv"
source_directory = "/Users/rohitkumar/Trades/NSE/BhavCopy/triggerPrice/priceMovementLevel"

count = 0

def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Exception occurred {e}")
        return None

for file in os.listdir(source_directory):
    if file.endswith(".csv"):
        file_path = os.path.join(source_directory, file)
        df = read_csv_file(file_path)
        trigger_prices = []
        symbol = ''
        for index, row in df.iterrows():
            trigger_prices.append(row["PrvsClsgPric"])
            symbol = row["TckrSymb"]

        df_fundamental = read_csv_file(fundamental_instruments_file)
        for i, rowf in df_fundamental.iterrows():
            if(rowf["Symbol"] == symbol):
                current_price = rowf["Day0CLosePrice"]
                for trigger_price in trigger_prices:
                    price_difference = current_price - trigger_price
                    trigger_percentage_difference = (price_difference/current_price)*100
                    if(trigger_percentage_difference<=2 and trigger_percentage_difference>=-2):
                        count = count + 1
                        print(f"Symbol {symbol} is at trigger level with trigger percentage difference of less than 2, current_price {current_price}, trigger_price {trigger_price}")

print(f"Total count of valid instruments {count}")
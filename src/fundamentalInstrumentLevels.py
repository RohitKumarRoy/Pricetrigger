# this program will filter all the instruments that has good fundamentals and price change percentage
# on daily basis is more than 5%
# run daily before calculateTrigger.py,
# delete all the files inside destination directory before running this program
# this need to run after CalculatePriceChange.py
import pandas as pd
import os

source_directory = "/Users/rohitkumar/Trades/NSE/BhavCopy/triggerPrice/Instruments"
destination_directory = "/Users/rohitkumar/Trades/NSE/BhavCopy/triggerPrice/priceMovementLevel"
fundamental_instruments_file = "/Users/rohitkumar/Trades/NSE/BhavCopy/result/fundamentallyStrongStocks.csv"

count = 0
match_count = 0

def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Exception occurred {e}")
        return None

def check_fundamental_instrunment(df):
    fundamental_df = pd.read_csv(fundamental_instruments_file)
    symbol_list = []
    for index, row in fundamental_df.iterrows():
        symbol_list.append(row["Symbol"])
    if(symbol_list.__contains__(df["TckrSymb"][0])):
        return True


# read all the csv files from source directory
for file in os.listdir(source_directory):
    if file.endswith(".csv"):
        count = count + 1
        file_path = os.path.join(source_directory, file)
        df = read_csv_file(file_path)
        if (check_fundamental_instrunment(df)):
            match_count = match_count + 1
            filtered_df = df[df["priceChangePercentage"] >= 5]
            destination_file_path = os.path.join(destination_directory, file)
            filtered_df.to_csv(destination_file_path, mode="w", header=True, index=False)


print(f"total number of files processed {count} and total fundamentally strong instruments {match_count}")
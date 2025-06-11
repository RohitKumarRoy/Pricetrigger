# this program will calculate the price variation on daily basis and the percentage of price change
# on daily basis for all the instruments present in NSE
# run once in a month
import pandas as pd
import os

source_directory = "/Users/rohitkumar/Trades/NSE/BhavCopy/OutDir"
destination_directory = "/Users/rohitkumar/Trades/NSE/BhavCopy/triggerPrice/Instruments"

# create an empty data frame
data_frames = []
count = 0

def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Exception occurred {e}")
        return None

def calculate_PriceChange_For_A_Day(df):
    df["dailyPriceChange"] = df.apply(lambda row: row["ClsPric"] - row["PrvsClsgPric"], axis=1)
    df["priceChangePercentage"] = df.apply(lambda row: ((row["ClsPric"] - row["PrvsClsgPric"]) * 100) / row["PrvsClsgPric"], axis=1)
    return df



def extract_columns(df, columns):
    try:
        selected_data = df[columns]
        return selected_data
    except KeyError:
        return df

def create_csv_for_each_df(df_list):
    for i, df in enumerate(df_list):
        fileName = os.path.join(destination_directory, f"{df["ISIN"][0]}.csv")
        if os.path.exists(fileName):
            df.to_csv(fileName, mode="a", header=False, index=False)
        else:
            df.to_csv(fileName, mode="w", header=True, index=False)



# read all the csv files from source directory
for file in os.listdir(source_directory):
    if file.endswith(".csv"):
        columns_to_extract = ["FinInstrmNm","TckrSymb","BizDt","ISIN","OpnPric","HghPric","LwPric","ClsPric","LastPric","PrvsClsgPric","TtlTradgVol","dailyPriceChange","priceChangePercentage"]
        count = count + 1
        file_path = os.path.join(source_directory, file)
        print(f"file path is {file_path}.")
        df = read_csv_file(file_path)
        df = calculate_PriceChange_For_A_Day(df)

        if df is not None:
            df_filtered = extract_columns(df, columns_to_extract)

        data_frames.append(df_filtered)

create_csv_for_each_df(data_frames)

print(f"total number of files analysed {count}")


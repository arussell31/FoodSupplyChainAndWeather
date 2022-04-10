import string
from pathlib import Path
from csv import reader
import numpy as np
import pandas as pd
import os
import glob


def load_data_from_folder(file_path: string, header_row: int):
    '''takes in path to folder where data is stored and the header row.
    yields dataframes from those csv files'''
    full_path = os.path.join(file_path, "*.csv")
    csv_files = glob.glob(full_path)
    for f in csv_files:
        yield pd.read_csv(f, header=header_row)

def load_weather_data_from_file(file_path: string, df_columns: list(), prefix=""):
    '''takes in path to folder where data is stored and the header row.
    yields dataframes from those csv files'''
    full_path = os.path.join(file_path, f"{prefix}*.csv")
    csv_files = glob.glob(full_path)
    for f in csv_files:
        country = ""
        try:
            with open(f, newline='') as data_file:
                csv_reader = reader(data_file, delimiter=',')
                prev_row = list()
                values = []
                for i, row in enumerate(csv_reader):
                    if i == 1:
                        country = row[1].strip()
                    if i == 3:
                        prev_row = row[1:]
                    if i > 3:
                        to_append = [row[0]]
                        to_append.extend(prev_row)
                        to_append.extend(row[1:])
                        values.append(to_append)
                        prev_row = row[1:]
                df = pd.DataFrame(values, columns=df_columns)
                df["Country"] = country
                yield df

        except FileNotFoundError as e:
            raise e

def process_temperature_data():
    '''processes temperature data'''
    avg_path = "./data/temp_data/"
    max_path = "./data/temp_data/"
    min_path = "./data/temp_data/"

    # loop over the list of csv files
    avg_cols = list(["Year",
                    "avg_temp_0","avg_temp_1","avg_temp_2","avg_temp_3",
                    "avg_temp_4","avg_temp_5","avg_temp_6","avg_temp_7",
                    "avg_temp_8","avg_temp_9","avg_temp_10","avg_temp_11",
                    "avg_temp_12","avg_temp_13","avg_temp_14","avg_temp_15",
                    "avg_temp_16","avg_temp_17","avg_temp_18","avg_temp_19",
                    "avg_temp_20","avg_temp_21","avg_temp_22","avg_temp_23"
                    ])
    df_avg_list = list(load_weather_data_from_file(avg_path, avg_cols, "tas_"))
    avg_temp_data = pd.DataFrame()
    for df in df_avg_list:
        avg_temp_data = pd.concat([avg_temp_data, df], ignore_index=True)

    max_cols = list(["Year",
                    "max_temp_0","max_temp_1","max_temp_2","max_temp_3",
                    "max_temp_4","max_temp_5","max_temp_6","max_temp_7",
                    "max_temp_8","max_temp_9","max_temp_10","max_temp_11",
                    "max_temp_12","max_temp_13","max_temp_14","max_temp_15",
                    "max_temp_16","max_temp_17","max_temp_18","max_temp_19",
                    "max_temp_20","max_temp_21","max_temp_22","max_temp_23"
                    ])
    df_max_list = list(load_weather_data_from_file(max_path, max_cols, "tasmax_"))
    max_temp_data = pd.DataFrame()
    for df in df_max_list:
        max_temp_data = pd.concat([max_temp_data, df], ignore_index=True)

    min_cols = list(["Year",
                    "min_temp_0","min_temp_1","min_temp_2","min_temp_3",
                    "min_temp_4","min_temp_5","min_temp_6","min_temp_7",
                    "min_temp_8","min_temp_9","min_temp_10","min_temp_11",
                    "min_temp_12","min_temp_13","min_temp_14","min_temp_15",
                    "min_temp_16","min_temp_17","min_temp_18","min_temp_19",
                    "min_temp_20","min_temp_21","min_temp_22","min_temp_23"
                    ])
    df_min_list = list(load_weather_data_from_file(min_path, min_cols, "tasmin_"))
    min_temp_data = pd.DataFrame()
    for df in df_min_list:
        min_temp_data = pd.concat([min_temp_data, df], ignore_index=True)

    min_max_df = pd.merge(min_temp_data, max_temp_data, on=["Year", "Country"], how='outer')
    temp_df = pd.merge(min_max_df, avg_temp_data, on=["Year", "Country"], how='outer')
    return temp_df

def process_precipitation_data():
    '''processes precipitation data'''
    path = "./data/rainfall_data/"

    # loop over the list of csv files
    precip_cols = list(["Year",
                    "precip_0","precip_1","precip_2","precip_3",
                    "precip_4","precip_5","precip_6","precip_7",
                    "precip_8","precip_9","precip_10","precip_11",
                    "precip_12","precip_13","precip_14","precip_15",
                    "precip_16","precip_17","precip_18","precip_19",
                    "precip_20","precip_21","precip_22","precip_23"
                    ])
    df_list = list(load_weather_data_from_file(path, precip_cols))
    precip_data = pd.DataFrame()
    for df in df_list:
        df.rename(columns={'Val': 'Precipitation'}, inplace=True)
        precip_data = pd.concat([precip_data, df], ignore_index=True)
    return precip_data

def process_crop_yield_data():
    '''processes crop yield data'''
    # crop name can be extracted from header col 4 or the file name
    path = "./data/crop_yield/"

    # loop over the list of csv files
    df_list = list(load_data_from_folder(path, 0))
    crop_data = pd.DataFrame(columns=["Country", "Year", "Yield", "Crop"])
    # keep cols 1,3,4 and add the crop name extracted from col 4 name.
    for df in df_list:
        crop_name = df.columns[3].split(" - ")[1]
        df = df.drop(columns=['Code'])
        df.rename(columns={'Entity': 'Country',
                  df.columns[2]: 'Yield'}, inplace=True)
        df["Crop"] = crop_name
        crop_data = pd.concat([crop_data, df], ignore_index=True)
    return crop_data

def process_agricultural_land_percentage_data():
    return

def process_disaster_data():
    # the file format is xlsx (i did get it converted to csv so will try this first)
    # header row is on row 7
    return

def process_grow_season_data():
    # first header col value is empty and is unnecessary as it just represents an index
    return

def create_dataframe():
    precip_df = process_precipitation_data()
    temp_df = process_temperature_data()
    crop_yield_df = process_crop_yield_data()
    weather_df = pd.merge(precip_df, temp_df, on=["Year", "Country"], how='outer')
    final_df = pd.merge(crop_yield_df, weather_df, on=["Year", "Country"], how='left')
    print(final_df)
    weather_filepath = Path('weather_out.csv')
    crop_filepath = Path('crop_out.csv')
    final_filepath = Path('final_out.csv')
    #weather_df.to_csv(weather_filepath)  
    #crop_yield_df.to_csv(crop_filepath)  
    final_df.to_csv(final_filepath)  
    return final_df

def main():
    create_dataframe()

if __name__ == "__main__":
    main()

from calendar import month
import string
from pathlib import Path
from csv import reader
import this
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
                        year = int(row[0].strip())
                        if year < 1960:
                            continue
                        to_append = [year]
                        to_append.extend(prev_row)
                        to_append.extend(row[1:])
                        values.append(to_append)
                        prev_row = row[1:]
                df = pd.DataFrame(values, columns=df_columns)
                df["Country"] = country
                yield df

        except FileNotFoundError as e:
            raise e

def load_disaster_data_from_file(file_path: string, df_columns: list()):
    '''takes in path to folder where data is stored and the header row.
    yields dataframes from those csv files'''
    full_path = os.path.join(file_path, "*.csv")
    csv_files = glob.glob(full_path)
    for f in csv_files:
        try:
            with open(f, newline='', encoding="utf8") as data_file:
                csv_reader = reader(data_file, delimiter=',')
                prev_row = list()
                values = []
                for i, row in enumerate(csv_reader):
                    if i >= 7:
                        country = row[10].strip()
                        year = int(row[1].strip())
                        if year < 1960:
                            continue
                        flood = [False] * 24
                        drought = [False] * 24
                        disaster = [False] * 24
                        total_ppl_affected = 0
                        to_append = [country, year]
                        to_append.extend(flood)
                        to_append.extend(drought)
                        to_append.extend(disaster)
                        to_append.append(total_ppl_affected)
                        flood_start_index = 2
                        drought_start_index = 26
                        disaster_start_index = 50
                        # if col 6, 7, 16, 17 contains disasters or if col 18 contains Yes
                        # check 28, 29 for start year and start month
                        # check 31, 32 for end year and end month
                        # check 34, 38 for total ppl affected
                        significant_events = \
                            ["flood", "drought", "tsunami", "famine", "food shortage",
                            "crop failure", "water shortage"]
                        event_list =[row[6], row[7], row[16], row[17]]
                        is_flood = False
                        is_drought = False
                        is_other = False
                        for events in event_list:
                            if any(x in events.lower() for x in significant_events) or \
                                ("yes" in row[18].lower()):
                                if "flood" in events.lower():
                                    is_flood = True
                                    break
                                elif "drought" in events.lower():
                                    is_drought = True
                                    break
                                else:
                                    is_other = True
                                    break
                        if is_flood or is_drought or is_other:
                            start_year = int(row[28])
                            start_month = (1 if row[29] == '' else int(row[29]))
                            end_year = int(row[31])
                            end_month = (12 if row[32] == '' else int(row[32]))
                            num_years = 1 + (end_year - start_year)
                            total_death = (0 if row[34] == '' else int(row[34]))
                            others_affected = (0 if row[38] == '' else int(row[38]))
                            total_ppl_affected =  total_death + others_affected
                            to_append[len(to_append) - 1] = total_ppl_affected

                            type_offset = 2
                            if is_flood:
                                type_offset = flood_start_index
                            if is_drought:
                                type_offset = drought_start_index
                            if is_other:
                                type_offset = disaster_start_index
                            j = 0
                            multiple_years = []
                            while j < num_years + 1:
                                multiple_years.append(to_append.copy())
                                j += 1
                            prev_year = [False] * 12
                            num_months = ((num_years-1) * 12) + (end_month - start_month + 1)
                            if (num_months <= 0):
                                continue
                            index = 0
                            current_month = start_month - 1
                            while index < len(multiple_years):
                                this_year = [False] * 12
                                multiple_years[index][1] = multiple_years[index][1] + index
                                if index < len(multiple_years) - 1:
                                    while current_month < (start_month + num_months - 1):
                                        mod_current_month = current_month%12
                                        if (mod_current_month != 0 or current_month == 0 or index == current_month/12):
                                            this_year[mod_current_month] = True
                                            current_month += 1
                                        else:
                                            two_year_data = prev_year.copy()
                                            two_year_data.extend(this_year)
                                            for x in range(len(two_year_data)):
                                                multiple_years[index][type_offset + x] = two_year_data[x]
                                            prev_year = this_year.copy()
                                            index += 1
                                            break
                                    if current_month == (start_month + num_months - 1):
                                        two_year_data = prev_year.copy()
                                        two_year_data.extend(this_year)
                                        for x in range(len(two_year_data)):
                                            multiple_years[index][type_offset + x] = two_year_data[x]
                                        prev_year = this_year.copy()
                                        index += 1

                                elif index == len(multiple_years) -1:
                                    two_year_data = prev_year.copy()
                                    two_year_data.extend(this_year.copy())
                                    for x in range(len(two_year_data)):
                                        multiple_years[index][type_offset + x] = two_year_data[x]
                                    # set the data from previous year
                                    # set the data from this year
                                    # no processing needed
                                    index += 1
                            values.extend(multiple_years)
                df = pd.DataFrame(values, columns=df_columns)
                return df

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
        df = df.reset_index()  # make sure indexes pair with number of rows
        for index, row in df.iterrows():
            row['Country'] = row['Country'].strip()
        crop_data = pd.concat([crop_data, df], ignore_index=True)
    return crop_data

def process_agricultural_land_percentage_data():
    '''processes agricultural data'''
    return

def process_disaster_data():
    '''processes disaster data'''
    path = "./data/disaster_data/"

    # the file format is xlsx (i did get it converted to csv so will try this first)
    # header row is on row 7

    disaster_cols = list(["Country", "Year",
                    "flood_0","flood_1","flood_2","flood_3",
                    "flood_4","flood_5","flood_6","flood_7",
                    "flood_8","flood_9","flood_10","flood_11",
                    "flood_12","flood_13","flood_14","flood_15",
                    "flood_16","flood_17","flood_18","flood_19",
                    "flood_20","flood_21","flood_22","flood_23",
                    "drought_0","drought_1","drought_2","drought_3",
                    "drought_4","drought_5","drought_6","drought_7",
                    "drought_8","drought_9","drought_10","drought_11",
                    "drought_12","drought_13","drought_14","drought_15",
                    "drought_16","drought_17","drought_18","drought_19",
                    "drought_20","drought_21","drought_22","drought_23",
                    "disaster_0","disaster_1","disaster_2","disaster_3",
                    "disaster_4","disaster_5","disaster_6","disaster_7",
                    "disaster_8","disaster_9","disaster_10","disaster_11",
                    "disaster_12","disaster_13","disaster_14","disaster_15",
                    "disaster_16","disaster_17","disaster_18","disaster_19",
                    "disaster_20","disaster_21","disaster_22","disaster_23",
                    "total_ppl_affected"
                    ])
    
    disaster_data = load_disaster_data_from_file(path, disaster_cols)
    return disaster_data

def process_grow_season_data():
    # first header col value is empty and is unnecessary as it just represents an index
    return

def create_dataframe():
    precip_df = process_precipitation_data()
    temp_df = process_temperature_data()
    crop_yield_df = process_crop_yield_data()
    disaster_df = process_disaster_data()
    weather_df = pd.merge(precip_df, temp_df, on=["Year", "Country"], how='outer')
    weather_and_crop_df = pd.merge(crop_yield_df, weather_df, on=["Year", "Country"], how='inner')
    final_df = pd.merge(weather_and_crop_df, disaster_df, on=["Year", "Country"], how='left')
    final_df = final_df.drop(columns=["index"])
    # final_filepath = Path('final_out.csv')
    # final_df.to_csv(final_filepath)  

    countries_list = final_df.Country.unique()
    crop_list = final_df.Crop.unique()
    print(countries_list)
    print(crop_list)
    df_list = []
    for country in countries_list:
        country_df = final_df[final_df['Country'] == country]
        for crop in crop_list:
            country_crop_df = country_df[country_df['Crop'] == crop]
            df_list.append(country_crop_df)
            final_filepath = Path(f"output/{country}-{crop}-final_out.csv")
            final_df.to_csv(final_filepath)
    return df_list

def main():
    create_dataframe()
    #process_disaster_data()

if __name__ == "__main__":
    main()

import polars as pl
import pandas as pd
import os 

dataraw_folder = 'data/raw/'
listof_files = os.listdir(dataraw_folder)

## create a list of just files from 2020
listof_files_2020 = [file for file in listof_files if '2020' in file]

## create a list of just files from 2021
listof_files_2021 = [file for file in listof_files if '2021' in file]

## function
def clean_excel(file, year):
    print(f'Cleaning {file}...')
    df = pl.read_excel(dataraw_folder + file, sheet_name=f'{year} Data')
    print(df.head())
    df.write_csv('data/processed/' + file.replace('xlsx', 'csv'))
    print(f'Cleaning {file} complete!')

## loop through 2020 files
for file in listof_files_2020:
    print(file)
    clean_excel(file, 2020)
    print('---')

## loop through 2021 files
for file in listof_files_2021:
    print(file)
    clean_excel(file, 2021)
    print('---')
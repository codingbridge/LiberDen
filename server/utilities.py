# pylint: disable=missing-docstring
import pandas as pd
import csv
import configparser

def read_excel_file_into_dict(file_name):
    excel = pd.read_excel(file_name, encoding='utf-8-sig')
    data = {}
    for header in excel.columns:
        for i in excel.index:
            str_value = str(excel[header][i]).strip()
            if str_value == 'nan':
                str_value = ''
            try:
                data[header].append(str_value)
            except KeyError:
                data[header] = [str_value]
    return data

def read_csv_file_into_dict(file_name):
    with open(file_name, encoding='utf-8-sig') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        data = {}
        header = []
        row_count = 0
        for row in csv_data:
            row_count += 1
            for i in row.count:
                str_value = str(row[i]).strip()
                if row_count == 1:
                    header.append(str_value)
                else:
                    try:
                        data[header[i]].append(str_value)
                    except KeyError:
                        data[header[i]] = [str_value]
    return data

def read_config_ini_into_dict(file_name):
    config = configparser.ConfigParser()
    config.read(file_name, encoding='utf-8-sig')
    data = {}
    for section in config:
        for item in section:
            data[f'{section}-{item}'] = item
    return data

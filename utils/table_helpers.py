from pandas.plotting import table
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def cast_seconds(v):
    list_ = v.split(':')
    hours, minutes, seconds = int(list_[0]), int(list_[1]), int(list_[2])
    return hours * 60 * 60 + minutes * 60 + seconds


def read_plot_table(path):
    df = pd.read_csv(path, index_col=False, error_bad_lines=False)
    column_name = df.columns[0]
    columns = ['VarName', 'TimeString', 'VarValue', 'Validity', 'Time_ms']
    df = df[column_name].str.split(';', expand=True)
    df.columns = columns
    df = df.iloc[:-1, :]
    df['time'] = df.TimeString.str.split(' ', expand=True).iloc[:, 1].apply(lambda x: x.replace('"', ''))
    df.time = df.time.apply(lambda x: cast_seconds(x))
    idx = []
    min_ = 0
    for i in df.time.index:
        if df.time.loc[i] >= min_:
            idx.append(i)
            min_ = df.time.loc[i]

    df = df.loc[idx]
    return df.time.values, df.VarValue.values.astype('float')


def read_customer_data(path):
    df = pd.read_csv(path, sep=';')
    df.columns = [col.strip() for col in df.columns]
    columns = ['Client', 'Order', 'N_serial', 'Dim1', 'Dim2']
    return df[columns].replace(np.nan, 0), df.Note.values[0]


def save_table_image(df, path):
    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(0)
    ax.yaxis.set_visible(0)
    table(ax, df, loc='upper center')
    plt.savefig(path)


def table_to_string(df):
    s = ''
    for c in df.columns:
        s += c
        s += ': '
        s += str(df[c].values[0])
        s += ' ' * 5
    return s


def step_data_reader(path):
    df = pd.read_csv(path, usecols=[0], skiprows=0)
    df.rename(columns={'List separator=;Decimal symbol=':
                           'split_'},
              inplace=True)
    df = df.split_.str.split(';', expand=True)
    df.rename(columns={0: 'name',
                       1: 'step'},
              inplace=True)
    return df


def cast_order(data, order):
    col_names = [x.split('_')[3:] for x in data.columns]
    data.columns = ['_'.join(name) for name in col_names]
    return data[order]


def aggregate_step_data(data, keys, order):
    table = pd.DataFrame()
    for key in keys:
        step = data.loc[data.name.apply(lambda x: key in x)]
        step = step.set_index('name').T
        step = cast_order(step, order)
        step.index = [key]

        table = pd.concat([table, step], axis=0)

    table.amp = table.amp.astype('float')
    table.temp_lav = table.temp_lav.astype('float')

    table.amp = table.amp / 10

    table.temp_lav = table.temp_lav / 10

    table.amp = table.amp.astype('str')
    table.temp_lav = table.temp_lav.astype('str')
    print(table.temp_lav.values)
    print(table.amp.values)

    table.mod_crom = table.mod_crom.apply(lambda x: 'crome' if x == 0 else 'etching')
    matches = {'0': 'Start from previous',
               '1': 'Start from max',
               '2': 'Start from min'}

    table.replace({'start_da': matches}, inplace=True)

    table.volt = table.volt.astype('float') / 10
    table.volt = table.volt.astype('str')
    return table

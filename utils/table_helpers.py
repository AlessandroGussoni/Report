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
    columns = ['VarName', 'TimeString', 'VarValue', 'Validity', 'Time_ms']
    df = df[columns]
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
    return df[columns].replace(np.nan, 0)


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
    return table

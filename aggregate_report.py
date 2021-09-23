import warnings
from datetime import datetime

import os

from pdf_extension import PDF

from utils.plot_helpers import save_plot
from utils.table_helpers import read_plot_table, table_to_string, read_customer_data
from utils.table_helpers import step_data_reader, aggregate_step_data
from utils.file_helpers import create_temporary_cache, clean_files

warnings.filterwarnings('ignore')

width = 210
height = 297

report = PDF()
today = str(datetime.today())

main_path = r'C:\Logs2'

data_path = create_temporary_cache(main_path)


def load_arrays():
    temp = os.path.join(main_path, 'Grafico_temperatura0.csv')
    tens = os.path.join(main_path, 'Grafico_tensione0.csv')
    corr = os.path.join(main_path, 'Grafico_corrente0.csv')

    x, temperatura = read_plot_table(temp)
    x, tensione = read_plot_table(tens)
    x, corrente = read_plot_table(corr)
    return x, tensione, corrente, temperatura


def create_title(day, pdf):
    # Unicode is not yet supported in the py3k version; use windows-1252 standard font
    pdf.set_font('Arial', '', 24)
    pdf.write(5, f"Process Report")
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'{day}')
    pdf.ln(5)
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)


def create_report(dday, pdf, folder):
    pdf.add_page()
    # Title
    create_title(dday, pdf)
    # Plot
    x, tensione, corrente, temperatura = load_arrays()
    image_path = r'' + folder + r'\plot.jpg'
    print(image_path)
    save_plot(x, tensione, corrente, temperatura, image_path)
    pdf.image(r'' + image_path, 0, 140, width - 10)
    # Customer data
    customer_path = os.path.join(main_path, 'Dati_cliente.csv')
    customer_data = read_customer_data(customer_path)
    string = table_to_string(customer_data)
    pdf.set_font('Arial', 'B', 16)
    # Move to 8 cm to the right
    pdf.cell(90, 80)
    # Centered text in a framed 20*10 mm cell and line break
    pdf.cell(20, 10, string, 0, 1, 'C')
    pdf.line(10, 50, 200, 50)

    step_path = os.path.join(main_path, 'ricetta.csv')
    step_df = step_data_reader(step_path)
    keys = ['P' + str(i) for i in range(1, 7)]
    order = ['volt', 'amp', 'mod_crom', 'start_da', 'lati',
             'n_flash', 'min_lav', 'sec_lav', 'temp_lav']
    table = aggregate_step_data(step_df, keys, order)
    cols = [['step'] + table.columns.tolist()]
    data = table.reset_index().values.tolist()
    ftable = cols + data
    pdf.create_table(table_data=ftable, cell_width=20, align_data='C', align_header='C',
                     x_start=5)

    pdf.output(os.path.join(main_path, 'report.pdf'), 'F')


create_report(today, report, data_path)
clean_files(main_path)

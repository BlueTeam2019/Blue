import os

import pandas


def generate_query_from_excel(file):
    """
    Receives an excel file, parses its content into a SQL query, then saves the file to ../in folder

    file: Excel file
    return: SQL VALUES query
    """
    data = pandas.read_excel(file)
    product, rate, scope = list(data.columns)
    query_values = []

    # Iterate over the file contents and build SQL VALUES query
    for idx, row in data.iterrows():
        query_values.append(f"('{row[product]}','{row[rate]}','{row[scope]}')")

    # Save and overwrite the new excel file
    path = '~/app/in/rates.xlsx' if os.environ.get("DEBUG", False) else '/app/in/rates.xlsx'
    data.to_excel(path, "rates", index=False)

    # Return properly formatted query
    return ',\n'.join(query_values) + ';'

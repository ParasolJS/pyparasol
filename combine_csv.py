from csv import reader
from pandas import DataFrame
from pandas import concat


# this function gets a list of all lists of headers from each csv file inputted
# returns a list of each list of headers from each csv file inputted
def get_header_list(csv_name_list):
    csv_header_list = []
    for csv_file_name in csv_name_list:
        temp_header_list = []
        with open(csv_file_name, 'r', newline='') as current_csv_file:
            header_line = current_csv_file.readline()
            for header in header_line.split(','):
                header = header.rstrip()
                temp_header_list.append(header)
            current_csv_file.close()
            csv_header_list.append(temp_header_list)

    return csv_header_list


# this function combines as many csv as are inputted and returns the data headers of each csv
# it outputs the csv header list in the order that the csv file names were given
def combine_csv(csv_name_list, output_csv_name):
    # creating header list for return statement
    # creates list of header lists in order of csv_name_list
    csv_header_list = get_header_list(csv_name_list)

    # adding the csv data into arrays
    # csv data master is a list of all the 2d arrays of data from each individual csv file
    # row_data keeps track of the number of rows that are in each csv file
    row_data = []
    csv_data_master = []
    for csv_file_name in csv_name_list:
        current_row_number = 0
        current_data = []
        csv_file_open = open(csv_file_name)
        current_csv_file = reader(csv_file_open)
        for row in current_csv_file:
            current_data.append(row)
            current_row_number += 1
        csv_data_master.append(current_data)
        row_data.append(current_row_number)

    csv_data_master_pandas = []
    for data in csv_data_master:
        new_dataframe = DataFrame(data)
        csv_data_master_pandas.append(new_dataframe)
    # opening new output file
    output_file = open(output_csv_name, 'w', newline='')
    # adding all data next to eachother and adding to output csv file
    data_final = concat(csv_data_master_pandas, axis=1)
    print()
    output_file.write(data_final.to_csv(index=False, index_label=False))
    output_file.close()

    # removing first line from file that was just created
    with open(output_csv_name, 'r') as file_in:
        data = file_in.read().splitlines(True)
    with open(output_csv_name, 'w') as file_out:
        file_out.writelines(data[1:])
    return csv_header_list


# print(combine_csv(['data/cars.csv', 'data/people.csv', 'data/computers.csv'], 'output.csv'))

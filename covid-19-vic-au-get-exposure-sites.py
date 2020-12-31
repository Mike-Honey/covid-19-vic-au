import datetime
import numpy
import os
import pandas
import requests


def processWebPage(webpageURL, datadir, filename, table_instance, check_diff):

    html_page_df = pandas.read_html(webpageURL)
    html_table_df = html_page_df[table_instance]
    print ( html_table_df )

    # strip unicode characters
    html_table_cols = html_table_df.select_dtypes(include=[numpy.object]).columns.tolist()
    html_table_df[html_table_cols] = html_table_df[html_table_cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))
    html_table_df = html_table_df.sort_values(by=html_table_cols)

    if check_diff:
        input_xlsx_df = pandas.read_excel(datadir + filename)
        # print ( input_xlsx_df )

        diff_df = pandas.merge(input_xlsx_df, html_table_df, how='outer', indicator='Exist')

        diff_df = diff_df.loc[diff_df['Exist'] != 'both']
        diff_df['Exist'] = diff_df['Exist'].replace('left_only', 'old')
        diff_df['Exist'] = diff_df['Exist'].replace('right_only', 'new')
        diff_df = diff_df.sort_values(by=diff_df.columns.tolist())
        diff_file_name = datadir + str.replace(filename, '.xlsx', '_diff.xlsx')
        if len(diff_df.index) > 0:
            print(str(datetime.datetime.now()) + ' Differences found, wrote to file: ' + diff_file_name )
            diff_df.to_excel (diff_file_name, index=False)

    # write current data to excel file for next comparison run, also to timestamped file.
    html_table_df.to_excel (datadir + filename, index=False)
    html_table_df.to_excel (datadir + 'archive/' + str.replace(filename, '.xlsx', '_' + datetime.datetime.now().strftime('%y-%m-%d_%H_%M_%S') + '.xlsx'), index=False)


def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    webpageURL = 'https://www.dhhs.vic.gov.au/case-locations-and-outbreaks'
    datadir = 'C:/Dev/covid-19-vic-au/'
    filename = 'case-locations-and-outbreaks_case-alerts--public-exposure-sites.xlsx'
    table_instance = 0
    check_diff = True

    processWebPage(webpageURL, datadir, filename, table_instance, check_diff)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()

import datetime
import numpy
import os
import pandas
import requests


def processWebPage(webpageURL, datadir, filename):

    html_page_df = pandas.read_html(webpageURL)
    html_table0_df = html_page_df[0]
    # print ( html_table0_df )

    # strip unicode characters
    html_table0_cols = html_table0_df.select_dtypes(include=[numpy.object]).columns
    html_table0_df[html_table0_cols] = html_table0_df[html_table0_cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    input_xlsx_df = pandas.read_excel(datadir + filename)
    # print ( input_xlsx_df )

    diff_df = pandas.merge(input_xlsx_df, html_table0_df, how='outer', indicator='Exist')

    diff_df = diff_df.loc[diff_df['Exist'] != 'both']
    print(diff_df.values)

    # assert_frame_equal(input_xlsx_df, html_table0_df, check_index_type=False)
    # print ( input_xlsx_df.compare(html_table0_df) )

    html_table0_df.to_excel (datadir + filename, index=False)

    return diff_df

def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    webpageURL = 'https://www.dhhs.vic.gov.au/case-locations-and-outbreaks'
    datadir = 'C:/Dev/covid-19-vic-au/'
    filename = 'case-locations-and-outbreaks#case-alerts--public-exposure-sites.xlsx'

    dataset = processWebPage(webpageURL, datadir, filename)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()

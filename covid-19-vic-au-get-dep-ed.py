import datetime
from io import StringIO
import os
import pandas
import requests
from bs4 import BeautifulSoup


def processWebPage(webpageURL, datadir):

    html_page = requests.get(webpageURL).text
    html_page = str.replace(str.replace(html_page , '&nbsp;' , ' '), '\n', ' ' )
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output_text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist and str.strip(t) > '':
            if t.parent.name == 'li':
                output_text += '\nli: {}\n'.format(str.strip(t))
            else:
                output_text += '{}'.format(str.strip(t))
            
    print(output_text)

    output_IO = StringIO(output_text)
    output_DF = pandas.read_csv(output_IO, sep='\|\|')
    print (output_DF)
    output_DF.to_excel (datadir + "Dep Ed Closures.xlsx", index=False)

def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    webpageURL = 'https://www.education.vic.gov.au/about/programs/health/pages/closures.aspx'
    datadir = 'C:/Dev/covid-19-vic-au/'

    processWebPage(webpageURL, datadir)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()

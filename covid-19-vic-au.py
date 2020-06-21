from area import area
import datetime
import geopandas
import os
import pandas
import subprocess
import zipfile
    
def processXlsx(dataurl, datadir):

    input_LGA_VIC_GDF = geopandas.read_file (dataurl + "LGA_2020_VIC.geojson")
    input_VIC_AU_Sites_DF = pandas.read_excel (dataurl + "Coronavirus%20COVID-19%20-%20VIC%20AU%20Exposure%20sites.xlsx")
    input_VIC_AU_Sites_GDF = geopandas.GeoDataFrame( input_VIC_AU_Sites_DF , 
        geometry=geopandas.points_from_xy(input_VIC_AU_Sites_DF.Longitude, input_VIC_AU_Sites_DF.Latitude))
    # derive a new geodata frame with the intersection of Basins and LGA shapes (constrained by Basins).
    output_VIC_AU_Sites_GDF = geopandas.sjoin( input_VIC_AU_Sites_GDF , input_LGA_VIC_GDF , how="left", op='intersects' )
    output_VIC_AU_Sites_DF = output_VIC_AU_Sites_GDF[output_VIC_AU_Sites_GDF.columns.intersection(['Location for Geocoding', 'Latitude', 'Longitude', 'LGA_NAME20'])]
    output_VIC_AU_Sites_DF.drop_duplicates()
    print(output_VIC_AU_Sites_DF)
    output_VIC_AU_Sites_DF.to_excel (datadir + "Coronavirus COVID-19 - VIC AU Exposure sites LGA.xlsx", index=False)

def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    dataurl = 'https://github.com/Mike-Honey/covid-19-vic-au/raw/master/'
    datadir = 'C:/Dev/covid-19-vic-au/'

    processXlsx(dataurl, datadir)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()

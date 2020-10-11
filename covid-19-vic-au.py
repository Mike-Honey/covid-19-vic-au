from area import area
import datetime
import geopandas
import os
import pandas
import subprocess
import zipfile

from shapely.geometry import Point, MultiPoint
from sklearn.neighbors import BallTree


def processXlsx(datadir):

    input_LGA_VIC_GDF = geopandas.read_file (datadir + "LGA_2020_VIC.geojson")
    
    input_VIC_AU_Sites_DF = pandas.read_excel (datadir + "Coronavirus COVID-19 - VIC AU Exposure sites.xlsx")
    input_VIC_AU_Sites_GDF = geopandas.GeoDataFrame( input_VIC_AU_Sites_DF , 
        geometry=geopandas.points_from_xy(input_VIC_AU_Sites_DF.Longitude, input_VIC_AU_Sites_DF.Latitude))
    # derive a new geodata frame with the intersection of Basins and LGA shapes (constrained by Basins).
    output_VIC_AU_Sites_GDF = geopandas.sjoin( input_VIC_AU_Sites_GDF , input_LGA_VIC_GDF , how="left", op='intersects' )
    output_VIC_AU_Sites_outside_LGA_GDF = output_VIC_AU_Sites_GDF[output_VIC_AU_Sites_GDF.LGA_NAME20.isna()]
    output_VIC_AU_Sites_outside_LGA_GDF = output_VIC_AU_Sites_outside_LGA_GDF[output_VIC_AU_Sites_outside_LGA_GDF.columns.intersection( \
        ['Location for Geocoding', 'Latitude', 'Longitude', 'geometry'])]
    print (output_VIC_AU_Sites_outside_LGA_GDF)
    print (input_LGA_VIC_GDF)

    input_LGA_VIC_GDF['geometry'] = input_LGA_VIC_GDF.centroid
    input_LGA_VIC_GDF['X'] = input_LGA_VIC_GDF.geometry.x
    input_LGA_VIC_GDF['Y'] = input_LGA_VIC_GDF.geometry.y
    output_VIC_AU_Sites_outside_LGA_GDF['X'] = output_VIC_AU_Sites_outside_LGA_GDF.geometry.x
    output_VIC_AU_Sites_outside_LGA_GDF['Y'] = output_VIC_AU_Sites_outside_LGA_GDF.geometry.y

    # Create a BallTree 
    tree = BallTree(input_LGA_VIC_GDF[['X', 'Y']].values, leaf_size=2)

    # Query the BallTree on each feature from sites to find the distance to the nearest LGA and its id
    output_VIC_AU_Sites_outside_LGA_GDF['distance_nearest'], output_VIC_AU_Sites_outside_LGA_GDF['id_nearest'] = tree.query(
        output_VIC_AU_Sites_outside_LGA_GDF[['X', 'Y']].values, # The input array for the query
        k=1, # The number of nearest neighbors
    )
    output_VIC_AU_Sites_outside_LGA_GDF= pandas.merge(output_VIC_AU_Sites_outside_LGA_GDF, input_LGA_VIC_GDF, left_on='id_nearest',right_index = True) 

    output_VIC_AU_Sites_outside_LGA_GDF = output_VIC_AU_Sites_outside_LGA_GDF[output_VIC_AU_Sites_outside_LGA_GDF.columns.intersection(['Location for Geocoding', 'Latitude', 'Longitude', 'LGA_NAME20'])]
    print (str(datetime.datetime.now()) + ' output_VIC_AU_Sites_outside_LGA_GDF:')
    print(output_VIC_AU_Sites_outside_LGA_GDF)

    output_VIC_AU_Sites_DF = output_VIC_AU_Sites_GDF[output_VIC_AU_Sites_GDF.columns.intersection(['Location for Geocoding', 'Latitude', 'Longitude', 'LGA_NAME20'])]
    output_VIC_AU_Sites_DF = output_VIC_AU_Sites_DF[output_VIC_AU_Sites_DF['LGA_NAME20'].notna()]
    output_VIC_AU_Sites_DF = geopandas.GeoDataFrame(pandas.concat([output_VIC_AU_Sites_DF, output_VIC_AU_Sites_outside_LGA_GDF], ignore_index=True, sort=False), crs='epsg:4326')

    output_VIC_AU_Sites_DF.drop_duplicates()
    print(output_VIC_AU_Sites_DF)
    output_VIC_AU_Sites_DF.to_excel (datadir + "Coronavirus COVID-19 - VIC AU Exposure sites LGA.xlsx", index=False)

def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    datadir = 'C:/Dev/covid-19-vic-au/'

    processXlsx(datadir)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()

from area import area
import datetime
import geopandas
import os
import subprocess
import zipfile
    
def processZip(datadir):

    # read input zip file, extract and pass contents to next function
    subdir = datadir + 'LGA/'
    inputFileName = datadir + '1270055003_lga_2020_aust_shp.zip'
    z = zipfile.ZipFile(inputFileName)
    z.extractall(subdir)
    z.close()
    
    for dirname, _, filenames in os.walk(subdir):
        for filename in filenames:
            # print (filename)
            if filename.endswith(".shp"): 
            #print(os.path.splitext(file)[0])
                processEachShp(dirname, filename)
                continue
            else:
                continue

def processEachShp(datadir , filename):
    # read input file and convert to geojson and Web Mercator CRS: WGS84 / EPSG:4326
    print ( str(datetime.datetime.now()) + ' Processing file: ' + filename)
    
    each_output_file = str.replace(datadir + filename , ".shp" , ".geojson" )
    inputGDF = geopandas.read_file (datadir + filename)
    inputGDF = inputGDF[inputGDF['AREASQKM20'] > 0]
    output_wgs84_GDF = inputGDF.to_crs('epsg:4326')
    output_wgs84_GDF.to_file(each_output_file, driver="GeoJSON")
    print ( str(datetime.datetime.now()) + ' Wrote file: ' + each_output_file)

    each_output_file = str.replace(each_output_file , ".geojson" , ".csv" )
    output_wgs84_GDF.to_csv(each_output_file, index=False)
    print ( str(datetime.datetime.now()) + ' Wrote file: ' + each_output_file)

    each_output_file = str.replace(each_output_file , ".csv" , ".geojson" )
    each_output_file = str.replace(each_output_file , "_AUST." , "_VIC." )
    output_wgs84_VIC_GDF = output_wgs84_GDF[output_wgs84_GDF['STE_CODE16'] == '2']
    output_wgs84_VIC_GDF.to_file(each_output_file, driver="GeoJSON")
    print ( str(datetime.datetime.now()) + ' Wrote file: ' + each_output_file)

    each_output_file = str.replace(each_output_file , ".geojson" , ".csv" )
    output_wgs84_VIC_GDF.to_csv(each_output_file, index=False)
    print ( str(datetime.datetime.now()) + ' Wrote file: ' + each_output_file)

    each_output_file = str.replace(each_output_file , ".csv" , ".geojson" )
    each_output_file = str.replace(each_output_file , "_VIC." , "_VIC_COVID_19." )
    LGA_NAME20_VIC_COVID_19 = { 'Hume (C)' , 'Casey (C)', 'Brimbank (C)' , 'Moreland (C)' , 'Cardinia (S)' , 'Darebin (C)' }
    output_wgs84_VIC_COVID_19_GDF = output_wgs84_VIC_GDF[output_wgs84_VIC_GDF['LGA_NAME20'].isin(LGA_NAME20_VIC_COVID_19)]
    print(output_wgs84_VIC_COVID_19_GDF)
    output_wgs84_VIC_COVID_19_GDF.to_file(each_output_file, driver="GeoJSON")
    print ( str(datetime.datetime.now()) + ' Wrote file: ' + each_output_file)

def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    datadir = 'C:/DEV/ABS/'
  
    processZip(datadir)

    # Call tippecanoe (Mapbox utility, linux only) to prepare large/complex shapes for Mapbox
    # Command line to run:
    subprocess.call ('"C://cygwin64//home//Mike Honey//tippecanoe//tippecanoe" -o C://DEV//ABS//LGA//LGA_2020_AUST.mbtiles -f -Z 0 -z 10 C://DEV//ABS//LGA//LGA_2020_AUST.geojson' , shell=True)
    subprocess.call ('"C://cygwin64//home//Mike Honey//tippecanoe//tippecanoe" -o C://DEV//ABS//LGA//LGA_2020_VIC.mbtiles -f -Z 0 -z 10 C://DEV//ABS//LGA//LGA_2020_VIC.geojson' , shell=True)
    subprocess.call ('"C://cygwin64//home//Mike Honey//tippecanoe//tippecanoe" -o C://DEV//ABS//LGA//LGA_2020_VIC_COVID_19.mbtiles -f -Z 0 -z 10 C://DEV//ABS//LGA//LGA_2020_VIC_COVID_19.geojson' , shell=True)
    

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()

import os
import csv
import argparse
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import logging

logging= logging.getLogger(__name__)

def ParseInput():

    #takes input
    parser= argparse.ArgumentParser("Welcome to the GPS Extractor version 1.0")
    parser.add_argument('-c', '--csvPath', type= ValidateDirectory, required= True, help= 'specify the directory for the output csv file')
    parser.add_argument('-s', '--scanPath', type= ValidateDirectory, required= True, help= 'specify the directory to scan for the img files')

    theArgs= parser.parse_args()
    return theArgs


def ValidateDirectory(theDir):

    #validates the directory input by the user
    if(not os.path.isdir(theDir)):
        raise argparse.ArgumentTypeError('Directory does not exist')

    if(os.access(theDir, os.W_OK)):
       return theDir
    else:
       raise argparse.ArgumentTypeError('Directory isn\'t writable!!')



def Extractdict(filePath):

    try:
       pilImage= Image.open(filePath)
       data= pilImage._getexif()
    except Exception:
       #log the error and exit
       logging.error("Could not open the image file!\n")
       return None, None

    imageTime= 'NA'
    CameraModel= 'NA'
    CameraMake= 'NA'

    if(data):
       for tag, theValue in data.items():
           #get the name of the tag from TAGS
           tagValue= TAGS.get(tag, tag)
           if(tagValue== 'DateTimeOriginal'):
               imageTime= data.get(tag)
           if(tagValue== 'Make'):
               CameraMake= data.get(tag)
           if(tagValue== 'Model'):
               CameraModel= data.get(tag)

           if(tagValue== 'GPSInfo'):
               #foundit
               gpsdict= {}
               for curtag in theValue:
                   #get the name for the tag from GPSTAGS
                   gpstag= GPSTAGS.get(curtag, curtag)
                   gpsdict[gpstag]= theValue[curtag]
       basicdata= [imageTime, CameraMake, CameraModel]
       return gpsdict, basicdata
       
    else:
       #log the error and exit
       logging.error("The data could not be extracted\n")
       return None, None



def Extractlatlon(gpsdict):

    #function to extract the values of latitude and longitude
    if(gpsdict.has_key("GPSLatitude") and gpsdict.has_key("GPSLongitude") and gpsdict.has_key("GPSLatitudeRef") and gpsdict.has_key("GPSLongitudeRef")):
       latitude= gpsdict['GPSLatitude']
       latituderef= gpsdict['GPSLatitudeRef']
       longitude= gpsdict['GPSLongitude']
       longituderef= gpsdict['GPSLongitudeRef']

       #bring them to correct format by processing the dictionaries
       lat= Convert(latitude)
       lon= Convert(longitude)

       #some conversions for degrees. South and west are considered negative
       if(latituderef== 'S'):
           lat= 0-lat

       if(longituderef== 'W'):
           lon= 0-lon
       
       gpsfinal= {'Lat': lat, 'LatRef': latituderef, 'Lon': lon, 'LonRef': longituderef}
       return gpsfinal
       
    else:
       logging.error("GPS Extraction couldn\'t be performed\n")
       return None


def Convert(gpscd):

    d0= gpscd[0][0]
    d1= gpscd[0][1]

    try:
       #prevent zero division
       degrees=float(d0)/float(d1)
    except:
       degrees= 0.0

    m0= gpscd[1][0]
    m1= gpscd[1][1]

    try:
       minutes= float(m0)/float(m1)
    except:
       minutes= 0.0

    s0= gpscd[2][0]
    s1= gpscd[2][1]

    try:
       seconds= float(s0)/float(s1)
    except:
       seconds= 0.0


    finalcd= float(degrees +  minutes/60.0 + seconds/3600.0)
    return finalcd



class _CSVWriter:

    def __init__(self, filePath):
       try:
           #create the op csv file with write only type
           self.csvfile= open(filePath, 'wb')
           self.writer= csv.writer(self.csvfile, delimiter= ',', quoting= csv.QUOTE_ALL)
           self.writer.writerow(('Image Path', 'TimeStamp', 'Camera Make', 'Camera Model', 'Lat Ref', 'Latitude', 'Lon Ref', 'Longitude'))
       except:
           #unable to write the csv file
           logging.error('CSV File failure\n')


    def writeCSVRow(self, filePath, timestamp, cameramake, cameramodel, latref, latitude, lonref, longitude):
       latstr= '%.8f'% latitude
       lonstr= '%.8f'% longitude
       self.writer.writerow((filePath, timestamp, cameramake, cameramodel, latref, latitude, lonref, longitude))
       
    def writerClose(self):#CHECK
       self.csvfile.close()
    
               

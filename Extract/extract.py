import os
import sys
import csv
import _extract
import logging
import time

if __name__== '__main__':
    EXTRACTOR_VERSION= 1.0

    #Turn om logging
    logging.basicConfig(filename= 'ExtractLog.log', level= logging.DEBUG, format= '%(asctime)s %(message)s', datefmt= '%d/%m/%Y %H/%M/%S %p')

    userargs= _extract.ParseInput()

    startTime= time.time()
    logging.info('Welcome to Extractor Version ' + str(EXTRACTOR_VERSION) + '.. Scan started\n')
    csvPath= userargs.csvPath + 'imageResults.csv'
    #store tha path

    opcsv= _extract._CSVWriter(csvPath)

    targetDir= userargs.scanPath
    #try and open the directory containing the image files
    try:
        pics= os.listdir(targetDir)
    except:
        logging.error('Invalid directory ' + targetDir + '\n')
        #not even one image file processed thus exit simply
        sys.exit()

    for thefile in pics:
        targetfile= targetDir  + thefile
        if(os.path.isfile(targetfile)):
            gpsdict, exiflist= _extract.Extractdict(targetfile)
            if(gpsdict):
                coor= _extract.Extractlatlon(gpsdict)
                if not (coor is None):
                    lat= coor.get('Lat')
                    latref= coor.get('LatRef')
                    lon= coor.get('Lon')
                    lonref= coor.get('LonRef')
                    if(lat and latref and lon and lonref):
                        print (str(lat) + ',  ' + str(lon))
                        opcsv.writeCSVRow(targetfile, exiflist[0], exiflist[1], exiflist[2], latref, lat, lonref, lon)
                        logging.info('Extraction complete for ' + targetfile + '\n')
                    else:
                        logging.warning('No data extracted for ' + targetfile + '\n')
                else:
                    logging.warning('No data extracted for ' + targetfile + '\n')
            else:
                logging.warning('No data extracted for ' + targetfile + '\n')
        else:
            logging.warning(targetfile + ' not a valid file!\n')

    endTime= time.time()
    logging.info('Elapsed time: ' + str(endTime - startTime) + '\n')
    logging.info('Program Terminated!!!\n')
    opcsv.writerClose()

    
    
    

    

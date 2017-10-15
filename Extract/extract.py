import os
import _extract
import logging
import time

if __name__= '__main__':
    EXTRACTOR_VERSION= 1.0

    #Turn om logging
    logging.basicConfig(filename= 'ExtractLog.log', level= logging.DEBUG, format= '%(asctime)s %(message)s', datefmt= '%d/%m/%Y %H/%M/%S %p')

    _extract.ParseInput()

    startTime= time.time()
    logging.info('Welcome to Extractor Version ' + str(EXTRACTOR_VERSION) + '.. Scan started\n')

    

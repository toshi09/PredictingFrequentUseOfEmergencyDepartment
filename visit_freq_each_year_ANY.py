'''
The code finds unique patients with ANY amission per year and their visit distribution
'''

column_index_map import *
from collections import  defaultdict

def visit_count(visits):
    cnts = defaultdict(int)
    for v in visits:
        yr = v[ADMIT_YEAR_IDX]
        cnts[yr] += 1

    return cnts

def rem(inputfile, year_str):
    prev_id = ''
    visits = []
    filehandle = open(inputfile)
    filehandle.readline()
    patient_hist = defaultdict(int)
    patient_ids = set()
    for line in filehandle:
        values = line.strip().split(",")
        patient = values[32]
        if patient != prev_id:
            num_visits = len(visits)
            if num_visits >= 4:
                patient_hist[4] += 1
            if num_visits >= 8:
                patient_hist[8] += 1
            if num_visits >= 16:
                patient_hist[16] += 1
            visits = []
        if values[ADMIT_YEAR_IDX] == year_str:
            visits.append(year_str)
            patient_ids.add(patient)
        prev_id  = patient

    print("Patient Visit dist: "+ str(year_str) + " " +str(patient_hist),"unique patients"+str(len(patient_ids)))
    filehandle.close()

rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv', '2008')
rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv', '2008')            
rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv', '2009')            
rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv', '2010')            
rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv', '2011')            
rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv', '2012')            
rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv','2013')             




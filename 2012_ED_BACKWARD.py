from column_index_map import *
from collections import  defaultdict

def visit_count(visits):
    cnts = defaultdict(int)
    for v in visits:
        yr = v[ADMIT_YEAR_IDX]
        cnts[yr] += 1

    return cnts

def update_visit_distibution(vist_dist_dict, total_visits):
    if total_visits >= 4:
        vist_dist_dict[4] += 1
    if total_visits >= 8:
        vist_dist_dict[8] += 1
    if total_visits >= 16:
        vist_dist_dict[16] += 1
    return vist_dist_dict

def visit_freq(visits):
    dict_obj = defaultdict(int)
    for element in visits:
        dict_obj[element] = dict_obj[element] + 1
    return dict_obj

def rem(inputfile,outfile):
    filehandle = open(inputfile)
    garbage = filehandle.readline()

    patient_ids = set()
    patient_ids_2011 = set()

    for line in filehandle:
        values = line.strip().split(",")

        if values[SRC_COL_IDX] == '1' and values[ADMIT_YEAR_IDX] == '2012':
            patient = values[32]
            patient_ids.add(patient)

    print("Number of patients in 2012 "+str(len(patient_ids)))
    filehandle.close()


    prev_id = ''
    visit = []
    filehandle = open(inputfile)
    w_fhand = open(outfile,'w')
    visit_dist_2011 = defaultdict(int)
    visit_dist_2012 = defaultdict(int)


    for line in filehandle:
        values = line.strip().split(",")
        patient = values[32]
        if patient not in patient_ids:
            continue

        if prev_id != patient:
            per_year_visit_cnt = visit_freq(visit)
            update_visit_distibution(visit_dist_2012, per_year_visit_cnt['2012'])
            update_visit_distibution(visit_dist_2011, per_year_visit_cnt['2011'])
            visit = []

        if values[SRC_COL_IDX] == '1' and values[ADMIT_YEAR_IDX] == '2012':
            visit.append('2012')
            w_fhand.write(line)

        elif values[SRC_COL_IDX] == '1'and values[ADMIT_YEAR_IDX] == '2011':
            visit.append('2011')
            w_fhand.write(line)
            patient_ids_2011.add(patient)


        prev_id = patient

    filehandle.close()
    w_fhand.close()
    print len(patient_ids), len(patient_ids_2011)
    print visit_dist_2012,  visit_dist_2011

rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv','/Users/oshpddata/Desktop/vikhyati/2012_ED_BACKWARD.csv' )

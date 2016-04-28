'''
Finds all the patients with ED visits in base years i.e(2012,2013), and find the visit distribution of
    such patients with at least one ED admission in other years i.e(2011).
    
'''



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

def get_only_ed_visit_distribution_for_years_backwards(inputfile, outfile, base_year, other_years):
    """
    :param inputfile: patient record file
    :param outfile:  write to file
    :param base_year: base year, e.g: 2012 or 2013
    :param other_years: list of other years. e.g: ['2011']
    :return:
    """
    filehandle = open(inputfile)
    filehandle.readline()

    patient_other_years = set()
    patient_ids_base_year = set()

    for line in filehandle:
        values = line.strip().split(",")

        if values[SRC_COL_IDX] == '1' and values[ADMIT_YEAR_IDX] == base_year:
            patient = values[32]
            patient_ids_base_year.add(patient)

    print("Number of patients in base year %s "%(base_year) +str(len(patient_ids_base_year)))
    filehandle.close()


    prev_id = ''
    visit = []
    filehandle = open(inputfile)
    w_fhand = open(outfile,'w')
    visit_dist_base_years = defaultdict(int)
    visit_dist_rest_of_year = defaultdict(int)
    year_str_all = " ".join(other_years)

    for line in filehandle:
        values = line.strip().split(",")
        patient = values[32]
        if patient not in patient_ids_base_year:
            continue

        if prev_id != patient:
            per_year_visit_cnt = visit_freq(visit)
            update_visit_distibution(visit_dist_rest_of_year, per_year_visit_cnt[year_str_all])
            update_visit_distibution(visit_dist_base_years, per_year_visit_cnt[base_year])
            visit = []

        if values[SRC_COL_IDX] == '1' and values[ADMIT_YEAR_IDX] in other_years:
            visit.append(year_str_all)
            w_fhand.write(line)
            patient_other_years.add(patient)

        elif values[SRC_COL_IDX] == '1'and values[ADMIT_YEAR_IDX] == base_year:
            visit.append(base_year)
            w_fhand.write(line)
            patient_ids_base_year.add(patient)


        prev_id = patient

    filehandle.close()
    w_fhand.close()
    print " Num patients in other years ", len(patient_other_years)
    print " Num patients in base years ", len(patient_ids_base_year)
    print 'visit_dist_rest_of_year'+ " for year "+ year_str_all + " ",  str(visit_dist_rest_of_year)
    print 'visit_dist_rest_of_year for year base year %s'%(base_year),  str(visit_dist_base_years)

get_only_ed_visit_distribution_for_years_backwards('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv','2012_ED_BACKWARD.csv' ,
                                                   '2012', ['2011'])
get_only_ed_visit_distribution_for_years_backwards('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv','2013_ED_BACKWARD.csv' ,
                                                   '2013', ['2011'])

'''Get the visit distribution and number of patients who were admitted to the emergency department at least once in 2011
and who were hpspitalized at least once more(Emergency department or otherwise) in 2012 '''

'''Get the visit distribution and number of patients who were admitted to the emergency department at least once in 2011
and who were hpspitalized at least once more(Emergency department or otherwise) in 2013 '''

'''Get the visit distribution and number of patients who were admitted to the emergency department at least once in 2011
and who were hpspitalized at least once more(Emergency department or otherwise) in 2012 or 2013 '''




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

def get_visit_distribution_against_against_ed_base_year(inputfile, base_year, other_years):
    """
    Get patients with ED visits in base year.
    For all such patients find the visit distribution in other_years.
    Other year is list of years, e.g ['2012'], ['2013'] or ['2012', '2013']
    This function prints the ED visit distribution in the base year.
    It also prints the visit distribution of all such patiens in the other years.
    Visit distribution is cumulative visit distribution in three categories:
    4 visits, 8 visits, 16 visits.
    :param inputfile: patient record file
    :param base_year: base year for patients with ED (Emeregence Department) visits
    :param other_years: Other years for which we want to find the visit distribution
    for all the patients sastisfying the criterion in base year.
    :return: prints number of patients in base year and other years. Also prints
    the visit distribution in base year and other year.
    """
    """
    :param inputfile:
    :param base_year:
    :param other_years:
    :return:
    """
    filehandle = open(inputfile)
    garbage = filehandle.readline()

    patient_ids = set()
    patient_ids_from_other_years = set()

    for line in filehandle:
        values = line.strip().split(",")

        if values[SRC_COL_IDX] == '1' and values[ADMIT_YEAR_IDX] == base_year:
            patient = values[32]
            patient_ids.add(patient)

    print("Number of patients in 2011 "+str(len(patient_ids)))
    filehandle.close()


    prev_id = ''
    visit = []
    filehandle = open(inputfile)

    visit_dist_base_year = defaultdict(int)
    visit_dist_for_other_years = defaultdict(int)
    other_years_str = " ".join(other_years)
    for line in filehandle:
        values = line.strip().split(",")
        patient = values[32]
        if patient not in patient_ids:
            continue

        if prev_id != patient:
            per_year_visit_cnt = visit_freq(visit)
            update_visit_distibution(visit_dist_base_year, per_year_visit_cnt[base_year])
            update_visit_distibution(visit_dist_for_other_years, per_year_visit_cnt[other_years_str])

            visit = []

        if values[SRC_COL_IDX] == '1' and values[ADMIT_YEAR_IDX] == base_year:
            visit.append(base_year)


        elif values[ADMIT_YEAR_IDX] in other_years:
            visit.append(other_years_str)
            patient_ids_from_other_years.add(patient)

        prev_id = patient
    filehandle.close()

    print len(patient_ids), len(patient_ids_from_other_years)
    print visit_dist_base_year,  visit_dist_for_other_years

'''Get the visit distribution and number of patients who were admitted to the emergency department at least once in 2011
and who were hpspitalized at least once more(Emergency department or otherwise) in 2012 '''
get_visit_distribution_against_against_ed_base_year('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv','2011', ['2012'])

'''Get the visit distribution and number of patients who were admitted to the emergency department at least once in 2011
and who were hpspitalized at least once more(Emergency department or otherwise) in 2013 '''
get_visit_distribution_against_against_ed_base_year('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv', '2011', ['2013'])

'''Get the visit distribution and number of patients who were admitted to the emergency department at least once in 2011
and who were hpspitalized at least once more(Emergency department or otherwise) in 2012 or 2013 '''
get_visit_distribution_against_against_ed_base_year('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv', '2011', ['2012', '2013'])

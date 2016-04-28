''' Find  total number of records per year
Find total number number of ED records per year
Find total number of unique patients per year
Find visit non cumulative distribution of patients per year
Find visit non cumulative distribution of ED patients per year
'''


import column_index_map as col_idx_map
from collections import  defaultdict
def number_of_record(file_name, year_str):
    """

    :param file_name: Name of the patient data file
    :param year_str: Year to find the total number of records
    :return: total number of records
    """
    count = 0
    with open(file_name) as fd:
        for line in fd:
            values = line.strip("\n").split(",")
            visit_year = values[col_idx_map.ADMIT_YEAR_IDX]
            if visit_year == year_str:
                count += 1
    return count

def number_of_record_in_ed(file_name, year_str):
    """

    :param file_name: Name of the patient data file
    :param year_str: Year to find the total number of records
    :return: total number of records
    """
    count = 0
    with open(file_name) as fd:
        for line in fd:
            values = line.strip("\n").split(",")
            visit_year = values[col_idx_map.ADMIT_YEAR_IDX]
            src_type = values[col_idx_map.SRC_COL_IDX]
            if visit_year == year_str and src_type == '1':
                count += 1
    return count

def unique_patients_per_year(file_name, year_str):
    pid_set = set()
    with open(file_name) as fd:
        for line in fd:
            values = line.strip("\n").split(",")
            visit_year = values[col_idx_map.ADMIT_YEAR_IDX]
            if visit_year == year_str:
                pid_set.add(values[col_idx_map.PID_IDX])
    return len(pid_set)

def visit_distribution_per_year(file_name, year_str):
    visit_dist = defaultdict(int)
    patient_visit_cnt = 0
    prev_id = ''
    with open(file_name) as fd:
        for line in fd:
            values = line.strip("\n").split(",")
            pid = values[col_idx_map.PID_IDX]
            visit_year = values[col_idx_map.ADMIT_YEAR_IDX]
            if prev_id and prev_id != pid:
                patient_visit_cnt += 1
                visit_dist[patient_visit_cnt]  += 1
                patient_visit_cnt = 0

            if visit_year == year_str:
                patient_visit_cnt += 1

            prev_id = pid

    return  visit_dist

def visit_distribution_per_year_for_ed(file_name, year_str):
    visit_dist = defaultdict(int)
    patient_visit_cnt = 0
    prev_id = ''
    with open(file_name) as fd:
        for line in fd:
            values = line.strip("\n").split(",")
            pid = values[col_idx_map.PID_IDX]
            visit_year = values[col_idx_map.ADMIT_YEAR_IDX]
            src_type = values[col_idx_map.SRC_COL_IDX]
            if prev_id and prev_id != pid:
                patient_visit_cnt += 1
                visit_dist[patient_visit_cnt]  += 1
                patient_visit_cnt = 0

            if visit_year == year_str and src_type == '1':
                patient_visit_cnt += 1

            prev_id = pid

    return  visit_dist

base_file_name = "/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv"
print "Number of records 2008 ", number_of_record(base_file_name, '2008')
print "Number of records 2009 ", number_of_record(base_file_name, '2009')
print "Number of records 2010 ", number_of_record(base_file_name, '2010')
print "Number of records 2011 ",  number_of_record(base_file_name, '2011')
print "Number of records 2012 ", number_of_record(base_file_name, '2012')
print "Number of records 2013 ", number_of_record(base_file_name, '2013')

print "Number of ED records 2008 ",  number_of_record_in_ed(base_file_name, '2008')
print "Number of ED records 2009 ", number_of_record_in_ed(base_file_name, '2009')
print "Number of ED records 2010 ", number_of_record_in_ed( base_file_name, '2010')
print "Number of ED records 2011 ",  number_of_record_in_ed(base_file_name, '2011')
print "Number of ED records 2012 ", number_of_record_in_ed(base_file_name, '2012')
print "Number of ED records 2013 ", number_of_record_in_ed( base_file_name, '2013')

print "Number of unique patients 2011" , unique_patients_per_year(base_file_name, '2011')
print "Number of unique patients 2012 ", unique_patients_per_year(base_file_name, '2012')
print "Number of unique patients 2013 ", unique_patients_per_year(base_file_name, '2013')

print "Visit distribution for patients in 2008 " , visit_distribution_per_year(base_file_name, '2008')
print "Visit distribution for patients in 2009 " , visit_distribution_per_year(base_file_name, '2009')
print "Visit distribution for patients in 2010 " , visit_distribution_per_year(base_file_name, '2010')
print "Visit distribution for patients in 2011 " , visit_distribution_per_year(base_file_name, '2011')
print "Visit distribution for patients in 2012 " , visit_distribution_per_year(base_file_name, '2012')
print "Visit distribution for patients in 2013 " , visit_distribution_per_year(base_file_name, '2013')

print "Visit distribution for ED patients in 2008" , visit_distribution_per_year_for_ed(base_file_name, '2011')
print "Visit distribution for ED patients in 2009 " , visit_distribution_per_year_for_ed(base_file_name, '2012')
print "Visit distribution for ED patients in 2010" , visit_distribution_per_year_for_ed(base_file_name, '2013')
print "Visit distribution for ED patients in 2011 " , visit_distribution_per_year_for_ed(base_file_name, '2011')
print "Visit distribution for ED patients in 2012 " , visit_distribution_per_year_for_ed(base_file_name, '2012')
print "Visit distribution for ED patients in 2013 " , visit_distribution_per_year_for_ed(base_file_name, '2013')

from column_index_map import *
import sys
import pickle
from collections import  defaultdict
from math import sin, cos, radians, degrees, acos

# library which converts zip code to latitude and longitude
from pyzipcode import ZipCodeDatabase

from collections import namedtuple

zip_db = ZipCodeDatabase()

def get_age_columns(age):
    """
    Returns a vector with correct age index
    set to 1
    :param age:
    :return:
    """
    age_cols = [0 for xx in range(6) ]
    if age < 5 :
        age_cols[0] = 1
    elif age >= 5 and age < 15:
        age_cols[1] = 1
    elif age >= 15 and age < 24:
        age_cols[2] = 1
    elif age >= 25 and age < 44:
        age_cols[3] = 1
    elif age_cols >= 45 and age_cols < 64:
        age_cols[4] = 1
    else:
        age_cols[5] = 1

    return age_cols


def get_visit_dist_column(visit_distribution_per_patient ,year):
    """
    :param visit_distribution_per_patient:
    :return:
    """
    visit_col = [0]
    visit_col[0] = visit_distribution_per_patient[year]

    return visit_col

def calc_dist(lat_a, long_a, lat_b, long_b):
    """
    Calculates the distance in miles
    between two points specified by
    latitude and longitude
    :param lat_a:
    :param long_a:
    :param lat_b:
    :param long_b:
    :return:
    """
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    return degrees(acos(distance)) * 69.09

def get_dist(hsp_zip, pat_zip):
    """
    Get this distance in miles between zip code.
    :param hsp_zip:
    :param pat_zip:
    :return:
    """
    try:
        hsp = zip_db[hsp_zip] # Get the latitude and longitude of hospital zipcode
        pat = zip_db[pat_zip] # Get the latitude and longitude of hospital zipcode
        return calc_dist(hsp.latitude, hsp.longitude, pat.latitude, pat.longitude)
    except:
        return None

def update_dist_dist(dist_dict, pat_lat, hsp_lat):
    distance = get_dist(pat_lat, hsp_lat)
    if distance is None:
        #print 'Zip code not found ', pat_lat, hsp_lat
        return
    dist = abs(distance)
    if dist <= 5:
        dist_dict[5] += 1.0
    elif dist > 5 and dist <= 20:
        dist_dict['5-20'] += 1.0
    else:
        dist_dict['20'] += 1.0

def featurize(file_name, out_file, year, predictor_year, category_visit_count_threshold):
    prev_id = ''
    age_dist = defaultdict(int)
    out_h = open(out_file, 'wb')
    header  = ['PID', 'gender','race_grp', 'distance_<=5', 'distance_6_20', 'distance_>20',
                'age_<5', 'age_5-14', 'age_15-24',   'age_25-44','age_45-64','age_>=65',
               'NUM_ADMIT_'+year,'NUM_EDADM_'+year,'category_>='+str(category_visit_count_threshold)]

    out_h.write(",".join(header) + "\n")
    visit_distribution_per_patient = defaultdict(int)
    ed_visit_distribution_per_patient = defaultdict(int)
    dist_dist = defaultdict(float)
    missing_zip = 0
    with open(file_name) as fd:
        fd.readline()

        for line in fd:
            values = line.strip("\n").split(",")
            pid = values[PID_IDX]
            visit_year = values[ADMIT_YEAR_IDX]
            birth_yr = values[BIRTH_IDX]
            src_type = values[SRC_COL_IDX]
            gender = values[GENDER_IDX]
            pat_zip = values[PATZIP_IDX]
            hsp_zip = values[HPLZIP_IDX]
            race_grp = values[RACE_GRP_IDX]

            if prev_id and pid != prev_id:
                age_as_per_last_vist = int(prev_visit_year) - int(prev_birth_year)

                age_cols = get_age_columns(age_as_per_last_vist)
                visit_col = get_visit_dist_column(visit_distribution_per_patient , year)
                ed_visit_col  = get_visit_dist_column(ed_visit_distribution_per_patient, year)

                total_visits = visit_distribution_per_patient[year]
                predictor_year_visit_cnt = ed_visit_distribution_per_patient[predictor_year]

                category = 1 if predictor_year_visit_cnt >= category_visit_count_threshold else 0
                #print ed_visit_distribution_per_patient
                if ed_visit_distribution_per_patient[year] > 0:

                    row = [prev_id, prev_gender, prev_race_group] + [dist_dist['5'] / total_visits,
                                                      dist_dist['5-20'] / total_visits,
                                                      dist_dist['20'] / total_visits,] + \
                      age_cols + visit_col + ed_visit_col + [category]

                    out_h.write(",".join([str(xx) for xx in row]) + "\n")

                visit_distribution_per_patient = defaultdict(int)
                ed_visit_distribution_per_patient = defaultdict(int)
                dist_dist = defaultdict(float)


            if src_type == '1':
                ed_visit_distribution_per_patient[visit_year] += 1

            visit_distribution_per_patient[visit_year] += 1

            if visit_year == year:
                if get_dist(pat_zip, hsp_zip):
                    missing_zip += 1
                update_dist_dist(dist_dist, pat_zip, hsp_zip)

            prev_id = pid
            prev_visit_year = visit_year
            prev_gender = gender
            prev_birth_year = birth_yr
            prev_race_group = race_grp

    print missing_zip
    out_h.close()
    return age_dist


base_file_name = "/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv"
featurize(base_file_name, "OSHPD_MASTER_2009.csv", '2009', '2010', 8)

from column_index_map_2 import *
from collections import  defaultdict
from math import sin, cos, radians, degrees, acos


# library which converts zip code to latitude and longitude
from pyzipcode import ZipCodeDatabase
import icd9_map

# The zipcode database
zip_db = ZipCodeDatabase()

# Comorbidity codes from the ICD-9 map defined in icd9_map
# http://czresearch.com/dropbox/Elixhauser_MedCare_1998v36p8.pdf
COMORBID_COLS = icd9_map.get_comorbidities() + ["ELIX_unclassified"]

def get_comorbid_list(pat_row):
    """
    From a patient, iterate over diagonsis indexes
    :0 to 25 to get the ICD_9 codes.
    For each of the ICD_9 codes find the comorbidity.
    Return a list of comorbidities for a
    patient at a particular visit.
    """
    disease_list = []
    for idx in range(0, 25):
        code = pat_row[idx]
        if not code:
            # columns can have no values.
            continue
        if code not in icd9_map.icd_9_processed_map:
            disease_list.append("ELIX_unclassified")
        else:
            disease_list.append(icd9_map.icd_9_processed_map[code])
    return disease_list

def get_age_vector(age):
    """
    Based on the age, returns a vector with correct age index
    set to 1
    :param age:
    :return:
    """

    age_cols = [0 for xx in range(6)] # list of six elements, all set to 0

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


def get_visit_count_vector(visit_distribution_per_patient, year):
    """
    Return a list with single element containing
    number of visits for year in the
    visit_distribution_per_patient.
    visit_distribution_per_patient can be either
    of ED type or ANY visit types.
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
    :param hsp_zip: Hospital zip code
    :param pat_zip: Patient zip code
    :return:
    """
    try:
        hsp = zip_db[hsp_zip] # Get the latitude and longitude of hospital zipcode
        pat = zip_db[pat_zip] # Get the latitude and longitude of hospital zipcode
        return calc_dist(hsp.latitude, hsp.longitude, pat.latitude, pat.longitude)
    except:
        return None

def update_distance_distribution(distance_distribution, pat_zip_code, hsp_zip_code):
    """
    Distance distribution is count of following categories of distances
    <=5, >5 and <=20 , > 20.
    This function updates the distribution with the distance between
    pat_zip and hsp_zip.
    :param distance_distribution:
    :param pat_zip_code:
    :param hsp_zip_code:
    :return:
    """
    distance = get_dist(pat_zip_code, hsp_zip_code)
    if distance is None:
        #print 'Zip code not found ', pat_lat, hsp_lat
        return
    dist = abs(distance)
    if dist <= 5:
        distance_distribution['5'] += 1.0
    elif dist > 5 and dist <= 20:
        distance_distribution['5-20'] += 1.0
    else:
        distance_distribution['20'] += 1.0

def update_comorbid_dist(comorbid_dist, disease_lst):
    """
    Updates the comorbid distribution with the
    diseases in the disease list.
    :param comorbid_dist: Map of disease to number of time
    it was observed.
    :param disease_lst: List of disease observed in a visit.
    :return:
    """
    for disease in disease_lst:
        comorbid_dist[disease] += 1.0

def get_comorbid_vector(comorbid_distribution, num_visits):
    """
    Return a vector of COMORBIDitie with
    vector indexes set to number of times each
    comorbidity has been observerd in set of visits.
    :param comorbid_distribution:
    :param num_visits:
    :return:
    """
    columns = [0.0 for xx in COMORBID_COLS]
    for idx, disease in enumerate(COMORBID_COLS):
        if disease in comorbid_distribution:
            columns[idx] = comorbid_distribution[disease] / num_visits
    return columns

def featurize(file_name, out_file, base_year, predictor_year, category_visit_count_threshold):
    """
    Generates the file which will be used for modeling
    :param file_name: OSHPD data (OSHPD_CLEAN.csv)
    :param out_file: output file.
    :param base_year: THe base year from which will construct our feature vectors
    :param predictor_year:
    :param category_visit_count_threshold:
    :return:
    """
    out_h = open(out_file, 'wb')
    header  = ['rln', 'gender','race_grp', 'distance_lt_eq_5', 'distance_6_20', 'distance_gt_20',
                'age_lt_5', 'age_5_14', 'age_15_24',   'age_25_44','age_45_64','age_gt_eq_65',
               'NUM_ADMIT_' + base_year, 'NUM_EDADMIT_' + base_year] + \
              COMORBID_COLS + \
              ['category_gt_eq_'+str(category_visit_count_threshold)]

    out_h.write(",".join(header) + "\n")
    
    prev_id = ''
    # Per year visit counts
    visit_distribution_per_patient = defaultdict(int)
    # Per year ED type visit count
    ed_visit_distribution_per_patient = defaultdict(int)

    # Distance count for the base year
    distance_distribution = defaultdict(float)
    # Comorbidities count for the base year.
    comorbid_distribution = defaultdict(float)

    with open(file_name) as fd:
        fd.readline() # skip header

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

                age_cols = get_age_vector(age_as_per_last_vist)

                visit_col = get_visit_count_vector(visit_distribution_per_patient, base_year)
                ed_visit_col  = get_visit_count_vector(ed_visit_distribution_per_patient, base_year)

                ed_total_visits = ed_visit_distribution_per_patient[base_year]

                predictor_year_visit_cnt = ed_visit_distribution_per_patient[predictor_year]
                category = 1 if predictor_year_visit_cnt >= category_visit_count_threshold else 0

                if ed_visit_distribution_per_patient[base_year] > 0:
                    # We only write a row to output file if there is atleast one ED visit from customer.
                    disease_cols = get_comorbid_vector(comorbid_distribution, ed_total_visits)
                    row = [prev_id, prev_gender, prev_race_group] + \
                          [distance_distribution['5'] / ed_total_visits, distance_distribution['5-20'] / ed_total_visits, distance_distribution['20'] / ed_total_visits] + \
                           age_cols + visit_col + ed_visit_col + disease_cols + \
                          [category]

                    assert len(row) == len(header)
                    out_h.write(",".join([str(xx) for xx in row]) + "\n")

                # Reset important distribution maps
                visit_distribution_per_patient = defaultdict(int)
                ed_visit_distribution_per_patient = defaultdict(int)
                distance_distribution = defaultdict(float)
                comorbid_distribution = defaultdict(float)


            if src_type == '1':
                ed_visit_distribution_per_patient[visit_year] += 1

            visit_distribution_per_patient[visit_year] += 1

            if src_type == '1' and visit_year == base_year:
                update_distance_distribution(distance_distribution, pat_zip, hsp_zip)
                ds_lst = get_comorbid_list(values)
                update_comorbid_dist(comorbid_distribution, ds_lst)

            prev_id = pid
            prev_visit_year = visit_year
            prev_gender = gender
            prev_birth_year = birth_yr
            prev_race_group = race_grp

    # The last patient info was not written. Following just does that.
    if ed_visit_distribution_per_patient[base_year] > 0:
        age_as_per_last_vist = int(prev_visit_year) - int(prev_birth_year)
        age_cols = get_age_vector(age_as_per_last_vist)
        visit_col = get_visit_count_vector(visit_distribution_per_patient, base_year)
        ed_visit_col  = get_visit_count_vector(ed_visit_distribution_per_patient, base_year)

        disease_cols = get_comorbid_vector(comorbid_distribution, ed_total_visits)
        ed_total_visits = ed_visit_distribution_per_patient[base_year]
        row = [prev_id, prev_gender, prev_race_group] + \
               [distance_distribution['5'] / ed_total_visits, distance_distribution['5-20'] / ed_total_visits, distance_distribution['20'] / ed_total_visits] + \
                age_cols + visit_col + ed_visit_col + disease_cols + \
                [category]

        assert len(row) == len(header)
        out_h.write(",".join([str(xx) for xx in row]) + "\n")

    out_h.close()


base_file_name = "/Users/oshpddata/Desktop/OSHPD2016/OSHPD_CLEAN.csv"
featurize(base_file_name, "MLHC_ED_2009.csv", '2009', '2010', 4)

#
# http://czresearch.com/dropbox/Elixhauser_MedCare_1998v36p8.pdf

ICD9_RAW_MAP = {
"398.91" : "ELIX_CHF",
"428.0-428.9" : "ELIX_CHF",
"093.20-093.24" : "ELIX_VALVE",
"394.0-397.1" : "ELIX_VALVE",
"397.9" : "ELIX_VALVE",
"424.0-424.99" : "ELIX_VALVE",
"746.3-746.6"  : "ELIX_VALVE",
"V42.2" : "ELIX_VALVE",
"V43.3" : "ELIX_VALVE",
"415.11-415.19" : "ELIX_PULMCIRC",
"416.0-416.9" : "ELIX_PULMCIRC",
"417.9" : "ELIX_PULMCIRC",
"440.0-440.9" : "ELIX_PERIVASC",
"441.0-441.9" : "ELIX_PERIVASC",
"442.0-442.9" : "ELIX_PERIVASC",
"443.1-443.9" : "ELIX_PERIVASC",

"444.21-444.22" : "ELIX_PERIVASC",
"447.1" : "ELIX_PERIVASC",
"449.0" : "ELIX_PERIVASC",
"557.1" : "ELIX_PERIVASC",
"557.9" : "ELIX_PERIVASC",
"V43.4" : "ELIX_PERIVASC",
"401.1" : "ELIX_HTN",
"401.9" : "ELIX_HTN",
"642.00-642.04":"ELIX_HTN",
"401.0" : "ELIX_HTN",
"437.2" : "ELIX_HTN",
"642.20-642.24" : "ELIX_HTN",
"402.00" : "ELIX_HTN",
"402.10" : "ELIX_HTN",
"402.90" : "ELIX_HTN",
"405.09" : "ELIX_HTN",
"405.19" : "ELIX_HTN",
"405.99" : "ELIX_HTN",
"402.01" : "ELIX_HTN",
"402.11" : "ELIX_HTN",
"402.91" : "ELIX_HTN",


"404.00" : "ELIX_HTN",
"404.10" : "ELIX_HTN",
"404.90" : "ELIX_HTN",


"403.00" : "ELIX_HTN",
"403.10" : "ELIX_HTN",
"403.90" : "ELIX_HTN",
"405.01" : "ELIX_HTN",
"405.11" : "ELIX_HTN",
"405.91" : "ELIX_HTN",
"642.10-642.14" : "ELIX_HTN",


"403.01" : "ELIX_HTN",
"403.11" : "ELIX_HTN",
"403.91" : "ELIX_HTN",

"404.00" : "ELIX_HTN",
"404.10" : "ELIX_HTN",
"404.90" : "ELIX_HTN",

"404.01" : "ELIX_HTN",
"404.11" : "ELIX_HTN",
"404.91" : "ELIX_HTN",

"404.02" : "ELIX_HTN",
"404.12":"ELIX_HTN",
"404.92":"ELIX_HTN",

"404.03":"ELIX_HTN",
"404.13":"ELIX_HTN",
"404.93":"ELIX_HTN",

"642.70-642.74":"ELIX_HTN",
"642.90-642.94":"ELIX_HTN",

"342.0-344.9 ":"ELIX_PARA",
"438.20-438.53":"ELIX_PARA",
"780.72":"ELIX_PARA",

"330.0-331.9" : "ELIX_NEURO",
"332.0":"ELIX_NEURO",
"333.4":"ELIX_NEURO",
"333.5":"ELIX_NEURO",
"333.7":"ELIX_NEURO",
"333.71":"ELIX_NEURO",
"333.72":"ELIX_NEURO",
"333.79":"ELIX_NEURO",
"333.85":"ELIX_NEURO",
"333.94":"ELIX_NEURO",
"334.0-335.9":"ELIX_NEURO",
"338.0":"ELIX_NEURO",
"340.0":"ELIX_NEURO",
"341.1-341.9":"ELIX_NEURO",
"345.00-345.11":"ELIX_NEURO",
"345.2-345.3":"ELIX_NEURO",
"345.40-345.91":"ELIX_NEURO",
"347.00-347.01":"ELIX_NEURO",
"347.10-347.11":"ELIX_NEURO",
"649.40-649.44":"ELIX_NEURO",
"768.7" : "ELIX_NEURO",
"768.70-768.73":"ELIX_NEURO",
"780.3":"ELIX_NEURO",
"780.31":"ELIX_NEURO",
"780.32":"ELIX_NEURO",
"780.33":"ELIX_NEURO",
"780.39":"ELIX_NEURO",
"780.97":"ELIX_NEURO",
"784.3":"ELIX_NEURO",
"490":"ELIX_CHRNLUNG",
"490.0-492.8":"ELIX_CHRNLUNG",
"493.00-493.92":"ELIX_CHRNLUNG",
"494.0-494.1":"ELIX_CHRNLUNG",
"4950 -505  ":"ELIX_CHRNLUNG",
"506.4" :"ELIX_CHRNLUNG",


"250.00-250.33":"ELIX_DM",
"648.00-648.04":"ELIX_DM",
"249.00-249.31":"ELIX_DM",

"250.40-250.93":"ELIX_DMCX",
"7751 ":"ELIX_DMCX",
"24940-24991" : "ELIX_DMCX",
"243" : "ELIX_HYPOTHY",
"243.0-244.2":"ELIX_HYPOTHY",
"244.8":"ELIX_HYPOTHY",
"244.9":"ELIX_HYPOTHY",

"585.3":"ELIX_RENLFAIL",
"585.4":"ELIX_RENLFAIL",
"585.5":"ELIX_RENLFAIL",
"585.6":"ELIX_RENLFAIL",
"585.9":"ELIX_RENLFAIL",
"586":"ELIX_RENLFAIL",
"V42.0":"ELIX_RENLFAIL",
"V45.1":"ELIX_RENLFAIL",
"V56.0-V56.32":"ELIX_RENLFAIL",
"V568":"ELIX_RENLFAIL",
"V45.11" : "ELIX_RENLFAIL",
"V45.12":"ELIX_RENLFAIL",

"070.22":"ELIX_LIVER",
"070.23":"ELIX_LIVER",
"070.32":"ELIX_LIVER",
"070.33":"ELIX_LIVER",
"070.44":"ELIX_LIVER",
"070.54":"ELIX_LIVER",
"456.0":"ELIX_LIVER",
"456.1":"ELIX_LIVER",
"456.20":"ELIX_LIVER",
"456.21":"ELIX_LIVER",
"571.0":"ELIX_LIVER",
"571.2":"ELIX_LIVER",
"571.3":"ELIX_LIVER",
"571.40-571.49":"ELIX_LIVER",
"571.5":"ELIX_LIVER",
"571.6":"ELIX_LIVER",
"571.8":"ELIX_LIVER",
"571.9":"ELIX_LIVER",
"572.3":"ELIX_LIVER",
"572.8":"ELIX_LIVER",
"573.5":"ELIX_LIVER",
"V42.7":"ELIX_LIVER",


"531.41":"ELIX_ULCER",
"531.51":"ELIX_ULCER",
"531.61":"ELIX_ULCER",
"531.70":"ELIX_ULCER",
"531.71":"ELIX_ULCER",
"531.91":"ELIX_ULCER",
"532.41":"ELIX_ULCER",
"532.51":"ELIX_ULCER",
"532.61":"ELIX_ULCER",
"532.70":"ELIX_ULCER",
"532.71":"ELIX_ULCER",
"532.91":"ELIX_ULCER",
"533.41":"ELIX_ULCER",
"533.51":"ELIX_ULCER",
"533.61":"ELIX_ULCER",
"533.70":"ELIX_ULCER",
"533.71":"ELIX_ULCER",
"533.91":"ELIX_ULCER",
"534.41":"ELIX_ULCER",
"534.51":"ELIX_ULCER",
"534.61":"ELIX_ULCER",
"534.70":"ELIX_ULCER",
"534.71":"ELIX_ULCER",
"534.91":"ELIX_ULCER",

"042" : "ELIX_AIDS",
"042.0-044.9" :"ELIX_AIDS",

"200.00-202.38":"ELIX_LYMPH",
"202.50-203.01":"ELIX_LYMPH",
"238.6":"ELIX_LYMPH",
"273.3":"ELIX_LYMPH",
"203.02-203.82" : "ELIX_LYMPH",

"196.0-199.1":"ELIX_METS",
"209.70-209.75":"ELIX_METS",
"209.79":"ELIX_METS",
"789.51":"ELIX_METS",

"140.0-172.9":"ELIX_TUMOR",
"174.0-175.9":"ELIX_TUMOR",
"179" : "ELIX_TUMOR",
"179.0-195.8 ":"ELIX_TUMOR",
"209.00-209.24":"ELIX_TUMOR",
"209.25-209.30":"ELIX_TUMOR",
"209.30-209.36":"ELIX_TUMOR",
"258.01-258.03" :"ELIX_TUMOR",

"701.0":"ELIX_ARTH",
"710.0-710.9":"ELIX_ARTH",
"714.0-714.9":"ELIX_ARTH",
"720.0-720.9 ":"ELIX_ARTH",
"725":"ELIX_ARTH",
"286.0-286.9 ":"ELIX_COAG",
"287.1":"ELIX_COAG",
"287.3-287.5":"ELIX_COAG",
"649.30-649.34":"ELIX_COAG",
"289.84" :"ELIX_COAG",


"278.0":"ELIX_OBESE",
"278.00":"ELIX_OBESE",
"278.01":"ELIX_OBESE",
"278.03":"ELIX_OBESE",
"649.10-649.14":"ELIX_OBESE",
"V85.30-V85.39":"ELIX_OBESE",
"V85.41-V85.45":"ELIX_OBESE",
"V85.54":"ELIX_OBESE",
"793.91":"ELIX_OBESE",

"260":"ELIX_WGHTLOSS",

"260.0-263.9":"ELIX_WGHTLOSS",
"783.21-783.22" :"ELIX_WGHTLOSS",

"276.0-276.9" : "ELIX_LYTES",

"280.0":"ELIX_BLDLOSS",
"648.20-648.24" : "ELIX_BLDLOSS",

"280.1-281.9":"ELIX_ANEMDEF",
"285.21-285.29":"ELIX_ANEMDEF",
"285.9" :"ELIX_ANEMDEF",

"291.0-291.3":"ELIX_ALCOHOL",
"291.5":"ELIX_ALCOHOL",
"291.8":"ELIX_ALCOHOL",
"291.81":"ELIX_ALCOHOL",
"291.82":"ELIX_ALCOHOL",
"291.89":"ELIX_ALCOHOL",
"291.9":"ELIX_ALCOHOL",
"303.00-303.93":"ELIX_ALCOHOL",
"305.00-305.03":"ELIX_ALCOHOL",

"292.0":"ELIX_DRUG",
"292.82-292.89":"ELIX_DRUG",
"292.9":"ELIX_DRUG",
"304.00-304.93":"ELIX_DRUG",
"305.20-305.93":"ELIX_DRUG",
"648.30-648.34":"ELIX_DRUG",

"295.00-298.9":"ELIX_PSYCH",
"299.10":"ELIX_PSYCH",
"299.11":"ELIX_PSYCH",

"300.4":"ELIX_DEPRESS",
"301.12":"ELIX_DEPRESS",
"309.0":"ELIX_DEPRESS",
"309.1":"ELIX_DEPRESS",
"311" :"ELIX_DEPRESS"

}
# ICD-9 codes in the OSHPD data have been transformed from
# actual codes to codes with out decimal place.
# For example 301.12 is transformed as 30112.
# 300.4 ==> 3004
# icd_9_processed_map is map from these transformed codes
# to comorbid codes.
icd_9_processed_map = {}

for key, value in ICD9_RAW_MAP.items():
    # icd-9 code can be single value or range of values,
    # e.g: 345.6 or "305.20-305.93"
    if "-" not in key:
        icd_9_processed_map[key.strip().replace(".", "")] = value
        continue

    # The icd-9 code is range, e.g: "305.20-305.93"
    start = key.split("-")[0].strip()
    end = key.split("-")[1].strip()

    step_factor = 0.01
    #if len(start) > 5 or len(end) > 5:
    #    #print start, end
    #    step_factor = 0.01

    prefix = ''
    if start.startswith("V"):
        start = start[1:]
        end = end[1:]
        prefix = 'V'

    start = float(start)
    end = float(end)

    while start <= end + 0.001:
        "Generate two icd-9 code for two decimal places"

        key = prefix + "%.1f"%(start)
        key = key.strip().replace(".", "")
        icd_9_processed_map[key] = value

        key = prefix + "%.2f"%(start)
        key = key.strip().replace(".", "")
        icd_9_processed_map[key] = value

        start  = start + step_factor


def get_comorbidities():
    """
    :return: List of comorbidities.
    """
    disease_set = set(icd_9_processed_map.values())
    return sorted([xx for xx in disease_set])

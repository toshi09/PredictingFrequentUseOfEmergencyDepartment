#from column_index_map import *
ADMIT_YEAR_IDX = 24
SRC_COL_IDX= 28
def rem(inputfile,outputfile):
    filehandle = open(inputfile)
    outhandle = open(outputfile, "w")
    garbage = filehandle.readline()

    for line in filehandle:
        values = line.strip().split(",")

        if values[SRC_COL_IDX] == '1':
            outhandle.write(line)
            print values[ADMIT_YEAR_IDX]
            print values[SRC_COL_IDX]
    outhandle.close()
    filehandle.close()


rem('/Users/oshpddata/Desktop/OSHPD2016/OSHPD_ALLCAUSE.csv','/Users/oshpddata/Desktop/vikhyati/OSHPD_ALLCAUSE_VISIT_ALLYEARS.csv')

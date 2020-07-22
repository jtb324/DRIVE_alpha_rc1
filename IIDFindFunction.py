# This file contains the functions used to determine how many total individuals contain some variant and how many individuals contain multiple variants

###################################################################################
# importing modules

import os
from os import path
import sys
import csv
import pandas as pd
import numpy as np
import logging

###################################################################################
# importing necessary functions from other files

from write_path import writePath
from check_directory import check_dir
from csv_dict_writer import csvDictWriter

###################################################################################
# Function to find the total number of variants


def totalVariantID(recodeFile, writeLocation):
    '''this is a function for the inner loop that will search through each position in the row and when it encouters a one or a two it will add that to the idlist and then return so that the outer loop in the main script moves on to the next row.'''

    logging.info('Using raw recode file found at {}'.format(recodeFile))

    if path.exist(recodeFile):

        with open(recodeFile[0]) as geno_file:

            headerLine = next(geno_file)  # This skips the 1st row

            # This next two lines create lists for the total variants and the multivariants ids
            totalVariantList = []

            for row in geno_file:  # This iterates through each row in the file

                row = row.split()  # This will split the row by white space

                genoRow = row[6:]

                if '1' in genoRow or '2' in genoRow:

                    totalVariantList.append(row[1])

            print("The total number of individual carrier of at least one desired variant is: {}".format(
                len(totalVariantList)))

            logging.info("The total number of individual carrier of at least one desired variant is: {}".format(
                len(totalVariantList)))

            writeDirectory = writePath(writeLocation, "totalVariantIDList.txt")

            MyFile = open(
                writeDirectory, 'w')

            for element in totalVariantList:
                MyFile.write(element)
                MyFile.write('\n')
            MyFile.close()

    else:

        print("The raw recoded file at {} was not found.".format())
        logging.error("The raw recoded file at {} was not found.".format())

############################################################################################
# This function determines all the individuals who have a specific variant


def singleVariantAnalysis(recodeFile, write_path, reformat, fileName):
    '''This function returns a csv containing a list of individuals who carry each variants. It takes a recoded variant file, a path to write the output to, and a file name'''

    logger = logging.getLogger(write_path+'/single_variant_analysis.log')

    try:

        raw_file = pd.read_csv(recodeFile[0], sep=" ")

    except FileNotFoundError:

        print("The raw recoded file at {} was not found.".format(
            recodeFile))

        logger.error("The raw recoded file at {} was not found.".format(
            recodeFile))

        sys.exit(1)

    logger.info('Using raw recode file found at {}'.format(recodeFile))

    column_list = list(raw_file.columns[6:].values)

    var_dict = dict()

    var_dict_reformat = dict()

    iid_list_reformat = []

    variant_list_reformat = []

    for column in column_list:

        iid_list = []

        index_list = raw_file.index[raw_file[column].isin([1, 2])].tolist()

        for i in index_list:
            iid_list.append(raw_file.loc[i, "IID"])

        if column in var_dict:  # This checks to see if the indexTuple is already a key in the multiVarDict

            # If true then it just appends the IID to the value of the multiVarDict
            var_dict[column].append(iid_list)

        else:

            # If false then it creates a new multiVarDict input with that key and value
            var_dict[column] = iid_list

        if reformat == True:

            for i in index_list:

                if "IID" and "Variant ID" in var_dict_reformat:

                    var_dict_reformat["IID"].append(raw_file.loc[i, "IID"])

                    var_dict_reformat["Variant ID"].append(column)

                else:

                    var_dict_reformat["IID"] = [raw_file.loc[i, "IID"]]
                    var_dict_reformat["Variant ID"] = [column]

    if var_dict_reformat:

        var_reformat_df = pd.DataFrame(
            var_dict_reformat, columns=["IID", "Variant ID"])

        reformat_directory = check_dir(write_path, "reformated")

        var_reformat_df.to_csv(
            writePath(reformat_directory, "single_var_list_reformat.csv"), index=False)

        logger.info('The list of IIDs for each probe id were written to this filepath, {}'.format(
            writePath(reformat_directory, "single_var_list_reformat.csv")
        ))

    elif reformat and not bool(var_dict_reformat):

        print("There were no individuals found so there dictionary was not written to a csv file.")

    logger.info(
        'writing the dictionary of individuals who carry a variant to a file...')

    csvDictWriter(
        var_dict, write_path, fileName, logger)


############################################################################################
# Function that counts how many individuals carry a set of variants

def individualCount(multiVarDict, writePath, logger):
    '''This function will create a new multiVarDict where the keys are the index of each variant and the values are the number of individuals containing those variants'''

    # This uses a map function. The .items makes of tuple of key:value pairs and then
    # the lambda function takes the items as a input and updates the original dictionary by
    # by assigning the length of the second element of the tuple to the correct key
    multiVarDict = dict(map(lambda x: (x[0], len(x[1])), multiVarDict.items()))

    # This uses the csvDictWriter function to write the individCountDict to a csv file named IndividualCount.csv

    logging.info(
        'Writing the number of individuals who carry any variants to a csv\
            file called IndividualCount.csv ...')

    csvDictWriter(multiVarDict,
                  writePath, "IndividualCount.csv", logger)

################################################################################################
# Function that groups individuals by which variants they carry


def multiVariantAnalysis(recodeFile, write_path, reformat, fileName):
    '''This function preforms the main multiple variant analysis and will make two dictionaries. One multiVarDict contains key that are the index of each variant from the original PLINK recode file (starts at the seventh position because the first 6 values are not important info in this function) and then the values are a list of individuals who contain those variants. The second multiVarDict contains the same keys, but the values are the number of individuals which carry those variants'''

    logger = logging.getLogger(write_path+'/multi_variant_analysis.log')

    #Reading in the file ########################################
    try:

        raw_file = pd.read_csv(recodeFile[0], sep=" ")

    except FileNotFoundError:

        print("The raw recoded file at {} was not found.".format(
            recodeFile))

        logger.error("The raw recoded file at {} was not found.".format(
            recodeFile))

        sys.exit(1)

    logger.info('Using the raw recode file at {}'.format(recodeFile))

    #############################################################

    column_list = list(raw_file.columns[6:].values)

    multi_var_carriers = dict()

    multi_var_carriers_reformat = dict()

    for ind in raw_file.index:

        index_1 = raw_file.loc[ind, column_list][raw_file.loc[ind,
                                                              column_list] == 1].index.tolist()

        index_2 = raw_file.loc[ind, column_list][raw_file.loc[ind,
                                                              column_list] == 2]. index.tolist()

        index_list = index_1 + index_2

        index_tuple = tuple(index_list)

        if len(index_tuple) > 1:

            if index_tuple in multi_var_carriers:

                multi_var_carriers[index_tuple].append(
                    raw_file.loc[ind, "IID"])

            else:

                multi_var_carriers[index_tuple] = [raw_file.loc[ind, "IID"]]

            if reformat == True:

                for index in index_tuple:

                    if "IID" and "Variant List" in multi_var_carriers_reformat:

                        multi_var_carriers_reformat["IID"].append(
                            raw_file.loc[ind, "IID"])
                        multi_var_carriers_reformat["Variant List"].append(
                            index)

                    else:

                        multi_var_carriers_reformat["IID"] = [
                            raw_file.loc[ind, "IID"]]
                        multi_var_carriers_reformat["Variant List"] = [
                            index]

    # This converts the reformated dictionary to a dataframe
    if multi_var_carriers_reformat:

        reformat_df = pd.DataFrame(multi_var_carriers_reformat, columns=[
            "IID", "Variant List"])

        reformat_directory = check_dir(write_path, "reformated")

        # This writes the reformated dataframe as a csv file
        reformat_df.to_csv(
            writePath(reformat_directory, "multi_var_reformated.csv"), index=False)

        logging.info('reformated file written to {}'.format(
            writePath(reformat_directory, "multi_var_reformated.csv")))

    elif reformat and not bool(multi_var_carriers_reformat):

        print("There were no individuals found within the reformated csv so the dictionary was not written to a csv file.")

    # This writes the original formated multivar_carrier dictionary to a csv
    logger.info(
        'Writing the number of individuals who carry multiple variants to a csv file...')

    csvDictWriter(
        multi_var_carriers, write_path, fileName, logger)

    # This passes the multiVarDict to the individualCount function to determine how many individuals have each combination of variants
    individualCount(multi_var_carriers, write_path, logger)

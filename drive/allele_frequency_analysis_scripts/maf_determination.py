import pandas as pd
import glob
import os
from os import path
import re
import population_filter_scripts
# need to gather all of the single var list


def get_var_files(directory: str, file_id: str) -> list:

    cur_dir = os.getcwd()

    os.chdir(directory)

    file_list = []

    for file in glob.glob(file_id):

        full_file_path = "".join([directory, file])

        file_list.append(full_file_path)

    os.chdir(cur_dir)

    return file_list


def get_chr_num(carrier_file: str) -> str:

    match = re.search(r'chr\d_', carrier_file)

    if match:
        chr_num = match.group(0)

        # removing the _ in the file name
        chr_num = chr_num[:len(chr_num) - 1]

    else:
        match = re.search(r'chr\d\d.', carrier_file)

        chr_num = match.group(0)

        # removing the _ in the file name
        chr_num = chr_num[:len(chr_num) - 1]

    return chr_num


def get_allele_frq(carrier_file_list: list, raw_file_list: list,
                   pop_info_filepath: str, pop_code: str, output_path: str):
    '''This is the function that determines the minor allele frequency of the 
    variants and then writes it to a file'''

    frequency_file_path: str = "".join(
        [output_path, "carrier_analysis_output/allele_frequencies.txt"])

    # deleting the previous file so that it does not write repeating values
    if path.exists(frequency_file_path):

        os.remove(frequency_file_path)

    # opening the file to write to it
    with open(frequency_file_path, "a+") as myFile:

        myFile.write("chr\tvariant_id\tallele_freq\n")

        for file in carrier_file_list:

            chr_num = get_chr_num(file)

            alt_chr: str = "".join([chr_num, "."])
            chr_num = "".join([chr_num, "_"])

            car_raw_file_tuple = [
                (carrier_file, raw_file) for carrier_file in carrier_file_list
                for raw_file in raw_file_list
                if alt_chr in carrier_file and chr_num in raw_file
            ]

            carrier_file = car_raw_file_tuple[0][0]

            raw_file = car_raw_file_tuple[0][1]

            # getting all the variants in a list
            carrier_file_df = pd.read_csv(carrier_file,
                                          sep=",")
            print(carrier_file_df)
            variant_list = list(set(carrier_file_df["Variant ID"].values.tolist()))

            print(variant_list)
            # loading in the raw file into a dataframe and filtering it just for the desired population code using the Pop_Filter code
            pop_filter = population_filter_scripts.Pop_Filter(
                pop_info_filepath, raw_file)

            pop_info_df, recode_df = pop_filter.load_files()

            pop_info_df = pop_filter.get_pop_info_subset(pop_info_df, pop_code)

            raw_file_df = pop_filter.filter_recode_df(pop_info_df, recode_df)

            for variant in variant_list:
                # get all rows for that variant in the raw-file_df

                total_allele_count = len(raw_file_df) * 2

                carry_allele_df = raw_file_df[raw_file_df[variant].isin(
                    [1, 2])][variant]

                minor_allele_count = carry_allele_df.count()

                allele_frq = minor_allele_count / total_allele_count

                myFile.write(
                    f"{chr_num[:len(chr_num)-1]}\t{variant}\t{allele_frq}\n")

        myFile.close()


def determine_maf(car_dir: str, raw_dir: str, pop_file: str, pop_code: str,
                  output: str):
    "function to run"
    carrier_file_list = get_var_files(car_dir, "*.single_variant_carrier.csv")

    raw_file_list = get_var_files(raw_dir, "*.raw")

    get_allele_frq(carrier_file_list, raw_file_list, pop_file, pop_code,
                   output)
# This script is designed to take the output and provide something more like davids ideal format
import pandas as pd
import glob
import os
import re

# need to get list of carriers
# First function will be designed to get a glob of files


def get_files(directory: str, file_id: str) -> list:

    cur_dir: str = os.getcwd()
    os.chdir(directory)

    file_list: list = []

    for file in glob.glob(file_id):

        full_file_path: str = "".join([directory, file])

        file_list.append(full_file_path)

    os.chdir(cur_dir)

    return file_list


def form_genotype_df(map_file_path: str, ped_file_path: str) -> pd.DataFrame:
    '''This function will form a dictionary of dictionaries where the outer key is the iid, 
    the inner key is the variant and the inner value is the genotype string'''

    # form three list for the iid, the variant, and the genotype string
    iid_list: list = []
    variant_list: list = []
    geno_list: list = []

    # opening the ped file
    with open(ped_file_path, "r") as ped_file:

        # iterating through row
        for row in ped_file:

            # split row
            row: list = row.split(" ")

            # getting only the genotype portion of the row

            geno_row: list = row[6:]

            # getting the iid
            iid: str = row[1]

            # using enumerate to iterate through each row of the file and get the index of the row
            with open(map_file_path, "r") as map_file:

                for index, map_row in enumerate(map_file):

                    map_row: list = map_row.split("\t")

                    # getting the variant id
                    variant_id: str = map_row[1]

                    # getting the genotype index positions
                    start_indx: int = index * 2

                    second_indx: int = start_indx + 1

                    # getting the genotypes from the geno_row
                    allele_1: str = geno_row[start_indx]

                    allele_2: str = geno_row[second_indx]

                    # appending to all the list
                    iid_list.append(iid)

                    variant_list.append(variant_id)

                    geno_list.append("".join([allele_1, allele_2]).strip("\n"))

    # inserting values into the genotyped dict
    genotype_dict = {
        "IID": iid_list,
        "Variant": variant_list,
        "Genotype": geno_list
    }

    genotype_df = pd.DataFrame.from_dict(genotype_dict)

    return genotype_df


def get_chr_num(file: str, pattern: str, alt_pattern: str) -> str:
    '''This function returns the chromosome number'''

    match = re.search(pattern, file)

    if match:

        chr_num: str = match.group(0)

        # removing the _ in the file name
        chr_num = chr_num[:len(chr_num)-1]

    else:

        match = re.search(alt_pattern, file)

        chr_num: str = match.group(0)

        # removing the _ in the file name
        chr_num = chr_num[:len(chr_num)-1]

    return chr_num


def run(args):
    "function to run"
    # Getting list of the carrier files, the map files, the ped files and the allpair_files
    carrier_files: list = get_files(args.directory, "*single_variant_list.csv")

    map_files: list = get_files(args.plink_dir, "*.map")

    ped_files: list = get_files(args.plink_dir, "*.ped")

    allpair_files: list = get_files(args.directory, "*allpair.new.txt")

    # Iterating through the ped files
    for file in ped_files:

        # This gets the chromosome number for the files
        chr_num: str = get_chr_num(file, r"chr\d_", r"chr\d\d_")

        map_file: str = [
            map_file for map_file in map_files if chr_num in map_file][0]

        print(map_file)

        genotype_dict = form_genotype_df(map_file, file)


def main():
    parser = argparse.ArgumentParser(
        description="")

    parser.add_argument("--input", help="This argument takes the initial input file which contains variants for multiple chromosomes and splits it into multiple files, one for each chromosome",
                        dest="", type="", nargs="", required="Bool")

    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
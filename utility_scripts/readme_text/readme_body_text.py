# This file contains text that will be used in making the readmes of each file

# This next section contains text that will be put in the main readme file within the parent directory
main_parameter_text: str = "* *Information about parameters used during the run can be found in the file mega_run.log within the main directory*\n\n"

main_directory_header: str = "## Direectory Structure:\n\n"

main_directory_text: str = "* **carrier_analysis_output**: This directory contains output that list iids that are identified as carrying a variant of interest on the MEGA_Ex array. These files usually end in single_variant_carrier.csv. This directory also has a file 'allele_frequencies.txt' that describes the allele frequencies for each variant based on Piper's dataset.\n\n* **formated_ibd_output**: This directory contains the output from the steps of the program that convert the ibd_files to a more human readable format. These files are the .small.txt.gz files. There are also output files from the steps that determine which pairs share segments. These files are the allpair.txt files. This directory also contains a file titled confirmed_carriers.txt that list which of the carriers identified on the MEGA array are actual confirmed carriers based on the shared segment analysis.\n\n* **networks**: This directory contains information about the percent of confirmed carriers for each variant (this is found in the carriers_in_networks.csv file) and about which network the confirmed carriers belong to (This is found in the network_groups.csv file).\n\n* **plink_output_files**: This directory contains the output from running the recode, recodeA, and freq option for plink.\n\n* **shell_scripts**:This directory contains the script that was used to run the program\n\n* **haplotype_analysis**: This directory contains output files that describe the start and the end positions of the shared haplotypes as well as the length of the haplotype for each pair (This is found in the haplotype_info.txt file). This directory also contains a file called nopairs_haplotype_analysis.txt file that list haplotypes that do not pass the haplotype analysis. There is also another file called all_genotypes.txt that lists the genotypes at each variant for all individuals within the provided dataset.\n"

# The next section contains text that will be inserted into the different
plink_readme_body_text: str = "* This directory contains the output from plink while running the initial steps of the program. There should be a ped, map, raw, freq file, and a log file output by plink.This files will be split up per chromosome. The main three types of files used during the analysis are the ped, map, and the raw files.\n"

# This next section contains text that will be placed within the readme of the carrier_analysiss_output directory
carrier_analysis_body_text: str = "* This directory contains the output that describes which IIDs were detected as carrier specific variants of interest\n\n* There are three main types of files and then a subdirectory. These are described below.\n\n* **allele_frequencies.txt**: This file describes the allele frequencies within the MEGA Ex array dataset for the provided variants of interest. There are three columns within this folder: chr, variant_id, and allele_freq. This columns are pretty self explanatory. The chromosome number still has the  chr at the beginning but this will be changed later on. The variant_id uses the mega array probe id not the rsid. The allele frequencies are a decimal value not a percentage.\n\n* **.single_variant_carrier.csv**: This file actually list the IIDs that were identified as carrying the variant of interest within the MEGA array dataset. This file has two columns where the first one is the variant of interest and the second column is the list of IIDs who were carrying this variant (These IIDs may be present in list for other variants if they carry more than one variant).\n\n* **.total_variant_ID_list.txt**: This file contains a list of each IID who is listed as carrying any variant of interest on the MEGA array. It has a single column and list an IID per row. This file is more of a record keeping process to just get an idea of how many individuals there are total.\n\n* **reformated/**: This subdirectory contains the same output as the .single_variant_carrier.csv file except it is in a format that is easier for a program that is not python to work with. The directory has a file for each chromosome being used in the analysis and contains two columns: IID and variant ID. The first column list one IID and then the second column listthe variant that the specific IID is listed as carrying. This means that each row has one IID and one variant. This format will also show the same IID more then once if the IID is identified as carrying more than one variant of interest.\n"

# This section contains text for the README that will be placed in the
# formated_ibd_output directory
formatted_ibd_dir_body_text_1: str = "* This directory contains the output from the mid steps where grids that share segments are identified from the ILASH and hapibd files.\n\n* This directory has several files of interest:\n\n    * **confirmed_carriers.txt**: This file indicates which of the identified carriers of a variant of interest were confirmed carriers by the networks analysis. This five has five columns: IID, variant_id, genotype, confirmed_status, chr. These columns just list the  grid IID, the variant of interest for that grid, the genotype that the grid is labeled as having from the MEGA array, the confirmed status which will be 1 if they were identified as being part of a network or 0 if they were not, and then the chromosome number.\n\n* **nopairs_identified.txt**: This file list the id of each variant that fails the step that converts the shared segment format from the hapibd and ilash format to a more human readable format.\n\n* **no_carriers_in_file.txt**: This file list the variants where there were no IIDs identified as carrying the variant on the MEGA array. These variants also fail the analysis like those in the nopoairs_identified.txt file but this failure has a significant difference and was therefore determined to necessitate a different output file.\n\n* **.allpair.txt**: These files list the pairs that were identified as sharing segments. The files have six columns: IBD_programs, pair_1, pair_2, carrier_status, potential_missed_carrier, connected_carriers. These columns describe which IBD_programs identified the pairs (in this case it is either hapibd or ilash or both), the IID for the first individual in the pair, the IID for the second individual in the pair, whether or not the second individual was identified as a carrier, meaning this will be a 1 if they were identified and a zero if not (The first individual is always a carrier in the way the code is set up), whether the individual is a suspected carrier or not (This will again be a 1 or 0), and how many other carriers they are connected to (This value was only determined for pairs where the second individual is not a carrier).\n\n* **variant_lists**: This directory has files for each variant that list the IIDs that were identified as carrying that variant. These files are formed during the shared segment analysis and are required to determine which IIDs to use to search for pairs.\n\n* **reformated_ibd_output**: This directory contains all the .small.txt.gz files for each variant. These files are the result of converting the hapibd and ilash output to a more human readable version. These files are also used to form the allpair.txt files\n"

formatted_ibd_dir_body_text_2: str = "* *More infomation about the location of the iLASH and hapid files cn be found in the mega_run.log file*"

# This next section contains text for the README that will be placed in
# the haplotype analysis directory
haplotype_analysis_body_text: str = "* This directory contains the output from a few of the haplotype analysis scripts that the program runs. There are a few files in this directory.\n\n* **all_genotypes.txt**: This file list the genotypes for a specific variant for all individuals inthe provided array dataset for a specific ancestory (if ancestory is specified, otherwise it would be for everybody). This file has five columns: IID, variant_id, genotype, confirmed_status, and chr. These columns list the IID of the grid, the variant id, the genotype at that position based on the the genotyping in the MEGA array, whether or not the IID was identified as a confirmed carrier (This column will have a 1 if they were confirmed, a 0 if not, and N/A if they were never identified as being a carrier), and then the chromosome number.\n\n* **nopairs_haplotype_analysis.txt**: This file records the variants that fail the haplotype analysis script. The variant fails if the pair is not found within the hapibd or ilash file (WORK ON THIS EXPLANATION). It has two columns: variant and chr. The first column list the variant id and the second column list the chromsome.\n\n* **haplotype_info.txt**: This file list information about the length of the haplotype segments for each pair for both hapibd and iLASH. This file has 11 columns: pair_1, pair_2, chr, variant_id, network_id, hapibd_start, hapibd_end, hapibd_len, ilash_start, ilash_end, ilash_len. The columns list the IID of the first individual in the pair, the IID of the second individual, the chromosome number, the variant id, the network id which is just a number, then the start base position of the haplotype as identified by hapibd, the end base position as identified by hapibd, the length of the haplotype in centimorgans, and then the final three columns repeat these values for ilash.\n"

# This next section contains text for the README that will be paced in
# the networks directory
networks_body_text: str = "* This directory contains output that describes the networks found for each variant. In the main directory there is a file and then a subdirectory:\n\n* **carriers_in_networks.csv**: This file list the percentage of identified carriers based on the mega array that were confirmed by the segment analysis. There are two columns. The first column list the variant id and the second column list the percentage of confirmed carriers.\n\n* **network_imgs/**: This subdirectory was original designed to have pdf images of the networks but this purpose is not used at the moment. Instead, it has a file called 'network_groups.csv'. This file list if an IID is in a network and which network it is a part of if it is in a network. The file has five columns: IID, In Network, Network ID, variant_id, chr_num. These columns tell the grid IID of the identified carrier, The next column list whether they are in the network or not (This value will be 1 if they are in the network and 0 if they are not), The network id that the IID belongs to (This will be a number or empty if it doesn't belong to a network), the id of the variant of interest, and the chromosome number."

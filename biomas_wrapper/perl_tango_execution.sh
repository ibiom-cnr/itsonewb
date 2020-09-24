#! /bin/bash

clear
script=$(basename $0)

help="This script performs the bowtie2 automatic execution
usage ./tango_execution.sh -d guide_tree
Options:
	-h    stampa questo help
	-d 	  albero guida per l'esecuzione di TANGO
"

while getopts ":hd:" opzione
do
	case "${opzione}" in 
	h) echo -e "\n$help";exit 1;;
	d) database=${OPTARG};;
	*) echo -e "\nÈ stata inserita un'opzione non valida.\n\n $help";exit 1;;
	esac
done

base_name=$(awk 'BEGIN { RS = "\n" } ; { FS = "\t" } ; { ORS = "\n" } { print $1 }' quality_check_and_consensus.log)
echo $base_name

database=$(pwd)/$database
#classificazione tassonomica delle sequenze che possono essere assegnate a livello di specie
tango_input=$(pwd)/$(grep over97 bowtie2-execution.log)
echo $tango_input
if [[ -e "$tango_input" && -s "$tango_input" ]]
	then
		#tango_output=tango_input/bowtie_result
		echo Tango on Bowtie2 mapping data
		cp -r /home/galaxy/New_TANGO_perl_version .
		cd New_TANGO_perl_version
		perl tango.pl --taxonomy $database --matches $tango_input --output ../ITSoneDB_fungi_mapping_data/bowtie_result_over_97
		cd ..
	else
		echo No input data usefull for tango computation
	fi

#classificazione tassonomica delle sequenze che non possono essere assegnate a livello di specie
tango_input=$(pwd)/$(grep under97 bowtie2-execution.log)
if [[ -e "$tango_input" && -s "$tango_input" ]]
	then
		#tango_output=tango_input/bowtie_result
		echo Tango on Bowtie2 mapping data
		cp -r /home/galaxy/New_TANGO_perl_version .
		cd New_TANGO_perl_version
		perl tango.pl --taxonomy $database --q-value 1 --matches $tango_input --output ../ITSoneDB_fungi_mapping_data/bowtie_result_under_97
		cd ..
	else
		echo No input data usefull for tango computation
	fi


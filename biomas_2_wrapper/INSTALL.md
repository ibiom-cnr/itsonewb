# BioMaS Galaxy
The *BioMaS (Bioinformatic analysis of Metagenomic ampliconS)* is an automated pipeline designed to taxonomically
classify metabarcoding data \[[PMID: 26130132](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4486701/)\].  

## Requirements
- Xfvb is needed to run ete2, without X.org server.
    * On CentOS:  
    ```
    # yum install xorg-x11-server-Xvfb
    ```
    * On Ubuntu:    
    ```
    # apt-get install libxrender1 libsm6 libxt6
    ```
- [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/);  
- [FLASh](https://ccb.jhu.edu/software/FLASH/);  
- [trim-galore!](https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/);  
- [vsearch](https://github.com/torognes/vsearch);  
- [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml);  
- [TANGO](https://sourceforge.net/projects/taxoassignment/) [Copy the New_TANGO_perl_version in `/home/galaxy`].  

## Preparation
The `biomas_function.pyx` needs to be compiled by using the script `setup.py`, as follow:  
```
python setup.py build_ext --inplace
```


## Usage
Following are listed listed the three python scripts that allows to perform **BioMaS** on ITS1 data, by using
**ITSoneDB** \[[PMID: 29036529](https://pubmed.ncbi.nlm.nih.gov/29036529/?from_term=Fosso+B&from_cauthor_id=26130132&from_pos=8)\]
as reference database.  

### Read Merging and dereplication
This step encompasses three procedures:  
1) it evaluates sequences qualities by using *FastQC*;  
2) Merge PE reads by using *flash* and dereplicat them by using *vsearch*;
3) trim low quality regions of unmerged reads by exploiting *trim-galore!*.  

Following the help page of the script:  
```
python quality_check_and_consensus.py -h
usage: quality_check_and_consensus.py [-h] -p1 PAIRED1 [-p2 PAIRED2] -b
                                      BASENAME [-t THREADS] [-f FRAGMENT]
                                      [-F FUNCTION_FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  -p1 PAIRED1, --paired1 PAIRED1. [MANDATORY]
                        paired-end fastq file R1.
  -p2 PAIRED2, --paired2 PAIRED2. [MANDATORY]
                        paired-end fastq file R2.
  -b BASENAME, --basename BASENAME. [MANDATORY]
                        sample name
  -t THREADS, --threads THREADS
                        number of threads
  -f FRAGMENT, --fragment FRAGMENT
                        fragment length (optional)
  -F FUNCTION_FOLDER, --Function_folder FUNCTION_FOLDER
                        the absolute or relative path to the folder containing
                        the Cyhton functions
```
An example of its application is available below (Please not that it expects the BioMaS functions module is in the working folder):  
```
python quality_check_and_consensus.py \
    -p1 fungi-illumina1.fq.gz \
    -p2 fungi-illumina2.fq.gz \
    -b full_test \
    -t 10 \
```  

### Reference mapping and taxonomic classification
This step encompasses three procedures:  
1) it maps metabarcode data on ITSoneDB fasta collection by using bowtie2;  
2) the alignments are filtered according to identity percentage and query coverage;
3) it performs taxonomic annotation by using TANGO.  

Following the help page of the script:
```
python bowtie2-execution_ITSoneDB.py -h
usage: bowtie2-execution_ITSoneDB.py [-h] -v MAPPING_FILE -i BOWTIE2_INDEXES
                                     [-F FUNCTION_FOLDER] [-t THREADS] -T
                                     TANGO_FOLDER -d TANGO_DMP

optional arguments:
  -h, --help            show this help message and exit
  -v MAPPING_FILE, --mapping_file MAPPING_FILE
                        tabular file containing the correspondence between
                        ITSoneDB accession and NCBI taxonomy ID. [MANDATORY]
  -i BOWTIE2_INDEXES, --bowtie2_indexes BOWTIE2_INDEXES
                        bowtie2 indexes path. [MANDATORY]
  -F FUNCTION_FOLDER, --Function_folder FUNCTION_FOLDER
                        the absolute or relative path to the folder containing
                        the Cyhton functions
  -t THREADS, --threads THREADS
                        number of available threads/processors
  -T TANGO_FOLDER, --tango_folder TANGO_FOLDER
                        path to the TANGO folder. [MANDATORY]
  -d TANGO_DMP, --tango_dmp TANGO_DMP
                        tango dmp file. [MANDATORY]
```  
An example of its application is available below (Please not that it expects the BioMaS functions module is in the working folder):  
```
python bowtie2-execution_ITSoneDB.py \
    -v /export/BRUNO_JUNE2020/bowtie2_indexes_rel138/ITSoneDB_rel138.json.gz \
    -i /export/BRUNO_JUNE2020/bowtie2_indexes_rel138/ITSITSoneDB_all_euk_r138   \
    -t 10 \
    -T ~/TANGO/New_TANGO_perl_version/ \
    -d /export/BRUNO_JUNE2020/bowtie2_indexes_rel138/ITSoneDB_1.138
```  

### Tree building and taxonomic summary preparation
This step encompasses two procedures:  
1) taxonomic tree building according to taxonomic assignments;  
2) summary files preparation.  

Following the help page of the script:
```
python new_tree_builder_for_perl_tango.py -h
usage: new_tree_builder_for_perl_tango.py [-h] -d NODE_FILE
                                          [-F FUNCTION_FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  -d NODE_FILE, --node_file NODE_FILE
                        tabular file containing the annotation info needed to
                        build the tree
  -F FUNCTION_FOLDER, --Function_folder FUNCTION_FOLDER
                        the absolute or relative path to the folder containing
                        the Cyhton functions
```  
An example of its application is available below (Please not that it expects the BioMaS functions module is in the working folder):  
```
python new_tree_builder_for_perl_tango.py \
    -d /export/BRUNO_JUNE2020/bowtie2_indexes_rel138/visualization_ITSoneDB_r131.dmp
```  

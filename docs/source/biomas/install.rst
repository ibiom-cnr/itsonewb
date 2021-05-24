Installation
============

Preliminary requirements
------------------------

BioMaS exploits Ete2, which run under python 2 and  qt ``4.8.7``. Moreover Ete2 needs a running X.org Server. To workaround this requirement, no Xorg is runningi on a server machine, Xfvb is used to correctly run run ete2, without X.org server.

To innstall Xvfb On CentOS:

::

  # yum install xorg-x11-server-Xvfb


On Ubuntu:

::

  # apt-get install libxrender1 libsm6 libxt6 xvfb

Install on Galaxy
-----------------

Galaxy is able to automatically solve conda dependecies when a tool is started.

To install BioMaS on Galaxy:

#. Clone the ITSoneWb repository

   ::

     git clone https://github.com/ibiom-cnr/itsonewb.git

#. Add BioMaS entry in the galaxy ``tool_conf.xml`` file with your favourite editor:

   ::

     <section name="BioMaS" id="biomas">
         <tool file="/path_to_itsonewb/itsonewb/biomas_2_wrapper/biomas_wrapper.xml" />
     </section>

#. Finally restart Galaxy.

Install as standalone tool
--------------------------

The following tools are used in BioMaS, and can be installed using `conda <https://docs.conda.io/en/latest/miniconda.html>`_, thorough its `Bioconda channel <https://bioconda.github.io/>`_:

#. `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_,

#. `FLASh <https://ccb.jhu.edu/software/FLASH/>`_,

#. `trim-galore <https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/>`_

#. `vsearch <https://github.com/torognes/vsearch>`_,

#. `bowtie2 <http://bowtie-bio.sourceforge.net/bowtie2/index.shtml>`_,

#. `TANGO <https://sourceforge.net/projects/taxoassignment>`_ (Copy the New_TANGO_perl_version in `/home/galaxy`).  

The following command will install BioMaS dependencies in a virtual environment called ``biomas``

::

  $ conda create --name biomas python=2.7 qt=4.8.7 fastqc bowtie2 numpy pysam biopython FLASH trim-galore ete2 xvfbwrapper vsearch argcomplete tbb=2020.2 cython -c conda-forge -c bioconda

To activate the virtual environment:

::

  $ conda activate biomas

Preparation
^^^^^^^^^^^
The `biomas_function.pyx` needs to be compiled by using the script `setup.py`, as follow:

:: 

  python setup.py build_ext --inplace

Usage
^^^^^

In the following are listed listed the three python scripts that allows to perform **BioMaS** on ITS1 data, by using `ITSoneDB <https://pubmed.ncbi.nlm.nih.gov/29036529/?from_term=Fosso+B&from_cauthor_id=26130132&from_pos=8>`_ as reference database.  

``Read Merging and dereplication``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This step encompasses three procedures:  

#. it evaluates sequences qualities by using **FastQC**;
#. merge PE reads by using *flash* and dereplicat them by using **vsearch**;
#. trim low quality regions of unmerged reads by exploiting **trim-galore**.  

Following the help page of the script:

::

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

An example of its application is available below (Please not that it expects the BioMaS functions module is in the working folder):  

::

  python quality_check_and_consensus.py \
    -p1 fungi-illumina1.fq.gz \
    -p2 fungi-illumina2.fq.gz \
    -b full_test \
    -t 10 \
  
``Reference mapping and taxonomic classification``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This step encompasses three procedures:  

#. it maps metabarcode data on ITSoneDB fasta collection by using bowtie2;  

#. the alignments are filtered according to identity percentage and query coverage;

#. it performs taxonomic annotation by using TANGO.  

Following the help page of the script:

::

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

An example of its application is available below (Please not that it expects the BioMaS functions module is in the working folder):  

::

  python bowtie2-execution_ITSoneDB.py \
      -v /path_to/bowtie2_indexes_rel138/ITSoneDB_rel138.json.gz \
      -i /path_to/bowtie2_indexes_rel138/ITSITSoneDB_all_euk_r138   \
      -t 10 \
      -T ~/TANGO/New_TANGO_perl_version/ \
      -d /path_to/bowtie2_indexes_rel138/ITSoneDB_1.138

``Tree building and taxonomic summary preparation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This step encompasses two procedures:  
#. taxonomic tree building according to taxonomic assignments;  
#.  summary files preparation.  

Following the help page of the script:

::

  Python new_tree_builder_for_perl_tango.py -h
  Usage: new_tree_builder_for_perl_tango.py [-h] -d NODE_FILE
                                            [-F FUNCTION_FOLDER]
  
  Optional arguments:
    -h, --help            show this help message and exit
    -d NODE_FILE, --node_file NODE_FILE
                          tabular file containing the annotation info needed to
                          build the tree
    -F FUNCTION_FOLDER, --Function_folder FUNCTION_FOLDER
                          the absolute or relative path to the folder containing
                          the Cyhton functions
  
An example of its application is available below (Please not that it expects the BioMaS functions module is in the working folder):  

::

  python new_tree_builder_for_perl_tango.py \
      -d /path_to/bowtie2_indexes_rel138/visualization_ITSoneDB_r131.dmp

Reference Data
--------------

ITSoneDB (r138) BioMaS indexes can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_3b4918e0a982493e8c3ebcc43586a2a8/ITSoneWB/itsonedb_biomas2_indexes.tar.gz>`_.

The archive includes:

#. Bowtie2 indexes, i.e. ``bowtie2_indexes_rel138/ITSITSoneDB_all_euk_r138*`` files.
#. Mapping file (``ITSoneDB_rel138.json.gz``), i.e. the tabular file containing the correspondence between ITSoneDB accession and NCBI taxonomy ID.
#. Node file (``visualization_ITSoneDB_r131.dmp``), i.e. tabular file containing the annotation info needed to build the tree.

To include them in Galaxy, please refer to the `Galaxy Project documnetation <https://galaxyproject.org/admin/tools/data-tables/>`_. The ``*loc`` files are on our github repository (``biomas_2_wrapper/tool-data``) with the corresponding ``tool_data_table_conf.xml`` entry.

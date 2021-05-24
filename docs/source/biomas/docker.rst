BioMaS Docker
=============

BioMaS is also packaged as Docker Container, hosted on `DockerHub <https://hub.docker.com/r/ibiomcnr/biomas2>`_.

You can pull it from DockerHub with the following command:

::

  docker push ibiomcnr/biomas2

.. note::

   The BioMaS docker container includes the ITSoneDB reference data.

Usage
-----

The Docker container includes a python script, the same used for the Galaxy wrapper, to parse BioMaS commands. The options are the same explained in the previous section.

To check biomas options:

::

  # docker run -it ibiomcnr/biomas2 biomas --help
  usage: biomas [-h] [-p1 IN_SEQ_1] [-p2 IN_SEQ_2] [-b BASENAME]
                [-F FUNCTION_FOLDER] [-f FRAGMENT_LENGHT] [-p N_THREADS]
                [-i BOWTIE2_INDEXES_PATH] [-v MAPPING_FILE] [-T TANGO_FOLDER]
                [-d TANGO_DMP] [-n NODE_FILE]
  
  BioMaS wrapper for Galaxy
  
  optional arguments:
    -h, --help            show this help message and exit
    -p1 IN_SEQ_1          First sequence input file
    -p2 IN_SEQ_2          Second sequence input file
    -b BASENAME           Sample name
    -F FUNCTION_FOLDER    Cython function folder
    -f FRAGMENT_LENGHT    Fragment length (optional)
    -p N_THREADS          Number of threads for bowtie2
    -i BOWTIE2_INDEXES_PATH
                          Database: choice the reference bowite indexes
                          [MANDATORY]
    -v MAPPING_FILE       Mapping file [MANDATORY]
    -T TANGO_FOLDER       Tango folder
    -d TANGO_DMP          Tango dmp file
    -n NODE_FILE          tabular file containing the annotation info needed to
                          build the tree

To properly use the BioMaS Docker container create a directory and store inside your input data, in the following ``fungi-illumina1_short.fastq``and ``fungi-illumina2_short.fastq``

::

  # mkdir biomas_docker

  # cp source/fungi-illumina1_short.fastq biomas_docker/

  # cp source/fungi-illumina2_short.fastq biomas_docker/

Since reference data are already included, it can be run as follows:

::

  docker run -it -v /path/to/your/data:/data ibiomcnr/biomas2 biomas -p1 fungi-illumina1_short.fastq -p2 fungi-illumina2_short.fastq -b output

The output will be located in ``/path/to/your/data`` directory, in our example ``biomas_docker``.

::

  # ls biomas_docker
  bowtie2-execution.log         flash.log                         output_consensus_local_ITS1.sam      output.notCombined_1.fastq           output_tree.svg                  vsearch_conversion.log
  bowtie2_stdout_glocal_SE.log  fungi-illumina1_short.fastq       output_dereplicated_consensus.fastq  output.notCombined_2.fastq           quality_check_and_consensus.log  vsearch_dereplication.log
  bowtie2_stdout_local_SE.log   fungi-illumina2_short.fastq       output.extendedFrags.fastq           output_taxonomic_classification.tsv  report_file.txt
  derep.log                     ITSoneDB_fungi_mapping_data       output.hist                          output_taxonomic_summary.csv         temp
  fastqc_computation            output_consensus_glocal_ITS1.sam  output.histogram                     output_tree.nwk                      tmp.uc


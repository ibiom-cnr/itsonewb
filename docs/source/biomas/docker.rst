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

Since reference data are already included, it can be run as follows:

::

  docker run -it -v /path/to/your/data:/data ibiomcnr/biomas2 biomas -p1 fungi-illumina1_short.fastq -p2 fungi-illumina2_short.fastout_testout_test

The output will be located in ``/path/to/your/data`` directory.

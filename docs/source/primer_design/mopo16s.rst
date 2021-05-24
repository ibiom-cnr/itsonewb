Mopo16s
=======

Mopo16s input data can be created using the ITSoneWB tool :doc:`prepare_primer_input_inference`.

Galaxy usage
------------

The tool provides four outputs:

#. init primers:

.. figure:: /_static/img/mopo16s/mopo16s_output_1.png
   :scale: 20 %
   :align: center

#. init scores:

.. figure:: /_static/img/mopo16s/mopo16s_output_2.png
   :scale: 20 %
   :align: center

#. output primers:

.. figure:: /_static/img/mopo16s/mopo16s_output_3.png
   :scale: 20 %
   :align: center

#. output scores:

.. figure:: /_static/img/mopo16s/mopo16s_output_3.png
   :scale: 20 %
   :align: center

Reference primer pair
---------------------

The reference primer pair can be loaded by the Galaxy History or the user can use the built in pair. 

Currently, the reference primer pair is:

::

  >forward
  GAACCWGCGGARGGATCA

  >reverse
  GCTGCGTTCTTCATCGATGC
  
This reference primer pair can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/mopo16s_initial_primer_pairs_file.tar.gz>`_.

Advanced options
----------------

All Mopo16s options are parsed by our Galaxy wrapper and hidden under the ``advanced menu`` option:

.. figure:: /_static/img/mopo16s/mopo16s_advanced_options_1.png
   :scale: 20 %
   :align: center

.. figure:: /_static/img/mopo16s/mopo16s_advanced_options_2.png
   :scale: 20 %
   :align: center

All Mopo16s option are listed and explained `here <https://www.dei.unipd.it/~baruzzog/mopo16S.html#Usag)>`_. Moreover each option help is reported in the tool in-line help.

Install on Galaxy
-----------------

Galaxy is able to automatically solve conda dependecies when a tool is started.

To install Mopo16s on Galaxy:

#. Clone the ITSoneWb repository

   ::

     git clone https://github.com/ibiom-cnr/itsonewb.git

#. Add the Mopo16s entry in the galaxy ``tool_conf.xml`` file with your favourite editor:

   ::

     <section name="Primer Design" id="primer_design">
         <tool file="/path/to/itsonewb/mopo16s_wrapper/mopo16s_wrapper.xml" />
     </section>

#. Add the reference primer pair using the ``.loc`` files. To include them in Galaxy, please refer to the `Galaxy Project documnetation <https://galaxyproject.org/admin/tools/data-tables/>`_. The ``*loc`` files are on our github repository (``mopo16s_wrapper/tool-data``) with the corresponding ``tool_data_table_conf.xml`` entry.

#. Finally restart Galaxy.

Command line usage
------------------

Please refer to Mopo16S official documentation `here <https://www.dei.unipd.it/~baruzzog/mopo16S.html#Usag)>`_, to run Mopo16S as command line tool.

Install as standalone tool
--------------------------

Please follow the instructions `here <https://www.dei.unipd.it/~baruzzog/mopo16S.html#Installation>`_ to install Mopo16S.

ITSoneWB is currently using `SeqAn 2.1.1 <http://packages.seqan.de/seqan-src/seqan-src-2.1.1.tar.gz>`_.

Docker usage
------------

The tool is also packaged as Docker Container, hosted on `DockerHub <hhttps://hub.docker.com/r/ibiomcnr/mopo16s>`_.

You can pull it from DockerHub with the following command:

::

  docker pull ibiomcnr/mopo16s
  
Mopo16S is built using ``seqan v2.1.1``and inside the Docker container is available at ``/opt/mopo16s``.  

::

  # docker run -it ibiomcnr/mopo16s ls -l /opt/mopo16s
  total 156
  -rw-rw-r--. 1 root root 100710 Feb  6  2017 Doxyfile
  -rw-rw-r--. 1 root root  35142 Feb  6  2017 LICENSE
  -rw-rw-r--. 1 root root    274 Feb  6  2017 Makefile
  -rw-rw-r--. 1 root root    606 May 12 16:21 Makefile.rules
  -rw-rw-r--. 1 root root   1688 Jul 26  2017 README.md
  drwx------. 2 root root     86 Jul 26  2017 data
  drwx------. 2 root root     22 Jul 26  2017 debug
  drwx------. 2 root root     22 Jul 26  2017 profile
  drwx------. 2 root root   4096 May 12 16:21 release
  drwx------. 2 root root   4096 Apr  5  2018 src

.. note::

   The primer reference pair can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/mopo16s_initial_primer_pairs_file.tar.gz>`_.

Mopo16S executable are in ``/opt/mopo16s/release``. This path has been added to the ``$PATH``, therefore you can call mopo16s, easily, with:

::

  # docker run -it ibiomcnr/mopo16s mopo16S
  
  No reference set file name provided
  Copyright (c) 2015 Francesco Sambo and Giacomo Baruzzo, Dept. of Information Engineering,
  University of Padova, Italy
  
  mopo16s V1.0: optimal multi-objective design of forward and reverse primer
  sets for metagenomics studies.
  
  Usage: mopo16s [OPTIONS] reference_set_file initial_primer_pairs_file
  
  reference_set_file is a .fasta file containing the reference set of
  sequences for which the primer are designed.
  
  initial_primer_pairs_file is a .fasta file containing a set of (possibly
  degenerate) primer pairs from which to start the optimisation, saved
  alterning the forward and its corresponding reverse primer.
  
  Common options:
  
    -s, --seed=LONG             Seed of the random number generator (default 0)
  
    -r, --restarts=INT          Number of restarts for each run of the multi-objective
                                optimisation algorithm (default 20)
  
    -R, --runs=INT              Number of runs of the multi-objective
                                optimisation algorithm (default 20)
  
    -o, --outFileName=FNAME     Root name of the output files (default "out")
  
    -I, --outInitFileName=FNAME Root name of the files where the initial good
                                primer pairs should be saved (default "init")
  
    -G, --threads=INT           Number of threads for parallel execution (default 1)
  
    -V, --verbose=INT           Verbosity level (default 0). If 0, no extra 
                                output would be created. If not 0, for each 
                                run would be created 3 files: 
                                1) primers scores file
                                2) primers sequences file
                                3) optimization steps performed at each restart
  
    -h, --help                  Print this help and exit
  
  Coverage-related options:
  
    -M, --maxMismatches=INT     Maximum number of mismatches between the
                                non-3'-end of the primer and a 16S sequence to
                                consider the latter covered by the primer, in
                                case also the 3'-end perfectly matches
                                (default 2)
  
    -S, --maxALenSpanC=INT      Maximum amplicon length span considered when
                                computing coverage (half above, half below 
                                median) (default 200)
  
  Efficiency-related options:
  
    -l, --minPrimerLen=INT      Minimum primer length (default 17)
  
    -L, --maxPrimerLen=INT      Maximum primer length (default 21)
  
    -m, --minTm=INT             Minimum primer melting temperature (default 52)
  
    -c, --minGCCont=DOUBLE      Minimum primer GC content (default 0.5)
  
    -C, --maxGCCont=DOUBLE      Maximum primer GC content (default 0.7)
  
    -D, --maxDimers=INT         Maximum number of self-dimers, ie of dimers
                                between all possible gap-less alignments of the
                                primer with its reverse complement (default 8)
  
    -p, --maxHomopLen=INT       Maximum homopolymer length (default 4)
  
    -d, --maxDeltaTm=INT        Maximum span of melting temparatures for the
                                primer sets (default 3)
  
    -e, --maxALenSpanE=INT      Maximum span (maxALenSpanE) between median and
    -q, --maxALenSpanEQ=DOUBLE  given quantile (maxALenSpanEQ) of amplicon
                                length (default 50 and 0.01, respectively)
  
  Fuzzy tolerance intervals for efficiency-related options:
  
    -t, --minTmInterv=INT       Fuzzy tolerance interval for minimum melting
                                temperature (default 2)
  
    -g, --minGCContInt=DOUBLE   Fuzzy tolerance interval for minimum GC
                                content (default 0.1)
  
    -i, --maxDimersInt=INT      Fuzzy tolerance interval for maximum number of
                                self dimers (default 3)
  
    -T, --deltaTmInt=INT        Fuzzy tolerance interval for span of melting
                                temperatures of the primer set (default 2)
  
    -P, --maxHLenInt=INT        Fuzzy tolerance interval for maximum
                                homopolymer length (default 2)
  
    -E, --maxALenSpanEI=INT     Fuzzy tolerance interval for maximum span
                                between median and given quantile amplicon
                                length (default 50)
  
  Mandatory arguments to long options are also mandatory for any corresponding
  short options.

Mopo16S options are listed `here <https://www.dei.unipd.it/~baruzzog/mopo16S.html#Usag)>`_.


Input data needs to be mounted in ``/data`` directory with the command

::

  # docker run -it -v /path/to/data:/data ibiomcnr/mopo16s mopo16S

where ``/path/to/data`` is the local path of your data.

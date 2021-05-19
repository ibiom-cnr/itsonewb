Barcoding gap
=============

Considering a specific sequence collection (e.g. ITS1 sequences belonging to two *Aspergillus* species), the barcoding gap corresponds to the difference between the greatest intra-specific distance and the smallest inter-specific distance. It is fundamental to evaluate the ability of a specific barcode to discriminate among closely related species and the existence of a barcoding-gap allows to verify it.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image13.jpg)

.. figure:: /_static/img/intro/image13.jpg
   :scale: 30 %
   :align: center

*Supplementary Figure 14: A snapshot of the Barcoding Gap submission mask. In the example, the barcoding gap was inferred on the species Saccharomyces cerevisiae.*

In particular, the Barcoding Gap (BG) inference tool requires two information:

#.  Taxon list: the name of the taxon on which the BG will be inferred. To streamline the taxon name search an interactive drop-down menu is available;

2.  Taxon rank: taxonomic rank corresponding to the chosen taxon. Two levels are allowed: species and genus. 

A boxplot, comparing intra- and inter- group distances is automatically produced as a png file (Supplementary Figure 15). In the result section are also listed two BG measures:

- the difference between the mean values of intra-taxon and inter-taxa genetic distance;

- the minimum inter-taxa and maximum intra-taxon genetic distance.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image14.png)

.. figure:: /_static/img/intro/image14.png
   :scale: 30 %
   :align: center

*Supplementary Figure 15: The obtained boxplot picture for the measured genetic distances for Saccharomyces cerevisiae.*

Galaxy usage
------------

.. figure:: /_static/img/barcoding_gap_inference/barcoding_gap_home.png
   :scale: 30 %
   :align: center

The tool allows to select between genus and species.

.. figure:: /_static/img/barcoding_gap_inference/barcoding_gap_select.png
   :scale: 30 %
   :align: center

A ``png`` file is produced as output.

.. figure:: /_static/img/barcoding_gap_inference/barcoding_gap_output.png
   :scale: 30 %
   :align: center

Install on Galaxy
-----------------

Galaxy is able to automatically solve conda dependecies when a tool is started.

To install the Barcoding Gap tool on Galaxy:

#. Clone the ITSoneWb repository

   ::

     git clone https://github.com/ibiom-cnr/itsonewb.git

#. Add Barcoding Gap tool entry in the galaxy ``tool_conf.xml`` file with your favourite editor:

   ::

     <section name="Barcoding Gap" id="barcoding_gap">
         <tool file="/opt/itsonewb/barcoding_gap_wrapper/py3/barcoding_gap_wrapper.xml" />
     </section>

#. Finally restart Galaxy.

Command line usage
------------------

Barcoding Gap inference tool can be run as follows:

::

  # python print_bg_may21_py3.py --help
  usage: print-bg [-h] -d DISTANCE_FOLDER -f ALL_TAXA_FILE_LIST -n TAXON_NAME -r
                  TAXONOMIC_RANK [-F OUT_FOLDER]

  print the barcoding gap

  optional arguments:
    -h, --help            show this help message and exit
    -d DISTANCE_FOLDER, --distance_folder DISTANCE_FOLDER
                          folder in which are stored the distances in family
                          specific files
    -f ALL_TAXA_FILE_LIST, --all_taxa_file_list ALL_TAXA_FILE_LIST
                          file containing all the taxon list
    -n TAXON_NAME, --taxon_name TAXON_NAME
                          taxon name
    -r TAXONOMIC_RANK, --taxonomic_rank TAXONOMIC_RANK
                          taxonomic_rank
    -F OUT_FOLDER, --out_folder OUT_FOLDER
                          output folder


For example for ``Aspergillus flavus`` you have:

::

  # python py3/print_bg_may21_py3.py -d barcoding_gap/data_01022019/family_split -f barcoding_gap/data_01022019/all_taxon_list_and_families.csv -n "Aspergillus flavus" -r species
  Aspergillus flavus
  barcoding_gap/data_01022019/family_split/Aspergillaceae_distaces.tsv.gz
  /root/itsonewb/barcoding_gap_wrapper/venv/lib/python3.8/site-packages/plotnine/ggplot.py:719: PlotnineWarning: Saving 4 x 4 in image.
  /root/itsonewb/barcoding_gap_wrapper/venv/lib/python3.8/site-packages/plotnine/ggplot.py:722: PlotnineWarning: Filename:    /root/itsonewb/barcoding_gap_wrapper/Aspergillus flavus_dist_plot.png
  /root/itsonewb/barcoding_gap_wrapper/venv/lib/python3.8/site-packages/plotnine/ggplot.py:729: MatplotlibDeprecationWarning: savefig() got   unexpected keyword argument "device" which is no longer supported as of 3.3 and will become an error two minor releases later
  ['0.27', '-0.44', '/root/itsonewb/barcoding_gap_wrapper/Aspergillus flavus_dist_plot.png']  

showing the path of the resulting plot.

In this case, file distances have been downloaded and extracted in a directory named ``barcoding_gap`` (see next section).

 .. note::

   Distances files can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/barcoding_gap.tar.gz>`_.

Install as standalone tool
--------------------------

The barcoding gap inference tool can be found on the `ITSoneWB Github <https://raw.githubusercontent.com/ibiom-cnr/itsonewb/master/barcoding_gap_wrapper/py3/print_bg_may21_py3.py>_ repository.

Download the script:

::

  wget https://raw.githubusercontent.com/ibiom-cnr/itsonewb/master/barcoding_gap_wrapper/py3/print_bg_may21_py3.py

The Barcoding Gap tool dependencies can be installed using `conda <https://docs.conda.io/en/latest/miniconda.html>`_, thorough its `Bioconda channel <https://bioconda.github.io/>`_:

::

  conda create --name barcoding_gap numpy matplotlib pandas plotnine -c conda-forge -c bioconda
  
The command will create a new virtual environment called ``barcoding_gap`` wich can be activated with:

::

  conda activate barcoding_gap
  
Distances files can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/barcoding_gap.tar.gz>`_.

Download and untar them:

::

  wget http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/barcoding_gap.tar.gz

::

  tar xvzf barcoding_gap.tar.gz

Docker usage
------------

The usage of the barcoding gap tool from the docker container is the same as that described in the section **Command line usage**, using ``print-bg``as alias to call the script.

.. note::

   Distance files are already included in the Docker Container in the ``/refdata`` directory. For this reason the option 

In the following we report the command example for ``Aspergillus Flavus``:

::

  # docker run -it -v $PWD/bg:/data ibiomcnr/barcoding-gap print-bg -d /refdata/barcoding_gap/data_01022019/family_split -f /refdata/barcoding_gap/data_01022019/all_taxon_list_and_families.csv -n "Aspergillus flavus" -r species -F /data
  Aspergillus flavus
  /refdata/barcoding_gap/data_01022019/family_split/Aspergillaceae_distaces.tsv.gz
  /opt/conda/envs/barcoding_gap/lib/python3.7/site-packages/plotnine/ggplot.py:721: PlotnineWarning: Saving 4 x 4 in image.
  /opt/conda/envs/barcoding_gap/lib/python3.7/site-packages/plotnine/ggplot.py:722: PlotnineWarning: Filename: /data/Aspergillus flavus_dist_plot.png
  /opt/conda/envs/barcoding_gap/lib/python3.7/site-packages/plotnine/ggplot.py:729: MatplotlibDeprecationWarning: savefig() got unexpected keyword argument "device" which is no longer supported as of 3.3 and will become an error two minor releases later
  ['0.27', '-0.44', '/data/Aspergillus flavus_dist_plot.png']

Finally the resulting ``png`` file can be found in the host directory ``$PWD/bg``.

Prepare primer input inference
==============================

This tool create primer input inference file for mopo16s tool.

Usage
-----

To run the tool using ITSoneWB wrapper:

1. Select the taxon name in the tool menu:

.. figure:: /_static/img/prepare_primer_inference_files_wrapper/prepare_input_1.png
   :scale: 20 %
   :align: center

2. Submit your request:

.. figure:: /_static/img/prepare_primer_inference_files_wrapper/prepare_input_2.png
   :scale: 20 %
   :align: center

3. The output can be esily reproduced from the history or downloaded.

.. figure:: /_static/img/prepare_primer_inference_files_wrapper/prepare_input_3.png
   :scale: 20 %
   :align: center

4. If no output is created, an error will be displayed:

.. figure:: /_static/img/prepare_primer_inference_files_wrapper/prepare_input_error.png
   :scale: 20 %
   :align: center

Command line usage
------------------

The command line tool is available as python script on `ITSoneWB GitHub repository <https://raw.githubusercontent.com/ibiom-cnr/itsonewb/master/prepare_primer_inference_files_wrapper/prepare_input_file2primer_inference.py>`_.

To run the tool using the `prepare_input_file2primer_inference.py` script:

::

  python prepare_input_file2primer_inference.py -t Aspergillus -f ITS1_r131_plus_flanking_region.fna.gz -p node2tax_name_path.tsv.gz -o output.fa

The reference data files are also hosted on GitHub:

#. `ITS1_r131_plus_flanking_region.fna.gz <https://github.com/ibiom-cnr/itsonewb/blob/master/prepare_primer_inference_files_wrapper/ITS1_r131_plus_flanking_region.fna.gz?raw=true>`_

#. `node2tax_name_path.tsv.gz <https://github.com/ibiom-cnr/itsonewb/blob/master/prepare_primer_inference_files_wrapper/node2tax_name_path.tsv.gz?raw=true>`_

Install on Galaxy
-----------------

Galaxy is able to automatically solve conda dependecies when a tool is started.

To install **Prepare primer input inference file** on Galaxy:

#. Clone the ITSoneWb repository

   ::

     git clone https://github.com/ibiom-cnr/itsonewb.git

#. Add the **Prepare primer input inference file** entry in the galaxy ``tool_conf.xml`` file with your favourite editor:

::

  <section name="Primer Design" id="primer_design">
      <tool file="/path/to/itsonewb/prepare_primer_inference_files_wrapper/prepare_input_file2primer_inference.xml" />
  </section>

#. Add the reference data using ``.loc`` files. To include them in Galaxy, please refer to the `Galaxy Project documnetation <https://galaxyproject.org/admin/tools/data-tables/>`_. The ``*loc`` files are on our github repository (``prepare_primer_inference_files_wrapper/tool-data``) with the corresponding ``tool_data_table_conf.xml`` entry.

#. Finally restart Galaxy.


Reference data
--------------

The reference data files are hosted on GitHub and can be easily downloaded:

#. `ITS1_r131_plus_flanking_region.fna.gz <https://github.com/ibiom-cnr/itsonewb/blob/master/prepare_primer_inference_files_wrapper/ITS1_r131_plus_flanking_region.fna.gz?raw=true>`_

#. `node2tax_name_path.tsv.gz <https://github.com/ibiom-cnr/itsonewb/blob/master/prepare_primer_inference_files_wrapper/node2tax_name_path.tsv.gz?raw=true>`_

Docker version
--------------

Usage
^^^^^

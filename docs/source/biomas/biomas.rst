BioMaS (Bioinformatic analysis of Metagenomic ampliconS)
--------------------------------------------------------

BioMaS is an automatic pipeline designed for the taxonomic classification of DNA metabarcoding data. The data processing requires Illumina paired-ends fastq sequence data. In particular BioMaS encompasses all the required steps to manage/filter raw data and perform the taxonomic classification. In Supplementary Figure 11 the data submission mask is shown.

.. figure:: /_static/img/intro/image10.jpg
   :scale: 30 %
   :align: center

*Supplementary Figure 11: A snapshot of the tool submission mask.*

.. figure:: /_static/img/intro/image11.jpeg
   :scale: 50 %
   :align: center

*Supplementary Figure 12: An example of the graphical representation of the taxonomic classification results obtained by using BioMaS.*

In particular, the users can set 4 parameters:

- First sequence: forward reads sequences input;

- Second sequence: reverse reads sequences input;

- Fragment length (optional): corresponds to the average amplicon length. If the amplicon length is highly variable leaving it blank is recommended;

- Bowtie 2 indexes: choose the reference ITSoneDB version.

BioMaS will produce 3 result files:

#. a taxonomic assignment file;

#. a svg tree (Supplementary Figure 12) summarizing the inferred taxonomy. For each node, the following information are shown:

   a. node scientific name: the NCBI official scientific name assigned to the node in red;

   #. taxonomic rank: the NCBI taxonomic rank in brown;

   #. number of directly assigned sequences in blue;

   #. number of sequences assigned to the node and its descendants in green: this number summarizes the number of reads that are directly assigned to the node and those that are assigned to the child nodes. In the example, at order level no direct assignments were observed, while reads were assigned to lower ranks (i.e. family and species).

#. taxonomic assignment summary file: a textual tabular file containing the following fields:

   e. Taxon Name: the NCBI official scientific name assigned to the node;

   #. NCBI Taxonomy ID: The NCBI taxonomy database unique identifier associated to the node;

   #. Taxonomic Rank: the NCBI taxonomic rank;

   #. Directly Assigned: number of directly assigned sequences;

   #. Total Assigned: number of sequences assigned to the node and its descendant;

.. toctree::
   :maxdepth: 2
   :caption: Use and Install BioMaS

   use.rst
   install.rst
   docker.rst

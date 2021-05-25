Third-Party Tools
=================

ITSoneWB allows to use Qiime, Qiime 2 and Mothur from Galaxy. 

Install on Galaxy
-----------------

These tools are available for installation through the `Galaxy Tool Shed <https://toolshed.g2.bx.psu.edu/>`_ directly from Galaxy. Dependecies are automatically solved with conda during the installation.

Reference data
--------------

It is possible to configure Qiime, Qiime 2 and Mothur to exploit ITSoneDB as reference data, as follows.

Qiime
^^^^^

Qiime ITSoneDB reference data are available `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/qiime_itsonedb.tar.gz>`_.

On Galaxy, add ``ITSoneDB_r138_NR99.fasta`` file to ``qiime_rep_set.loc`` loc file.

Qiime 2
^^^^^^^

Qiime 2 ITSoneDB reference data are available `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/qiime2_itsonedb.tar.gz>`_.

On Galaxy, add ``ITSoneDB_r138_NR99.taxa.qza`` file to ``qiime2_taxonomy.loc`` loc file.

Mothur
^^^^^^

Mothur ITSoneDB reference data are available `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/mothur_itsonedb.tar.gz>`_.

On Galaxy:

#. Add the ``ITSoneDB_r138_NR99_taxa.tsv`` file to ``mothur_aligndb.loc`` loc file.

#. Add the ``ITSoneDB_r138_NR99_taxa.tsv`` file to ``mothur_taxonomy.loc`` loc file.

Command line usage
------------------

For command line installation and usage, or for the Docker version,  please refer to the corresponding tool documentation: `Qiime <http://qiime.org/1.3.0/documentation/index.html>`_, `Qiime 2 <https://docs.qiime2.org/2021.4/>`_ and `Mothur <https://mothur.org/wiki/mothur_manual/>`_. 

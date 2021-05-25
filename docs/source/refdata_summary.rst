Reference Data Summary
======================

The reference data used by ITSoneWB are listed here. Please refere to tools documentation to use them.

-------------------------------------
``ITSoneDB vs. shotgun mapping tool``
-------------------------------------

ITSoneDB (r131) BioMaS indexes can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_3b4918e0a982493e8c3ebcc43586a2a8/ITSoneWB/itsonedb_r131_biomas_indexes.tar.gz>`_.

----------
``BioMaS``
----------

ITSoneDB (r138) BioMaS indexes can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_3b4918e0a982493e8c3ebcc43586a2a8/ITSoneWB/itsonedb_biomas2_indexes.tar.gz>`_.

-----------
``Mopo16S``
-----------

Mopo16S reference primer pair can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/mopo16s_initial_primer_pairs_file.tar.gz>`_.

----------------------------------
``Prepare primer input inference``
----------------------------------

The reference data files are hosted on GitHub and can be easily downloaded:

#. `ITS1_r131_plus_flanking_region.fna.gz <https://github.com/ibiom-cnr/itsonewb/blob/master/prepare_primer_inference_files_wrapper/ITS1_r131_plus_flanking_region.fna.gz?raw=true>`_.

#. `node2tax_name_path.tsv.gz <https://github.com/ibiom-cnr/itsonewb/blob/master/prepare_primer_inference_files_wrapper/node2tax_name_path.tsv.gz?raw=true>`_.

-----------------
``Barcoding Gap``
-----------------

The Distances files can be downloaded `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/barcoding_gap.tar.gz>`_.

---------
``Qiime``
---------

Qiime ITSoneDB reference data are available `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/qiime_itsonedb.tar.gz>`_.

On Galaxy, add ``ITSoneDB_r138_NR99.fasta`` file to ``qiime_rep_set.loc`` loc file.

-----------
``Qiime 2``
-----------

Qiime 2 ITSoneDB reference data are available `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/qiime2_itsonedb.tar.gz>`_.

On Galaxy, add ``ITSoneDB_r138_NR99.taxa.qza`` file to ``qiime2_taxonomy.loc`` loc file.

----------
``Mothur``
----------

Mothur ITSoneDB reference data are available `here <http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/mothur_itsonedb.tar.gz>`_.

On Galaxy:

#. Add the ``ITSoneDB_r138_NR99_taxa.tsv`` file to ``mothur_aligndb.loc`` loc file.

#. Add the ``ITSoneDB_r138_NR99_taxa.tsv`` file to ``mothur_taxonomy.loc`` loc file.

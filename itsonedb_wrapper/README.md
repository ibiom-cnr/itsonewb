ITSoneDB connector
==================

[ITSoneDB](http://itsonedb.cloud.ba.infn.it/index.jsp) is a comprehensive collection of eukaryotic ribosomal RNA Internal Transcribed Spacer 1 (ITS1) sequences. It is aimed at supporting metabarcoding surveys of fungal and other microbial eukaryotic environmental communities. The sequences were extracted from the European Nucleotide Archive (ENA) and arranged on the NCBI taxonomy tree. ITS1 start and end boundaries were defined by ENA annotations and/or designed by mapping Hidden Markov Model (HMM) profiles of flanking 18S and 5.8S ribosomal RNA coding genes on each sequence.

This tool allow to query ITSoneDB from Galaxy and import the results in the History.

![itsonedb_connector_home](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/itsonedb_connector_home.png

Usage
-----

The tool allows to query ITSoneDB by ``specie name``, ``taxon name`` and ``accession number```:

![itsonedb_connector_select](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/itsonedb_connector_select.png

The ITSoneDB connector provides the output sequences aand the metadata file:

![itsonedb_connector_output](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/itsonedb_connector_output.png
![itsonedb_connector_metadata](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/itsonedb_connector_output_metadata.png


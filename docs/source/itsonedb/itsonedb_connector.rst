ITSoneDB Connector
------------------

The ITSoneDB Connector allows querying ITSoneDB by using an API service with the same query schema available at the database website. In particular, it is possible to access the ITSoneDB entries by using the following parameters: species name, taxon name and entry accession (Supplementary Figure 5*)*.

.. figure:: /_static/img/intro/image5.jpg
   :scale: 30 %
   :align: center

*Supplementary Figure 5: : A snapshot of the ITSoneDB connector Service. ITSoneDB entries are accessible by using species name, taxon name and entry accession.*

In order to streamline querying by using both species and taxon names an interactive drop-down menù is available (Supplementary Figure 5). For instance, in *Figure ITSoneDB Connector 2* ITSoneDB is accessed by using the species name *Aspergillus flavus*.

.. figure:: /_static/img/intro/image6.jpg
   :scale: 30 %
   :align: center

*Supplementary Figure 6: The ITSoneDB connector service suggests a list of possible species names according to the user typing.*

As the species name selection is completed by clicking the "execute" button, the data retrieval from ITSoneDB is executed Supplementary Figure 7).

.. figure:: /_static/img/intro/image7.jpg
   :scale: 30 %
   :align: center

*Supplementary Figure 7: Following the query parameters selection ITSoneDB is accessed by clicking the "Execute" button.*

The query retrieves ITS1 fasta sequences and the contextual metadata. As exemple, 958 ITS1 belonging to *Aspergillus flavus* are available in ITSoneDB and retrieved. The metadata are arranged in a tabular file containing 5 fields:

-   Accession: ENA Accession number from which the ITSoneDB sequence was obtained;

-   Taxon name: The ITS1 taxonomic given name;

-   ITS1 localization: the method used to infer the ITS1 location (ENA or/end HMM);

-   Sequence description: the description of the sequences retrieved from the original ENA entry.

This information are downloadable as a textual file that can be imported in Excel.

.. figure:: /_static/img/intro/image8.jpg
   :scale: 30 %
   :align: center

*Supplementary Figure 8: A snapshot of the obtained metadata file.*

Usage
-----

The tool allows to query ITSoneDB by ``specie name``, ``taxon name`` and ``accession number```:

.. figure:: /_static/img/itsonedb_connector/itsonedb_connector_select.png
   :scale: 30 %
   :align: center

The ITSoneDB connector provides the output sequences and the metadata file:

.. figure:: /_static/img/itsonedb_connector/itsonedb_connector_output.png
   :scale: 30 %
   :align: center

.. figure:: /_static/img/itsonedb_connector/itsonedb_connector_output_metadata.png
   :scale: 30 %
   :align: center



Galaxy Docker version
---------------------

The ITSoneDB Connector tool shipped with the Docker version of the Workbench requires three additional:

#. ITSoneDB Url: the Database URL

#. User registered name

#. User registered password

.. figure:: /_static/img/itsonedb_connector/itsonedb_connector_docker_version.png
   :scale: 30 %
   :align: center

.. warning::

   This version of the ITSoneDB Connector is intended for personal use only. For security reason these information are not public, but the access can be requested at the followinf mail address ``<mail_placeholder>``.

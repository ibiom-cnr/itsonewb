Introduction
============

The amplicon-based metagenomic analysis (i.e. DNA metabarcoding), represents a powerful tool to rapidly, efficiently and cheaply investigate large microbial communities. The growing interest in its application results in a concomitant increase of appropriate resources designed to manage and analyze data in FAIR-compliant way (Wilkinson et al., 2019).

In this context, ITSoneWB (ITSone WorkBench) represents a well-defined environment collecting and integrating the high quality ITS1 reference collection in ITSoneDB (Santamaria et al., 2017) with DNA metabarcoding well-established analysis pipelines and new tools in an easy-to-use service addressing the eukaryotic domain of life. Specifically, BioMaS, QIIME (Caporaso *et al.*, 2010), QIIME2 (Bolyen *et al.*, 2019) Mothur (Schloss *et al.*, 2009) pipelines were included and new tools to infer the ITS1 *Barcoding gap and PCR primers pair* in a user defined taxonomic range and to identify ITS1 regions in shotgun metagenomic data were designed, developed and deployed in a Galaxy environment.

Galaxy environment setting
--------------------------

The Galaxy virtual instance hosting the ITSoneWB was deployed on the INFN-Bari ReCaS (Recas - ReCaS Bari, 2021) cloud facility running OpenStack (Open Source Cloud Computing Infrastructure, 2021). A dedicated tenant was created to host the workbench instance. Finally, a Galaxy virtual cluster was deployed to develop the workbench, exploiting the resources of the INFN-Bari cloud site, consisting in a front-end server running Galaxy 19.05 and the slurm server and 2 Worker Node (WN), each fit out with 8 CPUs and 16 Gb RAM and running CentOS 7. The TOSCA (TOSCA Simple Profile in YAML Version 1.0, 2021) templates used to deploy the cluster are hosted on `github <https://github.com/ibiom-cnr/itsonewb/tree/master/galaxy-deployment>`_.

A comprehensive description of Galaxy environment deployment is available in (Tangaro *et al.*, 2020).

Tools and Database implementation and deployment
------------------------------------------------

ITSoneDB 
^^^^^^^^

ITSoneDB is available as a free web service `here <http://itsonedb.cloud.ba.infn.it/>`_ where data query and download are enabled through a simple web-interface, whereas metadata can be accessed by cross-linking to ENA. ITSoneDB is updated every 6 months and always curated.

It collects ITS1 sequences and the associated taxonomic annotation originated from European Nucleotide Archive (ENA). The annotation of ITS1 boundaries were also refined or de novo inferred by using a reference-based approach relying on the mapping of the Hidden Markov Models (HMM) relative to conserved ribosomal gene for RNA 18S (Rfam accession: RF01960) and 5.8S (RF00002) on the original sequence.

Moreover the integration of ITSoneDB with the Marine reference databases (Klemetsen *et al.*, 2018) is ongoing within the ELIXIR EXCELERATE Projects and it is already implemented into the MGnify pipeline (Mitchell *et al.*, 2020) at EMBL-EBI as reference ITS1 collection and in META-pipe (Robertsen *et al.*, 2016). All these actions aimed at increasingly enhance its usefulness, exposure and interoperability in agreement to the FAIR (Wilkinson *et al.*, 2016) data principles, thereby improving its long-term value and reuse.

The same query criteria available in ITSoneDB have been implemented in
ITSoneWB in order to retrieve data by accession number (i.e. by using
ENA accession number) and/or by taxon name (e.g. species name).

ITSoneDB vs. shotgun mapping tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest way to taxonomically classify shotgun metagenomic data is to
search for DNA barcoding makers , such as 16S and 18S ribosomal RNA
genes (Bremges *et al.*, 2020) and ITS sequences.

We developed a Python script allowing users to search for ITS1 regions
in shotgun metagenomic data. In particular, the script automatically
aligns single-end (SE) and paired-end (PE) reads against ITSoneDB by
exploiting bowtie2, in both end-to-end (similar to a global alignment)
and local modality. The resulting alignments are then filtered according
to query coverage (default ≥70%) and similarity (default ≥97%). Finally,
a list of ITS1 sequences are returned.

It is important to note that the choice between the single-end and the
paired-end mapping may influence the results. In particular, in PE
mapping both the reads must pass the query coverage threshold.


![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media//image1.png)

*Supplementary Figure 1: A representation of the implemented mapping
schema. Red and blue lines correspond, respectively, to paired- and
single-end reads. For PE reads, R1 and R2 represents the forward and the
reverse reads, respectively.*

In Supplementary Figure 1 four hypothetical mapping situations are
shown. In the first one (A) both the PE mates align to the ITS1
reference for more than 70% of their length, so assuming the identity
percentage (measured as the mean of the similarity obtained by each
mate) is higher than the imposed threshold, this alignment is retained.
In the second case (B), the R1 aligns to the reference for less than 70%
and consequently the PE alignment is completely filtered-out. Single-end
cases are more simple because we check the requirements for each read
independently (C is retained and D is not).

### BioMaS (Bioinformatic analysis of Metagenomic ampliconS)

BioMaS (Fosso *et al.*, 2015) was released in 2015 as a user-friendly
pipeline designed to assess the microbiome composition directly from raw
DNA metabarcoding HTS data. Its purpose was to support the metabarcoding
investigation without requiring any installation or configuration step
by users, but just offering an already well-defined and configured
environment by using Galaxy (Blankenberg *et al.*, 2010), a WFMS
(Workflow management system). It was designed to perform the direct
taxonomic binning of metabarcoding data. It merges the Paired End (PE)
reads and trims low quality regions of unmerged reads. Its workflow has
been proven to carry out a very accurate taxon binning, outperforming
both QIIME and Mothur. Moreover, it is designed to work both with long
amplicons (e.g. ITS1) where the PE reads merging is not always possible
or efficient. Indeed, BioMaS is able to map metagenomic sequences to the
reference collection both in PE (unmerged reads) and SE (merged reads)
mode.

We developed the Galaxy wrapper file, responsible to set BioMaS options,
run BioMaS and produce the outputs, while each step of the pipeline is
called through a python script. All dependencies are automatically
solved exploiting CONDA through Galaxy. ITSoneDB is used as the default
reference database.

### QIIME (Quantitative Insight Into Microbial Ecology)

QIIME (Caporaso *et al.*, 2010) is probably the most used pipeline to
address the analysis of microbial data with more than 15,000 citations
(Scopus). It implements tools for NGS data quality check, OTU-picking,
Beta and Alpha diversity analysis and statistical test. Its deployment
in the ITSoneWB has been obtained through Galaxy ShedTools.

### QIIME2 (Quantitative Insight Into Microbial Ecology 2)

QIIME2 (Bolyen *et al.*, 2019) is a suite of tools and scripts designed
for the analysis of microbial data from raw sequencing data import to
statistical analysis of the obtained results. It has currently replaced
QIIME by improving both the suite installation and usage. Moreover,
according to FAIR principles and data traceability, it implements an
"artifact" based approach allowing to trace the data provenance and
tools application. The version available on the workbench is installed
through the Galaxy ShedTools.

### Mothur

Mothur (Schloss *et al.*, 2009) represents another well-established and
widely used pipeline for the analysis of metabarcoding data. It has been
installed in the workbench through Galaxy ShedTools.

### Mopo16S (Multi-Objective Primer Optimisation for 16s experiments)

The Mopo16s (Sambo *et al.*, 2018) tool has been designed to maximize
the primer design process on 16S rRNA sequences and released as a free
software under the GNU General Public License. It has been deployed in
ITSoneWB by optimizing its parameters to process ITS1 reference
sequences collected in ITSoneDB.

Actually, this tool is not currently available as a conda package,
therefore we built it from scratch, against the seqan library v2.2.1.
The tool was ported to Galaxy and deployed on ITSoneWB. Moreover, in
order to allow the user to compute the primer design in a specific
clade, a tool to prepare a set of input reference sequences was
developed and ported to Galaxy.

### Barcoding gap

The Barcoding gap has been defined as the difference between the
observed largest intraspecific and smallest inter-specific genetic
distances (e.g. ITS1 sequences belonging to two *Aspergillus* species)
(Meyer and Paulay, 2005). It is fundamental to evaluate the ability of a
specific barcode to discriminate between closely related species and the
existence of a barcoding-gap allows to verify it.

In order to evaluate the ITS1 efficiency in species or genus
discrimination, we developed a tool to infer the barcoding gap in a user
defined taxonomic clade.

The barcoding gap inference relies on the comparison of intra- and
inter- group genetic distances, so it is necessary to compute pairwise
sequence alignments and genetic distance inference. This operation may
be computationally expensive especially when hundreds of sequences need
to be compared (e.g. considering 100 sequences we need to perform
$\frac{100!}{2!(100 - 2)!}$combinations equal to 4,950 pairwise
alignments) and this represent a critical bottleneck if performed
whenever the user requests the calculation for a large taxonomic range.
In order to streamline this step, all the required pairwise comparison
and genetic distances were precomputed and results stored in a tabular
file.

In detail, a Python-based workflow was developed to perform pairwise
sequences alignments and compute genetic distance inference through the
following steps:

-   all the ITSoneDB sequences lacking complete taxonomic information
    were discarded (i.e. we retained sequences taxonomically annotated
    to both genus and species level). This procedure was necessary to
    avoid any error due to a taxonomic misclassification;

-   Sequences were split according to the species name;

-   A species dereplication was performed to reduce the computational
    requirements. For identical sequences the distance is settled to 0.

-   Dereplicated sequences were then grouped according to their family;

-   Pairwise alignments were performed by using the Needleman-Wunsch
    algorithm (global alignment). Genetic distance was measured as the
    number of mismatch normalized by the alignment length;

-   All the computed distances were stored in a csv (i.e. comma
    separated values) file collecting also the sequences taxonomic
    information.

The barcoding gap was then computed in the user selected clade by using
two approaches:

-   The largest intra-group genetic distance was compared to the
    smallest inter-group one;

-   The mean intra- and inter- group distances were compared.

Currently, this tool allows to measure the barcoding gap at genus and
species level.

Tools accessibility and use
===========================

ITSoneWB is available at
[[http://itsonewb.cloud.ba.infn.it/galaxy]{.underline}](http://itsonewb.cloud.ba.infn.it/galaxy)
through both registered and anonymous access. Aside from the access
modality, the user can exert the whole set of implemented utility and
pipelines. Nonetheless different computational capacity, storage and
data latency are assigned to registered and anonymous users. In
particular, 4 parallel jobs and 1 latency month and 2 parallel jobs, 500
Mb and 3 latency days are ensured to registered and anonymous users,
respectively.

The anonymization of log files ensures the compliance to the European
General Data Protection Regulation (GDPR).

How to register in ITSoneWB
---------------------------

As explained above, the access to ITSoneWB is not restricted and
anonymous users are allowed. Nonetheless, the registration is highly
recommended and, currently, does not require any approval from the
service provider.

In order to register to ITSoneWB, the user needs just to access the home
page by using the link
[[http://itsonewb.cloud.ba.infn.it/galaxy]{.underline}](http://itsonewb.cloud.ba.infn.it/galaxy)
and select "*Login or register*" (red arrow in the Supplementary Figure
2).

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media//image2.jpg)

*Supplementary Figure 2: ITSoneWB home page. The red arrow points to
"Login or register".*

Once the login page is available, the registered users need just to fill
the fields with the chosen username (or email) and password,
respectively, and push "*Login*". Unregistered users may proceed to the
registration portal by clicking "*Register here*" (Supplementary Figure
3).

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media//image3.jpg)

*Supplementary Figure 3: ITSoneWB login page. The red arrow points to the
registration page link.*

To complete the registration, it is required to fill the fields with the
information listed below (Supplementary Figure 4):

1.  Email Address: a valid email address.

2.  Password: a password allowing access to the account. Even if there
    are no particular requirements for password selection, the
    application of general
    [[advices]{.underline}](https://www.howtogeek.com/195430/how-to-create-a-strong-password-and-remember-it/)
    is suggested.

3.  Confirm Password: just write again the chosen password.

4.  Public Name: a username associated with the account.

By clicking "*Create*", the account will be automatically created and
the user logged in to ITSoneWB.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media//image4.jpg)

*Supplementary Figure 4: Registration page.*

The user is allowed to choose among the available pipelines and
services, all interfaced with the release 1.138 of ITSoneDB, by
accessing to the "ITSoneWB section". Following a list of guidelines to
use the tools.

ITSoneDB
--------

The ITSoneDB tool embeds two services: "*[ITSoneDB
Connector]{.underline}*" and "*ITSoneDB vs. shotgun mapping tool{.underline}*".

### ITSoneDB Connector

The ITSoneDB Connector allows querying ITSoneDB by using an API service
with the same query schema available at the database website. In
particular, it is possible to access the ITSoneDB entries by using the
following parameters: species name, taxon name and entry accession
(Supplementary Figure 5*)*.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media//image5.jpg)

*Supplementary Figure 5: : A snapshot of the ITSoneDB connector Service.
ITSoneDB entries are accessible by using species name, taxon name and
entry accession.*

In order to streamline querying by using both species and taxon names an
interactive drop-down menù is available (Supplementary Figure 5). For
instance, in *Figure ITSoneDB Connector 2* ITSoneDB is accessed by using
the species name *Aspergillus flavus*.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image6.jpg)

*Supplementary Figure 6: The ITSoneDB connector service suggests a list of
possible species names according to the user typing.*

As the species name selection is completed by clicking the "execute"
button, the data retrieval from ITSoneDB is executed Supplementary
Figure 7).

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image7.jpg)

*Supplementary Figure 7: Following the query parameters selection ITSoneDB
is accessed by clicking the "Execute" button.*

The query retrieves ITS1 fasta sequences and the contextual metadata. As
exemple, 958 ITS1 belonging to *Aspergillus flavus* are available in
ITSoneDB and retrieved. The metadata are arranged in a tabular file
containing 5 fields:

-   Accession: ENA Accession number from which the ITSoneDB sequence was
    obtained;

-   Taxon name: The ITS1 taxonomic given name;

-   ITS1 localization: the method used to infer the ITS1 location (ENA
    or/end HMM);

-   Sequence description: the description of the sequences retrieved
    from the original ENA entry.

This information are downloadable as a textual file that can be imported
in Excel.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media//image8.jpg)

*Supplementary Figure 8: A snapshot of the obtained metadata file.*

### ITSoneDB vs. shotgun mapping tool

The ITS1 *shotgun mapping* service allows to identify and eventually
taxonomically classify ITS1 regions in metagenomic shotgun data.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image9.jpg)

*Supplementary Figure 9: A snapshot of the tool setup mask.*

*ITSoneDB vs. shotgun mapping tool* is able to analyse both single-end
(SE) and paired-end (PE) fastq files. It exploits query sequence mapping
on the ITSoneDB collection by using bowtie2, in both end-to-end (similar
to a global alignment) and local modality. The resulting alignments are
then filtered according to query coverage and similarity. Finally, a
list of ITS1 sequences are returned.

It is important to note the choice between the single-end and the
paired-end mapping may influence the results. In particular, in PE
mapping both the reads must pass the query coverage threshold.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media//image1.png)

*Supplementary Figure 10: A schematic representation of the mapping schema
implemented in the tool. Red and blue lines correspond, respectively, to
paired- and single-end reads. For PE reads, R1 and R2 represents the
forward and the reverse reads, respectively.*

In Figure *ITS1 to ITSoneDB 2,* 4 hypothetical mapping situations are
represented. In the first one (A) both the PE mates align to the ITS1
reference for more than 70% of their length, so assuming the identity
percentage (measured as the mean of the similarity obtained by each
mate) is higher than the imposed threshold, this alignment is retained.
In the second case (B), the R1 aligns to the reference for less than 70%
and consequently the PE alignment is completely filtered-out. Single-end
cases are more simple because we check the requirements for each read
independently (C is retained and D not).

Taking into account the mapping and filtering modalities, the user needs
to choice between the following parameters:

-   Single or Paired, file or collection: type of input files;

-   Bowtie 2 indexes: ITSoneDB reference collection;

-   Identity percentage threshold: the identity percentage filtering
    threshold to consider the alignment relevant (default ≥ 97%);

-   Coverage of the query sequence: the query coverage filtering
    threshold to consider the alignment relevant (default ≥ 70%);

-   Number of bowtie2 matches: maximum number of relevant alignments
    retrieved per each query sequence (or paired-end sequence).

In *Supplementary Figure 10*, a simulation of single-end data analysis
by using default parameters is shown.

The result of the analysis is a tubular text file listing the query
sequences matching with ITS1 sequences.

BioMaS (Bioinformatic analysis of Metagenomic ampliconS)
--------------------------------------------------------

BioMaS is an automatic pipeline designed for the taxonomic
classification of DNA metabarcoding data. The data processing requires
Illumina paired-ends fastq sequence data. In particular BioMaS
encompasses all the required steps to manage/filter raw data and perform
the taxonomic classification. In Supplementary Figure 11 the data
submission mask is shown.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image10.jpg)

*Supplementary Figure 11: A snapshot of the tool submission mask.*

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image11.jpeg)

*Supplementary Figure 12: An example of the graphical representation of the
taxonomic classification results obtained by using BioMaS.*

In particular, the users can set 4 parameters:

-   First sequence: forward reads sequences input;

-   Second sequence: reverse reads sequences input;

-   Fragment length (optional): corresponds to the average amplicon
    length. If the amplicon length is highly variable leaving it blank
    is recommended;

-   Bowtie 2 indexes: choose the reference ITSoneDB version.

BioMaS will produce 3 result files:

1.  a taxonomic assignment file;

2.  a svg tree (Supplementary Figure 12) summarizing the inferred
    taxonomy. For each node, the following information are shown:

    a.  node scientific name: the NCBI official scientific name assigned
        to the node in red;

    b.  taxonomic rank: the NCBI taxonomic rank in brown;

    c.  number of directly assigned sequences in blue;

    d.  number of sequences assigned to the node and its descendants in
        green: this number summarizes the number of reads that are
        directly assigned to the node and those that are assigned to the
        child nodes. In the example, at order level no direct
        assignments were observed, while reads were assigned to lower
        ranks (i.e. family and species).

3.  taxonomic assignment summary file: a textual tabular file containing
    the following fields:

    e.  Taxon Name: the NCBI official scientific name assigned to the
        node;

    f.  NCBI Taxonomy ID: The NCBI taxonomy database unique identifier
        associated to the node;

    g.  Taxonomic Rank: the NCBI taxonomic rank;

    h.  Directly Assigned: number of directly assigned sequences;

    i.  Total Assigned: number of sequences assigned to the node and its
        descendant;

Primer Design
-------------

The Primer Design service uses the mopo16S tool to infer the best primer
pair able to amplify the ITS1 belonging to the taxonomic clade settled
by the user.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image12.jpg)

*Supplementary Figure 13: A snapshot of the tool submission mask.*

Initially, the user needs to apply the "*Prepare primer input inference
file*" tool, allowing to extract all the ITS1 sequences available for a
specific clade in ITSoneDB.

The user must select the taxonomic clade of interest. In order to
streamline the taxon name searching an interactive drop-down menu is
available. The sequence clustering ("Enable clustering" button) is
enabled by default and may be disabled only for datasets with less than
1000 sequences. Once executed, the tool will generate a fasta sequences
collection that will constitute the mopo16S tool input.

Following, the primer inference is performed by using the mopo16S tools.

The tool execution requires 2 mandatory inputs:

1.  Reference dataset file: a fasta collection of target sequences
    uploaded by the users or generated by using the *Prepare primer
    input inference file* tool;

2.  Reference primer file: mopo16s requires an initial primer set to
    eventually infer new primers. Otherwise a primer pair can be
    provided by the system \[PMID:25077016\].

It is also possible to set advanced parameters, for whose description we
suggest to visit the [[developer
site]{.underline}](https://www.dei.unipd.it/~baruzzog/mopo16S.html).

mopo16S starts by inferring the efficiency (a measure of the
amplification capacity of each primer), the coverage ("virtually
amplified" sequences in input collection) and the matching-bias
(mismatches between primers and input sequences) of the submitted primer
pairs. Then infers a new primer pair (or a set of pairs) that maximise
the efficiency and coverage and minimize the matching-bias.

Three outputs are produced:

1.  Efficiency, coverage and matching bias of the input primer pair;

2.  A list of new primers;

3.  Efficiency, coverage and matching bias of the new designed primers;

Barcoding gap
-------------
Considering a specific sequence collection (e.g. ITS1 sequences
belonging to two *Aspergillus* species), the barcoding gap corresponds
to the difference between the greatest intra-specific distance and the
smallest inter-specific distance. It is fundamental to evaluate the
ability of a specific barcode to discriminate among closely related
species and the existence of a barcoding-gap allows to verify it.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image13.jpg)

*Supplementary Figure 14: A snapshot of the Barcoding Gap submission mask.
In the example, the barcoding gap was inferred on the species
Saccharomyces cerevisiae.*

In particular, the Barcoding Gap (BG) inference tool requires two
information:

1.  Taxon list: the name of the taxon on which the BG will be inferred.
    To streamline the taxon name search an interactive drop-down menu is
    available;

2.  Taxon rank: taxonomic rank corresponding to the chosen taxon. Two
    levels are allowed: species and genus.

A boxplot, comparing intra- and inter- group distances is automatically
produced as a png file (Supplementary Figure 15). In the result section
are also listed two BG measures:

-   the difference between the mean values of intra-taxon and inter-taxa
    genetic distance;

-   the minimum inter-taxa and maximum intra-taxon genetic distance.

![](https://github.com/ibiom-cnr/itsonewb/blob/master/myMediaFolder/media/image14.png)

*Supplementary Figure 15: The obtained boxplot picture for the measured
genetic distances for Saccharomyces cerevisiae.*

References
-------------

* Blankenberg,D. *et al.* (2010) Galaxy: a web-based genome analysis tool
for experimentalists. *Current protocols in molecular biology / edited
by Frederick M. Ausubel \... \[et al.\]*, **Chapter 19**, Unit 19 10
1-21.  
* Bolyen,E. *et al.* (2019) Reproducible, interactive, scalable and
extensible microbiome data science using QIIME 2. *Nature
Biotechnology*, **37**, 852--857.  
* Bremges,A. *et al.* (2020) CAMITAX: Taxon labels for microbial genomes. *GigaScience*, **9**.  
Caporaso,J.G.*et al.* (2010)QIIME allows analysis of high-throughput community
sequencing data. *Nature methods*, **7**, 335--6.  
* Fosso,B. *et al.*(2015) BioMaS: a modular pipeline for Bioinformatic analysis of
Metagenomic AmpliconS. *BMC bioinformatics*, **16 %6**, 203 % &.  
* Klemetsen,T. *et al.* (2018) The MAR databases: development and
implementation of databases specific for marine metagenomics. *Nucleic
Acids Research*, **46**, D692--D699.  
* Meyer,C.P. and Paulay,G. (2005) DNA Barcoding: Error Rates Based on Comprehensive Sampling. *PLOS Biology*,
**3**, e422.  
* Mitchell,A.L. *et al.* (2020) MGnify: the microbiome analysis resource in 2020. *Nucleic Acids Research*, **48**,
D570--D578.  
* Open Source Cloud Computing Infrastructure (2021). 
* *OpenStack*.Recas - ReCaS Bari (2021).  
* Robertsen,E.M. *et al.* (2016) Meta-pipe-pipeline annotation, analysis and visualization of marine
metagenomic sequence data. *arXiv preprint arXiv:1604.04103*, **%6**, %& .  
* Sambo,F. *et al.* (2018) Optimizing PCR primers targeting the
bacterial 16S ribosomal RNA gene. *BMC Bioinformatics*, **19**,
343.  
* Schloss,P.D. *et al.* (2009) Introducing mothur: open-source,
platform-independent, community-supported software for describing and
comparing microbial communities. *Applied and environmental
microbiology*, **75**, 7537--41.  
* Tangaro,M.A. *et al.* (2020) Laniakea:
an open solution to provide Galaxy 'on-demand' instances over
heterogeneous cloud infrastructures. *Gigascience*, **9**.  
* TOSCA Simple Profile in YAML Version 1.0 (2021).  
* Wilkinson,M.D. *et al.* (2016) The
FAIR Guiding Principles for scientific data management and stewardship.
*Sci Data*, **3**, 160018.

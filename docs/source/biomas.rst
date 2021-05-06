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

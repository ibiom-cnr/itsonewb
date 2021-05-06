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

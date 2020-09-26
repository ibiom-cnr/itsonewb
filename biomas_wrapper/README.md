BioMaS Galaxy
=============

A modular pipeline for Bioinformatic analysis of Metagenomic AmpliconS (Galaxy Version 0.1.0)

![biomas wrapper](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/biomas/biomas_galaxy.png)

BioMaS Galaxy usage
-------------------

1. Select your input files:

![data input selection](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/biomas/biomas_galaxy_1.png)

2. Submit your job:

![data input selection](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/biomas/biomas_galaxy_2.png)

3. BioMaS Output

The output ov BioMaS tools is composed by two output collection: the fastqc output and the BioMaS pipeline output

<img src="https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/biomas/biomas_output_1.png" width="500" height="500"/>
![biomas_output_1](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/biomas/biomas_output_2.png)
![biomas_output_1](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/biomas/biomas_output_3.png)

by clicking on the "eye" icon is possible to preview the results, while expanding each entry is possible to download the results.
![biomas_output_1](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/biomas/biomas_output_4.png)

The fastqc output can be easily shown in galaxy:

![biomas_output_1](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/biomas/biomas_output_fastqc.png)

The biomas output is made by:

- the dereplicated output;

- the not combined output;

- the taxonomc classification;

- the taxonomic summary;

- the SVG Tree (you have to download it to display).


Testing BioMaS Galaxy
---------------------




Requirements
------------

Xfvb is needed to run ese2, without X.org server. On CentOS:

```
# yum install xorg-x11-server-Xvfb
```

On Ubuntu:
```
# apt-get install libxrender1 libsm6 libxt6
```

Usearch is needed and cannot be distributed with BioMaS, due to its licence. Download it and move it in `/usr/bin`.

Copy the ``New_TANGO_perl_version`` directory in `/home/galaxy`.

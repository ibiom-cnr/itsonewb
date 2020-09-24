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

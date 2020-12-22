Mopo16s Galaxy wrapper
======================

The [Mopo16s](https://www.dei.unipd.it/~baruzzog/mopo16S.html) software tool is a computational method for optimizing the choice of primer sets, based on multi-objective optimization, which simultaneously: 1) maximizes efficiency and specificity of target amplification; 2) maximizes the number of different bacterial 16S sequences matched by at least one primer; 3) minimizes the differences in the number of primers matching each bacterial 16S sequence. The algorithm can be applied to any desired amplicon length without affecting computational performance.

![Mopo16s wrapper](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/mopo16s/mopo16s_home.png)

This repository hosts only information on Mopo16s Galaxy wrapper. More information on Mopo16s can be found [here](https://www.dei.unipd.it/~baruzzog/mopo16S.html).

Usage
-----

Mopo16s input data can be created using the ITSoneWB tools [Prepare primer input inference file](https://github.com/ibiom-cnr/itsonewb/tree/master/prepare_primer_inference_files_wrapper#prepare-primer-input-inference).

The tool provides four outputs:

1. init primers:

![Mopo16s_output_1](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/mopo16s/mopo16s_output_1.png)

2. init scores:

![Mopo16s_output_2](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/mopo16s/mopo16s_output_2.png)

3. output primers:

![Mopo16s_output_3](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/mopo16s/mopo16s_output_3.png)

4. output scores:

![Mopo16s_output_4](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/mopo16s/mopo16s_output_4.png)

Reference primer pair
---------------------

The reference primer pair can be loaded by the Galaxy History or the user can use the built in pair.

The reference primer pair is:

```
>forward
GAACCWGCGGARGGATCA

>reverse
GCTGCGTTCTTCATCGATGC
```

Advanced options
----------------

All Mopo16s options are parsed by our Galaxy wrapper and hidden under the ``advanced menu`` option:

![Mopo16s_advanced_options_1](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/mopo16s/mopo16s_advanced_options_1.png)
![Mopo16s_advanced_options_2](https://github.com/ibiom-cnr/itsonewb/raw/master/docs/images/mopo16s/mopo16s_advanced_options_2.png)

All Mopo16s option are listed and explained [here](https://www.dei.unipd.it/~baruzzog/mopo16S.html#Usag). Moreover each option help is reported in the tool in-line help.

References
----------

Sambo et al., BMC Bioinformatics, 2018, 19.1: 343. [https://doi.org/10.1186/s12859-018-2360-6](https://doi.org/10.1186/s12859-018-2360-6)

[back to home](https://github.com/ibiom-cnr/itsonewb/tree/master/README.md)

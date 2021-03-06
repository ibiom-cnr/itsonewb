Primer Design tools
===================

The Primer Design service uses the mopo16S tool to infer the best primer pair able to amplify the ITS1 belonging to the taxonomic clade settled by the user.

.. figure:: /_static/img/intro/image12.jpg
   :scale: 30 %
   :align: center

*Supplementary Figure 13: A snapshot of the tool submission mask.*

Initially, the user needs to apply the **Prepare primer input inference file** tool, allowing to extract all the ITS1 sequences available for a specific clade in ITSoneDB. The user must select the taxonomic clade of interest. In order to streamline the taxon name searching an interactive drop-down menu is available. The sequence clustering (``Enable clustering`` button) is enabled by default and may be disabled only for datasets with less than 1000 sequences. Once executed, the tool will generate a fasta sequences collection that will constitute the mopo16S tool input.

Following, the primer inference is performed by using the mopo16S tools.

The tool execution requires 2 mandatory inputs:

#.  Reference dataset file: a fasta collection of target sequences uploaded by the users or generated by using the **Prepare primer input inference file** tool;

#.  Reference primer file: mopo16s requires an initial primer set to eventually infer new primers. Otherwise a primer pair can be provided by the system \[PMID:25077016\].

It is also possible to set advanced parameters, for whose description we suggest to visit the `developer site <https://www.dei.unipd.it/~baruzzog/mopo16S.html>`_.

Mopo16S starts by inferring the efficiency (a measure of the amplification capacity of each primer), the coverage (``virtually amplified`` sequences in input collection) and the matching-bias (mismatches between primers and input sequences) of the submitted primer pairs. Then infers a new primer pair (or a set of pairs) that maximise the efficiency and coverage and minimize the matching-bias. 

Three outputs are produced:

#.  Efficiency, coverage and matching bias of the input primer pair;

#.  A list of new primers;

#.  Efficiency, coverage and matching bias of the new designed primers;

.. toctree::
   :maxdepth: 2
   :caption: Tools

   mopo16s.rst
   prepare_primer_input_inference.rst
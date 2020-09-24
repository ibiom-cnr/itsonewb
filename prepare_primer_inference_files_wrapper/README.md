Prepare primer input inference
==============================

The tool create primer input inference file for mopo16s tool.

Galaxy usage
-------------

To run the tool using ITSoneWB wrapper:

1. Select the taxon name in the tool menu:
![prepare_primer_input_view](https://gitlab.com/mtangaro/itsonewb/-/raw/master/docs/images/prepare_primer_inference_files_wrapper/prepare_input_1.png)

2. Submit your request:
![prepare_primer_input_submit](https://gitlab.com/mtangaro/itsonewb/-/raw/master/docs/images/prepare_primer_inference_files_wrapper/prepare_input_2.png)

3. The output can be esily reproduced from the history or downloaded.
![prepare_primer_input_results](https://gitlab.com/mtangaro/itsonewb/-/raw/master/docs/images/prepare_primer_inference_files_wrapper/prepare_input_3.png)

4. If no output is crated, an error will be displayed:
![prepare_primer_input_error](https://gitlab.com/mtangaro/itsonewb/-/raw/master/docs/images/prepare_primer_inference_files_wrapper/prepare_input_error.png)

Command line usage
------------------

To run the tool using the `prepare_input_file2primer_inference.py` script:

```
python prepare_input_file2primer_inference.py -t Aspergillus -f ITS1_r131_plus_flanking_region.fna.gz -p node2tax_name_path.tsv.gz -o output.fa
```

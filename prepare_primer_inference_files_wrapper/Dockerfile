# Prepare Input Reference Files

FROM continuumio/miniconda3

MAINTAINER ma.tangaro@ibiom.cnr.it

RUN conda create --name prepare_input_reference_files python=2.7 vsearch -c conda-forge -c bioconda && \
    conda clean --tarballs --yes > /dev/null

COPY . /opt/prepare_input_reference_files

# Add ITSoneDB Reference data
RUN mv /opt/prepare_input_reference_files/ITS1_r131_plus_flanking_region.fna.gz /refdata/ITS1_r131_plus_flanking_region.fna.gz
RUN mv /opt/prepare_input_reference_files/files_wrapper/node2tax_name_path.tsv.gz /refdata/node2tax_name_path.tsv.gz

# Make RUN commands use the new environment:
RUN chmod +x /opt/prepare_input_reference_files/prepare-input-reference-files
ENV PATH /opt/prepare_input_reference_files:$PATH

RUN echo "source activate prepare_input_reference_files" >> ~/.bashrc
ENV PATH /opt/conda/envs/prepare_input_reference_files/bin:$PATH

RUN mkdir -p /data
WORKDIR /data

# BioMaS
# Ete2 requires pyqt4 and qt4 to properly run.
# XVFB is used instead of xorg.
# In this case conda is not installing libfontconfig, so it is explicitly installed with apt.

FROM continuumio/miniconda3

MAINTAINER ma.tangaro@ibiom.cnr.it

RUN conda create --name biomas python=2.7 qt=4.8.7 fastqc bowtie2 numpy pysam biopython FLASH trim-galore ete2 xvfbwrapper vsearch argcomplete cython -c conda-forge -c bioconda && \
    conda clean --tarballs --yes > /dev/null

COPY . /opt/biomas

# Copy script to /usr/local/bin, otherwise the biomas_wrapper.py will not find the executable
ADD quality_check_and_consensus.py /usr/local/bin/quality_check_and_consensus.py
ADD bowtie2-execution_ITSoneDB.py /usr/local/bin/bowtie2-execution_ITSoneDB.py
ADD new_tree_builder_for_perl_tango.py /usr/local/bin/new_tree_builder_for_perl_tango.py

# Copy BioMaS Wrapper
ADD biomas_wrapper.py /usr/local/bin/biomas
RUN chmod +x /usr/local/bin/biomas

# Build BioMaS Cython functions
WORKDIR /opt/biomas

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "biomas", "/bin/bash", "-c"]

# Install dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y gcc libfontconfig xvfb libtbb-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Build BioMaS Cython function
RUN python setup.py build_ext --inplace

# Add Reference data
COPY ./bowtie2_indexes_rel138/ /refdata/bowtie2_indexes_rel138
COPY ./New_TANGO_perl_version /opt/tango/New_TANGO_perl_version

# Make RUN commands use default environment
SHELL ["/bin/bash", "-c"]

# Make RUN commands use the new environment:
RUN echo "source activate biomas" > ~/.bashrc
ENV PATH /opt/conda/envs/biomas/bin:$PATH

RUN mkdir -p /data
WORKDIR /data

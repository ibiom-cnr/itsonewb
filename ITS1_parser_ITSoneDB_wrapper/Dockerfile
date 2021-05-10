# ITS1 to ITSoneDB

FROM continuumio/miniconda3

MAINTAINER ma.tangaro@ibiom.cnr.it

RUN conda create --name its1-to-itsonedb python=2.7 bowtie2=2.3.4.3 argcomplete=1.9.4 numpy=1.15.4 pysam -c conda-forge -c bioconda && \
    conda clean --tarballs --yes > /dev/null

COPY . /opt/its1_to_itsonedb

# Add ITSoneDB Reference data
ADD http://cloud.recas.ba.infn.it:8080/v1/AUTH_3b4918e0a982493e8c3ebcc43586a2a8/ITSoneWB/itsonedb_r131_biomas_indexes.tar.gz /refdata/itsonedb_r131_biomas_indexes.tar.gz
RUN cd /refdata && \
    tar xvzf /refdata/itsonedb_r131_biomas_indexes.tar.gz && \
    rm /refdata/itsonedb_r131_biomas_indexes.tar.gz

# Make RUN commands use the new environment:
RUN echo "alias ITS1-mapper-and-parser='python /opt/its1_to_itsonedb/ITS1_mapper_and_parser.py'" > ~/.bashrc
RUN echo "source activate its1-to-itsonedb" >> ~/.bashrc
ENV PATH /opt/conda/envs/its1-to-itsonedb/bin:$PATH

RUN mkdir -p /data
WORKDIR /data

# TSoneWB Connector

FROM continuumio/miniconda3

MAINTAINER ma.tangaro@ibiom.cnr.it

RUN conda create --name itsonewb python=2.7  sqlalchemy=1.2.8 mysql-python=1.2.5 -c conda-forge -c bioconda && \
    conda clean --tarballs --yes > /dev/null

ADD itsonedb_wrapper.py /usr/local/bin/itsonedb-connector

RUN chmod +x /usr/local/bin/itsonedb-connector

# Make RUN commands use the new environment:
RUN echo "source activate itsonewb" > ~/.bashrc
ENV PATH /opt/conda/envs/itsonewb/bin:$PATH

RUN mkdir -p /data
WORKDIR /data

# Barcoding Gap inference

FROM continuumio/miniconda3

MAINTAINER ma.tangaro@ibiom.cnr.it

RUN conda create --name barcoding_gap python=2.7 numpy matplotlib pandas plotnine -c conda-forge -c bioconda && \
    conda clean --tarballs --yes > /dev/null

COPY . /opt/barcoding_gap

# Add Reference data
ADD http://cloud.recas.ba.infn.it:8080/v1/AUTH_2e1bc341b93f480e9b936112962613d8/ITSoneWB/barcoding_gap.tar.gz /refdata/barcoding_gap.tar.gz
RUN cd /refdata && \
    tar xvzf barcoding_gap.tar.gz && \
    rm barcoding_gap.tar.gz

# Make RUN commands use the new environment:
COPY /opt/barcoding_gap/print_bg.py /opt/barcoding_gap/print-bg
RUN chmod +x /opt/barcoding_gap/print-bg
ENV PATH /opt/barcoding_gap:$PATH

RUN echo "source activate barcoding_gap" >> ~/.bashrc
ENV PATH /opt/conda/envs/barcoding_gap/bin:$PATH

RUN mkdir -p /data
WORKDIR /data

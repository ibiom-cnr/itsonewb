# Mopo16s

FROM continuumio/miniconda3

MAINTAINER ma.tangaro@ibiom.cnr.it

# Install dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y build-essential gcc unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD http://packages.seqan.de/seqan-src/seqan-src-2.1.1.tar.gz /opt/seqan-src-2.1.1.tar.gz

RUN cd /opt && \
    tar xvzf seqan-src-2.1.1.tar.gz && \
    rm /opt/seqan-src-2.1.1.tar.gz

ADD http://www.dei.unipd.it/~baruzzog/mopo16S/last_version/mopo16S.zip /opt/

RUN cd /opt && \
    unzip /opt/mopo16S.zip && \
    rm /opt/mopo16S.zip

RUN sed -i 's$CXXFLAGS+=-I../../seqan-library-2.0.0/include$CXXFLAGS+=-I/opt/seqan-seqan-v2.1.1/include$g' /opt/mopo16s/Makefile.rules

RUN cd /opt/mopo16s && make

RUN echo "export PATH=/opt/mopo16s/release:$PATH" >> ~/.bashrc
ENV PATH /opt/mopo16s/release:$PATH

RUN mkdir -p /data
WORKDIR /data

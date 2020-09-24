import argparse
import gzip
import os
import time
from string import strip
import sys

def name_search(input_tab, name):
    acc_list = []
    with gzip.open(input_tab) as tab:
        for line in tab:
            s = map(strip, line.split("\t"))
            path = map(strip, s[1].split(";"))
            if name in path:
                acc_list.append(s[0])
    return acc_list


def fasta2dict(fasta_seq):
    acc2seq = {}
    acc = ""
    with gzip.open(fasta_seq) as seq_file:
        for line in seq_file:
            if line.startswith(">"):
                acc = line.split()[0][1:]
                acc2seq[acc] = [line.strip(), ""]
            else:
                acc2seq[acc][1] += line.strip()
    return acc2seq


def fasta_parsing(fasta_file, acc_list, out_file):
    if out_file is None:
        folder = time.strftime("%b_%d_%Y_%H_%M_%S", time.localtime())
        while os.path.exists(folder):
            folder = time.strftime("%b_%d_%Y_%H_%M_%S", time.localtime())
        else:
            os.mkdir(folder)
        out_file = os.path.join(folder, "input_seq.fa")
        tmp = open(os.path.join(folder, "input_seq.fa"), "w")
    else:
        tmp = open(out_file, "w")
    seq_diz = fasta2dict(fasta_file)
    for accession in acc_list:
        tmp.write("%s\n" % seq_diz[accession][0])
        tmp.write("%s\n" % seq_diz[accession][1])
    tmp.close()
    return out_file

def clustering(fasta_in):
    import subprocess, shlex, shutil
    cmd = shlex.split("vsearch --cluster_fast %s --id 0.97 --centroids tmp" % fasta_in)
    p = subprocess.Popen(cmd)
    p.wait()
    if os.path.exists("tmp") and os.stat("tmp")[6] != 0:
        shutil.move("tmp",fasta_in)
    return fasta_in

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script extract the input ITS1 sequences according to a taxonomic name.", prefix_chars="-",
        usage="prepare_input_file2primer_inference.py -t 'Aspergillus Flavus' -f fasta_file -p taxonomy_file")
    parser.add_argument("-t", "--taxon_name", help="Taxon name [MANDATORY]", action="store",
                        required=True)
    parser.add_argument("-p", "--tax_path",
                        help="CSV file containing the association between the accession number and the taxonomic path "
                             "[MANDATORY]",
                        action="store",
                        required=True)
    parser.add_argument("-f", "--fasta",
                        help="FASTA file containing the ITS1 sequences and the flanking regions [MANDATORY]",
                        action="store", required=True)
    parser.add_argument("-o", "--output_file",
                        help="complete path and name of the output file",
                        action="store", required=False, default=None)
    parser.add_argument("-c","--cluster",action='store_false', help= "If the number of selected ITS1 sequences is more than 1000, the sequences are clusterd at 97% of identity", default=True)
    args = parser.parse_args()
    taxa = args.taxon_name
    output = args.output_file
    # print str(taxa)
    fasta = args.fasta
    path_list = args.tax_path
    cluster = args.cluster
    lista_accession = name_search(path_list, taxa)
    if cluster and lista_accession >= 1000:
        print clustering(fasta_parsing(fasta, lista_accession, output))
    else:
        print fasta_parsing(fasta, lista_accession, output)

    if os.stat(output).st_size == 0:
        sys.stderr.write('No output. The file is empty.')
    else:
        sys.stdout.write('DONE')

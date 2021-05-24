#!/usr/bin/env python
__author__ = 'Bruno Fosso'
__version__ = 2.0

import argcomplete
import argparse
import os
import shlex
import subprocess
import sys
from string import strip

from numpy import mean as calcola_media
from pysam import Samfile


def ITS1_parser():
    parser = argparse.ArgumentParser(description="Map and parse metagenomic data to ITSoneDB", prefix_chars="-")
    parser.add_argument("-f", "--ITSoneDB_fasta", type=str,
                        help="fasta file containing the ITSoneDB sequences",
                        action="store", required=False)
    parser.add_argument("-p1", "--paired1", type=str,
                        help="paired-end fastq file R1. Multiple files must be listed space separated",
                        action="store", required=False, nargs="*", default=[])
    parser.add_argument("-p2", "--paired2", type=str,
                        help="paired-end fastq file R2. Multiple files must be listed space separated",
                        action="store", nargs="*", default=[], required='--paired1' in sys.argv)
    parser.add_argument("-s", "--single", type=str, help="single-end sam file", action="store", required=False,
                        nargs="*", default=[])
    parser.add_argument("-i", "--identity_percentage", type=float,
                        help="identity percentage threshold (a floating number from 0 to 1, default is 0.97)",
                        action="store", required=False, default=97)
    parser.add_argument("-c", "--coverage", type=float,
                        help="Coverage of the query sequence (a floating number from 0 to 1, default is 0.7)",
                        action="store", required=False,
                        default=0.7)
    parser.add_argument("-b", "--bowtie_index", type=str,
                        help="Path to the bowtie index folder",
                        action="store", required=False,
                        default="/home/bfosso/share/bowtie2_db/ITSoneDB/ITSoneDB_all_EUkaryotes/ITSoneDB_all_euk_r131")
    parser.add_argument("-d", "--output_folder", type=str,
                        help="Path to the folder where intermediate files will be written",
                        action="store", required=False,
                        default=os.getcwd())
    parser.add_argument("-t", "--threads", type=str,
                        help="number of threads",
                        action="store", required=False,
                        default="10")
    parser.add_argument("-n", "--match_number", type=str,
                        help="number of bowtie matches",
                        action="store", required=False,
                        default="50")
    argcomplete.autocomplete(parser)
    return parser.parse_args()


def cigar_parsing(cigar_object):
    cigar_list = list(cigar_object)
    mm = 0
    insertion = 0
    d = 0
    for item in cigar_list:
        if item[0] == 0:
            mm += item[1]
        elif item[0] == 1:
            insertion += item[1]
        elif item[0] == 2:
            d += item[1]
    alen = mm + insertion + d
    qalgn = float(mm + insertion)
    return alen, qalgn


def make_tuple(identifier):
    parts = identifier.split("|")
    return parts[0]


def itsonedb2node(itsonedb_fasta_file):
    diz = {}
    """

    :param itsonedb_fasta_file: a fasta file downladed from ITSoneDB (http://itsonedb.cloud.ba.infn.it)
    :return: a dictionary containing the association between the ITSoneDB accession number and NCBI taxonomy identifier.
    :return: If the input fasta file is None or it doesn't exist the function returns None
    """
    import os
    if itsonedb_fasta_file is not None:
        if os.path.exists(itsonedb_fasta_file):
            with open(itsonedb_fasta_file) as b:
                for linea in b:
                    if linea.startswith(">"):
                        s = map(strip, linea.split("\t"))
                        diz[s[0].lstrip(">")] = s[-2]
        else:
            diz = None
    else:
        diz = None
    return diz


def verifica_file(file_name):
    if os.path.exists(file_name):
        res = True
    else:
        res = False
    return res


def error_file_check(l):
    from string import find
    count = 0
    for line in open(l):
        line = line.strip()
        if find(line.lower(), "error") != -1:
            count += 1
    return count


def bowtie_pair(R1_list, R2_list, indici, threads, match_n, out_f):
    out_sam_list = []
    sam_output_glocal = os.path.join(out_f, "paired_glocal.sam")
    cmd = shlex.split(
        "bowtie2 -q -N1 -k%s -L20 --no-unal -x  %s -1 %s -2 %s -S %s -p %s --mm" % (
            match_n, indici, ",".join(R1_list), ",".join(R2_list), sam_output_glocal, threads))
    # print cmd
    tmp = open(os.path.join(out_f, "error.lst"), "w")
    p = subprocess.Popen(cmd, stderr=tmp)
    p.wait()
    tmp.close()
    if error_file_check(os.path.join(out_f, "error.lst")) == 0:
        out_sam_list.append(sam_output_glocal)
    else:
        out_sam_list.append(None)
    sam_output_local = os.path.join(out_f, "paired_local.sam")
    cmd = shlex.split(
        "bowtie2 -q -N1 -k%s -L20 --local --no-unal -x  %s -1 %s -2 %s -S %s -p %s --mm" % (
            match_n, indici, ",".join(R1_list), ",".join(R2_list), sam_output_local, threads))
    tmp = open(os.path.join(out_f, "error.lst"), "w")
    # print cmd
    p = subprocess.Popen(cmd, stderr=tmp)
    p.wait()
    tmp.close()
    if error_file_check(os.path.join(out_f, "error.lst")) == 0:
        out_sam_list.append(sam_output_local)
    else:
        out_sam_list.append(None)
    return out_sam_list


def bowtie_single(single_list, indici, threads, match_n, out_f):
    out_sam_list = []
    sam_output_glocal = os.path.join(out_f, "single_glocal.sam")
    cmd = shlex.split(
        "bowtie2 -q -N1 -k%s -L20 --no-unal -x  %s -U %s -S %s -p %s --mm" % (
            match_n, indici, ",".join(single_list), sam_output_glocal, threads))
    tmp = open(os.path.join(out_f, "error.lst"), "w")
    # print cmd
    p = subprocess.Popen(cmd, stderr=tmp)
    p.wait()
    tmp.close()
    if error_file_check(os.path.join(out_f, "error.lst")) == 0:
        out_sam_list.append(sam_output_glocal)
    else:
        out_sam_list.append(None)
    sam_output_local = os.path.join(out_f, "single_local.sam")
    cmd = shlex.split(
        "bowtie2 -q -N1 -k%s -L20 --local --no-unal -x  %s -U %s -S %s -p %s --mm" % (
            match_n, indici, ",".join(single_list), sam_output_local, threads))
    tmp = open(os.path.join(out_f, "error.lst"), "w")
    # print cmd
    p = subprocess.Popen(cmd, stderr=tmp)
    p.wait()
    tmp.close()
    if error_file_check(os.path.join(out_f, "error.lst")) == 0:
        out_sam_list.append(sam_output_local)
    else:
        out_sam_list.append(None)
    return out_sam_list


def index_controll(f, prefisso):
    c = 0
    for name in os.listdir(f):
        if name.startswith(prefisso) and name.endswith("bt2"):
            c += 1
    if c != 6:
        sys.exit("In the index folder some index files are missing")


def single_end_sam_parsing(sam_list, cov, identity_threshold):
    match = {}
    to_process = []
    if sam_list[0] is None:
        print "The ene-to-end mapping of SE data produced an error."
    else:
        to_process.append(sam_list[0])
    if sam_list[1] is None:
        print "The local mapping mode of SE data  produced an error."
    else:
        to_process.append(sam_list[1])
    for single_sam in to_process:
        sam = Samfile(single_sam)
        for align in sam:
            if align.tid != -1:
                query_name, query_len, ref_name = align.qname, float(align.rlen), sam.getrname(align.tid)
                if align.cigar is not None:
                    align_len, query_aligned_len = cigar_parsing(align.cigar)
                    nm = -1
                    if (query_aligned_len / query_len) * 100 >= cov:
                        for coppia in align.tags:
                            if coppia[0] == "NM":
                                nm = float(coppia[1])
                    if align_len != 0 and nm >= 0:
                        paired_perc_id = ((align_len - nm) / align_len) * 100
                        if paired_perc_id >= identity_threshold:
                            match.setdefault(query_name, set())
                            match[query_name].add(ref_name)
        sam.close()
    return match


def paired_end_sam_parsing(sam_list, cov, identity_threshold):
    match = {}
    to_process = []
    if sam_list[0] is None:
            print "The ene-to-end mapping of SE data produced an error."
    else:
        to_process.append(sam_list[0])
    if sam_list[1] is None:
        print "The local mapping mode of SE data  produced an error."
    else:
        to_process.append(sam_list[1])
    for paired_sam in to_process:
        r1_match = {}
        r2_match = {}
        sam = Samfile(paired_sam)
        for align in sam:
            if align.tid != -1:
                query_name, query_len, ref_name = align.qname, float(align.rlen), sam.getrname(align.tid)
                if align.cigar is not None:
                    align_len, query_aligned_len = cigar_parsing(align.cigar)
                    # print query_name, align_len, query_aligned_len
                    nm = -1
                    if (query_aligned_len / query_len) * 100 >= cov:
                        for coppia in align.tags:
                            if coppia[0] == "NM":
                                nm = float(coppia[1])
                    if align_len != 0 and nm >= 0:
                        paired_perc_id = ((align_len - nm) / align_len) * 100
                        if paired_perc_id >= 90:
                            if align.is_read1:
                                r1_match.setdefault(query_name, {})
                                r1_match[query_name].setdefault(ref_name, [])
                                r1_match[query_name][ref_name].append(paired_perc_id)
                            if align.is_read2:
                                r2_match.setdefault(query_name, {})
                                r2_match[query_name].setdefault(ref_name, [])
                                r2_match[query_name][ref_name].append(paired_perc_id)
        sam.close()
        for query in set(r1_match.keys()).intersection(set(r2_match.keys())):
            for ref in set(r1_match[query].keys()).intersection(r2_match[query].keys()):
                average_perc_id = calcola_media([max(r1_match[query][ref]), max(r2_match[query][ref])])
                if average_perc_id >= identity_threshold:
                    match.setdefault(query, set())
                    match[query].add(ref)
    return match


if __name__ == "__main__":
    args = ITS1_parser()
    fasta_itesondb = args.ITSoneDB_fasta
    R1 = args.paired1
    R2 = args.paired2
    single = args.single
    identity_perc = args.identity_percentage * 100
    coverage = args.coverage * 100
    bowtie_index = args.bowtie_index
    folder = args.output_folder
    processori = args.threads
    expected_matches = args.match_number
    outfile = open(os.path.join(folder, "mapping_file.tsv"), "w")

    acc2node = itsonedb2node(fasta_itesondb)
    index_folder, basename = os.path.split(bowtie_index)
    index_controll(index_folder, basename)

    paired_matches = None
    single_matches = None
    # verifichiamo che tutti i file siano disponibili
    if R1:
        for i in R1:
            if verifica_file(i) is False:
                sys.exit("the following file is missing:  %s" % i)

    if R2:
        for i in R2:
            if verifica_file(i) is False:
                sys.exit("the following file is missing:  %s" % i)
        if len(R1) == len(R2):
            print "Paired End files mapping on ITSoneDB"
            paired_matches = paired_end_sam_parsing(bowtie_pair(R1, R2, bowtie_index, processori, expected_matches, folder),
                                                coverage, identity_perc)
        else:
            sys.exit("Please note you have to submit the same number of forward and reverse fastq files")

    if single:
        for i in single:
            if verifica_file(i) is False:
                sys.exit("the following file is missing:  %s" % i)
        print "Single End files mapping on ITSoneDB"
        single_matches = single_end_sam_parsing(
            bowtie_single(single, bowtie_index, processori, expected_matches, folder),
            coverage, identity_perc)

    if paired_matches is not None:
        for acc in paired_matches.keys():
            if acc2node is not None:
                match_list = [acc2node[make_tuple(i)] for i in paired_matches[acc]]
                outfile.write("%s %s\n" % (acc, " ".join(match_list)))
            else:
                match_list = [make_tuple(i) for i in paired_matches[acc]]
                outfile.write("%s %s\n" % (acc, " ".join(match_list)))
    if single_matches is not None:
        for acc in single_matches.keys():
            if acc2node is not None:
                match_list = [acc2node[make_tuple(i)] for i in single_matches[acc]]
                outfile.write("%s %s\n" % (acc, " ".join(match_list)))
            else:
                match_list = [make_tuple(i) for i in single_matches[acc]]
                outfile.write("%s %s\n" % (acc, " ".join(match_list)))
    outfile.close()
    print "DONE"

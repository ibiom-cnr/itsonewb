__author__ = 'Bruno Fosso'
__version__ = 1.0

import json
import sys
import os
import gzip
from numpy import asarray
from numpy import mean as calcola_media
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from pysam import Samfile
from ete2 import *


def controllo_esecuzione(l):
    if not os.path.exists(l):
        sys.exit("no paired-end file list!!!")

def acc_modifier(acc_num):
    if acc_num[-2] == "/":
        s = acc_num.split("/")
        acc = s[0]
    else:
        s = acc_num.split(" ")
        acc = s[0]
    return acc

def parse_fastq_for_control(a):
    acc_list = set()
    size_list = []
    if not a.endswith("gz"):
        with open(a) as read_file:
            line = read_file.readline()
            if line.startswith("@"):
                read_file.seek(0)
                for title, seq, qual in FastqGeneralIterator(read_file):
                    acc_list.add(acc_modifier(title))
                    size_list.append(len(seq))
            else:
                print line
                acc_list = None
    else:
        with gzip.open(a) as read_file:
            line = read_file.readline()
            if line.startswith("@"):
                read_file.seek(0)
                for title, seq, qual in FastqGeneralIterator(read_file):
                    acc_list.add(acc_modifier(title))
                    size_list.append(len(seq))
            else:
                acc_list = None
    return acc_list, size_list

def verify_PE_files(a, b):
    result = None
    error = ""
    r1_acc, r1_size = parse_fastq_for_control(a)
    r2_acc, r2_size = parse_fastq_for_control(b)
    sizes = asarray(r1_size+r2_size)
    if r1_acc and r2_acc is not None:
        print len(r1_acc), len(r2_acc)
        if not len(r1_acc) == len(r2_acc) and not len(r1_acc.intersection(r2_acc)) == len(r1_acc):
            error += "\tunequal number of PE reads among files"
    else:
        error += "\tThe indicated fastq files are not in fastq format"
    if not error == "":
        result = error
    return result, sizes

def controllo_quality_check(l):
    if os.path.exists(l):
        print "quality_check_and_consensus.py completes its computation"
    else:
        print "Errors during quality_check_and_consensus.py computation"
        sys.exit()

def index_controll(path):
    """
    This function verifies the bowtie2 indexes
    :param path:
    :type path: str
    """
    cdef int c = 0
    f, prefisso = os.path.split(path)
    for name in os.listdir(f):
        if name.startswith(prefisso) and name.endswith("bt2"):
            c += 1
    if c != 6:
        sys.exit("In the index folder some index files are missing")

def make_tuple(identifier):
    """
    converts the identifier
    :param identifier: accession number
    :type identifier: str
    :return parts[0]: str
    """
    parts = identifier.split("|")
    return parts[0]


def verify_mapping_file(itsonedb_json_file):
    diz = None
    errore = None
    if os.path.exists(itsonedb_json_file):
        if itsonedb_json_file.endswith(".json.gz"):
            with gzip.open(itsonedb_json_file) as b:
                diz = json.load(b)
        else:
            with open(itsonedb_json_file) as b:
                diz = json.load(b)
    else:
        diz = None
        errore = "The mapping file does not exist"
    return diz, errore

def prune_match(set match_list, acc2node):
    """

    :param match_list:
    :type match_list: list
    :param acc2node:
    :type acc2node: dict
    :return result:
    """
    unc_id = ("447265","175245")
    ok_list = []
    not_ok_list = []
    result = None
    for acc in match_list:
        acc = make_tuple(acc)
        if acc in acc2node:
            node = acc2node[acc].split("|")[1]
            if node in unc_id:
                not_ok_list.append(node)
            else:
                ok_list.append(node)
    if len(ok_list) > 0:
        result = ok_list
    elif len(not_ok_list) > 0:
        result = not_ok_list
    return result

def cigar_parsing(list cigar_object):
    """
    This function parses CIGAR objects in SAM file.
    :param cigar_object: object containing the CIGAR field
    :type cigar_object: list
    :return alen: alignment len
    :return qalgn: aligned query length
    """
    cdef int mm, insertion, d
    cdef (int, int) item
    mm, insertion, d = 0, 0 ,0
    for item in cigar_object:
        if item[0] == 0:
            mm += item[1]
        elif item[0] == 1:
            insertion += item[1]
        elif item[0] == 2:
            d += item[1]
    alen = float(mm + insertion + d)
    qalgn = float(mm + insertion)
    return alen, qalgn

def single_end_sam_parsing(list sam_list):
    """
    SAM parsing for SE alignments.
    :param sam_list: list containing the produced sam files
    :type sam_list: list
    :return match_over_97: dictionary containing the significant matches
    :return match_under_97: dictionary containing the significant matches
    :return mapped: set containing mapped items
    """
    cdef list to_process = []
    cdef int align_len, query_aligned_len
    cdef float cov
    cov = 70
    mapped = set()
    match_over_97 = {}
    match_under_97 = {}
    to_process = []
    if sam_list[0] is None:
        print "The ene-to-end mapping of SE data produced an error."
    else:
        to_process.append(sam_list[0])
    if sam_list[1] is None:
        print "The local mapping mode of SE data produced an error."
    else:
        to_process.append(sam_list[1])
    for single_sam in to_process:
        with Samfile(single_sam) as sam:
            for align in sam:
                query_name, query_len, ref_name = align.qname, float(align.rlen), sam.getrname(align.tid)
                if align.cigar is not None:
                    align_len, query_aligned_len = cigar_parsing(align.cigar)
                    nm = None
                    if (query_aligned_len / query_len) * 100 >= cov:
                        nm = float(filter(lambda x: "NM" in x, align.tags)[0][1])
                    if align_len != 0 and nm is not None:
                        paired_perc_id = ((align_len - nm) / align_len) * 100
                        if paired_perc_id >= 97:
                            # print perc_id
                            match_over_97.setdefault(query_name, set())
                            match_over_97[query_name].add(ref_name)
                            mapped.add(query_name)
                        if 90 <= paired_perc_id < 97:
                            match_under_97.setdefault(query_name, set())
                            match_under_97[query_name].add(ref_name)
                            mapped.add(query_name)
    return match_over_97, match_under_97, mapped


def error_file_check(l):
    from string import find
    count = 0
    for line in open(l):
        line = line.strip()
        if find(line.lower(), "error counts") != -1:
            count += 1
    return count


def paired_end_sam_parsing(list sam_list):
    """
    SAM parsing for PE alignments.
    :param sam_list: list containing the produced sam files
    :type sam_list: list
    :return match_over_97: dictionary containing the significant matches
    :return match_under_97: dictionary containing the significant matches
    :return mapped: set containing mapped items
    """
    cdef list to_process = []
    cdef int align_len, query_aligned_len
    cdef float cov
    cov = 70
    mapped = set()
    match_over_97 = {}
    match_under_97 = {}
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
        with Samfile(paired_sam) as sam:
            for align in sam:
                query_name, query_len, ref_name = align.qname, float(align.rlen), sam.getrname(align.tid)
                if align.cigar is not None:
                    align_len, query_aligned_len = cigar_parsing(align.cigar)
                    # print query_name, align_len, query_aligned_len
                    nm = None
                    # print query_name, (query_aligned_len / query_len) * 100, cov
                    if (query_aligned_len / query_len) * 100 >= cov:
                        nm = float(filter(lambda x: "NM" in x, align.tags)[0][1])
                        # print nm
                    if align_len != 0 and nm is not None:
                        paired_perc_id = ((align_len - nm) / align_len) * 100
                        # print paired_perc_id
                        if paired_perc_id >= 90:
                            if align.is_read1:
                                r1_match.setdefault(query_name, {})
                                r1_match[query_name].setdefault(ref_name, [])
                                r1_match[query_name][ref_name].append(paired_perc_id)
                            if align.is_read2:
                                r2_match.setdefault(query_name, {})
                                r2_match[query_name].setdefault(ref_name, [])
                                r2_match[query_name][ref_name].append(paired_perc_id)
            # print r1_match.keys()
            # print r2_match.keys()
            for query in set(r1_match.keys()).intersection(set(r2_match.keys())):
                for ref in set(r1_match[query].keys()).intersection(r2_match[query].keys()):
                    average_perc_id = calcola_media([max(r1_match[query][ref]), max(r2_match[query][ref])])
                    if average_perc_id >= 97:
                        match_over_97.setdefault(query, set())
                        match_over_97[query].add(ref)
                        mapped.add(query)
                    elif 90 <= average_perc_id < 97:
                        match_under_97.setdefault(query, set())
                        match_under_97[query].add(ref)
                        mapped.add(query)
    return match_over_97, match_under_97, mapped

def tools_installation(tool_name):
    return any(
        os.access(os.path.join(path, tool_name), os.X_OK)
        for path in os.environ["PATH"].split(os.pathsep)
    )

def count_merged_seq(merged):
    acc_list = []
    with open(merged) as a:
        for title, seq, qual in FastqGeneralIterator(a):
                acc_list.append(title)
    return len(acc_list)

def my_layout(plotting_node):
    # print '--------------->'+ plotting_node.name
    nameFace = faces.AttrFace("name", fsize=10, fgcolor="#ff0000")  # nome in rosso
    orderFace = faces.AttrFace("Order", fsize=10, fgcolor="#800000")  # ordine in marrone
    rdpFace = faces.AttrFace("assigned", fsize=10, fgcolor="#0000ff")  # assegnati al nodo in blu
    progFace = faces.AttrFace("summarized", fsize=10, fgcolor="#00ff00")  # sommarizzati al nodo in verde

    if "name" in plotting_node.features and "taxid" in plotting_node.features:
        faces.add_face_to_node(nameFace, plotting_node, column=0)
        faces.add_face_to_node(orderFace, plotting_node, column=0)
        faces.add_face_to_node(rdpFace, plotting_node, column=2)
        faces.add_face_to_node(progFace, plotting_node, column=2)
        plotting_node.img_style["size"] = 12
        plotting_node.img_style["shape"] = "sphere"

def controllo_tango_exec(l, m, list q, list r):
    """
    this function verifies if tango worked properly
    :param l: tango input over 97
    :type l: str
    :param m: tango input under 97
    :type m: str
    :param q: tango output over 97
    :type q: list
    :param r: tango output under 97
    :typer r: list
    """
    if os.path.exists(l):
        if os.stat(l)[6] > 0:
            over_97, tot = None, None
            with open(l) as res_file:
                over_97 = len(res_file.readlines())
            for name_file in q:
                with open(name_file) as res_file:
                    tot = len(res_file.readlines())
            if not tot and over_97 is None and not tot == over_97:
                print "Not all the data are processed for the over_97"
    else:
        sys.exit("No tango input for sequences with a similarity percentage over the 97%")
    if os.path.exists(m):
        if os.stat(m)[6] > 0:
            under_97, tot = None, None
            with open(m) as res_file:
                under_97 = len(res_file.readlines())
            tot = 0
            for name_file in r:
                with open(name_file) as res_file:
                    tot += len(res_file.readlines())
            if not under_97 and tot is None and tot == under_97:
                print "Not all the data are processed for the over_97"
    else:
        sys.exit("No tango input for sequences with a similarity percentage under the 97%")

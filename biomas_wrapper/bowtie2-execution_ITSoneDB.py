__author__ = 'Bruno Fosso'
__version__ = 1.0

import getopt
import shlex
import subprocess
from string import strip
from numpy import mean as calcola_media
from pysam import *
import os
import sys


def usage():
    print ('This script performs the Bowtie2 execution:\n'
           'Option:'
           '\t-d database: choice the reference bowite indexes [MANDATORY]'
           '\t-v mapping file [MANDATORY]'
           '\t-h    print this help\n'
           'Usage:\n'
           '\tpython bowtie2-execution_ITSoneDB.py -d bowtie_indexes -v mapping_file\n'
           '\t')


def verify_input_bowtie_index(db):
    if db == "":
        usage()
        print "\n"
        sys.exit("-d option values is MANDATORY!!!")
    else:
        folder = "/".join(db.split("/")[:-1])
        i_name = db.split("/")[-1]
        count = 0
        if os.path.exists(folder) is False:
            usage()
            print "\n"
            sys.exit("The folder containing the bowtie indexes does not exist")
        for name in os.listdir(folder):
            if name.split(".")[0] == i_name:
                count += 1
        if count == 0:
            usage()
            print "\n"
            sys.exit("No bowtie index with the indicated name where found in the indicated path.")


def verify_mapping_file(l):
    diz = None
    if l is not "":
        if os.path.exists(l):
            diz = {}
            with open(l) as tab_file:
                for linea in tab_file:
                    field = map(strip, linea.split("\t"))
                    diz[field[0]] = field[1]
            errore = ""
        else:
            errore = "The folder containing the bowtie indexes does not exist"
    else:
        errore = "-v option values is MANDATORY!!!"
    return diz, errore


def controllo_quality_check(l):
    if os.path.exists(l):
        print "quality_check_and_consensus.py completes its computation"
    else:
        print "Errors during quality_check_and_consensus.py computation"
        sys.exit()


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


bowtie_index = ""
mapping_file = ""
try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:v:")
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit()
if len(opts) == 0:
    usage()
    sys.exit()
for o, a in opts:
    if o == "-h":
        usage()
        sys.exit()
    elif o == "-d":
        bowtie_index = a
    elif o == "-v":
        mapping_file = a
    else:
        print "Unhandled option."
        usage()
        sys.exit()

controllo_quality_check("quality_check_and_consensus.log")

basename = ""
consensus = ""
R1 = ""
R2 = ""
for line in open("quality_check_and_consensus.log"):
    line = line.strip()
    s = line.split("\t")
    if len(s) == 4:
        basename = s[0]
        consensus = s[1]
        R1 = s[2]
        R2 = s[3]
    else:
        print "not correct log file"

acc2node, error = verify_mapping_file(mapping_file)
if acc2node is None:
    usage()
    sys.exit(error)

rdp_match_over_97 = {}
rdp_match_under_97 = {}
print "Consensus processing"
# mappiamo prima in modalita' glocal
mapped = set()
bowtie2_stdout = open("bowtie2_stdout.log", "w")
bowtie2_stdout.write("Consensus processing\n")
if consensus != "none":
    print "Bowtie2 execution on Consensus data glocal mode"
    output = basename + "_consensus_glocal_ITS1.sam"
    # esecuzione del primo bowtie contro
    cmd = shlex.split(
        "bowtie2 -X 2000 -q -N1 -k100 -x " + bowtie_index + " -U " + consensus + " -S " + output + " -p 10")
    p = subprocess.Popen(cmd, stdout=bowtie2_stdout)
    p.wait()
    if os.path.exists(output):
        sam = Samfile(output)
        for align in sam:
            if align.tid != -1:
                query_name, query_len, ref_name = align.qname, float(align.rlen), sam.getrname(align.tid)
                if align.cigar is not None:
                    par_cig = cigar_parsing(align.cigar)
                    align_len, query_aligned_len = par_cig[0], par_cig[1]
                    nm = 0
                    if query_aligned_len / query_len >= 0.7:
                        for coppia in align.tags:
                            if coppia[0] == "NM":
                                nm = float(coppia[1])
                    # print nm,align_len
                    if align_len != 0 and type(nm) == float:
                        paired_perc_id = ((align_len - nm) / align_len) * 100
                        if paired_perc_id >= 97:
                            # print perc_id
                            rdp_match_over_97.setdefault(query_name, set())
                            rdp_match_over_97[query_name].add(ref_name)
                            mapped.add(query_name)
                        if 90 <= paired_perc_id < 97:
                            rdp_match_under_97.setdefault(query_name, set())
                            rdp_match_under_97[query_name].add(ref_name)
                            mapped.add(query_name)
    else:
        print "no mapping data"
        sys.exit()

    print "Bowtie2 execution on Consensus data local mode"
    output = basename + "_consensus_local_ITS1.sam"
    cmd = shlex.split(
        "bowtie2 -X 2000 -q -N1 -k100 --local -x " + bowtie_index + " -U " + consensus + " -S " + output + " -p 10")
    p = subprocess.Popen(cmd, stdout=bowtie2_stdout)
    p.wait()
    if os.path.exists(output):
        sam = Samfile(output)
        for align in sam:
            if align.tid != -1:
                query_name, query_len, ref_name = align.qname, float(align.rlen), sam.getrname(align.tid)
                if align.cigar is not None:
                    par_cig = cigar_parsing(align.cigar)
                    align_len, query_aligned_len = par_cig[0], par_cig[1]
                    nm = 0
                    if query_aligned_len / query_len >= 0.7:
                        for coppia in align.tags:
                            if coppia[0] == "NM":
                                nm = float(coppia[1])
                    # print nm,align_len
                    if align_len != 0 and type(nm) == float:
                        paired_perc_id = ((align_len - nm) / align_len) * 100
                        if paired_perc_id >= 97:
                            # print perc_id
                            rdp_match_over_97.setdefault(query_name, set())
                            rdp_match_over_97[query_name].add(ref_name)
                            mapped.add(query_name)
                        if 90 <= paired_perc_id < 97:
                            rdp_match_under_97.setdefault(query_name, set())
                            rdp_match_under_97[query_name].add(ref_name)
                            mapped.add(query_name)
    else:
        print "no mapping data"
        sys.exit()

print "Unmerged processing"
bowtie2_stdout.write("Unmerged processing\n")
if R1 != "none":
    print "Bowtie2 execution on Unmerged data glocal mode"
    output = basename + "_unmerged_glocal_ITS1.sam"
    # esecuzione del primo bowtie contro
    cmd = shlex.split(
        "bowtie2 -X 2000 -q -N1 -k100 -x " + bowtie_index + " -1 " + R1 + " -2 " + R2 + " -S " + output + " -p 10")
    p = subprocess.Popen(cmd, stdout=bowtie2_stdout)
    p.wait()
    if os.path.exists(output):
        r1_match = {}
        r2_match = {}
        sam = Samfile(output)
        for align in sam:
            if align.tid != -1:
                query_name, query_len, ref_name = align.qname, float(align.rlen), sam.getrname(align.tid)
                if align.cigar is not None:
                    par_cig = cigar_parsing(align.cigar)
                    align_len, query_aligned_len = par_cig[0], par_cig[1]
                    nm = 0
                    if query_aligned_len / query_len >= 0.7:
                        for coppia in align.tags:
                            if coppia[0] == "NM":
                                nm = float(coppia[1])
                    if align_len != 0 and type(nm) == float:
                        paired_perc_id = ((align_len - nm) / align_len) * 100
                        if paired_perc_id >= 90:
                            if align.is_read1:
                                r1_match.setdefault(query_name, {})
                                r1_match[query_name].setdefault(ref_name, [])
                                r1_match[query_name][ref_name].append(paired_perc_id)
                            elif align.is_read2:
                                r2_match.setdefault(query_name, {})
                                r2_match[query_name].setdefault(ref_name, [])
                                r2_match[query_name][ref_name].append(paired_perc_id)
        for query in set(r1_match.keys()).intersection(set(r2_match.keys())):
            # definiamo le coppie per cui le due read mappano sulla stessa seq di riferimento
            for ref in set(r1_match[query].keys()).intersection(r2_match[query].keys()):
                average_perc_id = calcola_media([max(r1_match[query][ref]), max(r2_match[query][ref])])
                if average_perc_id >= 97:
                    rdp_match_over_97.setdefault(query, set())
                    rdp_match_over_97[query].add(ref)
                    mapped.add(query)
                elif 90 <= average_perc_id < 97:
                    rdp_match_under_97.setdefault(query, set())
                    rdp_match_under_97[query].add(ref)
                    mapped.add(query)
    else:
        print "no mapping data"
        sys.exit()

    print "Bowtie2 execution on Unmerged data local mode"
    output = basename + "_unmerged_local_ITS1.sam"
    # esecuzione del primo bowtie contro
    cmd = shlex.split(
        "bowtie2 -X 2000 -q -N1 -k100 -x " + bowtie_index + " -1 " + R1 + " -2 " + R2 + " -S " + output + " -p 10")
    p = subprocess.Popen(cmd, stdout=bowtie2_stdout)
    p.wait()
    if os.path.exists(output):
        r1_match = {}
        r2_match = {}
        sam = Samfile(output)
        for align in sam:
            if align.tid != -1:
                query_name, query_len, ref_name = align.qname, float(align.rlen), sam.getrname(align.tid)
                if align.cigar is not None:
                    par_cig = cigar_parsing(align.cigar)
                    align_len, query_aligned_len = par_cig[0], par_cig[1]
                    nm = 0
                    if query_aligned_len / query_len >= 0.7:
                        for coppia in align.tags:
                            if coppia[0] == "NM":
                                nm = float(coppia[1])
                    # print nm,align_len
                    if align_len != 0 and type(nm) == float:
                        paired_perc_id = ((align_len - nm) / align_len) * 100
                        if paired_perc_id >= 90:
                            if align.is_read1:
                                r1_match.setdefault(query_name, {})
                                r1_match[query_name].setdefault(ref_name, [])
                                r1_match[query_name][ref_name].append(paired_perc_id)
                            elif align.is_read2:
                                r2_match.setdefault(query_name, {})
                                r2_match[query_name].setdefault(ref_name, [])
                                r2_match[query_name][ref_name].append(paired_perc_id)
        for query in set(r1_match.keys()).intersection(set(r2_match.keys())):
            # definiamo le coppie per cui le due read mappano sulla stessa seq di riferimento
            for ref in set(r1_match[query].keys()).intersection(r2_match[query].keys()):
                average_perc_id = calcola_media([max(r1_match[query][ref]), max(r2_match[query][ref])])
                if average_perc_id >= 97:
                    rdp_match_over_97.setdefault(query, set())
                    rdp_match_over_97[query].add(ref)
                    mapped.add(query)
                elif 90 <= average_perc_id < 97:
                    rdp_match_under_97.setdefault(query, set())
                    rdp_match_under_97[query].add(ref)
                    mapped.add(query)
    else:
        print "no mapping data"
        sys.exit()

bowtie2_stdout.close()
if os.path.exists("ITSoneDB_fungi_mapping_data") is False:
    os.mkdir("ITSoneDB_fungi_mapping_data")

log = open("bowtie2-execution.log", "w")
for i in rdp_match_over_97:
    if rdp_match_under_97.has_key(i):
        del (rdp_match_under_97[i])
match_file_over97 = open(os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_over97" % basename), "w")
match_file_under97 = open(os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_under97" % basename), "w")
for acc in rdp_match_over_97.keys():
    match_list = [acc2node[make_tuple(i)] for i in rdp_match_over_97[acc]]
    match_file_over97.write("%s %s\n" % (acc, " ".join(match_list)))
for acc in rdp_match_under_97.keys():
    if rdp_match_over_97.has_key(acc) is False:
        match_list = [acc2node[make_tuple(i)] for i in rdp_match_under_97[acc]]
        match_file_under97.write("%s %s\n" % (acc, " ".join(match_list)))
match_file_over97.close()
match_file_under97.close()
if len(rdp_match_over_97) == len(
        open(os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_over97" % basename)).readlines()):
    log.write("ITSoneDB_fungi_mapping_data/" + basename + "_match_over97\n")
else:
    print len(rdp_match_over_97), len(
        open(os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_over97" % basename)).readlines())
    log.write("bowtie2-execution.py writes a number of matches different from the expected\n")
if len(rdp_match_under_97) == len(
        open(os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_under97" % basename)).readlines()):
    log.write("ITSoneDB_fungi_mapping_data/" + basename + "_match_under97\n")
else:
    print len(rdp_match_under_97), len(
        open(os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_under97" % basename)).readlines())
    log.write("bowtie2-execution.py writes a number of matches different from the expected\n")
log.close()

print len(mapped)
sys.exit("DONE")

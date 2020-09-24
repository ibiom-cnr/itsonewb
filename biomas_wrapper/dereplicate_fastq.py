__author__ = 'Bruno Fosso'
from Bio import SeqIO
import os, sys
import subprocess, shlex
import numpy
from random import choice

#numpy.seterr(over='raise')
def controllo_quality_check(l):
    if os.path.exists(l):
        print "quality_check_and_consensus.py completes its computation"
    else:
        print "Errors during quality_check_and_consensus.py computation"
        sys.exit()


controllo_quality_check("quality_check_and_consensus.log")

f_in = ""
basename = ""
R1 = ""
R2 = ""
for line in open("quality_check_and_consensus.log"):
    line = line.strip()
    s = line.split("\t")
    if len(s) == 4:
        f_in = s[1]
        basename = s[0]
        R1 = s[2]
        R2 = s[3]
    else:
        print "not correct log file"

if f_in == "":
    sys.exit()
#controllo che i file prodotti nel precedente step
consensus_data = os.stat(f_in)
if consensus_data[6] != 0:
    os.system("grep -c '^+$' "+ f_in + " > tmp")
    l = open("tmp")
    N_cons = l.readlines()[0].strip()
    pass
else:
    print "there is not consensus sequences"
    log = open("quality_check_and_consensus.log", "w")
    log.write(basename + "\tnone\t" + R1 + "\t" + R2)
    log.close()
    tmp = open("report_file.txt", "r")
    report_data = tmp.readlines()
    tmp.close()
    tmp = open("report_file.txt", "w")
    for line in report_data:
        tmp.write(line)
    tmp.write("N consensus:\tnone")
    tmp.write("consensus under 50 nt:\tnone")
    tmp.close()
    sys.exit()

print "conversion step from fastq to fasta"
SeqIO.convert(f_in, "fastq", "tmp", "fasta")

temp = open("temp", "w")
to_short = 0
for record in SeqIO.parse("tmp", "fasta"):
    if len(record) >= 50:
        temp.write(record.format("fasta"))
    else:
        to_short += 1
temp.close()

print "dereplication on fasta file"
cmd = shlex.split("/home/galaxy/usearch6.1.544_i86linux32 -derep_fulllength temp -uc tmp.uc -log derep.log -quiet")
p = subprocess.Popen(cmd)
p.wait()

print "cluster investigation"
cluster = {}
usearch_file = open("tmp.uc", "r")
for line in usearch_file:
    line = line.strip()
    s = line.split("\t")
    if s[0] == "H":
        cluster.setdefault(s[-1], set())
        #cluster[s[-1]].add(s[-1])
        cluster[s[-1]].add(s[-2])
    elif s[0] == "S":
        cluster.setdefault(s[-2], set())
        cluster[s[-2]].add(s[-2])
usearch_file.close()
print len(cluster)

acc2size = {}
input_dict = SeqIO.index(f_in, "fastq")
for key in cluster.keys():
    if len(cluster[key]) > 1:
        acc2qual = {}
        acc2len = {}
        for acc in cluster[key]:
            acc2len[acc] = len(input_dict[acc])
            acc2qual.setdefault(acc, [])
            for qual in input_dict[acc].letter_annotations["phred_quality"]:
                #print qual
                if qual < 25:
                    acc2qual[acc].append(qual)
        max_len = max(acc2len.values())
        acc_set = set()
        for acc in acc2len.keys():
            if acc2len[acc] == max_len:
                acc_set.add(acc)
        if len(acc_set) == 1:
            acc2size[key] = "size=" + str(len(cluster[key]))
        else:
            under = []
            for acc in acc_set:
                under.append(len(acc2qual[acc]))
                #print under
            minimum = min(under)
            acc_definition = set()
            for acc in acc_set:
                if len(acc2qual[acc]) == minimum:
                    acc_definition.add(acc)
                #print acc_set
            #print acc_definition
            #print "____"
            if len(acc_definition) == 1:
                acc2size[key] = "size=" + str(len(cluster[key]))
            else:
                final_acc = []
                highest_median = 0
                for acc in acc_definition:
                    size = []
                    #print acc
                    for qual in input_dict[acc].letter_annotations["phred_quality"]:
                        size.append(qual)
                        #print numpy.median(qual)
                    if numpy.median(qual) >= highest_median:
                        #print highest_median
                        highest_median = numpy.median(qual)
                        final_acc.append(acc)
                acc2size[choice(final_acc)] = "size=" + str(len(cluster[key]))
    else:
        acc2size[key] = "size=1"

print len(acc2size)

f_out = basename + "_dereplicated_consensus.fastq"
new = open(f_out, "w")
for seq in SeqIO.parse(f_in, "fastq"):
    if acc2size.has_key(seq.id):
        seq.id = seq.id + ";" + acc2size[seq.id]
        seq.description = ""
        #print seq.format("fastq")
        new.writelines(seq.format("fastq"))
new.close()

os.system("rm temp tmp tmp.uc")

tmp = open("report_file.txt", "r")
report_data = tmp.readlines()
tmp.close()

report = open("report_file.txt", "w")
for line in report_data:
    report.write(line)
report.write("N consensus:\t" + N_cons.strip() + "\n")
report.write("consensus under 50 nt:\t" + str(to_short) + "\n")


if R1 != "none":
    r1_data = os.stat(R1)
    if r1_data[6] == 0:
        print "there is not unmerged pairs "
        log = open("quality_check_and_consensus.log", "w")
        log.write(basename + "\t" + f_out + "\tnone\tnone")
        log.close()
        report.write("N unmerged pairs\tnone")
    else:
        log = open("quality_check_and_consensus.log", "w")
        log.write(basename + "\t" + f_out + "\t" + R1 + "\t" + R2)
        log.close()
        unmerged = len(SeqIO.index(R1,"fastq"))
        report.write("N unmerged pairs\t"+str(unmerged))
else:
    print "there is not unmerged pairs "
    log = open("quality_check_and_consensus.log", "w")
    log.write(basename + "\t" + f_out + "\tnone\tnone")
    log.close()
    report.write("N unmerged pairs\tnone")
report.close()

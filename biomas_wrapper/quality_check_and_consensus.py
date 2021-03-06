import getopt
import sys
import os
import subprocess
import shlex
from string import *
import fpformat
import numpy
from Bio import SeqIO


def usage():
    print ('This script works in three different steps:\n'
           '\t(1) it performs a statistical and quality snapshot of the produced data using FastQC;\n'
           '\t(2) it performs the merging of overlapping ends by mean Flash;\n'
           '\t(3) the low quality regions are removed from non overlapping paired-end reads.'
           'Options:\n'
           '\t-i    paired-end file list: a line containing the R1, the R2 file-names and a base-name used to \n'
           '\t      annotate the files generated by BioMaS, tab separated\n'
           '\t-f    fragment length (optional)'
           '\t-h    print this help.\n'
           'Usage:\n'
           '\tpython quality_check_and_consensus.py -i read_list -f 287\n'
           '\t'
    )

if len(sys.argv) == 1:
    usage()
    sys.exit()

fragment = "0"
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:f:h")
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit()
for o, a in opts:
    if o == "-h":
        usage()
        sys.exit()
    elif o == "-i":
        f_in = a
    elif o == "-f":
        fragment = a
    else:
        assert False, "Unhandled option."

# complemento = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N"}

def controllo_esecuzione(l):
    if os.path.exists(l):
        pass
    else:
        print "no paired-end file list!!!"
        sys.exit()

def acc_modifier(acc_num):
    if acc_num[-2] == "/":
        s = acc_num.split("/")
        acc = s[0]
    else:
        s = acc_num.split(" ")
        acc = s[0]
    return acc

def verify_PE_files(a,b):
    from Bio.SeqIO.QualityIO import FastqGeneralIterator
    result = 0
    r1_acc = set()
    with open(a) as r1_file:
        try:
            for title, seq, qual in FastqGeneralIterator(r1_file):
                r1_acc.add(acc_modifier(title))
        except:
            print "%s is not a fastq file" % (a)
            result += 1
    r2_acc = set()        
    with open(b) as r2_file:
        try:
            for title, seq, qual in FastqGeneralIterator(r2_file):
                r2_acc.add(acc_modifier(title))
        except:
            print "%s is not a fastq file" % (a)
            result += 1
    print len(r1_acc), len(r2_acc)
    if len(r1_acc) == len(r2_acc):
        if len(r1_acc.intersection(r2_acc)) == len(r1_acc):
            pass
        else:
            print len(r1_acc.intersection(r2_acc)), len(r1_acc)
            result += 1
    else:
        result += 1
    return result
    #controllo prima 

#def complement(seq):
#    return (''.join(map(lambda x: complemento[x], seq)))

# noinspection PyUnboundLocalVariable
controllo_esecuzione(f_in)





log = open("quality_check_and_consensus.log", "w")
l = open(f_in)
for line in l:
    line = line.strip()
    s = line.split("\t")
    print s
    if len(s) != 3:
        print "not correctly formatted list file"
        sys.exit()
    else:
        r1 = s[0].strip()
        r2 = s[1].strip()
        if verify_PE_files(r1,r2) > 0:
            print "ERROR!!! There is a unequal number of reads in file between R1 and R2 files"
            log.close()
            os.remove("quality_check_and_consensus.log")
            sys.exit()
        basename = s[2].strip()
        report = open("report_file.txt", "w")
        report.write("label\t" + basename + " \n")
        if os.path.exists("fastqc_computation"):
            pass
        else:
            os.mkdir("fastqc_computation")
        #iniziamo con la valutazione delle read prodotte da FastQC
        cmd = shlex.split("fastqc -t 4 --noextract -q -o fastqc_computation " + r1 + " " + r2)
        p = subprocess.Popen(cmd)
        p.wait()
        #controllo fastqc output
        fastqc_output = set()
        for name in os.listdir("fastqc_computation"):
            if find(name,r1.split(".")[0]):
                fastqc_output.add(name)
            elif find(name,r2.split(".")[0]):
                fastqc_output.add(name)
        #if len(fastqc_output) == 2:
        #    pass
        #else:
        #    print "Error during FastQC computation"
        #    print "exit"
        #    exit()
        #adesso andiamo ad effettuare il merging delle sequenze
        sizes = []
        for seq in SeqIO.parse(r1, "fastq"):
            sizes.append(len(seq))
        for seq in SeqIO.parse(r2, "fastq"):
            sizes.append(len(seq))
        report.write("produced pairs\t"+str(len(sizes)/2) + " \n")
        report.write("produced reads\t"+str(len(sizes)) + " \n")
        media = fpformat.fix(numpy.mean(sizes), 2)
        sd = fpformat.fix(numpy.std(sizes), 2)
        report.write("average length\t"+media + " \n")
        report.write("sd\t"+sd + " \n")
        if fragment != "0":
            f_sd = fpformat.fix(int(fragment)/10,0)
            media = fpformat.fix(numpy.mean(sizes), 0)
            #dovremmo inserire una variabile con la lunghezza del frammento amplificato
            cmd = shlex.split(
                "flash " + r1 + " " + r2 + " -f "+fragment+" -r " + media + " -s " + f_sd + " --threads=4 -o " + basename)
            p = subprocess.Popen(cmd)
            p.wait()
        else:
            media = fpformat.fix(numpy.mean(sizes), 0)
            max_overlap = fpformat.fix(int(media)/3, 0)
            #dovremmo inserire una variabile con la lunghezza del frammento amplificato
            cmd = shlex.split("flash " + r1 + " " + r2 + " -M "+max_overlap+" --threads=4 -o " + basename)
            p = subprocess.Popen(cmd)
            p.wait()
        if os.path.exists(basename + ".extendedFrags.fastq") and os.path.exists(
                        basename + ".notCombined_1.fastq") and os.path.exists(basename + ".notCombined_2.fastq"):
            #processamento delle read per cui non e' stata creata la consenso
            R1 = basename + ".notCombined_1.fastq"
            R2 = basename + ".notCombined_2.fastq"
            consensus = basename + ".extendedFrags.fastq"
            if os.stat(R1)[6] != 0:
                cmd = shlex.split("trim_galore -q 25 --length 50 --stringency 5 --paired " + R1 + " " + R2)
                p = subprocess.Popen(cmd)
                p.wait()
                if os.path.exists(basename + ".notCombined_1_val_1.fq") and os.path.exists(
                                basename + ".notCombined_2_val_2.fq"):
                    R1 = basename + ".notCombined_1_val_1.fq"
                    R2 = basename + ".notCombined_2_val_2.fq"
                    consensus = basename + ".extendedFrags.fastq"
                    log.write(basename + "\t" + consensus + "\t" + R1 + "\t" + R2)
                else:
                    print "Error during trim-galore computation"
                    sys.exit()
            else:
                print "there are not unmerged pairs"
                log.write(basename + "\t" + consensus + "\tnone\tnone")
        else:
            print "Error during Flash computation"
            sys.exit()
        report.close()
log.close()

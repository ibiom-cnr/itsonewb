__author__ = 'Bruno Fosso'
__version__ = 1.0

import os
import shlex
import subprocess
import sys
import argparse
import argcomplete
import numpy
import fpformat
from string import strip
from Bio import SeqIO


def qc_parser():
    parser = argparse.ArgumentParser(description=usage(), prefix_chars="-")
    parser.add_argument("-p1", "--paired1", type=str,
                        help="paired-end fastq file R1. [MANDATORY]",
                        action="store", required=True)
    parser.add_argument("-p2", "--paired2", type=str,
                        help="paired-end fastq file R2. [MANDATORY]",
                        action="store", required='--paired1' in sys.argv)
    parser.add_argument("-b", "--basename", type=str,
                        help="sample name. [MANDATORY]",
                        action="store", required=True)
    parser.add_argument("-t", "--threads", type=str,
                        help="number of threads",
                        action="store", required=False,
                        default="5")
    parser.add_argument("-f", "--fragment", type=str,
                        help="fragment length (optional)",
                        action="store", required=False,
                        default="0")
    parser.add_argument("-F", "--Function_folder", type=str,
                        help="the absolute or relative path to the folder containing the Cyhton functions",
                        action="store", required=False,
                        default=os.getcwd())
    argcomplete.autocomplete(parser)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


def usage():
    """This script works in four different steps:
    \t(1) it performs a statistical and quality snapshot of the produced data using FastQC;
    \t(2) it performs the merging of overlapping ends by mean Flash;
    \t(3) the low quality regions are removed from non overlapping paired-end reads.
    """


if __name__ == "__main__":
    args = qc_parser()
    r1, r2, basename, fragment, threads = args.paired1, args.paired2, args.basename, args.fragment, args.threads
    f_dir = args.Function_folder
    sys.path.append(f_dir)
    from biomas_function import verify_PE_files, error_file_check, tools_installation, count_merged_seq

    if not tools_installation("fastqc"):
        sys.exit("fastqc is not installed")
    if not tools_installation("flash"):
        sys.exit("flash is not installed")
    if not tools_installation("trim_galore"):
        sys.exit("trim_galore is not installed")
    if not tools_installation("vsearch"):
        sys.exit("vsearch is not installed")

    with open("quality_check_and_consensus.log", "w") as log:
        message, sizes = verify_PE_files(r1, r2)
        if message is not None:
            log.close()
            os.remove("quality_check_and_consensus.log")
            sys.exit(message)
        with open("report_file.txt", "w") as report:
            report.write("label\t" + basename + " \n")
            if not os.path.exists("fastqc_computation"):
                os.mkdir("fastqc_computation")
            # iniziamo con la valutazione delle read prodotte da FastQC
            cmd = shlex.split("fastqc -t {} --noextract -q -o fastqc_computation {} {}".format(threads, r1, r2))
            p = subprocess.Popen(cmd)
            p.wait()
            report.write("produced pairs\t{}\n".format(len(sizes) / 2))
            report.write("produced reads\t{}\n".format(len(sizes)))
            media = fpformat.fix(numpy.mean(sizes), 2)
            sd = fpformat.fix(numpy.std(sizes), 2)
            report.write("average length\t{}\n".format(media))
            report.write("sd\t{}\n".format(sd))
            if fragment != "0":
                f_sd = int(float(fragment) / 10)
                media = int(numpy.mean(sizes))
                # dovremmo inserire una variabile con la lunghezza del frammento amplificato
                with open("flash.log", "w") as f_log:
                    cmd = shlex.split(
                        "flash {} {} -f {} -r {} -s {} --threads={} -o {}".format(r1, r2, fragment, media, f_sd,
                                                                                  threads,
                                                                                  basename))
                    p = subprocess.Popen(cmd, stdout=f_log, stderr=subprocess.STDOUT)
                    p.wait()
            else:
                max_overlap = int((numpy.mean(sizes) / 100) * 90)
                # dovremmo inserire una variabile con la lunghezza del frammento amplificato
                with open("flash.log", "w") as f_log:
                    cmd = shlex.split(
                        "flash {} {} -M {} --threads={} -o {}".format(r1, r2, max_overlap, threads, basename))
                    p = subprocess.Popen(cmd, stdout=f_log, stderr=subprocess.STDOUT)
                    p.wait()
            # if os.path.exists(basename + ".extendedFrags.fastq") and os.path.exists(
            #        basename + ".notCombined_1.fastq") and os.path.exists(basename + ".notCombined_2.fastq"):
            if error_file_check("flash.log") == 0:
                # processamento delle read per cui non e' stata creata la consenso
                R1 = basename + ".notCombined_1.fastq"
                R2 = basename + ".notCombined_2.fastq"
                consensus = basename + ".extendedFrags.fastq"
                # qua inserire la dereplicazione
                if os.stat(consensus)[6] != 0:
                    N_cons = count_merged_seq(consensus)
                    # vsearch --fastq_filter test_fungi.extendedFrags.fastq -fastaout tmp --fastq_minlen 50 --threads 5
                    print "conversion step from fastq to fasta"
                    with open("vsearch_conversion.log", "w") as f_log:
                        cmd = shlex.split(
                            "vsearch --fastq_filter {} -fastaout temp --fastq_minlen 50 --threads {}".format(consensus,
                                                                                                             threads))
                        p = subprocess.Popen(cmd, stdout=f_log, stderr=subprocess.STDOUT)
                        p.wait()
                    if error_file_check("vsearch_conversion.log") == 0:
                        cmd = shlex.split("grep -c '^>' temp")
                        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                        p.wait()
                        short_seq = int(p.stdout.read())
                        print "dereplication on fasta file"
                        with open("vsearch_dereplication.log", "w") as f_log:
                            cmd = shlex.split(
                                "vsearch --derep_fulllength temp --uc tmp.uc --log derep.log --quiet --threads {}".format(
                                    threads))
                            p = subprocess.Popen(cmd, stdout=f_log, stderr=subprocess.STDOUT)
                            p.wait()
                        if error_file_check("vsearch_dereplication.log") == 0:
                            print "cluster investigation"
                            cluster = {}
                            with open("tmp.uc", "r") as usearch_file:
                                for line in usearch_file:
                                    s = map(strip, line.split("\t"))
                                    if s[0] == "H":
                                        cluster.setdefault(s[-1], set())
                                        cluster[s[-1]].add(s[-2])
                                    elif s[0] == "S":
                                        cluster.setdefault(s[-2], set())
                                        cluster[s[-2]].add(s[-2])
                            print len(cluster)
                            print "write dereplicated file"
                            f_out = basename + "_dereplicated_consensus.fastq"
                            with open(f_out, "w") as tmp, open(consensus) as f_in:
                                for record in SeqIO.parse(f_in, "fastq"):
                                    if record.name in cluster:
                                        record.id = record.id + ";size={}".format(len(cluster[record.id]))
                                        record.description = ""
                                        tmp.writelines(record.format("fastq"))
                            report.write("N consensus:\t{}1n".format(N_cons))
                            report.write("consensus under 50 nt:\t{}\n".format(short_seq))
                            consensus = f_out
                else:
                    print "there is not consensus sequences"
                    log.write(basename + "\tnone\t" + R1 + "\t" + R2)
                    report.write("N consensus:\tnone")
                    report.write("consensus under 50 nt:\tnone")
                if os.stat(R1)[6] != 0:
                    with open("trim_galore.log", "w") as f_log:
                        cmd = shlex.split("trim_galore -q 25 --length 50 --stringency 5 --paired {} {}".format(R1, R2))
                        p = subprocess.Popen(cmd, stdout=f_log, stderr=subprocess.STDOUT)
                        p.wait()
                    R1 = basename + ".notCombined_1_val_1.fq"
                    R2 = basename + ".notCombined_2_val_2.fq"
                    if os.path.exists(R1) and os.stat(R1)[6] > 0 and os.path.exists(R2) and os.stat(R2)[6] > 0:
                        log.write("{}\t{}\t{}\t{}\n".format(basename, consensus, R1, R2))
                    else:
                        sys.exit("Error during trim-galore computation")
                else:
                    print "there are not unmerged pairs"
                    log.write("{}\t{}\tnone\tnone".format(basename, consensus))
            else:
                sys.exit("Error during Flash computation")

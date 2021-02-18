__author__ = 'Bruno Fosso'
__version__ = 2.0

import shlex
import subprocess
from string import strip
import os
import sys
import argparse
import argcomplete
from shutil import copytree, rmtree



def be_parser():
    parser = argparse.ArgumentParser(description=usage(), prefix_chars="-")
    parser.add_argument("-v", "--mapping_file", type=str,
                        help="tabular file containing the correspondence between ITSoneDB accession and NCBI taxonomy ID",
                        action="store", required=True)
    parser.add_argument("-i", "--bowtie2_indexes", type=str,
                        help="bowtie2 indexes path",
                        action="store", required=True)
    parser.add_argument("-F", "--Function_folder", type=str,
                        help="the absolute or relative path to the folder containing the Cyhton functions",
                        action="store", required=False,
                        default=os.getcwd())
    parser.add_argument("-t", "--threads", type=str,
                        help="number of available threads/processors",
                        action="store", required=False,
                        default=10)
    parser.add_argument("-T", "--tango_folder", type=str,
                        help="path to the TANGO folder",
                        action="store", required=True)
    parser.add_argument("-d", "--tango_dmp", type=str,
                        help="tango dmp file",
                        action="store", required=True)
    argcomplete.autocomplete(parser)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


def usage():
    """
    This script exectues Bowtie2:\n
           Usage:\n
           \tpython bowtie2-execution_ITSoneDB.py -d bowtie_indexes -v mapping_file -T tango_folder -d tango_dmp\n
    """


if __name__ == "__main__":
    args = be_parser()
    bowtie_index, mapping_file, f_dir, threads, tango_f, tango_d = args.bowtie2_indexes, args.mapping_file, args.Function_folder, args.threads, args.tango_folder, args.tango_dmp
    sys.path.append(f_dir)
    from biomas_function import controllo_quality_check, index_controll, verify_mapping_file, single_end_sam_parsing, \
        error_file_check, paired_end_sam_parsing, tools_installation, prune_match

    if not tools_installation("bowtie2"):
        sys.exit("bowtie2 is not installed")

    controllo_quality_check("quality_check_and_consensus.log")
    with open("quality_check_and_consensus.log") as a:
        try:
            line = a.readline()
            basename, consensus, R1, R2 = map(strip, line.split("\t"))
        except ValueError:
            sys.exit("not correct log file")
    index_controll(bowtie_index)
    acc2node, error = verify_mapping_file(mapping_file)
    if error is not None:
        print usage()
        sys.exit(error)

    rdp_match_over_97 = {}
    rdp_match_under_97 = {}
    print "Consensus processing"
    # mappiamo prima in modalita' glocal
    mapped = set()
    if consensus != "none":
        sam_file_list = []
        print "Bowtie2 execution on Consensus data glocal mode"
        output = basename + "_consensus_glocal_ITS1.sam"
        with open("bowtie2_stdout_glocal_SE.log", "w") as bowtie2_stdout:

            bowtie2_stdout.write("Consensus processing\n")
            cmd = shlex.split(
                "bowtie2 -X 2000 -q -N1 -k100 -x {} -U {} -S {} -p {}".format(bowtie_index, consensus, output, threads))
            p = subprocess.Popen(cmd, stderr=bowtie2_stdout)
            p.wait()
        if not os.path.exists(output) or error_file_check("bowtie2_stdout_glocal_SE.log") > 0:
            output = None
        sam_file_list.append(output)
        print "Bowtie2 execution on Consensus data local mode"
        output = basename + "_consensus_local_ITS1.sam"
        with open("bowtie2_stdout_local_SE.log", "w") as bowtie2_stdout:

            cmd = shlex.split(
                "bowtie2 -X 2000 -q -N1 -k100 --local -x {} -U {} -S {} -p {}".format(bowtie_index, consensus, output,
                                                                                      threads))
            p = subprocess.Popen(cmd, stderr=bowtie2_stdout)
            p.wait()
        if not os.path.exists(output) or error_file_check("bowtie2_stdout_glocal_SE.log") > 0:
            output = None
        sam_file_list.append(output)
        rdp_match_over_97, rdp_match_under_97, mapped = single_end_sam_parsing(sam_file_list)

    print "Unmerged processing"
    if R1 != "none":
        sam_file_list = []
        print "Bowtie2 execution on Unmerged data glocal mode"
        output = basename + "_unmerged_glocal_ITS1.sam"
        with open("bowtie2_stdout_glocal_PE.log", "w") as bowtie2_stdout:
            cmd = shlex.split(
                "bowtie2 -X 2000 -q -N1 -k100 -x {} -1 {} -2 {} -S {} -p {}".format(bowtie_index, R1, R2, output,
                                                                                    threads))
            p = subprocess.Popen(cmd, stderr=bowtie2_stdout)
            p.wait()
        if not os.path.exists(output) or error_file_check("bowtie2_stdout_glocal_SE.log") > 0:
            output = None
        sam_file_list.append(output)

        print "Bowtie2 execution on Unmerged data local mode"
        output = basename + "_unmerged_local_ITS1.sam"
        with open("bowtie2_stdout_local_PE.log", "w") as bowtie2_stdout:
            # esecuzione del primo bowtie contro
            cmd = shlex.split(
                "bowtie2 -X 2000 -q --local -N1 -k100 -x {} -1 {} -2 {} -S {} -p {}".format(bowtie_index, R1, R2, output,
                                                                                           threads))
            p = subprocess.Popen(cmd, stderr=bowtie2_stdout)
            p.wait()
        if not os.path.exists(output) or error_file_check("bowtie2_stdout_local_SE.log") > 0:
            output = None
        sam_file_list.append(output)
        diz1, diz2, map_set = paired_end_sam_parsing(sam_file_list)
        rdp_match_over_97.update(diz1)
        rdp_match_under_97.update(diz2)
        mapped.update(map_set)

    if not os.path.exists("ITSoneDB_fungi_mapping_data"):
        os.mkdir("ITSoneDB_fungi_mapping_data")
    over_match = os.path.join(os.getcwd(), "ITSoneDB_fungi_mapping_data", "%s_match_over97" % basename)
    under_match = os.path.join(os.getcwd(), "ITSoneDB_fungi_mapping_data", "%s_match_under97" % basename)
    with open("bowtie2-execution.log", "w") as log:
        for i in set(rdp_match_over_97).intersection(set(rdp_match_under_97)):
            del (rdp_match_under_97[i])
        with open(over_match, "w") as match_file_over97, open(under_match, "w") as match_file_under97:
            for acc, match_list in rdp_match_over_97.items():
                match_list = prune_match(match_list, acc2node)
                if match_list is not None:
                    match_file_over97.write("%s %s\n" % (acc, " ".join(match_list)))
            for acc, match_list in rdp_match_under_97.items():
                match_list = prune_match(match_list, acc2node)
                if match_list is not None:
                    match_file_under97.write("%s %s\n" % (acc, " ".join(match_list)))
            log.write("ITSoneDB_fungi_mapping_data/" + basename + "_match_over97\n")
            log.write("ITSoneDB_fungi_mapping_data/" + basename + "_match_under97\n")
    print len(mapped)

    print "Taxonomic Classification using TANGO"
    wd = os.getcwd()
    exec_f = os.path.basename(tango_f.rstrip("/"))
    if not os.path.exists(exec_f):
        copytree(tango_f, os.path.join(wd, exec_f))
    os.chdir(exec_f)
    if os.path.exists(over_match):
        if os.stat(over_match)[6] > 0:
            output = os.path.join(wd, "ITSoneDB_fungi_mapping_data", "bowtie_result_over_97")
            cmd = shlex.split(
                "perl tango.pl --taxonomy {} --matches {} --output {}".format(tango_d, over_match, output))
            p = subprocess.Popen(cmd)
            p.wait()
    else:
        sys.exit("The match file over_97 is missing")
    if os.path.exists(under_match):
        if os.stat(over_match)[6] > 0:
            output = os.path.join(wd, "ITSoneDB_fungi_mapping_data", "bowtie_result_under_97")
            cmd = shlex.split(
                "perl tango.pl --taxonomy {} --q-value 1 --matches {} --output {}".format(tango_d, under_match, output))
            p = subprocess.Popen(cmd)
            p.wait()
    else:
        sys.exit("The match file under_97 is missing")
    os.chdir(wd)
    rmtree(exec_f)
    sys.exit("DONE")



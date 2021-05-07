#!/usr/bin/env python

import os, sys
import argparse
import subprocess

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

__python_executable__='python2'

#______________________________________
def cli_options():
  """
  Parse BioMaS tools options.
  """
  parser = argparse.ArgumentParser(description='BioMaS wrapper for Galaxy')
  parser.add_argument('-p1', dest='in_seq_1', help='First sequence input file')
  parser.add_argument('-p2', dest='in_seq_2', help='Second sequence input file')
  parser.add_argument('-b', dest='basename', help='Sample name')
  parser.add_argument('-F', dest='function_folder', default="/opt/biomas", help='Cython function folder')
  ### quality check and consensus outputs
  parser.add_argument('-f', dest='fragment_lenght', default="0", help='Fragment length (optional)')
  parser.add_argument('-p', dest='n_threads', help='Number of threads for bowtie2')
  ### bowtie2 and tango execution ITSoneDB
  parser.add_argument('-i', dest='bowtie2_indexes_path', default="/refdata/bowtie2_indexes_rel138/ITSITSoneDB_all_euk_r138", help='Database: choice the reference bowite indexes [MANDATORY]')
  parser.add_argument('-v', dest='mapping_file', default="/refdata/bowtie2_indexes_rel138/ITSoneDB_rel138.json.gz", help='Mapping file [MANDATORY]')
  parser.add_argument('-T', dest='tango_folder', default="/opt/tango/New_TANGO_perl_version/", help='Tango folder')
  parser.add_argument('-d', dest='tango_dmp', default="/refdata/bowtie2_indexes_rel138/ITSoneDB_1.138", help='Tango dmp file')
  ### Tree Builder for Tango execution
  parser.add_argument('-n', dest='node_file', default="/refdata/bowtie2_indexes_rel138/visualization_ITSoneDB_r131.dmp", help='tabular file containing the annotation info needed to build the tree')

  return parser.parse_args()

#______________________________________
def run_command(cmd):
  """
  Run subprocess call redirecting stdout, stderr and the command exit code.
  """
  proc = subprocess.Popen( args=cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE )
  communicateRes = proc.communicate()
  stdout, stderr = communicateRes
  status = proc.wait()
  return stdout, stderr, status

#______________________________________
def read_stdio_and_redirect_to(stdfield, pattern, redirect_to):
  """
  Read stdio searching for matching pattern (used to search errors)
  and redirect to wanted stdout or stderr.
  This function return a boolean control variable.
  If pattern is found, True is retuned and the correspondin standar io is updated.
  Else it return False.
  """
  for line in stdfield.splitlines():
    if pattern in line:
      if redirect_to == 'stderr': sys.stderr.write(stdfield)
      elif redirect_to == 'stdout': sys.stdout.write(stdfield)
      return True
  return False

#______________________________________
def quality_check_and_consensus(in_seq_1, in_seq_2, frag_len, basename, function_folder): 
  """
  Run quality_check_and_consensus script for BioMaS.
  Errors are searched in the standard output (since they are printed on screen)
  and redirected on the standard error, causing Galaxy to exit.
  Script usage: python quality_check_and_consensus.py -p1 input1.fq.gz -p1 input2.fq.gz -b full_test
  """
  sys.stdout.write('### Step 1: quality check and consensus\n')

  command = __python_executable__+' '+__location__+'/quality_check_and_consensus.py -p1 ' + in_seq_1 + ' -p2 ' + in_seq_2 + ' -b ' + basename + ' -F ' + function_folder

  if frag_len != "0": command += ' -f '+ frag_len

  stdout, stderr, status = run_command(command)

  # Read stdout for error. If found exit and write the error in the stderr.
  #if read_stdio_and_redirect_to(stdout, 'ERROR!!! There is a unequal number of reads in file between R1 and R2 files','stderr') is True: sys.exit
  #if read_stdio_and_redirect_to(stdout, 'Error during trim-galore computation','stderr') is True: sys.exit
  #if read_stdio_and_redirect_to(stdout, 'Error during Flash computation','stderr') is True: sys.exit

  if status == 0:
    sys.stdout.write(stdout)
  else:
    sys.stderr.write(stderr)
    sys.exit()

#______________________________________
def bowtie2_execution_ITSoneDB(index_path, mapping_file, tango_folder, tango_dmp, function_folder):
  """
  Run bowtie2 for alignment.
  Script usage: python bowtie2-execution_ITSoneDB.py -d /path/to/ITSoneDB_all_euk_r131 -v /path/to/seq2node.dmp 
  """
  sys.stdout.write('\n### Step 3: bowtie 2 alignemnt\n')

  command = __python_executable__+' '+__location__+'/bowtie2-execution_ITSoneDB.py -i ' + index_path + ' -v ' + mapping_file + ' -T ' + tango_folder + ' -d ' + tango_dmp + ' -F ' + function_folder

  stdout, stderr, status = run_command(command)

  # Search for 'DONE'. In this case the stderr is redirected to the stdout.
  if read_stdio_and_redirect_to(stderr, 'DONE','stdout') is True: return

  # Read stdout for errors
  #if read_stdio_and_redirect_to(stdout, 'The folder containing the bowtie indexes does not exist','stderr') is True: sys.exit
  #if read_stdio_and_redirect_to(stdout, '-v option values is MANDATORY!!!','stderr') is True: sys.exit

  if status == 0:
    sys.stdout.write(stdout)
  else:
    sys.stderr.write(stderr)

#______________________________________
def tree_builder(node_file, function_folder):
  """
  Perform tree builder script to extract csv, tsv and svg.
  To correctly run tree_builder needs Xorg. We are using xvfb-run to workaround
  on "x-server-less" systems.
  Script usage: python new_tree_builder_for_perl_tango.py -d visualization_ITSoneDB_r131.dmp
  """
  sys.stdout.write('\n### Step 5: Tree Builder\n')

  # xvbf-run issue:
  # /bin/xvfb-run: line 181: 17066 Segmentation fault      DISPLAY=:$SERVERNUM XAUTHORITY=$AUTHFILE "$@" 2>&1
  # solution: https://unix.stackexchange.com/questions/152957/xvfb-run-aborting-on-cluster
  ###command = 'xvfb-run -d -e /tmp/biomas_xvfb.log '+__python_executable__+' '+__location__+'/new_tree_builder_for_perl_tango.py -d '+ visualization
  ###command = 'xvfb-run '+__python_executable__+' '+__location__+'/new_tree_builder_for_perl_tango.py -d '+ visualization
  #stdout, stderr, status = run_command(command)

  command = __python_executable__+' '+__location__+'/new_tree_builder_for_perl_tango.py -d '+ node_file + ' -F ' + function_folder
  sys.stdout.write(command)
  from xvfbwrapper import Xvfb

  vdisplay = Xvfb()
  vdisplay.start()

  stdout, stderr, status = run_command(command)

  vdisplay.stop()

  # Read stdout for errors

  if status == 0:
    sys.stdout.write(stdout)
  else:
    sys.stderr.write(stderr)

#______________________________________
def biomas_wrapper():

  options = cli_options()

  quality_check_and_consensus(options.in_seq_1, options.in_seq_2, options.fragment_lenght, options.basename, options.function_folder)

  bowtie2_execution_ITSoneDB(options.bowtie2_indexes_path, options.mapping_file, options.tango_folder, options.tango_dmp, options.function_folder)

  tree_builder(options.node_file, options.function_folder)

#______________________________________
if __name__ == '__main__':
  biomas_wrapper()

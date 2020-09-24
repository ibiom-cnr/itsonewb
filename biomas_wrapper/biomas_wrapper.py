#/usr/bin/env python

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
  parser.add_argument('-i1', '--input_1', dest='in_seq_1', help='First sequence input file')
  parser.add_argument('-i2', '--input_2', dest='in_seq_2', help='Second sequence input file')
  parser.add_argument('-o', '--output-prefix', dest='out_prefix', help='Output file prefix')
  ### quality check and consensus outputs
  parser.add_argument('-qcc1', dest='qcc_1', help='First sequence fastqc output file name')
  parser.add_argument('-qcc2', dest='qcc_2', help='Second sequence fastqc output file name')
  parser.add_argument('-f', '--fragment-lenght', dest='fragment_lenght', default="0", help='Fragment length (optional)')
  parser.add_argument('-p', dest='n_threads', help='Number of threads for bowtie2')
  ### bowtie2 execution ITSoneDB
  parser.add_argument('-d', dest='bowtie2_indexes_path', default=None, help='Database: choice the reference bowite indexes [MANDATORY]')
  parser.add_argument('-v', dest='mapping_file', default=None, help='Mapping file [MANDATORY]')
  ### Tango execution
  parser.add_argument('-D', dest='tango_tree', help='Tree for Tango execution')
  ### Tree Builder for Tango execution
  parser.add_argument('-T', dest='visualization', help='Map file for Tree buileder for Perl Tango execution')

  return parser.parse_args()

#______________________________________
def fill_read_list(seq1, seq2, out_prefix):
  """
  Create BioMaS input read list.
  """
  f = open('read_list','w+')
  f.write(seq1+'\t'+seq2+'\t'+out_prefix)
  f.close()

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
def quality_check_and_consensus(in_seq_1, qcc_1, in_seq_2, qcc_2, frag_len): 
  """
  Run quality_check_and_consensus script for BioMaS.
  Errors are searched in the standard output (since they are printed on screen)
  and redirected on the standard error, causing Galaxy to exit.
  Script usage: python quality_check_and_consensus.py -i read_list
  """
  sys.stdout.write('### Step 1: quality check and consensus\n')

  command = __python_executable__+' '+__location__+'/quality_check_and_consensus.py -i read_list'

  if frag_len != "0": command += ' -f '+frag_len

  stdout, stderr, status = run_command(command)

  # Read stdout for error. If found exit and write the error in the stderr.
  if read_stdio_and_redirect_to(stdout, 'ERROR!!! There is a unequal number of reads in file between R1 and R2 files','stderr') is True: sys.exit
  if read_stdio_and_redirect_to(stdout, 'Error during trim-galore computation','stderr') is True: sys.exit
  if read_stdio_and_redirect_to(stdout, 'Error during Flash computation','stderr') is True: sys.exit

  if status == 0:
    # rename output to have them in qcc list
    rename_fastqc_output(in_seq_1, qcc_1)
    rename_fastqc_output(in_seq_2, qcc_2)
    sys.stdout.write(stdout)
  else:
    sys.stderr.write(stderr)
    sys.exit()

#______________________________________
def rename_fastqc_output(dataset_pathname, outname):
  """
  Rename fastqc output for better history recognition.
  """
  pair = os.path.split(dataset_pathname)
  pathname = './fastqc_computation/'+pair[1]+'_fastqc.html'
  outname = './fastqc_computation/'+outname+'_fastqc.html'
  os.rename(pathname, outname)

#______________________________________
def dereplicate_fastq():
  """
  Run dereplicate_fastq script for BioMaS.
  At least usearch6.1.544_i86linux32 is needed.
  If not able to dereplicate the pipeline will continue.
  Script usage: python dereplicate_fastq.py
  """
  sys.stdout.write('\n### Step 2: dereplicate fastq\n')
  command = __python_executable__+' '+__location__+'/dereplicate_fastq.py'
  stdout, stderr, status = run_command(command)

  if status == 0:
    sys.stdout.write(stdout)
  else:
    sys.stderr.write(stderr)

#______________________________________
def bowtie2_execution_ITSoneDB(index_path, map_file):
  """
  Run bowtie2 for alignment.
  Script usage: python bowtie2-execution_ITSoneDB.py -d /path/to/ITSoneDB_all_euk_r131 -v /path/to/seq2node.dmp 
  """
  sys.stdout.write('\n### Step 3: bowtie 2 alignemnt\n')

  command = __python_executable__+' '+__location__+'/bowtie2-execution_ITSoneDB.py'
  if index_path is not None: command += ' -d '+index_path
  if map_file is not None: command += ' -v '+ map_file
  stdout, stderr, status = run_command(command)

  # Search for 'DONE'. In this case the stderr is redirected to the stdout.
  if read_stdio_and_redirect_to(stderr, 'DONE','stdout') is True: return

  # Read stdout for errors
  if read_stdio_and_redirect_to(stdout, 'The folder containing the bowtie indexes does not exist','stderr') is True: sys.exit
  if read_stdio_and_redirect_to(stdout, '-v option values is MANDATORY!!!','stderr') is True: sys.exit

  if status == 0:
    sys.stdout.write(stdout)
  else:
    sys.stderr.write(stderr)

#______________________________________
def perl_tango_execution(tango_tree):
  """
  Perform Tango computation, using perl tango script.
  Script usage: ./perl_tango_execution.sh -d ITSonedb_r131
  """
  sys.stdout.write('\n### Step 4: Tango mapping\n')

  os.symlink(tango_tree, './reference_db')

  command = __location__+'/perl_tango_execution.sh -d reference_db'
  stdout, stderr, status = run_command(command)

  if status == 0:
    sys.stdout.write(stdout)
  else:
    sys.stderr.write(stderr)

#______________________________________
def tree_builder(visualization):
  """
  Perform tree builder script to extract csv, tsv and svg.
  To correctly run tree_builder needs Xorg. We are using xvfb-run to workaround
  on "x-server-less" systems.
  Script usage: python new_tree_builder_for_perl_tango.py -d visualization_ITSoneDB_r131.dmp
  """
  sys.stdout.write('\n### Step 5: Tree Builder\n')

  #command = 'xvfb-run -a -e /export/xvfb.log '+__python_executable__+' '+__location__+'/new_tree_builder_for_perl_tango.py -d '+ visualization
  #stdout, stderr, status = run_command(command)

  command = __python_executable__+' '+__location__+'/new_tree_builder_for_perl_tango.py -d '+ visualization

  from xvfbwrapper import Xvfb
  vdisplay = Xvfb()
  vdisplay.start()
  stdout, stderr, status = run_command(command)
  vdisplay.stop()

  # Read stdout for errors

  if status == 0:
    sys.stdout.write(stdout)
  else:
    sys.stderr.write(stdout)
    sys.stderr.write(stderr)

#______________________________________
def biomas_wrapper():

  options = cli_options()

  fill_read_list(options.in_seq_1, options.in_seq_2, options.out_prefix)

  quality_check_and_consensus(options.in_seq_1, options.qcc_1, options.in_seq_2, options.qcc_2, options.fragment_lenght)

  dereplicate_fastq()

  bowtie2_execution_ITSoneDB(options.bowtie2_indexes_path, options.mapping_file)

  perl_tango_execution(options.tango_tree)

  tree_builder(options.visualization)

#______________________________________
if __name__ == '__main__':
  biomas_wrapper()

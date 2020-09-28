#/usr/bin/env python

import os, sys, shutil
import argparse
import subprocess

import pandas as pd
import numpy as np

__mopo16s_path__ = '/home/galaxy/mopo16s/release'

__mopo16s_exec__='mopo16s'

#______________________________________
def cli_options():
  """
  Parse Mopo16s tools options.
  """
  parser = argparse.ArgumentParser(description='Mopo16s wrapper for Galaxy')
  # Input files
  parser.add_argument('--reference', dest='reference_set_file', help='Reference set file is a .fasta file containing the reference set of sequences for which the primer are designed.')
  parser.add_argument('--input', dest='initial_primer_pairs_file', help='Initial primer pairs file is a .fasta file containing a set of (possibly degenerate) primer pairs from which to start the optimisation, saved alterning forward and corresponding reverse primers.')

  parser.add_argument('--init-primers', dest='fin_primers', help="Initial set of good primer pairs. The file contain one line for each primer pair: each line contains a tab delimited list of all forward primers, followed by x and then by the list of all reverse primers.")
  parser.add_argument('--init-scores', dest='fin_scores', help="Initial set of good primer pairs. The file contain one line for each line in the corresponding *.primers. Each line contain the values of the Efficiency, Coverage and Matching-bias score of the primer pair.")

  parser.add_argument('--out-primers', dest='fout_primers', help="Pareto front of optimal primer pairs. The file contain one line for each primer pair: each line contains a tab delimited list of all forward primers, followed by x and then by the list of all reverse primers.")
  parser.add_argument('--out-scores', dest='fout_scores', help="Pareto front of optimal primer pairs. The file contain one line for each line in the corresponding *.primers. Each line contain the values of the Efficiency, Coverage and Matching-bias score of the primer pair.")

  # Common options:
  parser.add_argument('-s', '--seed', dest='seed', default='0', help='Seed of the random number generator (default 0)')
  parser.add_argument('-r', '--restarts', dest='n_restarts', default='20', help='Number of restarts for each run of the multi-objective optimisation algorithm (default 20)')
  parser.add_argument('-R', '--runs', dest='n_runs', default='20', help='Number of runs of the multi-objective optimisation algorithm (default 20)')
  parser.add_argument('-G', '--threads', dest='n_threads', default='1', help='Number of threads for parallel execution (default 1)')
  parser.add_argument('-V', '--verbose', dest='verbosity_level', default='0', help='Verbosity level (default 0). If 0, no extra output would be created. If not 0, for each run would be created 3 files: 1) primers scores file 2) primers sequences file 3) optimization steps performed at each restart')

  # Coverage-related options:
  parser.add_argument('-M', '--maxMismatches', dest='max_mismatches', default='2', help='Maximum number of mismatches between the non-3-end of the primer and a 16S sequence to consider the latter covered by the primer, in case also the 3-end perfectly matches (default 2)')
  parser.add_argument('-S', '--maxALenSpanC', dest='max_ALenSpanC', default='200', help='Maximum amplicon length span considered when computing coverage (half above, half below median) (default 200)')

  # Efficiency-related options:
  parser.add_argument('-l', '--minPrimerLen', dest='min_primer_len', default='17', help='Minimum primer length (default 17)')
  parser.add_argument('-L', '--maxPrimerLen', dest='max_primer_len', default='21', help='Maximum primer length (default 21)')
  parser.add_argument('-m', '--minTm', dest='min_tm', default='52', help='Minimum primer melting temperature (default 52)')
  parser.add_argument('-c', '--minGCCont', dest='min_gcc_content', default='0.5', help='Minimum primer GC content (default 0.5)')
  parser.add_argument('-C', '--maxGCCont', dest='max_gcc_content', default='0.7', help='Maximum primer GC content (default 0.7)')
  parser.add_argument('-D', '--maxDimers', dest='max_dimers', default='8', help='Maximum number of self-dimers, ie of dimers between all possible gap-less alignments of the primer with its reverse complement (default 8)')
  parser.add_argument('-p', '--maxHomopLen', dest='max_homopolymer_len', default='4', help='Maximum homopolymer length (default 4)')
  parser.add_argument('-d', '--maxDeltaTm', dest='max_delta_tm', default='3', help='Maximum span of melting temparatures for the primer sets (default 3)')
  parser.add_argument('-e', '--maxALenSpanE', dest='max_ALenSpanE', default='50', help='Maximum span (maxALenSpanE) between median and given quantile (maxALenSpanEQ) of amplicon length (default 50 and 0.01, respectively)')
  parser.add_argument('-q', '--maxALenSpanEQ', dest='max_ALenSpanEQ', default='0.01', help=' Maximum span (maxALenSpanE) between median and given quantile (maxALenSpanEQ) of amplicon length (default 50 and 0.01, respectively)')

  # Fuzzy tolerance intervals for efficiency-related options:
  parser.add_argument('-t', '--minTmInterv', dest='min_TmInterv', default='2', help='Fuzzy tolerance interval for minimum melting temperature (default 2)')
  parser.add_argument('-g', '--minGCContInt', dest='min_GCContInt', default='0.1',help='Fuzzy tolerance interval for minimum GC content (default 0.1)')
  parser.add_argument('-i', '--maxDimersInt', dest='max_DimersInt', default='3', help='Fuzzy tolerance interval for maximum number of self dimers (default 3)')
  parser.add_argument('-T', '--deltaTmInt', dest='delta_TmInt', default='2', help='Fuzzy tolerance interval for span of melting temperatures of the primer set (default 2)')
  parser.add_argument('-P', '--maxHLenInt', dest='max_HLenInt', default='2', help='Fuzzy tolerance interval for maximum homopolymer length (default 2)')
  parser.add_argument('-E', '--maxALenSpanEI', dest='max_ALenSpanEI', default='50', help='Fuzzy tolerance interval for maximum span between median and given quantile amplicon length (default 50)')

  return parser

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
def parse_output(fin, fout):

  df = pd.DataFrame(columns=['Forward'])
  dr = pd.DataFrame(columns=['Reverse'])

  forward=[]
  reverse=[]

  with open(fin) as fp:
    line = fp.readline()
    while line:
      cont = 0
      seq_list = line.strip().split("\t")
      for i in seq_list:
        if i == "x": break
        forward.append(i)
        cont +=1
      for i in seq_list[(cont+1):]:
        reverse.append(i)
      line = fp.readline()

  df['Forward'] = forward
  dr['Reverse'] = reverse

  result = pd.concat([df,dr], ignore_index=True, axis=1)
  result = result.replace(np.nan, '', regex=True)
  result.columns = ['Forward', 'Reverse']

  tfile = open(fout, 'w')
  tfile.write(result.to_string())
  tfile.close()

#______________________________________
def mopo16s_wrapper():

  parser = cli_options()
  options = parser.parse_args()

  # fix error terminate called after throwing an instance of 'seqan::UnknownExtensionError'
  #   what():  Unknown file extension of ***
  # using a symlink
  os.symlink(options.reference_set_file, "./__reference_set_file.fasta")

  # Build mopo16s command
  command = '%s/%s %s %s' % (__mopo16s_path__, __mopo16s_exec__, "./__reference_set_file.fasta", options.initial_primer_pairs_file)

  if options.seed != parser.get_default('seed'):
    command += ' -s %s' % (options.seed)
 
  if options.n_restarts != parser.get_default('n_restarts'):
    command += ' -r %s' % (options.n_restarts)

  if options.n_runs != parser.get_default('n_runs'):
    command += ' -R %s' % (options.n_runs)

  if options.n_threads != parser.get_default('n_threads'):
    command += ' -G %s' % (options.n_threads)

  if options.verbosity_level != parser.get_default('verbosity_level'):
    command += ' -V %s' % (options.verbosity_level)

  ## Coverage-related options:

  if options.max_mismatches != parser.get_default('max_mismatches'):
    command += ' -M %s' % (options.max_mismatches)

  if options.max_ALenSpanC != parser.get_default('max_ALenSpanC'):
    command += ' -S %s' % (options.max_ALenSpanC)

  # Efficiency-related options:

  if options.min_primer_len != parser.get_default('min_primer_len'):
    command += ' -l %s' % (options.min_primer_len)

  if options.max_primer_len != parser.get_default('max_primer_len'):
    command += ' -L %s' % (options.max_primer_len)

  if options.min_tm != parser.get_default('min_tm'):
    command += ' -m %s' % (options.min_tm)

  if options.min_gcc_content != parser.get_default('min_gcc_content'):
    command += ' -c %s' % (options.min_gcc_content)

  if options.max_gcc_content != parser.get_default('max_gcc_content'):
    command += ' -C %s' % (options.max_gcc_content)

  if options.max_dimers != parser.get_default('max_dimers'):
    command += ' -D %s' % (options.max_dimers)

  if options.max_homopolymer_len != parser.get_default('max_homopolymer_len'):
    command += ' -p %s' % (options.max_homopolymer_len)

  if options.max_delta_tm != parser.get_default('max_delta_tm'):
    command += ' -d %s' % (options.max_delta_tm)

  if options.max_ALenSpanE != parser.get_default('max_ALenSpanE'):
    command += ' -e %s' % (options.max_ALenSpanE)

  if options.max_ALenSpanEQ != parser.get_default('max_ALenSpanEQ'):
    command += ' -q %s' % (options.max_ALenSpanEQ)

  # Fuzzy tolerance intervals for efficiency-related options:

  if options.min_TmInterv != parser.get_default('min_TmInterv'):
    command += ' -t %s' % (options.min_TmInterv)

  if options.min_GCContInt != parser.get_default('min_GCContInt'):
    command += ' -g %s' % (options.min_GCContInt)

  if options.max_DimersInt != parser.get_default('max_DimersInt'):
    command += ' -i %s' % (options.max_DimersInt)

  if options.delta_TmInt != parser.get_default('delta_TmInt'):
    command += ' -T %s' % (options.delta_TmInt)

  if options.max_HLenInt != parser.get_default('max_HLenInt'):
    command += ' -P %s' % (options.max_HLenInt)

  if options.max_ALenSpanEI != parser.get_default('max_ALenSpanEI'):
    command += ' -E %s' % (options.max_ALenSpanEI)

  #print command
  sys.stdout.write(command)

  stdout, stderr, status = run_command(command)

  if status == 0:
    sys.stdout.write(str(stdout))
  else:
    sys.stderr.write(str(stderr))

  parse_output("init.primers", options.fin_primers)
  shutil.move("init.scores", options.fin_scores)
  parse_output("out.primers", options.fout_primers)
  shutil.move("out.scores", options.fout_scores)

#______________________________________
if __name__ == '__main__':
  mopo16s_wrapper()


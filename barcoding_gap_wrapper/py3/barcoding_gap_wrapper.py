#/usr/bin/env python

import os, sys
import argparse
import subprocess

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#______________________________________
def cli_options():
  """
  Parse Barcoding Gap Inference tool options.
  """
  parser = argparse.ArgumentParser(description='Barcoding gap inference tool wrapper for Galaxy')

  parser.add_argument("-d", "--distance_folder", type=str, help="folder in which are stored the distances in family specific files", action="store", required=True)
  parser.add_argument("-f", "--all_taxa_file_list", type=str, help="file containing all the taxon list", action="store", required=True)
  parser.add_argument("-n", "--taxon_name", type=str, help="taxon name", action="store", required=True)
  parser.add_argument("-r", "--taxonomic_rank", type=str, help="taxonomic_rank", action="store", required=True)
  parser.add_argument("-o", "--outfile", type=str, help="output file", action="store", required=True)
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
def barcoding_gap_wrapper():

  options = cli_options()

  command = 'python '+__location__+'/print_bg_may21_py3.py -d "%s" -f "%s" -n "%s" -r "%s"' % (options.distance_folder, options.all_taxa_file_list, options.taxon_name, options.taxonomic_rank)

  sys.stdout.write('%s: ' % options.taxon_name)

  stdout, stderr, status = run_command(command)

  if status != 0: sys.stderr.write(str(stderr))

  # take only the barcodingap output
  stdout = stdout.splitlines()[2]

  if stdout == "No extragenus data":
    sys.exit('\nNo extragenus data')

  if stdout == "No extraspecies data":
    sys.exit('\nNo extraspecies data')

  if stdout == "No intragenus data":
    sys.exit('\nNo intragenus data')

  if stdout == "No intraspecies data":
    sys.exit('\nNo intraspecies data')

  # convert stdout to list
  import ast
  stdout = ast.literal_eval(stdout)

  sys.stdout.write('\nThe Barcoding Gap inferred as the difference of inter and intra group mean is %s' % stdout[0])
  sys.stdout.write('\nThe Barcoding Gap inferred as the difference of the largest intragroup distance and the smallest intergroup distance is %s ' % stdout[1])

  # Rename output png to be shown in galaxy
  os.rename(stdout[2], options.outfile)

#______________________________________
if __name__ == '__main__':
  barcoding_gap_wrapper()

#!/usr/bin/env python

import ast
import argparse


#______________________________________
def cli_options():
  parser = argparse.ArgumentParser(description='Galaxy Central Management Tool script')
  parser.add_argument('action', choices=['accession', 'specie', 'taxon'], nargs='?', help='Loc to be create')
  parser.add_argument('-i', '--input-file', dest='input_data', help='Input data')
  parser.add_argument('-o', '--output-file', dest='output_data', help='Output data')
  return parser.parse_args()


#______________________________________
def create_loc():

  options = cli_options()

  with open(options.input_data) as fin:
    ini_list = fin.read().replace('\n', '')
    #print(ini_list)

  if( options.action == "accession"):
    print('Create accession numbers list') 

    accessions_list = ast.literal_eval(ini_list) 
    print(type(accessions_list))

    fout = open(options.output_data, 'w')
    for accession in accessions_list:
      #print(accession)
      fout.write(accession + "\n")

  elif( options.action == 'specie'):
    print('Create specie list')

    ini_list = ini_list.replace("null,", "") # remove all null occurrence
    ini_list = ini_list.replace(",null", "") # remove last null occurrence
    specie_list = ast.literal_eval(ini_list)
    print(type(specie_list))
    
    fout = open(options.output_data, 'w')
    for specie in specie_list:
      fout.write(specie + "\n")

  elif ( options.action == 'taxon'):
    print('Crate taxon names list')

    specie_list = ast.literal_eval(ini_list)
    print(type(specie_list))
    
    fout = open(options.output_data, 'w')
    for specie in specie_list:
      fout.write(specie + "\n")


#______________________________________
if __name__ == "__main__":
    create_loc()

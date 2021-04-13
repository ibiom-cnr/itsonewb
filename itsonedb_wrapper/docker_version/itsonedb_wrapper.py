#!/usr/bin/env python
"""
"""

import sys, os
#import logging
import argparse

from sqlalchemy import *

logfile = '/tmp/readdb.log'

#______________________________________
def cli_options():
  parser = argparse.ArgumentParser(description='Read itsonedb script')
  parser.add_argument('-l', '--itsonedb-url', dest='itsonedb_url', help='ITSoneDB URL')
  parser.add_argument('-u', '--itsonedb-username', dest='itsonedb_username', help='ITSoneDB Username')
  parser.add_argument('-p', '--itsonedb-password', dest='itsonedb_password', help='ITSoneDB Password')
  parser.add_argument('-a', '--entry-accession', dest='accession_number', help='Accession Number')
  parser.add_argument('-s', '--specie-name', dest='specie_name', help='Specie name')
  parser.add_argument('-t', '--taxon-name', dest='taxon_name', help='Taxon name')
  return parser.parse_args()

#______________________________________
def db_connection(db):
  """
  Connect to ItsOneDB.
  """

  engine = create_engine(db)
  engine.echo = False
  #print engine.table_names()
  connection = engine.connect()
  metadata = MetaData()

  return engine, connection, metadata

#______________________________________
def get_sequences(engine, connection, metadata, accession_number):
  """
  function description
  put queries here
  """

  # Get sequence from Accession number
  gbentry_sequence = Table('gbentry_sequence', metadata, autoload=True, autoload_with=engine)
  select_gbentry_sequence = select([gbentry_sequence], and_(gbentry_sequence.c.gbentryAccession==accession_number))
  result_gbentry_sequence = connection.execute(select_gbentry_sequence)
  for row in result_gbentry_sequence: sequence_full = row[1]

  # Get ENA and HMM  localization
  its1feature = Table('its1feature', metadata, autoload=True, autoload_with=engine)
  select_its1feature = select([its1feature], and_(its1feature.c.GBentry_Accession==accession_number))
  result_its1feature = connection.execute(select_its1feature)
  for row in result_its1feature:
    hasGBannotation = row[1]
    GBstart = row[6]
    GBend = row[7]
    hasHMM = row[10]
    HMMstart = row[12]
    HMMend = row[13]

  try: hasGBannotation
  except NameError: hasGBannotation = None

  # ENA sequence output array
  ena_output = []
  ena_length = 0
  if hasGBannotation == 1:
    ena_sequence = sequence_full[GBstart-1:GBend]
    ena_length = GBend - GBstart + 1
    ena_output = [ena_sequence[i:i+80] for i in range(0, len(ena_sequence), 80)]

  try: hasHMM
  except NameError: hasHMM = None

  # HMM sequence output array
  hmm_output = []
  hmm_length = 0
  if hasHMM == 1:
    hmm_sequence = sequence_full[HMMstart-1:HMMend]
    hmm_length = HMMend - HMMstart + 1
    hmm_output = [hmm_sequence[i:i+80] for i in range(0, len(hmm_sequence), 80)]

  if hasGBannotation is None and hasHMM is None: return [None]*4

  return ena_output, ena_length, hmm_output, hmm_length

#______________________________________
def get_info(engine, connection, metadata, accession_number):
  """
  get info from tables
  put queries here
  """
  gbentry = Table('gbentry', metadata, autoload=True, autoload_with=engine)
  select_gbentry = select([gbentry], and_(gbentry.c.Accession==accession_number))
  result_gbentry = connection.execute(select_gbentry)
  for row in result_gbentry:
    version = row[1]
    description = row[3]
    length = row[4]
    taxon_db_xref = row[7]

  taxon_fungi = Table('taxon_fungi', metadata, autoload=True, autoload_with=engine)
  select_taxon_fungi = select([taxon_fungi], and_(taxon_fungi.c.db_xref==taxon_db_xref))
  result_taxon_fungi = connection.execute(select_taxon_fungi)
  for row in result_taxon_fungi:
    db_xref = row[0]
    taxon_name = row[1]
    lineage = row[2]
    taxontank_idtaxonrank = row[4]

  taxonrank = Table('taxonrank', metadata, autoload=True, autoload_with=engine)
  select_taxonrank = select([taxonrank], and_(taxonrank.c.idTaxonRank==taxontank_idtaxonrank))
  result_taxonrank = connection.execute(select_taxonrank)
  for row in result_taxonrank:
    taxon_rank_name =  row[1]

  return version, description, length, taxon_db_xref, taxon_name, lineage, taxon_rank_name

#______________________________________
def search_by_entry_accession(engine, connection, metadata, accession_number):
  
  fout= open("output.fasta","w+")
  mout = open("metadata.txt","w+")

  ena_out, ena_len, hmm_out, hmm_len = get_sequences(engine, connection, metadata, accession_number)
  version, description, length, taxon_db_xref, taxon_name, lineage, taxon_rank_name = get_info(engine, connection, metadata, accession_number)

  # write metadata info
  mout.write('Entry %s details\n\n' % accession_number)
  mout.write('Accession: %s\n' % accession_number)
  mout.write('Version: %s\n' % version)
  mout.write('Description: %s\n' % description)
  mout.write('Sequence length: %s\n' % length)
  mout.write('Taxon name: %s\n' % taxon_name)
  mout.write('Taxon rank: %s\n' % taxon_rank_name)
  mout.write('Lineage: %s\n' % lineage)

  # write sequence
  if ena_out is None and hmm_out is None:
    sys.stderr.write('[ERROR] No matching neither accession nor GI')
    sys.exit(1)

  if ena_len > 0:
    ena_output_prefix = '>%s_ITS1_ENA|ITS1 localized by ENA annotation, %s bp length;' % (accession_number, str(ena_len))
    ena_out.insert(0,ena_output_prefix)
    fill_fasta(fout,ena_out)

  if hmm_len > 0:
    hmm_output_prefix = '>%s_ITS1_HMM|ITS1 localized by HMM profiles, %s bp length;' % (accession_number, str(hmm_len))
    hmm_out.insert(0,hmm_output_prefix)
    fill_fasta(fout,hmm_out)

  fout.close()
  mout.close()

#______________________________________
def search_by_specie_name(engine, connection, metadata, specie_name):
  """
  #select * from gbentry where Description LIKE "%Aspergillus flavus%";
  """

  gbentry = Table('gbentry', metadata, autoload=True, autoload_with=engine)

  select_gbentry = select([gbentry], and_(gbentry.c.Description.like("%"+specie_name+"%")))
  result_gbentry = connection.execute(select_gbentry)
  accession_list = []
  for row in result_gbentry:
    accession_list.append(row[0])

  if not accession_list:
    sys.stderr.write('[ERROR] No matching species')
    sys.exit(1)

  # Fill fasta files
  fout = open("output.fasta","w+")
  mout = open("metadata.txt","w+")
  # write table header
  mout.write('Accession\t\t\tTaxon name\t\t\tITS1 localization\t\t\tSequence description\n')

  for i in accession_list:
    # get sequences
    ena_out, ena_len, hmm_out, hmm_len = get_sequences(engine, connection, metadata, str(i))

    # get info
    version, description, length, taxon_db_xref, taxon_name, lineage, taxon_rank_name = get_info(engine, connection, metadata, str(i))

    if ena_len > 0:
      ena_output_prefix = '>%s_ITS1_ENA|%s|%s|ITS1 located by ENA annotation, %s bp' % (str(i), str(taxon_name), str(taxon_db_xref), str(ena_len))
      ena_out.insert(0,ena_output_prefix)
      fill_fasta(fout,ena_out)
      fill_metadata(mout, str(i), str(taxon_name), 'ENA', str(description))


    if hmm_len > 0:
      hmm_output_prefix = '>%s_ITS1_HMM|%s|%s|ITS1 located by HMM profiles, %s bp' % (str(i), str(taxon_name), str(taxon_db_xref), str(hmm_len))
      hmm_out.insert(0,hmm_output_prefix)
      fill_fasta(fout,hmm_out)
      fill_metadata(mout, str(i), str(taxon_name), 'HMM', str(description))

  fout.close()
  mout.close()

#______________________________________
def search_by_taxon_name(engine, connection, metadata, taxon_name):

  taxon_fungi = Table('taxon_fungi', metadata, autoload=True, autoload_with=engine)
  gbentry = Table('gbentry', metadata, autoload=True, autoload_with=engine)

  select_taxon_fungi = select([taxon_fungi], and_(taxon_fungi.c.Name.like("%"+taxon_name+"%")))
  result_taxon_fungi = connection.execute(select_taxon_fungi)
  accession_list = []
  for row in result_taxon_fungi:

    select_gbentry = select([gbentry], and_(gbentry.c.Taxon_db_xref==row[0]))
    result_gbentry = connection.execute(select_gbentry)
    for row in result_gbentry:
      accession_list.append(row[0])

  # Fill fasta files
  fout = open("output.fasta","w+")
  mout = open("metadata.txt","w+")
  # write table header
  mout.write('Accession\t\t\tTaxon name\t\t\tITS1 localization\t\t\tSequence description\n')

  for i in accession_list:
    # get sequences
    ena_out, ena_len, hmm_out, hmm_len = get_sequences(engine, connection, metadata, str(i))

    # get info
    version, description, length, taxon_db_xref, taxon_name, lineage, taxon_rank_name = get_info(engine, connection, metadata, str(i))

    if ena_len > 0:
      ena_output_prefix = '>%s_ITS1_ENA|%s|%s|ITS1 located by ENA annotation, %s bp' % (str(i), str(taxon_name), str(taxon_db_xref), str(ena_len))
      ena_out.insert(0,ena_output_prefix)
      fill_fasta(fout,ena_out)
      fill_metadata(mout, str(i), str(taxon_name), 'ENA', str(description))


    if hmm_len > 0:
      hmm_output_prefix = '>%s_ITS1_HMM|%s|%s|ITS1 located by HMM profiles, %s bp' % (str(i), str(taxon_name), str(taxon_db_xref), str(hmm_len))
      hmm_out.insert(0,hmm_output_prefix)
      fill_fasta(fout,hmm_out)
      fill_metadata(mout, str(i), str(taxon_name), 'HMM', str(description))

  fout.close()
  mout.close()

#______________________________________
def fill_fasta(fout, aout):
  """
  Fill fasta output files
  """
  for i in aout:
    fout.write("%s\n" % i)

def fill_metadata(mout, accession, taxon_name, localization, description):
  """
  Fill metadata output file
  """
  mout.write('%s\t\t\t%s\t\t\t%s\t\t\t%si\n' % (accession, taxon_name, localization, description))

#______________________________________
def itsonedb_wrapper():

  options = cli_options()

  itsonedb = 'mysql://' + options.itsonedb_username + ':' + options.itsonedb_password + '@' + options.itsonedb_url + '/itsonedb'

  engine, connection, metadata = db_connection(itsonedb)
  
  if options.accession_number:
    search_by_entry_accession(engine, connection, metadata, options.accession_number)

  if options.specie_name:
    search_by_specie_name(engine, connection, metadata, options.specie_name)

  if options.taxon_name:
    search_by_taxon_name(engine, connection, metadata, options.taxon_name)

#______________________________________
if __name__ == '__main__':
  itsonedb_wrapper()

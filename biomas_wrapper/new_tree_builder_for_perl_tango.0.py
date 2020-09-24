__author__ = 'Bruno Fosso'
import getopt
import os
import sys
from string import strip
from string import find
from ete2 import Tree, TreeNode


def usage():
    print ('This script converts the taxonomic assignments made by TANGO in a taxonomic tree:\n'
           'Options:\n'
           '\t-d    nodes file of the taxonomic reference tree. If not indicated it uses the bacterial taxonomy \n'
           '\t-h    print this help.\n'
           'Usage:\n'
           '\tpython tango_ass_2_taxa_freq.py -d nodes_file\n'
           '\t'
    )


NODESFILE = ""
try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:h")
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit()
for o, a in opts:
    if o == "-h":
        usage()
        sys.exit()
    elif o == "-d":
        NODESFILE = a
    else:
        assert False, "Unhandled option."




#l'analisi dell'output prodotto da tango
basename = ""
tango_input = ""
tango_output_over_97 = []
tango_output_under_97 = []
for line in open("quality_check_and_consensus.log").readlines():
    line = line.strip()
    s = line.split("\t")
    basename = s[0]
    tango_input_over_97 = "ITSoneDB_fungi_mapping_data/%s_match_over97 " % basename
    tango_input_under_97 = "ITSoneDB_fungi_mapping_data/%s_match_under97" % basename
    for name in os.listdir("ITSoneDB_fungi_mapping_data"):
        if find(name, "bowtie_result_over_97") == 0:
            tango_output_over_97.append("ITSoneDB_fungi_mapping_data/" + name)
        elif find(name, "bowtie_result_under_97") == 0:
            tango_output_under_97.append("ITSoneDB_fungi_mapping_data/" + name)
#print tango_input
#print tango_output


def controllo_tango_exec(l,m,n,o):
    """


    """
    if os.path.exists(l):
        over_97 = len(open(l).readlines())
        tot = 0
        for name_file in n:
            tot += len(open(name_file).readlines())
        if tot == over_97:
            pass
        else:
            print "Not all the data are processed for the over_97"
    else:
        print "No tango input for sequences with a similarity percentage over the 97%"
        sys.exit()
    if os.path.exists(m):
        under_97 = len(open(m).readlines())
        tot = 0
        for name_file in o:
            tot += len(open(name_file).readlines())
        if tot == under_97:
            pass
        else:
            print "Not all the data are processed for the over_97"
    else:
        print "No tango input for sequences with a similarity percentage under the 97%"
        sys.exit()
    somma = 0
    for name in os.listdir("."):
        if find(name, "tango_error") == 0:
            if os.stat(name)[6] == 0:
                somma += 0
            else:
                somma += 1
    if somma == 0:
        print "tango computation is completed"
    else:
        print "no correct tango output"
        print "please read the tango_error.log file"
        sys.exit()


controllo_tango_exec(tango_input_over_97,tango_input_under_97,tango_output_over_97,tango_output_under_97)

##################################
# COSTRUZIONE DEI DIZIONARI	     #
##################################
id2node = {}
node2parent = {}
node2name = {}
node2order = {}
all_ids = set([])
all_nodes = []
with open(NODESFILE) as a:
    for line in a:
        s = map(strip, line.split("|"))
        field1 = map(strip,s[0].split("###"))
        field2 = map(strip, s[1].split("###"))
        node2parent[field1[0]] = field2[0]
        node2order[field1[0]] = field2[2]
        node2name[field1[0]] = field2[1]


exclusion_list = set()
species_node = set()
for node,rank in node2order.items():
    if rank == "species":
        species_node.add(node)
        exclusion_list.add(node)

for taxid in node2parent:
    path = set()
    if node not in exclusion_list:
        node = taxid
        parent = node2parent[node]
        while node != parent:
            path.add(node)
            node = parent
            parent = node2parent[node]
        if len(species_node.intersection(path)) > 0:
            exclusion_list.add(taxid)



seq2taxa = {}
##################################
# ANALISI DEI DATI			     #
##################################
#analisi risultati tango over_97
out_acc = set()
if len(tango_output_over_97) != 0:
    for name in tango_output_over_97:
        result = open(name)
        for line in result.readlines():
            line = line.strip()
            s = line.split("\t")
            out_acc.add(s[0])
            path = s[2].split(";")
            if node2order[path[0]] == "GB acc":
                seq2taxa[s[0]] = node2parent[path[0]]
            else:
                seq2taxa[s[0]] = path[0]
        result.close()
else:
    print "no tango output files"
    sys.exit()

print
no_processed = open(basename + "_no_processed_data", "w")
if tango_input_over_97 is not "":
    match = open(tango_input_over_97)
    for line in match.readlines():
        line = line.strip()
        s = line.split(" ")
        if s[0] in out_acc:
            pass
        else:
            seq2taxa[s[0]] = node2parent[s[1]]
            if len(s) != 2:
                print>> no_processed, line
    match.close()
    no_processed.close()
else:
    print "no tango input_folder file"
    sys.exit()

if os.stat(basename + "_no_processed_data")[6] == 0:
    os.remove(basename + "_no_processed_data")
else:
    print "there are some not processed data...Please controll the " + basename + "_no_processed_data file"
    sys.exit()


#analisi risultati tango under_97
# accepted_ranks = ["root","superkingdom","phylum","class","order","family","genus"]
out_acc = set()
if len(tango_output_under_97) != 0:
    for name in tango_output_under_97:
        result = open(name)
        for line in result.readlines():
            line = line.strip()
            s = line.split("\t")
            out_acc.add(s[0])
            path = s[2].split(";")
            node_ass = path[0]
            # print node_ass, node2name[node_ass], node2order[node_ass]
            while node_ass in exclusion_list:
                node_ass = node2parent[node_ass]
            seq2taxa[s[0]] = node_ass
            print node2order[node_ass]
        result.close()
else:
    print "no tango output files"
    sys.exit()

print
no_processed = open(basename + "_no_processed_data", "w")
if tango_input_under_97 is not "":
    match = open(tango_input_under_97)
    for line in match.readlines():
        line = line.strip()
        s = line.split(" ")
        if s[0] in out_acc:
            pass
        else:
            seq2taxa[s[0]] = node2parent[s[1]]
            if len(s) != 2:
                print>> no_processed, line
    match.close()
    no_processed.close()
else:
    print "no tango input_folder file"
    sys.exit()

if os.stat(basename + "_no_processed_data")[6] == 0:
    os.remove(basename + "_no_processed_data")
else:
    print "there are some not processed data...Please controll the " + basename + "_no_processed_data file"
    sys.exit()



#costruzione di un dizionario delle assegnazioni avvenute al singolo nodo e costruizione dell'albero
taxa = set()
assigned = {}
for key in seq2taxa.keys():
    taxa.add(seq2taxa[key])
    s = key.split(";")
    if len(s) >= 2:
        value = int(s[1].lstrip("size="))
    else:
        value = 1
    if assigned.has_key(seq2taxa[key]):
        assigned[seq2taxa[key]] += value
    else:
        assigned[seq2taxa[key]] = value

##################################
# COSTRUZIONE ALBERO			 #
##################################
ass_node2parent = {"1": "1"}
for nodeid in taxa:
    parentid = node2parent[nodeid]
    while nodeid != parentid:  #costruiamo un nuovo dizionario per i soli taxa che abbiamo identificato nel campione
        ass_node2parent[nodeid] = parentid
        nodeid = parentid
        parentid = node2parent[nodeid]

node2parentid = {}
for nodeid in ass_node2parent.keys():
    parentid = ass_node2parent[nodeid]
    # Stores node connections
    all_ids.update([nodeid, parentid])
    # Creates a new TreeNode instance for each new node in file
    n = TreeNode()
    # Sets some TreeNode attributes
    n.add_feature("name", node2name[nodeid])
    n.add_feature("taxid", nodeid)
    n.add_feature("Order", node2order[nodeid])

    # updates node list and connections
    node2parentid[n] = parentid
    id2node[nodeid] = n
print len(id2node)
# Reconstruct tree topology from previously stored tree connections
print 'Reconstructing tree topology...'
for node in id2node.itervalues():
    parentid = node2parentid[node]
    parent = id2node[parentid]
    # node with taxid=1 is the root of the tree
    if node.taxid == "1":
        t = node
    else:
        parent.add_child(node)

freq = {}
for node in t.iter_search_nodes():
    if assigned.has_key(node.taxid):
        val = int(assigned[node.taxid])
        node.add_feature("assigned", assigned[node.taxid])
    else:
        val = 0
        node.add_feature("assigned", "0")
    for child in node.iter_descendants():
        if assigned.has_key(child.taxid):
            val = val + assigned[child.taxid]
    node.add_feature("summarized", str(val))

for node in t.iter_search_nodes(name="NoName"):
    if node.is_root():
        node.add_feature("assigned", "0")
        node.add_feature("Order", "root")
        count = 0
        for nodo in node.iter_descendants():
            count += int(nodo.assigned)
        node.add_feature("summarized", str(count))

open(basename + "_tree.nwk", "w").write(t.write(features=["name", "taxid", "assigned", "summarized", "Order"]))

t = Tree(basename + "_tree.nwk")

print t

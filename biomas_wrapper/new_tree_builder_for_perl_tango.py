__author__ = 'Bruno Fosso'
import getopt
import os
import sys
from string import strip
from string import find
# from ete2 import Tree, TreeNode, TreeStyle, faces
from ete2 import *


def usage():
    print ('This script converts the taxonomic assignments made by TANGO in a taxonomic tree.\n'
           'Moreover it produces the taxonomic graphical representation and the 2 TSV summary files:\n'
           'Options:\n'
           '\t-d    nodes file of the taxonomic reference tree. [MANDATORY] \n'
           '\t-h    print this help.\n'
           'Usage:\n'
           '\tpython tango_ass_2_taxa_freq.py -d nodes_file\n'
           '\t')


def controllo_tango_exec(l, m, q, r):
    """
    this function verifies if tango worked properly

    """
    # folder = l.split("/")[0]
    # print folder, os.path.exists(folder)
    # print os.listdir(folder)
    # name_file = l.split("/")[1]
    # print name_file, name_file in os.listdir(folder)
    if os.path.exists(l):
        over_97 = 0
        with open(l) as res_file:
            over_97 += len(res_file.readlines())
        tot = 0
        for name_file in q:
            with open(name_file) as res_file:
                tot += len(res_file.readlines())
        if tot == over_97:
            pass
        else:
            print "Not all the data are processed for the over_97"
    else:
        print "No tango input for sequences with a similarity percentage over the 97%"
        sys.exit()
    if os.path.exists(m):
        under_97 = 0
        with open(m) as res_file:
            under_97 += len(res_file.readlines())
        tot = 0
        for name_file in r:
            with open(name_file) as res_file:
                tot += len(res_file.readlines())
        if tot == under_97:
            pass
        else:
            print "Not all the data are processed for the over_97"
    else:
        print "No tango input for sequences with a similarity percentage under the 97%"
        sys.exit()
    somma = 0
    for name_file in os.listdir("."):
        if find(name_file, "tango_error") == 0:
            if os.stat(name_file)[6] == 0:
                somma += 0
            else:
                somma += 1
    if somma == 0:
        print "tango computation is completed"
    else:
        print "no correct tango output"
        print "please read the tango_error.log file"
        sys.exit()


def my_layout(plotting_node):
    # print '--------------->'+ plotting_node.name
    nameFace = faces.AttrFace("name", fsize=10, fgcolor="#ff0000")  # nome in rosso
    orderFace = faces.AttrFace("Order", fsize=10, fgcolor="#800000")  # ordine in marrone
    rdpFace = faces.AttrFace("assigned", fsize=10, fgcolor="#0000ff")  # assegnati al nodo in blu
    progFace = faces.AttrFace("summarized", fsize=10, fgcolor="#00ff00")  # sommarizzati al nodo in verde

    if "name" in plotting_node.features and "taxid" in plotting_node.features:
        faces.add_face_to_node(nameFace, plotting_node, column=0)
        faces.add_face_to_node(orderFace, plotting_node, column=0)
        faces.add_face_to_node(rdpFace, plotting_node, column=2)
        faces.add_face_to_node(progFace, plotting_node, column=2)
        plotting_node.img_style["size"] = 12
        plotting_node.img_style["shape"] = "sphere"


NODESFILE = ""
try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:")
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

# analisi dell'output prodotto da tango
# basename = ""
# tango_input_over_97 = ""
# tango_input_under_97 = ""
tango_output_over_97 = []
tango_output_under_97 = []
if os.path.exists("quality_check_and_consensus.log"):
    with open("quality_check_and_consensus.log") as qual_log:
        line = qual_log.readline()
        basename = map(strip, line.split("\t"))[0]
        tango_input_over_97 = os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_over97" % basename)
        tango_input_under_97 = os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_under97" % basename)
        for name in os.listdir("ITSoneDB_fungi_mapping_data"):
            if find(name, "bowtie_result_over_97") == 0:
                tango_output_over_97.append(os.path.join("ITSoneDB_fungi_mapping_data", name))
            elif find(name, "bowtie_result_under_97") == 0:
                tango_output_under_97.append(os.path.join("ITSoneDB_fungi_mapping_data", name))
else:
    sys.exit("no quality_check_and_consensus.log file")

# print tango_input
# print tango_output

# print tango_input_over_97, tango_input_under_97, tango_output_over_97, tango_output_under_97
controllo_tango_exec(tango_input_over_97, tango_input_under_97, tango_output_over_97, tango_output_under_97)

##################################
# COSTRUZIONE DEI DIZIONARI	     #
##################################
id2node = {}
node2parent = {}
node2name = {}
node2order = {}
all_ids = set([])
all_nodes = []
exclusion_list = set()
species_node = set()
with open(NODESFILE) as a:
    for line in a:
        s = map(strip, line.split("|"))
        field1 = map(strip, s[0].split("###"))  # node info
        field2 = map(strip, s[1].split("###"))  # parent info
        node2parent[field1[0]] = field2[0]
        node2order[field1[0]] = field1[2]
        node2name[field1[0]] = field1[1]
        if field1[2] == "species":
            species_node.add(field1[0])
            exclusion_list.add(field1[0])

for taxid in node2parent:
    path = set()
    if taxid not in exclusion_list:
        node = taxid
        parent = node2parent[node]
        while node != parent:
            path.add(node)
            node = parent
            parent = node2parent[node]
        if len(species_node.intersection(path)) > 0:
            exclusion_list.add(taxid)

tmp = open("%s_taxonomic_classification.tsv" % basename, "w")
seq2taxa = {}
##################################
# ANALISI DEI DATI			     #
##################################
# analisi risultati tango over_97
out_acc = set()
if len(tango_output_over_97) != 0:
    for name in tango_output_over_97:
        with open(name) as result:
            for line in result:
                s = map(strip, line.split("\t"))
                out_acc.add(s[0])
                path = s[2].split(";")
                path_data = []
                for node in path:
                    if node2order[node] != "GB acc":
                        path_data.append("%s:taxa_rank:(%s)" % (node2name[node], node2order[node]))
                path_data.reverse()
                tmp.write("%s\t%s\n" % (s[0], ";".join(path_data)))
                if node2order[path[0]] == "GB acc":
                    seq2taxa[s[0]] = node2parent[path[0]]
                else:
                    seq2taxa[s[0]] = path[0]
else:
    print "no tango output files for over 97 data"

# analisi risultati tango under_97
# accepted_ranks = ["root","superkingdom","phylum","class","order","family","genus"]
out_acc = set()
if len(tango_output_under_97) != 0:
    for name in tango_output_under_97:
        with open(name) as result:
            for line in result.readlines():
                s = map(strip, line.split("\t"))
                out_acc.add(s[0])
                path = s[2].split(";")
                node_ass = path[0]
                path_data = []
                for node in path:
                    if node not in exclusion_list:
                        path_data.append("%s:taxa_rank:(%s)" % (node2name[node], node2order[node]))
                path_data.reverse()
                tmp.write("%s\t%s\n" % (s[0], ";".join(path_data)))
                while node_ass in exclusion_list:
                    node_ass = node2parent[node_ass]
                seq2taxa[s[0]] = node_ass
                # print node2order[node_ass]
else:
    print "no tango output files"
tmp.close()

# costruzione di un dizionario delle assegnazioni avvenute al singolo nodo e costruizione dell'albero
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
    while nodeid != parentid:  # costruiamo un nuovo dizionario per i soli taxa che abbiamo identificato nel campione
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
        t = node  # type: TreeNode
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

tmp = open("%s_taxonomic_summary.csv" % basename, "w")
tmp.write("Taxon Name\tNCBI Taxonomy ID\tTaxonomic Rank\tDirectly Assigned\tTotal Assigned\n")
for nodo in t.iter_search_nodes():
    if "assigned" in  nodo.features:
        tmp.write("%s\n" % "\t".join([nodo.name, nodo.taxid, nodo.Order, nodo.assigned, nodo.summarized]))
tmp.close()


ts = TreeStyle()
ts.show_leaf_name = False
# ts.rotation = 90
for node in t.iter_search_nodes(Order="species"):
    for nodo in node.get_descendants():
        nodo.detach()
t.render("%s_tree.svg" % basename, layout=my_layout,tree_style=ts, dpi=300)

__author__ = 'Bruno Fosso'

import argparse
from string import strip, find
# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
import os
import argcomplete
from ete2 import *


def tb_parser():
    parser = argparse.ArgumentParser(description=usage(), prefix_chars="-")
    parser.add_argument("-d", "--node_file", type=str,
                        help="tabular file containing the annotation info needed to build the tree",
                        action="store", required=True)
    parser.add_argument("-F", "--Function_folder", type=str,
                        help="the absolute or relative path to the folder containing the Cyhton functions",
                        action="store", required=False,
                        default=os.getcwd())
    argcomplete.autocomplete(parser)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

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

def usage():
    """
    This script converts the taxonomic assignments made by TANGO in a taxonomic tree.
    Moreover it produces the taxonomic graphical representation and the 2 TSV summary files.
    Usage:
    \tpython tango_ass_2_taxa_freq.py -d nodes_file
    """


if __name__ == "__main__":
    args = tb_parser()
    NODESFILE, f_dir = args.node_file, args.Function_folder
    sys.path.append(f_dir)
    from biomas_function import controllo_tango_exec

    tango_output_over_97 = []
    tango_output_under_97 = []
    if os.path.exists("quality_check_and_consensus.log"):
        with open("quality_check_and_consensus.log") as qual_log:
            line = qual_log.readline()
            basename = map(strip, line.split("\t"))[0]
    else:
        sys.exit("no quality_check_and_consensus.log file")
    tango_input_over_97 = os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_over97" % basename)
    tango_input_under_97 = os.path.join("ITSoneDB_fungi_mapping_data", "%s_match_under97" % basename)
    for name in os.listdir("ITSoneDB_fungi_mapping_data"):
        if find(name, "bowtie_result_over_97") == 0:
            tango_output_over_97.append(os.path.join("ITSoneDB_fungi_mapping_data", name))
        elif find(name, "bowtie_result_under_97") == 0:
            tango_output_under_97.append(os.path.join("ITSoneDB_fungi_mapping_data", name))

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

    seq2taxa = {}
    with open("%s_taxonomic_classification.tsv" % basename, "w") as tmp:
        # analisi risultati tango over_97
        for name in tango_output_over_97:
            with open(name) as result:
                for line in result:
                    s = map(strip, line.split("\t"))
                    path = map(strip, s[2].split(";"))
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
        # analisi risultati tango under_97
        for name in tango_output_under_97:
            with open(name) as result:
                for line in result.readlines():
                    s = map(strip, line.split("\t"))
                    path = map(strip, s[2].split(";"))

                    path_data = []
                    for node in path:
                        if node not in exclusion_list:
                            path_data.append("%s:taxa_rank:(%s)" % (node2name[node], node2order[node]))
                    path_data.reverse()
                    tmp.write("%s\t%s\n" % (s[0], ";".join(path_data)))
                    i = 0
                    node_ass = path[i]
                    while node_ass in exclusion_list:
                        i += 1
                        node_ass = path[i]
                    else:
                        seq2taxa[s[0]] = node_ass

    # costruzione di un dizionario delle assegnazioni avvenute al singolo nodo e costruizione dell'albero
    taxa = set()
    assigned = {}
    for seq, node in seq2taxa.items():
        taxa.add(node)
        if find(seq, "size=") == -1:
            value = 1
        else:
            value = int(seq.split("size=")[1])
        assigned.setdefault(node, 0)
        assigned[node] += value

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
    t = None
    for node in id2node.itervalues():  # type: TreeNode
        parent = id2node[node2parentid[node]]
        # node with taxid=1 is the root of the tree
        if node.taxid == "1":
            t = node  # type: Tree
        else:
            parent.add_child(node)

    freq = {}
    if t is not None:
        for node in t.iter_search_nodes():  # type: TreeNode
            if node.taxid in assigned:
                val = int(assigned[node.taxid])
                node.add_feature("assigned", assigned[node.taxid])
            else:
                val = 0
                node.add_feature("assigned", "0")
            for child in node.iter_descendants():
                if child.taxid in assigned:
                    val += assigned[child.taxid]
            node.add_feature("summarized", str(val))

    for node in t.iter_search_nodes(name="NoName"):
        if node.is_root():
            node.add_feature("assigned", "0")
            node.add_feature("Order", "root")
            count = 0
            for nodo in node.iter_descendants():
                count += int(nodo.assigned)
            node.add_feature("summarized", str(count))

    with open(basename + "_tree.nwk", "w") as tree_file:
        tree_file.write(t.write(features=["name", "taxid", "assigned", "summarized", "Order"]))
    t = Tree(basename + "_tree.nwk")
    with open("%s_taxonomic_summary.csv" % basename, "w") as tmp:
        tmp.write("Taxon Name\tNCBI Taxonomy ID\tTaxonomic Rank\tDirectly Assigned\tTotal Assigned\n")
        for nodo in t.iter_search_nodes():
            if "assigned" in nodo.features:
                tmp.write("%s\n" % "\t".join([nodo.name, nodo.taxid, nodo.Order, nodo.assigned, nodo.summarized]))

    ts = TreeStyle()
    ts.show_leaf_name = False
    # ts.rotation = 90
    for node in t.iter_search_nodes(Order="species"):
        for nodo in node.get_descendants():
            nodo.detach()
    t.render("%s_tree.svg" % basename, layout=my_layout, tree_style=ts, dpi=300)

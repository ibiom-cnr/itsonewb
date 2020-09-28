from string import strip
import argparse
import fpformat
from numpy import mean
import os
import gzip
import matplotlib as mpl
mpl.use('agg')
from plotnine import *
import pandas as pd


def bg_options():
    parser = argparse.ArgumentParser(description="print the barcoding gap", prefix_chars="-")
    parser.add_argument("-d", "--distance_folder", type=str,
                        help="folder in which are stored the distances in family specific files",
                        action="store", required=True)
    parser.add_argument("-f", "--all_taxa_file_list", type=str,
                        help="file containing all the taxon list",
                        action="store", required=True)
    parser.add_argument("-n", "--taxon_name", type=str, help="taxon name", action="store", required=True)
    parser.add_argument("-r", "--taxonomic_rank", type=str, help="taxonomic_rank", action="store", required=True)
    parser.add_argument("-F", "--out_folder", type=str, help="output folder", action="store", required=False,
                        default=os.getcwd())
    return parser.parse_args()


def inclusion_set(rank):
    intra_string = []
    extra_string = []
    if rank == "species":
        intra_string.append("interspecies")
        extra_string.append("intergenus")
    elif rank == "genus":
        intra_string.extend(["interspecies", "intergenus"])
        extra_string.append("interfamily")
    return intra_string, extra_string


def distance_file_selection(all_taxa_file_list, taxa, folder):
    file_name = False
    with open(all_taxa_file_list) as a:
        for line in a:
            s = map(strip, line.split("\t"))
            if s[0] == taxa:
                file_name = os.path.join(folder, "%s_distaces.tsv.gz" % s[2].replace(" ", "_"))
                break
    return file_name


def infer_bg(distance_file, taxon, rank, outfolder):
    intra = []
    extra = []
    intra_str, extra_str = inclusion_set(rank)
    bg = None
    with gzip.open(distance_file) as a:
        for line in a:
            field = map(strip, line.split("\t"))
            if taxon in field and field[3] in intra_str:
                intra.append(float(field[2]))
            elif taxon in field and field[3] in extra_str:
                extra.append(float(field[2]))
    if len(extra) and len(intra):
        bg_mean = fpformat.fix(mean(extra) - mean(intra), 2)
        bg_diff = fpformat.fix(min(extra) - max(intra), 2)
        plot = plot_distance_dist(intra, extra, taxon, outfolder)
        bg = [bg_mean, bg_diff, plot]
    elif len(intra) == 0:
        bg = "No intra%s data" % rank
    elif len(extra) == 0:
        bg = "No extra%s data" % rank
    return bg


def plot_distance_dist(intra, inter, taxa, folder):
    measure_list_index = ["Intra"]*len(intra)
    measure_list_index.extend(["Inter"]*len(inter))
    df = pd.DataFrame({
        'variable': measure_list_index,
        'Distance': intra + inter,
    })
    p = (ggplot(df, aes(x='variable', y='Distance', fill='variable')) + geom_boxplot(alpha=.7) + theme(
        axis_text_x=element_text(face="bold"), plot_title=element_text(face="bold", hjust=0.5), axis_title_x = element_blank(), axis_title_y = element_text(face = "bold"), legend_position = "none", legend_title = element_blank()) + labs(title=taxa))
    out_name = os.path.join(folder, "%s_dist_plot.png" % taxa)
    (ggsave(filename=out_name, dpi=300, device="png", plot=p,width=4,height=4))
    return out_name



def print_bg():
    params = bg_options()
    print params.taxon_name.strip("'")
    dist_file = distance_file_selection(params.all_taxa_file_list, params.taxon_name.strip("'"), params.distance_folder)
    print dist_file
    if dist_file:
        barcodinggap = infer_bg(dist_file, params.taxon_name.strip("'"), params.taxonomic_rank, params.out_folder)
    else:
        barcodinggap = "the selected name is currently not available "
    return barcodinggap


if __name__ == "__main__":
    print print_bg()

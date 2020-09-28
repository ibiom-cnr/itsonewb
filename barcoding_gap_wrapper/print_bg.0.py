from string import strip
import argparse
import fpformat
from numpy import mean
import os
import gzip
import matplotlib as mpl

mpl.use('agg')
from matplotlib.pyplot import figure


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
    data_to_plot = [intra, inter]
    fig = figure(1, figsize=(9, 6))
    # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot
    bp = ax.boxplot(data_to_plot, patch_artist=True)
    for box in bp['boxes']:
        # change outline color
        box.set(color='#7570b3', linewidth=2)
        # change fill color
        box.set(facecolor='#1b9e77')
    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)
    # change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=2)
    # change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='#b2df8a', linewidth=2)
    # change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_title('%s' % taxa)
    # Save the figure
    ax.set_xticklabels(['Intra', 'Inter'])
    out_name = os.path.join(folder, "%s_dist_plot.png" % taxa)
    fig.savefig(out_name, bbox_inches='tight')
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

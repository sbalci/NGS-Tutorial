#!/usr/bin/env python2

from __future__ import print_function
import sys

input_file = open(sys.argv[1], 'r')
ref_file = open(sys.argv[2], 'r')
output_file = open(sys.argv[3], 'w')

peak_dict = {}

for line in input_file:
    line = line.rstrip()
    data = line.split("\t")
    if data[6] == '.':
        continue
    strand_peaks = data[5]
    strand_anno = data[9]
    peak_anno = data[10]
    gene_id = data[11].split('|')[1]
    peak_count = data[3].split('|')[2]
    if strand_peaks != strand_anno:
        continue
    site = "{0}:{1}-{2},{3},{4}".format(data[0],data[1],data[2],data[5],data[10])
    if not gene_id in peak_dict:
        peak_dict[gene_id] = [[site, peak_anno, int(peak_count)]]
    else:
        peak_dict[gene_id].append([site, peak_anno, int(peak_count)])

for line in ref_file:
    line = line.rstrip()
    data = line.split("\t")
    if line.startswith('#'):
        print("gr_id", "gene_id", "gene_symbol", "Akimitsu_lab_type", "Gencode_gene_type", "chrom_infor", "peak_sites", "peak_anno", sep="\t", end="\n", file=output_file)
        continue
    gene_symbol = data[1]
    if gene_symbol in peak_dict:
        peak_infor = peak_dict[gene_symbol]
        peak_infor.sort(key=lambda x:x[2])
        best_peak_infor = peak_infor[-1]
        peak_sites = best_peak_infor[0]
        peak_anno = best_peak_infor[1]
        peak_anno_compact = []
        if '5UTR' in peak_anno:
            peak_anno_compact.append('5UTR')
        if 'CDS' in peak_anno:
            peak_anno_compact.append('CDS')
        if '3UTR' in peak_anno:
            peak_anno_compact.append('3UTR')
        if 'Intron' in peak_anno:
            peak_anno_compact.append('Intron')
        print(line, peak_sites, '|'.join(peak_anno_compact), sep="\t", end="\n", file=output_file)
    else:
        print(line, "NA", "NA", sep="\t", end="\n", file=output_file)
        continue

#!/usr/bin/env python

import argparse
from qsub import *

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-vcf', help='vcf file to summarise sfs for', required=True)
parser.add_argument('-mode', help='mode to run in', choices=['SNP', 'INDEL'], required=True)
parser.add_argument('-out', help='Output directory', required=True)
parser.add_argument('-spp', help='Species', required=True)
parser.add_argument('-evolgen', help='If specified will run on lab queue', action='store_true', default=False)
args = parser.parse_args()

# variables
vcf = args.vcf
out = args.out
spp = args.spp
mode = args.mode
mode_dict = {'SNP': ['snp'], 'INDEL': ['ins', 'del']}
region_dict = {'SNP': ['ALL', 'CDS_non_frameshift', 'intron', 'intergenic', 'ar'],
               'INDEL': ['ALL', 'CDS_frameshift', 'CDS_non_frameshift', 'intron', 'intergenic', 'ar']}
evolgen = args.evolgen

# SFS
for m in mode_dict[mode]:
    for r in region_dict[mode]:
        new_out = '{}{}_{}_{}.sfs.txt'.format(out, spp, m, r.replace('_', ''))
        if r == 'ar':
            r = 'intergenic_ar -region intron_ar'
        sfs_cmd = ('~/sfs_utils/vcf2raw_sfs.py '
                   '-vcf {} '
                   '-mode {} '
                   '-auto_only '
                   '-skip_hetero '
                   '-region {} '
                   '| sort | uniq -c | while read i; do echo " "$i; done | tr -s " " '
                   '> {}').format(vcf, m, r, new_out)

        if r == 'ALL':
            sfs_cmd = sfs_cmd.replace('-region ALL ', '')
        q_sub([sfs_cmd], out=new_out.replace('.txt', ''), evolgen=evolgen)

#!/usr/bin/env python

import argparse
from qsub import *

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-fa', help='Fasta file to soft mask', required=True)
parser.add_argument('-evolgen', help='If specified will run on lab queue', default=False, action='store_true')
args = parser.parse_args()

# variables
fa = args.fa
evolgen = args.evolgen
out_dir = fa[:fa.rfind('/')+1]

# cmd line
rep_mask_cmd = ('RepeatMasker -species drosophila -xsmall ' + fa)

q_sub(['cd ' + out_dir, rep_mask_cmd], out=fa.replace('.fa', ''), evolgen=evolgen)

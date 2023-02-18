import os
import itertools
import subprocess
import bpy
import random
import sys
import csv

argv = sys.argv
argv = argv[argv.index("--") + 1:]

groupName = argv[0]
senderBlend = argv[1]

with bpy.data.libraries.load(senderBlend, link=False) as (data_from, data_to):
    n_gs = []
    for ng in data_from.node_groups:
        if groupName in ng:
            n_gs.append(ng)
    data_to.node_groups = n_gs

nuName = f'NS_{groupName}'
bpy.data.node_groups[groupName].name = nuName
bpy.data.node_groups[nuName].use_fake_user = True
bpy.ops.wm.save_mainfile()
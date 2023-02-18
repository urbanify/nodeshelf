"""import random
import bpy
import os



def write_metadata(self, context):
    pass"""
import random


def customFunction(nb_vars):
    elements = []
    for x in range(nb_vars):
        elements.append(random.randint(0, 100))

    return elements

a, b, c, d, e = customFunction(5)

print(a)
print(b)
print(c)
print(d)
print(e)
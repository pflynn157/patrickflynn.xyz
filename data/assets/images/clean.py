#!/usr/bin/python3
import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.endswith("-scaled.jpg") or f.endswith("-scaled.png"):
        os.remove("./" + f)

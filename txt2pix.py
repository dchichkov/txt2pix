#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
"""

#
#  (C) Dmitry Chichkov, 2017, All rights reserved.
#
__version__='$Id$'
#

import os, sys, gzip, pickle, shutil, random, numpy as np
from os.path import join, getsize, basename
from PIL import Image


def loadEmbedding(embeddings_path):
    """ Initialize embeddings with word2vec-like vectors
    """
    print("Loading embeddings from %s " % embeddings_path)
    with open(embeddings_path, "rb") as f:
        header = f.readline()
        vocab_size, vector_size = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * vector_size
        initW = np.full((vocab_size, 8, 8), 0, dtype=np.uint8)
        for id in range(vocab_size):
            vector = np.fromstring(f.readline(), sep=' ', dtype=np.float32).astype(np.uint8) * 255 
            initW[id] = vector.reshape((8, 8))
            
    return initW


if __name__ == "__main__":    
    embedding = loadEmbedding('codepage_437_embedding.vec')     
    fEN, fFR, fOUT = open(sys.argv[1], 'r'), open(sys.argv[2], 'r'), sys.argv[3] 
    DX,DY = 32,8
    EF = np.full( (DY, 8, 2, DX, 8), 0, dtype=np.uint8 )

    def render(sentence, iEF):
        try: sentence = sentence.decode('utf8').encode('cp437')
        except: 
            print "Skipping..."
            return False 
        X, Y = 0, 0
        for word in sentence.split():
            if X + len(word) >= DX:
                X, Y = 0, Y + 1
                if Y >= DY: return False
                if X + len(word) >= DX: return False 
                                 
            for letter in word:                
                EF[Y, :, iEF, X, :] = embedding[ord(letter)]
                X += 1
            X += 1           # space
                
        return True


    print("Rendering images... ")
    I = 0
    for lEN, lFR in zip(fEN, fFR):
        EF[:] = 0
        if render(lEN, 0) and render(lFR, 1):
            img = Image.fromarray(EF.reshape((DY * 8, 2 * DX * 8)), mode = 'L').convert('1')
            partition = 'val' if I % 100 == 0 else ('test' if I % 111 == 0 else 'train') 
            img.save(join(fOUT, partition, "%08d.png" % I))
            I += 1
            #if I == 200000: break
        
        
        
         
                                                
        
        
        
            
            

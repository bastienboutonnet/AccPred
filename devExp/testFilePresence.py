import os, re, time
import pandas as pd

#go through trial list sent IDs
#for each ID, combined with each speaker and relatedness is there a file with that name.
#if not print the combination in a text file.

filenames=os.listdir('/Users/boutonnetbpa/Dropbox/3.CurrentProjects/AThEME/accentedSpeech/AccPred/devExp/stimuli') ## UPDATE path

sentList=pd.read_csv('../database/120allAbove70.csv', encoding='utf-16')
# missing=open('missingSentences.txt','w')
#
# def writeToFile(fileHandle,trial,sync=True):
# 	"""Writes a trial (array of lists) to a fileHandle"""
# 	line = '\t'.join([str(i) for i in trial]) #TABify
# 	line += '\n' #add a newline
# 	fileHandle.write(line)
# 	if sync:
# 		fileHandle.flush()
# 		os.fsync(fileHandle)
t=time.strftime("%m%d%H%M")
with open('missingSentences_'+t+'.txt','a') as file:
    for curID in sentList['sentID']:
        curNatRel='Nat_'+str(curID)+'_related.wav'
        curNatUnrel='Nat_'+str(curID)+'_unrelated.wav'
        curNonNatRel='nonNat_'+str(curID)+'_related.wav'
        curNonNatUnrel='nonNat_'+str(curID)+'_unrelated.wav'

        if curNatRel not in filenames:
            file.write(curNatRel+'\n')
        if curNatUnrel not in filenames:
            file.write(curNatUnrel+'\n')
        if curNonNatRel not in filenames:
            file.write(curNonNatRel+'\n')
        if curNonNatUnrel not in filenames:
            file.write(curNonNatUnrel+'\n')

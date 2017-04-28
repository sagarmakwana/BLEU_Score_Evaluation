# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:43:33 2017

@author: Sagar Makwana
"""

import sys
import os
import math
import codecs

reload(sys)
sys.setdefaultencoding("utf-8")

def get_precision_brevity(candidateFile,referencesFiles,n):
    #Initializing the parameters
    cand_ngram_count = 0
    clipped_count = 0
    c = 0
    r = 0
    
    #Iterating over each sentence
    for i in range(len(candidateFile)):
        closest_ref_can_len = 0
        diff_ref_can_len = float('inf')
        
        ref_ngrams_dict_list = []
        
        cand_sentence = candidateFile[i]
        cand_sentence_split = cand_sentence.strip().split()
        cand_ngram_count += len(cand_sentence_split) - n + 1;
        #Generating candidate ngram dictionary
        cand_ngram_dict = {}
        for j in range(len(cand_sentence_split) - n + 1):
            ngram = ''.join(cand_sentence_split[j:j + n]).lower()
            if ngram in cand_ngram_dict:
                cand_ngram_dict[ngram] += 1
            else:
                cand_ngram_dict[ngram] = 1
    
        
        
        #Generate reference ngram dictionary
        for referenceFile in referencesFiles:
            #Generate reference ngram dictionary
            ref_sentence = referenceFile[i]
            ref_sentence_split = ref_sentence.strip().split()
            
            ref_ngram_dict = {}
            for j in range(len(ref_sentence_split) - n + 1):
                ngram = ''.join(ref_sentence_split[j:j + n]).lower()
                if ngram in ref_ngram_dict:
                    ref_ngram_dict[ngram] += 1
                else:
                    ref_ngram_dict[ngram] = 1
                                  
            if diff_ref_can_len > abs(len(cand_sentence_split) - len(ref_sentence_split)):
                diff_ref_can_len = abs(len(cand_sentence_split) - len(ref_sentence_split))
                closest_ref_can_len = len(ref_sentence_split)
                              
            ref_ngrams_dict_list.append(ref_ngram_dict)
        
        #Generating clipped count
        for ngram in cand_ngram_dict:
            cand_count = cand_ngram_dict[ngram]
            ref_max = 0
            for ref_dict in ref_ngrams_dict_list:
                if ngram in ref_dict:
                    ref_max = max(ref_dict[ngram],ref_max)
            clipped_count += min(ref_max,cand_count)
            
        r += closest_ref_can_len
        c += len(cand_sentence_split)
                   
    precision =0
    if clipped_count != 0:
        precision = clipped_count*1.0/cand_ngram_count
        
    brev_penalty = 1
    if c < r:
        brev_penalty = math.exp(1.0 - (r * 1.0 / c))
        
    return precision,brev_penalty
            
#-------------------------------------------------Logic-------------------------------
candidatePath = sys.argv[1]
referencesPath = sys.argv[2]

#Generate candidate and reference files
referencesFiles = []
if os.path.isdir(referencesPath):
    for root, dirs, files in os.walk(referencesPath):
        for eachFile in files:
            currFile = codecs.open(os.path.join(root, eachFile), 'r', 'utf-8')
            referencesFiles.append(currFile.readlines())
            currFile.close()
else:
    currFile = codecs.open(referencesPath, 'r', 'utf-8')
    referencesFiles.append(currFile.readlines())
    currFile.close()

currFile = codecs.open(candidatePath, 'r', 'utf-8')
candidateFile = currFile.readlines()
currFile.close()


bleu_score = 0
geometric_mean = 1.0

for i in range(1, 5, 1):
    precision, brevity_penalty = get_precision_brevity(candidateFile, referencesFiles, i)
    geometric_mean *= precision


geometric_mean = math.pow(geometric_mean, (1.0 / 4))
bleu_score = geometric_mean * brevity_penalty

outputFile =  open('bleu_out.txt','w')
outputFile.write(str(bleu_score))
outputFile.close()

    


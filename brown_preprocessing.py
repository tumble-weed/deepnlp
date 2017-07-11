# copy pasted from brown_preprocessing.ipynb
import numpy as np
import pdb

def brown_to_idx(vocab_size=np.inf,keep_words = []):
    # check the brown corpus
    from nltk.corpus import brown
    sents =  list(brown.sents()) # convert the sentences to a list

    print 'number of sentences %d'%len(sents)
    #print sents[0]
    
    """ Just see all the words """
#     all_words = [w.lower() for s in sents for w in s] # convert all words to lowercase
#     print len(all_words) # total number of words (with repetitions)
#     unique_words = np.unique(all_words) # get all unique words
#     print len(unique_words) # total number of unique words

    # Goal:
    # 1. go sentence by sentence, tracking each unique word and its count
    # 2. only keep the top 'vocab_size' words and the keep_words , we are expecting the final vocabulary size
    # to be between vocab_size and vocab_size + len(keep_words)
    
    word2idx = {} 
    idx2count = []
    nwords = 0

    for s in sents:
        for w in s:
            w = w.lower() 
            if w not in word2idx:
                word2idx[w] = nwords
                idx2count.extend([1])
                nwords += 1
            else:
                idx2count[word2idx[w]] += 1

    top_indices = np.argsort(idx2count)[::-1] # default sorting order is ascending
    kept_indices = top_indices[:vocab_size] # indices of the top words
    # check if any of the keep words are not in the word2idx dictionary
    for w in keep_words:
        if w not in word2idx:
            print w,' not in word2idx '
    keep_word_indices = [word2idx[w] for w in keep_words if w in word2idx] # indices of the keep_words
    kept_indices=set(kept_indices) # make the kept_indices into a set
    kept_indices = kept_indices.union(keep_word_indices) # now we can use union to add the keep_words 
                                                         # and frequent_words
    kept_indices = list(kept_indices) # list of kept indices
    print len(kept_indices)
#     print kept_indices, keep_word_indices

    # second pass only keep information about the kept_indices
    # the rest convert to 'UNKNOWN'
    word2idx_lim_vocab = {'UNKNOWN':0} # a default value for all the words that will be discarded
    idx2word_lim_vocab = ['UNKNOWN'] 
    nwords_lim = 1
    indexed_sents = [] # to hold the indexed senteces
    for s in sents:
        indexed_sents.append([])
        for w in s:
            w = w.lower()
            if w not in word2idx_lim_vocab:
                if word2idx[w] in kept_indices:
                    word2idx_lim_vocab[w] = nwords_lim
                    idx2word_lim_vocab.extend([w])
                    nwords_lim+=1
            indexed_sents[-1].extend([word2idx_lim_vocab.get(w,0)])
    return indexed_sents, word2idx_lim_vocab, idx2word_lim_vocab
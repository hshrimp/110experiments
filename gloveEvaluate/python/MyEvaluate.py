import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vocab_file', default='wiki_aabcde_300/vocab.txt', type=str)
    parser.add_argument('--vectors_file', default='wiki_aabcde_300/vectors.txt', type=str)
    args = parser.parse_args()

    with open(args.vocab_file, 'r') as f:
        words = [x.rstrip().split(' ')[0] for x in f.readlines()]
        #print 'words = ',words
    with open(args.vectors_file, 'r') as f:
        vectors = {}
        for line in f:
            vals = line.rstrip().split(' ')
            vectors[vals[0]] = [float(x) for x in vals[1:]]

    vocab_size = len(words)
    vocab = {w: idx for idx, w in enumerate(words)}
    ivocab = {idx: w for idx, w in enumerate(words)}

    #print ivocab[0]
    vector_dim = len(vectors[ivocab[0]])
    W = np.zeros((vocab_size, vector_dim))
    for word, v in vectors.items():
        if word == '<unk>':
            continue
        W[vocab[word], :] = v
        #print 'np.dot(v,np.linspace(1,1,50))=',np.dot(v,np.linspace(1,1,50))
        #print 'sum(v)=',sum(v)

    # normalize each word vector to unit variance
    W_norm = np.zeros(W.shape)
    d = (np.sum(W ** 2, 1) ** (0.5))
    W_norm = (W.T / d).T
    # count = 0
    # count2 = 0
    # for i in range(len(W)):
    #     print 'sum(W[i])=',sum(W[i])
    #     print i,'sum(W_norm)=',sum(W_norm[i])
    #     if abs(sum(W[i]))>abs(sum(W_norm[i])):
    #         count+=1
    #     val = (abs(W[i])>abs(W_norm[i]))
    #     count2 += sum(val)
    # print 'count=',count,'\ncount2=',count2
    evaluate_vectors(W_norm, vocab, ivocab)

def evaluate_vectors(W, vocab, ivocab):
    """Evaluate the trained word vectors on capital-common-countries.txt variety of tasks"""

    filenames = [
        'capital-common-countries.txt',
        'city-in-state.txt', 'family.txt',
        ]
    prefix = '/home/wshong/Desktop/analogy_data/'

    # to avoid memory overflow, could be increased/decreased
    # depending on system and vocab size
    split_size = 100

    correct_sem = 0; # count correct semantic questions
    correct_syn = 0; # count correct syntactic questions
    correct_tot = 0 # count correct questions
    count_sem = 0; # count all semantic questions
    count_syn = 0; # count all syntactic questions
    count_tot = 0 # count all questions
    full_count = 0 # count all questions, including those with unknown words

    for i in range(len(filenames)):
        with open('%s/%s' % (prefix, filenames[i]), 'r') as f:
            full_data = [line.rstrip().split(' ') for line in f]
            full_count += len(full_data)
            data = [x for x in full_data if all(word in vocab for word in x)]

        indices = np.array([[vocab[word] for word in row] for row in data])
	#print 'filenames[',i,']=',filenames[i]
        #print 'indices=',indices
        ind1, ind2, ind3, ind4 = indices.T
        #print "ind1=%s\n, ind2=%s\n, ind3=%s\n, ind4=%s"%(ind1,ind2,ind3,ind4)
        predictions = np.zeros((len(indices),))
        num_iter = int(np.ceil(len(indices) / float(split_size)))
        for j in range(num_iter):
            subset = np.arange(j*split_size, min((j + 1)*split_size, len(ind1)))
            #print 'W[ind2[subset], :]=',W[ind2[subset], :],'\nW[ind1[subset], :]=',W[ind1[subset], :],'\nW[ind3[subset], :]=',W[ind3[subset], :]
            pred_vec = (W[ind2[subset], :] - W[ind1[subset], :]
                +  W[ind3[subset], :])
            #print 'pred_vec=',pred_vec
            #cosine similarity if input W has been normalized
            dist = np.dot(W, pred_vec.T)
            #print 'dist=',dist
            for k in range(len(subset)):
                #print 'subset[k]=',subset[k],'\nk=',k,'\nind1[subset[k]]=',ind1[subset[k]],'\nind2[subset[k]]=',ind2[subset[k]],'\nind3[subset[k]]=',ind3[subset[k]]
                dist[ind1[subset[k]], k] = -np.Inf
                dist[ind2[subset[k]], k] = -np.Inf
                dist[ind3[subset[k]], k] = -np.Inf

            # predicted word index
            predictions[subset] = np.argmax(dist, 0).flatten()
            #print 'predictions[subset]=',predictions[subset]
        val = (ind4 == predictions) # correct predictions
        count_tot = count_tot + len(ind1)
        correct_tot = correct_tot + sum(val)
        if i < 5:
            count_sem = count_sem + len(ind1)
            correct_sem = correct_sem + sum(val)
        else:
            count_syn = count_syn + len(ind1)
            correct_syn = correct_syn + sum(val)

        print("%s:" % filenames[i])
        print('ACCURACY TOP1: %.2f%% (%d/%d)' %
            (np.mean(val) * 100, np.sum(val), len(val)))

    print('Questions seen/total: %.2f%% (%d/%d)' %
        (100 * count_tot / float(full_count), count_tot, full_count))
    print('Semantic accuracy: %.2f%%  (%i/%i)' %
        (100 * correct_sem / float(count_sem), correct_sem, count_sem))
    # print('Syntactic accuracy: %.2f%%  (%i/%i)' %
    #     (100 * correct_syn / float(count_syn), correct_syn, count_syn))
    print('Total accuracy: %.2f%%  (%i/%i)' % (100 * correct_tot / float(count_tot), correct_tot, count_tot))


if __name__ == "__main__":
    main()

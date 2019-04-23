


if __name__ == "__main__":
    #N = 10;          # number of closest words that will be shown
    with open('/home/wshong/Downloads/glove/bk1_21result/vectors.txt', 'r') as f:
        words = []
        vectors = {}
        for line in f:
            vals = line.rstrip().split(' ')
            words.append(vals[0])
            vectors[vals[0]] = ' '.join(map(str,vals[1:]))
        #vocab2 = dict((vocab))

    with open('newvocab', 'r') as f:
        dictwords = [x.rstrip().split(' ')[0] for x in f.readlines()]
    dictvocab = {w: idx for idx, w in enumerate(dictwords)}
    fi=open('newvectors.txt','w')
    for word in words:
        #print word,' ',num,' ',(int(num) >= 100),'&&',(dictvocab.has_key(word))
        if dictvocab.has_key(word):
            #newvocab.write(word+' '+num+'\n')
            fi.write(word+' '+vectors[word]+'\n')
            print word,' ',vectors[word]
    fi.close()









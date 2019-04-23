


if __name__ == "__main__":
    #N = 10;          # number of closest words that will be shown
    with open('vocab.txt', 'r') as f:
        #words = [x.rstrip().split(' ')[0] for x in f.readlines()]
        vocab = dict([x.rstrip().split(' ') for x in f.readlines()])
        #vocab2 = dict((vocab))

    with open('dict.txt', 'r') as f:
        dictwords = [x.rstrip().split(' ')[0] for x in f.readlines()]

    # vocab_size = len(words)
    #vocab = {w: idx for idx, w in enumerate(words)}
    #ivocab = {idx: w for idx, w in enumerate(words)}
    dictvocab = {w: idx for idx, w in enumerate(dictwords)}
    # ivocab, dictvocab = generate()
    dic={}
    for word,num in vocab.items():
        #print word,' ',num,' ',(int(num) >= 100),'&&',(dictvocab.has_key(word))
        if int(num) >= 100:
            #newvocab.write(word+' '+num+'\n')
            dic[word] = int(num)
        elif dictvocab.has_key(word):
            #newvocab.write(word+' '+num+'\n')
            dic[word] = int(num)
            #print 'true ',num

    newdic = sorted(dic.iteritems(), key=lambda asd: asd[1],reverse=True)
    newvocab=open('newvocab','w+')
    count=0.0
    for line in newdic:
        newvocab.write(line[0]+' '+str(line[1])+'\n')
        #print line[0],' ',line[1]
        if dictvocab.has_key(line[0]):
            count +=1.0
    print count,' / ',len(dictvocab),' = ',count/len(dictvocab)
    newvocab.close()









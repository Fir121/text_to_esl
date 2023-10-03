import gensim

embeddings = gensim.models.KeyedVectors.load_word2vec_format('data/w2vec_sg.bin',binary=True,unicode_errors='ignore')

sims = embeddings.wv.most_similar('مركبة', topn=10) 

print(sims)
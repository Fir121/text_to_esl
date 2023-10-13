from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format('Mazajak/data/sg_250.bin',binary=True,unicode_errors='ignore')
print(model.get_normed_vectors())
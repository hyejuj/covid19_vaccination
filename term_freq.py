import csv
import sys
import spacy
from collections import Counter
import preprocessor as p

nlp = spacy.load('en_core_web_sm')
p.set_options(p.OPT.URL, p.OPT.RESERVED) #, p.OPT.HASHTAG)
def compute(input_file, target, threshold=100):
    tf = Counter()
    output_file = '%s.csv' % target
    with open(output_file, 'w') as wf, open(input_file, 'r') as rf:
        reader = csv.DictReader(rf)
        writer = csv.writer(wf)
        header = ['term', 'freq']
        writer.writerow(header)
        cnt = 0
        for row in reader:
            if cnt >= threshold:
                break
            else:
                cleaned = p.clean(row['tweet'])
                doc = nlp(cleaned)
                token_set = set()
                for token in doc:
                    if token.pos_ == 'NOUN':
                        token_set.add(token.lemma_.lower())
                for tok in token_set:
                    tf[tok] += 1
                cnt += 1
        for k in tf.most_common():
            writer.writerow([k[0], k[1]])

if __name__ == '__main__':
    input_file = 'orig_sort_favorite.csv'
    target = 'favorite_count'
    threshold = 100
    compute(input_file, target, threshold)

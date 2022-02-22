from nlp_architect.models.absa.inference.inference import SentimentInference
import csv
import re
import sys
import json

class Aspect:
    term = None
    pos = 0
    neg = 0
    score = 0
    cnt = 0

ASPECT_LEX = '/home/hyejuj/nlp-architect/cache/absa/train/lexicons/generated_aspect_lex.csv'
OPINION_LEX = '/home/hyejuj/nlp-architect/cache/absa/train/lexicons/generated_opinion_lex_reranked.csv'

#input_file = 'ca_clean_v.csv'
input_file = 'orig_sort_favorite.csv'
num = int(sys.argv[1])
output_file = 'sentiment_ca_v_June_%d.csv' % num
output2_file = 'sentiment_ca_v_June_%d.json' % num
with open(input_file, 'r') as rf, open(output_file, 'w') as wf, open(output2_file, 'w') as wf2:
    reader = csv.DictReader(rf)
    inference = SentimentInference(ASPECT_LEX, OPINION_LEX)
    writer = csv.writer(wf)
    headers = ['term', 'pos', 'neg', 'score', 'cnt']
    writer.writerow(headers)
    aspect_dic = {}
    cnt = 0
    #wf2.write('[\n') # beginning of the output file for Dave
    for row in reader:
        json_dic = {}
        author = row['author']
        json_dic['sub_author'] = author
        tweet_id = row['tweet_id']
        json_dic['sub_id'] = tweet_id
        tweet_time = row['tweet_time']
        json_dic['sub_time'] = tweet_time
        orig_tweet = row['tweet']
        json_dic['sub_body'] = orig_tweet
        tweet = row['clean_tweet']
        if cnt < num:
            cnt += 1
            continue
        if cnt > num + 100:
            break
        print(cnt, tweet)
        sentiment_doc = inference.run(tweet)
        if sentiment_doc == None:
            continue
        json_dic['sub_body_inference'] = re.sub(' +', ' ', str(sentiment_doc).replace('\n', ''))
        wf2.write(json.dumps(json_dic))
        wf2.write(',\n')
        #print('##', sentiment_doc)
        if sentiment_doc == None:
            cnt += 1
            continue
        sents = sentiment_doc._sentences
        for sent in sents: 
            if sent == None:
                continue
            events = sent._events
            for event_list in events:
                if len(event_list) == 0:
                    continue
                for event in event_list:
                    term = event._text
                    term_type = event._type
                    polarity = event._polarity
                    score = event._score

                    if str(term_type) != 'TermType.ASPECT':
                        continue
                    if term in aspect_dic:
                        a_class = aspect_dic[term]
                        if str(polarity) == 'Polarity.POS':
                            a_class.pos += 1
                        elif str(polarity) == 'Polarity.NEG':
                            a_class.neg += 1
                        else:
                            print('WRONG SENTIMENT', polarity)
                        a_class.cnt += 1
                        a_class.score += score
                    else:
                        a_class = Aspect()
                        a_class.term = term
                        if str(polarity) == 'Polarity.POS':
                            a_class.pos = 1
                        elif str(polarity) == 'Polarity.NEG':
                            a_class.neg = 1
                        else:
                            print('WRONG SENTIMENT2', polarity)
                        a_class.cnt = 1
                        a_class.score = score
                        aspect_dic[term] = a_class
        cnt += 1
    #wf2.write('\n]') # end of the output file for Dave
    for term, a_class in aspect_dic.items():
        new_row = [term, a_class.pos, a_class.neg, 
                a_class.score, a_class.cnt]
        writer.writerow(new_row)

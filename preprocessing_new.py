import json
import csv
import sys
import pickle

import preprocessor as p

keywords = ['immunity', 'immune', 'vaccine', 'vaccination', 'herd', 'rollout', 'program', 'mrna', 'distribution', 'side effect', 'reaction', 'dose', 'campaign', 'candidate', 'antibody', 'antibodies', 'anti-vaxxer', 'adverse', 'response', 'adenovirus', 'astrazeneca', 'moderna', 'pfizer', 'johnson', 'allergy', 'allergic']
def get_texts(input_file, output_file):
    with open(input_file, 'r') as rf, open(output_file, 'w') as wf:
        writer = csv.writer(wf, quoting=csv.QUOTE_ALL)
        writer.writerow(['author', 'tweet', 'clean_tweet', 'tweet_id', 'tweet_time', 'user_id', 'followers_count', 
            'favourites_count', 'friends_count', 'statuses_count', 'retweet_count', 'favorite_count', 'retweet_yes', 'quote_yes', 
            'reply_yes'])
        p.set_options(p.OPT.URL, p.OPT.RESERVED)
        for line in rf:
            data_json = json.loads(line)
            text = data_json['full_text']
            clean_text = p.clean(text)
            vaccine_related = False
            for keyword in keywords:
                if keyword in clean_text.lower():
                    vaccine_related = True
                    break
            if vaccine_related == False:
                continue
            tweet_id = data_json['id_str']
            tweet_time = data_json['created_at']
            user = data_json['user']['screen_name']
            user_id = data_json['user']['id']
            followers_count = data_json['user']['followers_count']
            favourites_count = data_json['user']['favourites_count']
            friends_count = data_json['user']['friends_count']
            statuses_count = data_json['user']['statuses_count']
            retweet_count = data_json['retweet_count']
            favorite_count = data_json['favorite_count']
            retweet_yes = False if data_json['retweeted'] == False else True
            quote_yes = False if data_json['is_quote_status'] == False else True
            reply_yes = False if data_json['in_reply_to_status_id'] == None else True 
            newrow = [user, text, clean_text, tweet_id, tweet_time, user_id,
                    followers_count, favourites_count, friends_count, statuses_count,
                    retweet_count, favorite_count, retweet_yes, quote_yes, reply_yes]
            writer.writerow(newrow)
    
if __name__ == '__main__':
    month_index = int(sys.argv[1])
    input_file = 'tweets_ca_v_en_%d.txt' % month_index
    output_file = 'ca_clean_v_influence_%d.csv' % month_index
    
    texts = get_texts(input_file, output_file)




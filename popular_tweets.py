import csv
import sys

def show(input_file_prefix, input_file_nums):
    reply_cnt = 0
    retweet_cnt = 0
    quote_cnt = 0
    reply_quote_cnt = 0
    orig_cnt = 0
    total_cnt = 0
    output_file = 'orig_sort_favorite.csv'
    with open(output_file, 'w') as wf:
        writer = None
        begin = True
        tweets_list = []
        for input_file_num in input_file_nums:
            input_file = input_file_prefix + str(input_file_num) + '.csv'
            print(input_file)
            with open(input_file, 'r') as rf:
                reader = list(csv.DictReader(rf))
                header = reader[0].keys()
                if begin:
                    writer = csv.DictWriter(wf, fieldnames=header)
                    writer.writeheader()
                    begin = False
                tweets_list.extend(reader)
        sorted_list = sorted(tweets_list, key=lambda x:int(x['retweet_count']), reverse=True)
                
        for row in sorted_list:
            total_cnt += 1
            if row['quote_yes'] == 'True':
                if row['reply_yes'] == 'True':
                    reply_quote_cnt += 1
                quote_cnt += 1
                continue
            if row['reply_yes'] == 'True':
                reply_cnt += 1
                continue
            if row['retweet_yes'] == 'True':
                retweet_cnt += 1
                continue
            print(row)
            #print(row['retweet_count'], row['favorite_count'])
            writer.writerow(row)
            orig_cnt += 1
        print('reply: %d, retweet: %d, quote: %d, reply+quote: %d, orig: %d, total: %d'%(reply_cnt, retweet_cnt, quote_cnt, reply_quote_cnt, orig_cnt, total_cnt))

if __name__ == '__main__':
    input_file_prefix = 'ca_clean_v_influence_'
    input_file_nums = [0, 1, 2, 3, 4, 5]
    show(input_file_prefix, input_file_nums)

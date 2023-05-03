import json
import textPreprocessing


def main():
    preprocessor = textPreprocessing.TextPreprocess()

    mention_sent_dict = {}
    with open('bc5cdr_mention_sent.json', 'r') as f:
        mention_sent_dict = json.load(f)

    wrong_mention_lst = []
    with open('bc5cdr_wrong_mention.txt', 'r') as f:
        for line in f:
            wrong_mention_lst.append(line.strip())

    keys = list(mention_sent_dict.keys())
    with open('bc5cdr_test_keys.txt', 'w') as fh:
        for k in keys:
            fh.write(f'{k}\n')
    
    processed_keys_to_original_keys = {}
    for wr_mention in wrong_mention_lst:
        for k in keys:
            if preprocessor.run(wr_mention) == preprocessor.run(k):
                processed_keys_to_original_keys[wr_mention] = k 

    
    # print(len(wrong_mention_lst), len(mention_sent_dict))
    with open('wrong_mention_and_sentence.txt', 'w') as fh:
        for wr_mention in list(set(wrong_mention_lst)):
            fh.write(f'{wr_mention}\n')
            if wr_mention not in processed_keys_to_original_keys or processed_keys_to_original_keys[wr_mention] not in mention_sent_dict:
                continue
            for sent in mention_sent_dict[processed_keys_to_original_keys[wr_mention]]:
                fh.write(f'\t- {sent}\n')

    





if __name__ == '__main__':
    main()

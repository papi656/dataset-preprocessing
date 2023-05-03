import spacy 
import os
import argparse
import textPreprocessing



#___________Approach 3 - Comparing text rather than position________


def convert_dataset_to_BIO_format(nlp, tokenizer, preprocessor, dataset, processed_file_path, is_medmention=False, pmid_file_path=""):
    # delete output file if it exists (needed as append used while writing to file)
    if os.path.exists(processed_file_path):
        os.remove(processed_file_path)
        print(f'{processed_file_path} was removed.')
    given_mentions = []
    sentence = []
    tokenized_sent = []
    tokenized_token = []
    bio_tags = []
    curr_pmid = ""
    pmid_lst = []
    if is_medmention:
        with open(pmid_file_path, 'r') as fh:
            for line in fh:
                pmid_lst.append(line.strip())

    with open(dataset, 'r') as fh:
        for line in fh:            
            #line containing title(t) and abstract(a)
            if '\t' not in line and '|' in line:
                parts = line.split('|')
                curr_pmid = parts[0].strip()
                if len(parts[-1]) > 0:
                    sentence.append(parts[-1].rstrip('\n'))

            # lines containing mentions
            # given_mentions has all mentions for a t+a combine
            if '\t' in line:
                parts = line.split('\t')
                if len(parts) <= 4:
                    continue
                tmp_str = ""
                for i in range(3,len(parts)-2):
                    if tmp_str == "":
                        tmp_str += parts[i]
                    else:
                        tmp_str = tmp_str + ' ' + parts[i]
                given_mentions.append(tmp_str)
            
            # when one t+a finished reading
            if len(line.strip()) == 0:
                if is_medmention and curr_pmid not in pmid_lst:
                    given_mentions = []
                    sentence = []
                    tokenized_sent = []
                    tokenized_token = []
                    bio_tags = []
                if len(sentence) == 0:
                    continue
                for s in sentence:
                    doc = nlp(s)
                    for x in doc.sents:
                        tokenized_sent.append(str(x))
                        # if len(x) != 0:
                        #     tokenized_sent.append("")
                

                #tokenizing sentences
                for sent in tokenized_sent:
                    if len(sent.strip()) == 0:
                        tokenized_token.append(sent)
                        continue 

                    temp = tokenizer(sent)

                    for x in temp:
                        tokenized_token.append(str(x).strip())
                    tokenized_token.append("") # to signify end of a sentence

                #Adding BIO tokens
                i = 0
                for mention in given_mentions:
                    splited_mention = mention.split()
                    m_len = 0
                    for s_m in splited_mention:
                        m_len += len(s_m)
                    # print(m_len)
                    while i < len(tokenized_token):
                        token_to_match = ""
                        itr = -1
                        our_len = 0
                        steps_count = 0
                        while our_len < m_len:
                            if len(tokenized_token[i]) > 0 and len(mention) > 0 and preprocessor.run(tokenized_token[i][0].strip()) != preprocessor.run(mention[0].strip()):
                                break
                            if i + itr >= len(tokenized_token):
                                break
                            steps_count += 1
                            itr += 1
                            if token_to_match == "":
                                token_to_match = tokenized_token[i].strip()
                                our_len += len(tokenized_token[i].strip())
                            elif i+itr < len(tokenized_token):
                                token_to_match = token_to_match + ' ' + tokenized_token[i+itr].strip()
                                our_len += len(tokenized_token[i+itr].strip())

                        if preprocessor.run(token_to_match) == preprocessor.run(mention.strip()):
                            bio_tags.append('B')
                            for itr in range(steps_count-1):
                                bio_tags.append('I')
                            i += steps_count
                            break
                        elif len(str(tokenized_token[i]).strip()) == 0:
                            bio_tags.append('X')
                            i += 1 
                        else:
                            bio_tags.append('O')
                            i += 1

                while i < len(tokenized_token):
                    bio_tags.append('O')
                    i += 1

                with open(processed_file_path, 'a') as fh:
                    for token, tag in zip(tokenized_token, bio_tags):
                        if token.strip('\n') == "" or tag == 'X':
                            fh.write("\n")
                        else:
                            # fh.write("{}\t{}\n".format(token, tag))
                            fh.write(f'{token}\t{tag}\n')

                given_mentions = []
                sentence = []
                tokenized_sent = []
                tokenized_token = []
                bio_tags = []
            

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', type=str, required=True)
    parser.add_argument('--pmid_file', type=str, required=False)#____used for MedMentions_____
    parser.add_argument('--processed_file_path', type=str, required=True)

    args = parser.parse_args()

    #tokenizer for tokenizing the dataset
    nlp = spacy.load('en_core_web_trf')
    tokenizer = nlp.tokenizer

    #for preprocessing the text
    preprocessor = textPreprocessing.TextPreprocess()

    convert_dataset_to_BIO_format(nlp, tokenizer, preprocessor, args.dataset, args.processed_file_path)

if __name__ == '__main__':
    main()



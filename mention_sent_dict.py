import spacy
import json

def generate_mention_sent_dict(nlp, dataset, output_file):
    word_sent_dict = {}
    sent_lst = []
    mention_lst = []
    with open(dataset, 'r') as fh:
        for line in fh:
            if '|' in line:
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                para = parts[-1]
                doc = nlp(para)
                for s in doc.sents:
                    sent_lst.append(str(s).strip())
            if '\t' in line:
                parts = line.split('\t')
                if parts[1] == 'CID':
                    continue
                tmp_str = ""
                for i in range(3, len(parts)-2):
                    if tmp_str == "":
                        tmp_str += parts[i]
                    else:
                        tmp_str = tmp_str + ' ' + parts[i]
                mention_lst.append(str(tmp_str).strip())
            if len(line.strip('\n')) == 0:
                if len(sent_lst) == 0:
                    continue 
                for m in mention_lst:
                    for i in range(len(sent_lst)):
                        if m in sent_lst[i]:
                            # print(f'{m} - {i}')
                            if m not in word_sent_dict:
                                word_sent_dict[m] = []
                                word_sent_dict[m].append(sent_lst[i])
                            else:
                                tmp_lst = word_sent_dict[m]
                                j = 0
                                for seen_sent in tmp_lst:
                                    if sent_lst[i] == seen_sent:
                                        j += 1
                                if j == 0:
                                    word_sent_dict[m].append(sent_lst[i])
                sent_lst = []
                mention_lst = []

    with open(output_file, 'w') as f:
        json.dump(word_sent_dict, f)

def main():
    nlp = spacy.load('en_core_web_trf')
                
    generate_mention_sent_dict(nlp, 'datasets/NCBI_disease/NCBItestset_corpus.txt', 'ncbi_mention_sent.json')
    generate_mention_sent_dict(nlp, 'datasets/BC5CDR/CDR.Corpus.v010516/CDR_TestSet.PubTator.txt', 'bc5cdr_mention_sent.json')



if __name__ == '__main__':
    main()
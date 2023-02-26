import argparse 


def create_mention_cui_dictionary(dataset, pmid_file, mention_dict_path, cui_dict_path):

    #training_pmids used for Medmentions
    training_pmids = []
    if pmid_file is not None:
        with open(pmid_file, 'r') as fh:
            for line in fh:
                training_pmids.append(line.rstrip())

    mentions = set()
    cuis = set()
    with open(dataset, 'r') as fh:
        for line in fh:
            if '\t' in line:
                entities = line.split('\t')
                cuis_lst = []
                if '|' in entities[-1]:
                    cuis_lst = entities[-1].split('|')
                if '+' in entities[-1]:
                    cuis_lst = entities[-1].split('+')
                if len(cuis_lst) == 0:
                    cuis_lst = [entities[-1]]
                if len(training_pmids) == 0:
                    mentions.add(entities[3].rstrip())
                    for c in cuis_lst:
                        c = c.strip()
                        cuis.add(c.rstrip('\n'))
                elif entities[0] in training_pmids:
                    mentions.add(entities[3].rstrip())
                    for c in cuis_lst:
                        c = c.strip()
                        cuis.add(c.rstrip('\n'))
    
    #writing mention_dict
    with open(mention_dict_path, 'w') as fh:
        for mention in mentions:
            fh.write(mention)
            fh.write('\n')
    #writing cui_dict
    with open(cui_dict_path, 'w') as fh:
        for cui in cuis:
            fh.write(cui)
            fh.write('\n')



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', type=str, required=True)
    parser.add_argument('--pmid_file', type=str, required=False)
    parser.add_argument('--mention_dict_path', type=str, required=True)
    parser.add_argument('--cui_dict_path', type=str, required=True)

    args = parser.parse_args()

    if args.pmid_file is not None:
        create_mention_cui_dictionary(args.dataset, args.pmid_file, args.mention_dict_path, args.cui_dict_path)
    else:
        create_mention_cui_dictionary(args.dataset, None, args.mention_dict_path, args.cui_dict_path)


if __name__ == '__main__':
    main()
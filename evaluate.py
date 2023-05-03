import argparse 
from tqdm import tqdm 


def get_single_cuis(cuis):
    if type(cuis) == str: cuis = [cuis]
    elif type(cuis) == list: cuis = cuis

    cui_list = []
    for cc in cuis:
        if '|' in cc:
            cs = cc.split('|')
            for c in cs:
                cui_list.append(c)
        elif '+' in cc:  # For NCBI
            cs = cc.split('+')
            for c in cs:
                cui_list.append(c)
        else:
            cui_list.append(cc)
    return cui_list


def update(spl, entity_str, index_tmp, num_mem, num_syn, num_con, mention_dictionary, cui_dictionary, test_splits, cuis):
    if spl == 'Mem':
        if entity_str in mention_dictionary:
            num_mem += 1
        else:
            for j in index_tmp:
                test_splits[spl][j] = 'O'
    elif spl == 'Syn':
        if entity_str not in mention_dictionary and sum([1 if c in cui_dictionary else 0 for c in get_single_cuis(cuis[index_tmp[0]])]) > 0:
            num_syn += 1
        else:
            for j in index_tmp:
                test_splits[spl][j] = 'O'
    elif spl == 'Con':
        if entity_str not in mention_dictionary and sum([1 if c in cui_dictionary else 0 for c in get_single_cuis(cuis[index_tmp[0]])]) == 0:
            num_con += 1
        else:
            for j in index_tmp:
                test_splits[spl][j] = 'O'
    else:
        raise ValueError("Invalid name: {}.".format(spl))

    return num_mem, num_syn, num_con, test_splits


def partition(mention_dictionary, cui_dictionary, test_splits, tokens, cuis):
    num_mem = num_syn = num_con = 0
    for spl in list(test_splits.keys()):
        if spl == 'Overall':
            continue

        entity_tmp = []
        index_tmp = []
        inside_entity = False 
        i = -1
        for pred in tqdm(test_splits[spl]):
            i += 1

            if pred[0] == 'B':
                if inside_entity:
                    assert cuis[index_tmp[0]] != '-'
                    entity_str = ' '.join(entity_tmp)
                    num_mem, num_syn, num_con, test_splits = update(spl, entity_str, index_tmp, num_mem, num_syn, num_con, mention_dictionary, cui_dictionary, test_splits, cuis)
                    
                    #init
                    inside_entity = False
                    entity_tmp = []
                    index_tmp = []

                    inside_entity = True
                    entity_tmp.append(tokens[i])
                    index_tmp.append(i)
                else:
                    inside_entity = True 
                    entity_tmp.append(tokens[i])
                    index_tmp.append(i)
            elif pred[0] == 'I':
                inside_entity = True 
                entity_tmp.append(tokens[i])
                index_tmp.append(i)
            elif pred[0] == 'O':
                if inside_entity:
                    assert cuis[index_tmp[0]] != '-'
                    entity_str = ' '.join(entity_tmp)
                    num_mem, num_syn, num_con, test_splits = update(spl, entity_str, index_tmp, num_mem, num_syn, num_con, mention_dictionary, cui_dictionary, test_splits, cuis)

                    #init
                    inside_entity = False
                    entity_tmp = []
                    index_tmp = []

    print("Splits | Mem: {}, Syn: {}, Con: {}.".format(num_mem, num_syn, num_con))
    return test_splits

def print_score(SPLITS, test_splits, predictions):
    print("\n--Evaluation--")
    

def main():
    """
    TODO - cite the paper
    Code taken from IEEE Access - How BioNER model generalize
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--mention_dictionary', type=str, required=True)
    parser.add_argument('--cui_dictionary', type=str, required=True)
    parser.add_argument('--gold_labels', type=str, required=True)
    parser.add_argument('--gold_cuis', type=str, required=True)
    parser.add_argument('--predictions', type=str, required=True)

    args = parser.parse_args()

    #______TODO - Preprocess text (punctuation, capitialization)________


    #load dictionaries
    with open(args.mention_dictionary) as g:
        mention_dictionary = [line.rstrip('\n') for line in g.readlines()]
    with open(args.cui_dictionary) as g:
        cui_dictionary = [line.rstrip('\n') for line in g.readlines()]

    print(len(mention_dictionary), len(set(mention_dictionary)))

    # Load model predictions
    f = open(args.predictions)
    preds = f.readlines()

    # Load test data
    g = open(args.gold_labels)
    gold_labels = g.readlines()
    g = open(args.gold_cuis)
    gold_cuis = g.readlines()

    # Initialize
    SPLITS = ['Overall', 'Mem', 'Syn', 'Con']
    test_splits = {}
    for l in SPLITS:
        test_splits[l] = []

    predictions = []
    tokens = []
    cuis = []
    for i, (pred, label) in enumerate(zip(preds, gold_labels)):
        if not pred.split(): continue # empty line

        p_token = pred.split()[0]
        p_label = pred.split()[1]
        l_token = label.split()[0]
        c_token = gold_cuis[i].split()[0]
        assert p_token == l_token 
        assert c_token == l_token

        l_label = label.split()[1]

        # seqeval framework requires entity types for entity-level NER evaluation
        #Medmentions has 128 entity types. But initially we assing 'MISC' to all annotations
        if p_label == 'B' or p_label == 'I':
            p_label = p_label + '-MISC'
        if l_label == 'B' or l_label == 'I':
            l_label = l_label + '-MISC'

        cuis.append(gold_cuis[i].split()[1])
        predictions.append(p_label)
        tokens.append(p_token)
        for spl in SPLITS:
            test_splits[spl].append(l_label)

    #partition benchmarks
    test_splits = partition(mention_dictionary, cui_dictionary, test_splits, tokens, cuis)

    #Evaluation
    print_score(SPLITS, test_splits, predictions)

if __name__ == '__main__':
    main()
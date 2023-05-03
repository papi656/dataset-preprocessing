import pandas as pd
import csv 


def main():
    gold_data = pd.read_csv('resources/BC5CDR/test.tsv', sep='\t', quoting=csv.QUOTE_NONE, names=["Tokens", "Labels"], skip_blank_lines=False)
    
    gold_tokens = []
    gold_labels = []
    for ind, row in gold_data.iterrows():
        gold_tokens.append(str(row['Tokens']))
        gold_labels.append(str(row['Labels']))
    # gold_tokens = gold_data['Tokens'].tolist()
    # gold_labels = gold_data['Labels'].tolist()

    pred_tokens = []
    pred_labels = []
    with open('resources/BC5CDR/test_predictions.txt', 'r') as fh:
        for line in fh:
            parts = line.split(' ')
            pred_tokens.append(str(parts[0]).strip())
            pred_labels.append(str(parts[-1]).strip())

    for i in range(10):
        print(pred_labels[i])
    print(len(gold_labels), len(pred_labels), len(gold_tokens), len(pred_tokens))
    
    wrong_mention_lst = []
    wrong_other_lst = []
    current_mention = ""
    store = False
    for p_token, p_label, g_token, g_label in zip(pred_tokens, pred_labels, gold_tokens, gold_labels):
        if len(p_label.strip()) == 0:
            continue
        try:
            assert p_token == g_token
        except AssertionError:
            print(f'{p_token} - {g_token}')
        if g_label == 'B':
            if store and len(current_mention) > 0:
                wrong_mention_lst.append(current_mention)
                store = False
            current_mention = ""
            current_mention = g_token
        elif g_label == 'I':
            current_mention = current_mention + ' ' + g_token
        else:
            if store and len(current_mention) > 0:
                wrong_mention_lst.append(current_mention)
                store = False
            current_mention = ""

        if p_label != g_label:
            if g_label == 'O':
                wrong_other_lst.append(p_token)
            else:
                store = True

    
    if len(wrong_mention_lst) > 0:
        with open("bc5cdr_wrong_mention.txt", 'w') as fh:
            for m in wrong_mention_lst:
                fh.write(f'{m}\n')

    if len(wrong_other_lst) > 0:
        with open("b5cdr_wrong_other.txt", 'w') as fh:
            for o in wrong_other_lst:
                fh.write(f'{o}\n')

        
        


if __name__ == '__main__':
    main()
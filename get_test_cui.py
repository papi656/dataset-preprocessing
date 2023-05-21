import argparse


def get_test_cui(dataset_path, test_data_path, processed_file_path, pmid_file=""):
    # get the list of cuis in the datas0et
    pmid_lst = []
    # print(type(pmid_file))
    if pmid_file != 'empty':
        with open(pmid_file, 'r') as f:
            for line in f:
                pmid_lst.append(line.strip())
    #BC5CDR has CID in mention list, ignore it.
    cuis_list = []
    with open(dataset_path, 'r') as fh:
        for line in fh:
            #lines containing mentions
            if '\t' in line:
                parts = line.split('\t')
                if len(pmid_lst) > 0:
                    if parts[0].strip() in pmid_lst:
                        cuis_list.append(parts[5].strip())
                elif len(parts) > 4:
                    cuis_list.append(parts[5].strip())

    token_lst, label_lst = [], []
    with open(test_data_path, 'r') as fh:
        for line in fh:
            if len(line.strip()) == 0:
                token_lst.append("")
                label_lst.append("")
                continue
            parts = line.split('\t')
            token_lst.append(parts[0].strip())
            label_lst.append(parts[1].strip())

    print(label_lst.count('B'), len(cuis_list))

    # with open('test_labels.txt','w') as fh:
    #     for x in label_lst:
    #         fh.write(f'{x}\n')
    fname = 'test_cuis_' + dataset_path[-10:] + '.txt'
    with open(fname, 'w') as fh:
        for c in cuis_list:
            fh.write(f'{c}\n')
    
    # assert label_lst.count('B') == len(cuis_list), 'Number of mentions not equal to number of CUIs.'

    with open(processed_file_path, 'w') as fh:
        i = 0
        for token, label in zip(token_lst, label_lst):
            if len(token) == 0:
                fh.write('\n')
            elif label == 'B':
                fh.write(f'{token}\t{cuis_list[i]}\n')
                i += 1
            else:
                fh.write(f'{token}\t-\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', type=str, required=True)
    parser.add_argument('--test_data_path', type=str, required=True)
    parser.add_argument('--pmid_file', type=str, required=True)
    parser.add_argument('--processed_file_path', type=str, required=True)

    args = parser.parse_args()
    
    get_test_cui(args.dataset_path, args.test_data_path, args.processed_file_path, args.pmid_file)


if __name__ == '__main__':
    main()
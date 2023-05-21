echo "Creating test_cui.txt for MedMentions."

python3 get_test_cui.py \
    --dataset_path datasets/MedMentions/full/data/corpus_pubtator.txt \
    --test_data_path resources/MedMentions/test.txt \
    --pmid_file datasets/MedMentions/full/data/corpus_pubtator_pmids_test.txt \
    --processed_file_path resources/MedMentions/test_cuis.txt

echo "Creating test_cui.txt for BC5CDR"

python3 get_test_cui.py \
    --dataset_path datasets/BC5CDR/CDR.Corpus.v010516/CDR_TestSet.PubTator.txt \
    --test_data_path resources/BC5CDR/test.txt \
    --pmid_file  empty \
    --processed_file_path resources/BC5CDR/test_cuis.txt

echo "Creating test_cui.txt for NCBI-disease"

python3 get_test_cui.py \
    --dataset_path datasets/NCBI_disease/NCBItestset_corpus.txt \
    --test_data_path resources/NCBI_disease/test.txt \
    --pmid_file  empty \
    --processed_file_path resources/NCBI_disease/test_cuis.txt
if [ ! -d resources/ ];
then
    mkdir resources 
fi 

if [ ! -d resources/MedMentions ];
then 
    mkdir resources/MedMentions 
fi 

echo "Creating dicts for MedMentions."
python3 get_dict.py \
    --dataset datasets/MedMentions/full/data/corpus_pubtator.txt \
    --pmid_file datasets/MedMentions/full/data/corpus_pubtator_pmids_trng.txt \
    --mention_dict_path resources/MedMentions/mention_dict.txt \
    --cui_dict_path resources/MedMentions/cui_dict.txt 


if [ ! -d resources/NCBI_disease ];
then
    mkdir resources/NCBI_disease
fi 

echo "Creating dicts for NCBI-disease"

python3 get_dict.py \
    --dataset datasets/NCBI_disease/NCBItrainset_corpus.txt \
    --mention_dict_path resources/NCBI_disease/mention_dict.txt \
    --cui_dict_path resources/NCBI_disease/cui_dict.txt 


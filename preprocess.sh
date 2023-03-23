if [ ! -d resources/ ];
then
    mkdir resources 
fi 

# if [ ! -d resources/MedMentions ];
# then 
#     mkdir resources/MedMentions 
# fi 

# echo "Creating dicts for MedMentions."
# python3 get_dict.py \
#     --dataset datasets/MedMentions/full/data/corpus_pubtator.txt \
#     --pmid_file datasets/MedMentions/full/data/corpus_pubtator_pmids_trng.txt \
#     --mention_dict_path resources/MedMentions/mention_dict.txt \
#     --cui_dict_path resources/MedMentions/cui_dict.txt 


if [ ! -d resources/NCBI_disease ];
then
    mkdir resources/NCBI_disease
fi 

echo "Creating dicts for NCBI-disease"

python3 get_dict.py \
    --dataset datasets/NCBI_disease/NCBItrainset_corpus.txt \
    --mention_dict_path resources/NCBI_disease/mention_dict.txt \
    --cui_dict_path resources/NCBI_disease/cui_dict.txt 

echo "Converting NCBI dataset to BIO tag format:"

python3 preprocess.py \
    --dataset datasets/NCBI_disease/NCBItrainset_corpus.txt \
    --processed_file_path resources/NCBI_disease/train.txt 

echo " - Training set done"

python3 preprocess.py \
    --dataset datasets/NCBI_disease/NCBIdevelopset_corpus.txt \
    --processed_file_path resources/NCBI_disease/devel.txt 

echo " - Development set done"

python3 preprocess.py \
    --dataset datasets/NCBI_disease/NCBItestset_corpus.txt \
    --processed_file_path resources/NCBI_disease/test.txt 

echo " - Test set done"

if [ ! -d resources/BC5CDR ];
then
    mkdir resources/BC5CDR
fi 

echo "Creating dicts for BC5CDR"

python3 get_dict.py \
    --dataset datasets/BC5CDR/CDR.Corpus.v010516/CDR_TrainingSet.PubTator.txt \
    --mention_dict_path resources/BC5CDR/mention_dict.txt \
    --cui_dict_path resources/BC5CDR/cui_dict.txt 

echo "Converting BC5CDR dataset to BIO tag format"

python3 preprocess.py \
    --dataset datasets/BC5CDR/CDR.Corpus.v010516/CDR_TrainingSet.PubTator.txt \
    --processed_file_path resources/BC5CDR/train.txt 

echo " - Training set done"

python3 preprocess.py \
    --dataset datasets/BC5CDR/CDR.Corpus.v010516/CDR_DevelopmentSet.PubTator.txt \
    --processed_file_path resources/BC5CDR/devel.txt 

echo " - Development set done"

python3 preprocess.py \
    --dataset datasets/BC5CDR/CDR.Corpus.v010516/CDR_TestSet.PubTator.txt \
    --processed_file_path resources/BC5CDR/test.txt 

echo " - Test set done"
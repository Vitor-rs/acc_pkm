---
title: Portuguese named entity recognition using BERT-CRF
citekey: Souza2019
authors:
- Fábio Souza
- Rodrigo Nogueira
- Roberto Lotufo
year: 2019
date: '2019'
item_type: preprint
doi: 10.48550/ARXIV.1909.10649
url: https://arxiv.org/abs/1909.10649
zotero_key: D82QAK2H
collections:
- SA9KZ2CI
tags:
- Computer Science - Information Retrieval
- Computer Science - Computation and Language
- Computer Science - Machine Learning
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: portuguese named entity recognition using bert-crf.pdf
synced_at: '2026-09-29T18:03:02.253047'
---

# Portuguese named entity recognition using BERT-CRF

**Autores:** Fábio Souza, Rodrigo Nogueira, Roberto Lotufo
**DOI:** [10.48550/ARXIV.1909.10649](https://doi.org/10.48550/ARXIV.1909.10649)
**URL:** https://arxiv.org/abs/1909.10649

## 📄 Conteúdo Completo do Documento

# **Portuguese Named Entity Recognition using BERT-CRF** 

## **F´abio Souza**<sup>1,3</sup> **, Rodrigo Nogueira**<sup>2</sup> **, Roberto Lotufo**<sup>1,3</sup> 

1University of Campinas 

f116735@dac.unicamp.br, lotufo@dca.fee.unicamp.br 

2New York University 

rodrigonogueira@nyu.edu 

3NeuralMind Inteligˆencia Artificial 

_{_ fabiosouza, roberto _}_ @neuralmind.ai 

## **Abstract** 

Recent advances in language representation using neural networks have made it viable to transfer the learned internal states of a trained model to downstream natural language processing tasks, such as named entity recognition (NER) and question answering. It has been shown that the leverage of pre-trained language models improves the overall performance on many tasks and is highly beneficial when labeled data is scarce. In this work, we train Portuguese BERT models and employ a BERT-CRF architecture to the NER task on the Portuguese language, combining the transfer capabilities of BERT with the structured predictions of CRF. We explore feature-based and fine-tuning training strategies for the BERT model. Our fine-tuning approach obtains new state-of-the-art results on the HAREM I dataset, improving the F1-score by 1 point on the selective scenario (5 NE classes) and by 4 points on the total scenario (10 NE classes). 

## **1 Introduction** 

Named entity recognition (NER) is the task of identifying text spans that mention named entities (NEs) and classifying them into predefined categories, such as person, organization, location, or any other classes of interest. Despite being conceptually simple, NER is not an easy task. The category of a named entity is highly dependent on textual semantics and its surrounding context. Moreover, there are many definitions of named entity and evaluation criteria, introducing evaluation complications (Marrero et al., 2013). 

Current state-of-the-art NER systems employ neural architectures that have been pre-trained on language modeling tasks. Examples of such models are ELMo (Peters et al., 2018), OpenAI GPT (Radford et al., 2018), BERT (Devlin et al., 2018), XL- 

Net (Yang et al., 2019), RoBERTa (Liu et al., 2019), Albert (Lan et al., 2019) and T5 (Raffel et al., 2019). It has been shown that language modeling pretraining significantly improves the performance of many natural language processing tasks and also reduces the amount of labeled data needed for supervised learning (Howard and Ruder, 2018; Peters et al., 2018). 

Applying these recent techniques to the Portuguese language can be highly valuable, given that annotated resources are scarce, but unlabeled text data is abundant. In this work, we assess several neural architectures using BERT (Bidirectional Encoder Representation from Transformers) models to the NER task in Portuguese and compare feature-based and fine-tuning based training strategies. This is the first work to employ BERT models to the NER task in Portuguese. We also discuss the main complications that we face when on existing datasets. With that in mind, we aim to facilitate the reproducibility of this work by making our implementation and models publicly available.<sup>12</sup> 

## **2 Related Work** 

NER systems can be based on handcrafted rules or machine learning approaches. For the Portuguese language, previous works explored machine learning techniques and a few ones applied neural networks models. do Amaral and Vieira (2014) created a CRF model using 15 features extracted from the central and surrounding words. (Pirovani and Oliveira, 2018) combined a CRF model with Local Grammars, following a similar approach. 

Starting with Collobert et al. (2011), neural network NER systems have become popular due to the 

> 1Code will be available at https:// gist.github.com/fabiocapsouza/ 62c98576d1c826894be2b3ae0993ef53. 

> 2BERT models available at https://github.com/ neuralmind-ai/portuguese-bert. 



Figure 1: Illustration of the proposed method. Given an input document, the text is tokenized using WordPiece (Wu et al., 2016) and the tokenized document is split into overlapping spans of the maximum length using a defined stride (with a stride of 3 in the example). Maximum context tokens of each span are marked in bold. The spans are fed into BERT and then into the classification layer, producing a sequence of tag scores for each span. The sub-token entries (starting with ##) are removed from the spans and the remaining tokens are passed to the CRF layer. The maximum context tokens are selected and concatenated to form the final predicted tags. 

minimal feature engineering requirements, which contributes to a higher domain independence (Yadav and Bethard, 2018). The CharWNN model (Santos and Guimaraes, 2015) extended the work of Collobert et al. (2011) by employing a convolutional layer to extract character-level features from each word. These features were concatenated with pre-trained word embeddings and then used to perform sequential classification. 

The CharWNN model (Santos and Guimaraes, 2015) extended the work of Collobert et al. (2011) by employing a convolutional layer to extract character-level features from each word. The LSTM-CRF architecture (Lample et al., 2016) has been commonly used in NER task (Castro et al., 2018; de Araujo et al., 2018; Fernandes et al., 2018). The model is composed of two bidirectional LSTM networks that extract and combine character-level and word-level features. A sequential classification is then performed by the CRF layer. 

Recent works explored contextual embeddings extracted from language models in conjunction with the LSTM-CRF architecture. Santos et al. (2019b,a) employ Flair Embeddings (Akbik et al., 2018) to extract contextual word embeddings from a bidirectional character-level LM trained on Portuguese corpora. These embeddings are concatenated with pre-trained word embeddings and fed to a BiLSTM-CRF model. Castro et al. (2019) uses ELMo embeddings that are a combination of character-level features extracted by convolutional 

neural networks and the hidden states of each layer of a bidirectional LM (biLM) composed of a BiLSTM model. 

## **3 Model** 

In this section we describe the model architecture and the training and evaluation procedures for NER. 

### **3.1 BERT-CRF for NER** 

The model architecture is composed of a BERT model with a token-level classifier on top followed by a Linear-Chain CRF. For an input sequence of _n_ tokens, BERT outputs an encoded token sequence with hidden dimension _H_ . The classification model projects each token’s encoded representation to the tag space, i.e. R<sup>_H_</sup> _�→_ R<sup>_K_</sup> , where _K_ is the number of tags and depends on the the number of classes and on the tagging scheme. The output scores **P** _∈_ R<sup>_n×K_</sup> of the classification model are then fed to the CRF layer, whose parameters are a matrix of tag transitions **A** _∈_ R<sup>_K_+2</sup><sup>_×K_+2</sup> . The matrix **A** is such that _Ai,j_ represents the score of transitioning from tag _i_ to tag _j_ . **A** includes 2 additional states: start and end of sequence. 

As described by Lample et al. (2016), for an input sequence **X** = ( **x** 1 _, ...,_ **x** _n_ ) and a sequence of tag predictions **y** = ( _y_ 1 _, ..., yn_ ) _, yi ∈{_ 1 _, ..., K}_ , the score of the sequence is defined as 



where _y_ 0 and _yn_ +1 are start and end tags. The model is trained to maximize the log-probability of the correct tag sequence: 



where **YX** are all possible tag sequences. The summation in Eq. 1 is computed using dynamic programming. During evaluation, the most likely sequence is obtained by Viterbi decoding. Following Devlin et al. (2018), we compute predictions and losses only for the first sub-token of each token. 

### **3.2 Feature-based and Fine-tuning approaches** 

We experiment with two transfer learning approaches: _feature-based_ and _fine-tuning_ . For the feature-based approach, the BERT model weights are kept frozen and only the classifier model and CRF layer are trained. The classifier model consists of a 1-layer BiLSTM with hidden size _dLSTM_ followed by a Linear layer. Instead of using only the last hidden representation layer of BERT, we sum the last 4 layers, following Devlin et al. (2018). The resulting architecture resembles the LSTMCRF model Lample et al. (2016) but with BERT embeddings. 

For the fine-tuning approach, the classifier is a linear layer and all weights, including BERT’s, are updated jointly during training. For both approaches, models without the CRF layer are also evaluated. In this case, they are optimized by minimizing the cross entropy loss. 

### **3.3 Document context and max context evaluation** 

To take advantage of longer contexts when computing the token representations from BERT, we use document context for input examples instead of sentence context. Following the approach of Devlin et al. (2018) on the SQuAD dataset, examples longer than _S_ tokens are broken into spans of length up to _S_ using a stride of _D_ tokens. Each span is used as a separate example during training. During evaluation, however, a single token _Ti_ can be present in _N_ = _D_<sup>_<u>S</u>_multiple spans</sup><sup>_sj_, and so may</sup> have up to _N_ distinct tag predictions _yi,j_ . Each token’s final prediction is taken from the span where the token is closer to the central position, that is, the span where it has the most contextual information. 

Figure 1 illustrates the evaluation procedure. 

## **4 Experiments** 

In this section, we present the experimental setups for BERT pre-trainings and NER training. We present the datasets that are used, the training setups and hyperparameters. 

### **4.1 BERT pre-trainings** 

We train Portuguese BERT models for the two model sizes defined in Devlin et al. (2018): BERT Base and BERT Large. The maximum sentence length is set to _S_ = 512 tokens. We train cased models only since capitalization is relevant for NER (Castro et al., 2018). 

### **4.1.1 Vocabulary generation** 

A cased Portuguese vocabulary of 30k subword units is generated using SentencePiece (Kudo and Richardson, 2018) with the BPE algorithm and 200k random Portuguese Wikipedia articles, which is then converted to WordPiece format. Details about SentencePiece to WordPiece conversion can be found in Appendix A.1. 

### **4.1.2 Pre-training data** 

For pre-training data, we use the brWaC corpus (Wagner Filho et al., 2018), which contains 2.68 billion tokens from 3.53 million documents and is the largest open Portuguese corpus to date. On top of its size, brWaC is composed of whole documents and its methodology ensures high domain diversity and content quality, which are desirable features for BERT pre-training. 

We use only the document body (ignoring the titles) and we apply a single post-processing step on the data to remove _mojibakes_<sup>3</sup> and remnant HTML tags using the _ftfy_ library (Speer, 2019). The final processed corpus has 17.5GB of raw text. 

### **4.1.3 Pre-training setup** 

The pre-training input sequences are generated with default parameters and use whole work masking (if a word composed of multiple subword units is masked, all of its subword units are masked and have to be predicted in Masked Language Modeling task). The models are trained for 1,000,000 steps. We use a learning rate of 1e-4, learning rate 

> 3Mojibake is a kind of text corruption that occurs when strings are decoded using the incorrect character encoding. For example, the word “codificac¸˜ao” becomes “codificaA<sup>˜</sup> _§_ A<sup>˜</sup> _£_ o” when encoded in UTF-8 and decoded using ISO-8859-1. 

warmup over the first 10,000 steps followed by a linear decay of the learning rate. 

For BERT Base models, the weights are initialized with the checkpoint of Multilingual BERT Base. We use a batch size of 128 and sequences of 512 tokens the entire training. This training takes 4 days on a TPUv3-8 instance and performs about 8 epochs over the training data. 

For BERT Large, the weights are initialized with the checkpoint of English BERT Large. Since it is a bigger model with longer training time, we follow the instructions of Devlin et al. (2018) and use sequences of 128 tokens in batches of size 256 for the first 900,000 steps and then sequences of 512 tokens and batch size 128 for the last 100,000 steps. This training takes 7 days on a TPUv3-8 instance and performs about 6 epochs over the training data. 

Note that in the calculation of the number of epochs, we are taking into consideration a duplication factor of 10 when generating the input examples. This means that under 10 epochs, the same sentence is seen with different masking and sentence pair in each epoch, which effectively is equal to dynamic example generation. 

### **4.2 NER experiments** 

### **4.2.1 NER datasets** 

|**Dataset**|**Documents**|**Tokens**|**Entities**<br>(selective/total)|
|---|---|---|---|
|First HAREM|129|95585|4151 / 5017|
|MiniHAREM|128|64853|3018 / 3642|



Table 1: Dataset and tokenization statistics for the HAREM I corpora. The _Tokens_ column refers to whitespace and punctuation tokenization. The _Entities_ column comprises the two defined scenarios. Popular datasets for training and evaluating Portuguese NER are the HAREM Golden Collections (GC) (Santos et al., 2006; Freitas et al., 2010). We use the GCs of the First HAREM evaluation contests, which is divided in two subsets: First HAREM and MiniHAREM. Each GC contains manually annotated named entities of 10 classes: Location, Person, Organization, Value, Date, Title, Thing, Event, Abstraction and Other. 

Following Santos and Guimaraes (2015) and Castro et al. (2018), we use the First HAREM as training set and MiniHAREM as test set. The experiments are conducted on two scenarios: a Selective scenario, with 5 entity classes (Person, Organization, Location, Value and Date) and a Total scenario, that considers all 10 classes. Table 1 

contains some dataset statistics. 

### **4.2.2 HAREM preprocessing** 

The HAREM datasets were annotated taking into consideration vagueness and indeterminacy in text, such as ambiguity in sentences. This way, some text segments contain _<_ ALT _>_ tags that enclose multiple alternative named entity identification solutions. Additionally, multiple categories may be assigned to a single named entity. 

To model NER as a sequence tagging problem, we must select a single truth for each undetermined segment and/or entity. To resolve each _<_ ALT _>_ tag in the datasets, our approach is to select the alternative that contains the highest number of named entities. In case of ties, the first one is selected. To resolve each named entity that is assigned multiple classes, we simply select the first valid class for the scenario. The dataset preprocessing script is available on GitHub<sup>4</sup> and Appendix A.2 contains an example. 

### **4.2.3 NER experimental setup** 

For NER training, we use 3 distinct BERT models: Multilingual BERT-Base,<sup>5</sup> Portuguese BERT-Base and Portuguese BERT-Large. We use the IOB2 tagging scheme and a stride of _D_ = 128 tokens to split the input examples into spans. 

The model parameters are divided in two groups with different learning rates: 5e-5 for BERT model and 1e-3 for the rest. The numbers of epochs are 100 for BERT-LSTM, 50 for BERT-LSTM-CRF and BERT, and 15 for BERT-CRF. The numbers of epochs are found using a development set comprised of 10% of the First HAREM training set. We use a batch of size 16 and the customized Adam optimizer of Devlin et al. (2018) with weight decay of 0 _._ 01. Similar to pre-training, we use learning rate warmup for the first 10% of steps and linear decay of the learning rate for the remaining steps. 

To deal with class imbalance, we initialize the bias term of the ”O” tag in the linear layer of the classifier with value of 6 in order to promote a better stability in early training (Lin et al., 2017). We also use a weight of 0 _._ 01 for ”O” tag losses when not using a CRF layer. 

For the feature-based approach, we use a biLSTM with 1 layer and hidden dimension of _dLSTM_ = 100 units for each direction. 

> 4https://github.com/fabiocapsouza/harem ~~p~~ reprocessing 

> 5Available at https://github.com/google-research/bert 

|**Ahitt**|**To**|**tal scena**|**rio**|**Selec**|**tive sce**|**nario**|
|---|---|---|---|---|---|---|
|**rcecure**|**Prec.**|**Rec.**|**F1**|**Prec.**|**Rec.**|**F1**|
|CharWNN (Santos and Guimaraes,2015)|67.16|63.74|65.41|73.98|68.68|71.23|
|LSTM-CRF (Castro et al.,2018)|72.78|68.03|70.33|78.26|74.39|76.27|
|BiLSTM-CRF+FlairBBP(Santos et al.,2019a)|74.91|74.37|74.64|83.38|81.17|82.26|
|ML-BERTBASE-LSTM_†_|69.68|69.51|69.59|75.59|77.13|76.35|
|<br>ML-BERTBASE-LSTM-CRF_†_|74.70|69.74|72.14|80.66|75.06|77.76|
|ML-BERTBASE|72.97|73.78|73.37|77.35|79.16|78.25|
|ML-BERTBASE-CRF|74.82|73.49|74.15|80.10|78.78|79.44|
|PT-BERTBASE-LSTM_†_|75.00|73.61|74.30|79.88|80.29|80.09|
|<br>PT-BERTBASE-LSTM-CRF_†_|78.33|73.23|75.69|84.58|78.72|81.66|
|<br>PT-BERTBASE|78.36|77.62|77.98|83.22|82.85|**83.03**|
|PT-BERTBASE-CRF|78.60|76.89|77.73|83.89|81.50|82.68|
|PT-BERTLARGE-LSTM_†_|72.96|72.05|72.50|78.13|78.93|78.53|
|PT-BERTLARGE-LSTM-CRF_†_|77.45|72.43|74.86|83.08|77.83|80.37|
|PT-BERTLARGE|78.45|77.40|77.92|83.45|83.15|**83.30**|
|PT-BERTLARGE-CRF|80.08|77.31|**78.67**|84.82|81.72|**83.24**|



Table 2: Comparison of Precision, Recall and F1-scores results on the test set (MiniHAREM). All metrics are calculated using the CoNLL 2003 evaluation script. **Bold** values indicate SOTA results (multiple results bolded if difference within 95% bootstrap confidence interval). Reported values are the average of multiple runs with different random seeds. _†_ : feature-based approach. 

When evaluating, we produce valid predictions by removing all invalid tag transitions for the IOB2 scheme, such as ”I-” tags coming directly after ”O” tags or after an ”I-” tag of a different class. This post-processing step trades off recall for a possibly higher precision. 

## **5 Results** 

The main results of our experiments are presented in Table 2. We compare the performances of our models on the two scenarios (total and selective). All metrics are computed using CoNLL 2003 evaluation script,<sup>6</sup> that consists of an entity-level micro F1-score considering only exact matches. 

Our proposed Portuguese BERT-CRF model outperforms the previous state-of-the-art (BiLSTMCRF+FlairBBP), improving the F1-score by about 1 point on the selective scenario and by 4 points on the total scenario. Interestingly, Flair embeddings outperforms BERT models on English NER (Akbik et al., 2018). Compared to LSTM-CRF architecure without contextual embeddings, our model outperforms by 8.3 and 7.0 absolute points on F1-score on total and selective scenarios, respectively. 

We also remove the CRF layer to evaluate its contribution. Portuguese BERT (PT-BERT-BASE and PT-BERT-LARGE) also outperforms previous works, even without the enforcement of sequential 

> 6https://www.clips.uantwerpen.be/ conll2002/ner/bin/conlleval.txt 

classification provided by the CRF layer. Models with CRF improves or performs similarly to its simpler variants when comparing the overall F1 scores. We note that in most cases they show higher precision scores but lower recall. 

While Portuguese BERTLARGE models are the highest performers in both scenarios, we observe that they experience performance degradation when used in the feature-based approach, performing worse than their smaller variants but still better than the Multilingual BERT. In addition, it can be seen that BERTLARGE models do not bring much improvement to the selective scenario when compared to BERTBASE models. We hypothesize that it is due to the small size of the NER dataset. 

The models of the feature-based approach perform significantly worse compared to the ones of the fine-tuning approach. The performance gap is found to be much higher than the reported values for NER on English language (Peters et al., 2019). 

The post-processing step of filtering out invalid transitions for the IOB2 scheme increases the F1scores by 1.9 and 1.2 points, on average, for the feature-based and fine-tuning approaches, respectively. This step produces a reduction of 0.4 points in the recall, but boosts the precision by 3.5 points, on average. 

## **6 Conclusion** 

We present a new state-of-the-art on the HAREM I corpora by pre-training Portuguese BERT models on a large corpus of unlabeled text and fine-tuning a BERT-CRF model on the Portuguese NER task. Our proposed model outperforms the previous state of the art (BiLSTM-CRF+FlairBBP), even though it was pre-trained on much less data. Considering the issues regarding preprocessing and dataset decisions that affect evaluation compatibility, we give special attention to reproducibility of our results and we make our code and models publicly available. We hope that by releasing our Portuguese BERT models, others will be able to benchmark and improve the performance of many other NLP tasks in Portuguese. Experiments with more recent and efficient models, such as RoBERTa and T5, are left for future works. 

## **7 Acknowledgements** 

R Lotufo acknowledges the support of the Brazilian government through the CNPq Fellowship ref. 310828/2018-0. 

## **References** 

- Alan Akbik, Duncan Blythe, and Roland Vollgraf. 2018. Contextual string embeddings for sequence labeling. In _COLING 2018, 27th International Conference on Computational Linguistics_ , pages 1638– 1649. 

- Daniela Oliveira F do Amaral and Renata Vieira. 2014. Nerp-crf: A tool for the named entity recognition using conditional random fields. _Linguam´atica_ , 6(1):41–49. 

- Pedro Henrique Luz de Araujo, Te´ofilo E de Campos, Renato RR de Oliveira, Matheus Stauffer, Samuel Couto, and Paulo Bermejo. 2018. Lener-br: A dataset for named entity recognition in brazilian legal text. In _International Conference on Computational Processing of the Portuguese Language_ , pages 313–323. Springer. 

- Pedro Castro, Nadia Felix, and Anderson Soares. 2019. Contextual representations and semi-supervised named entity recognition for portuguese language. 

- Pedro Vitor Quinta de Castro, N´adia F´elix Felipe da Silva, and Anderson da Silva Soares. 2018. Portuguese named entity recognition using lstm-crf. In _Computational Processing of the Portuguese Language_ , pages 83–92, Cham. Springer International Publishing. 

- Ronan Collobert, Jason Weston, L´eon Bottou, Michael Karlen, Koray Kavukcuoglu, and Pavel Kuksa. 

2011. Natural language processing (almost) from scratch. _Journal of machine learning research_ , 12(Aug):2493–2537. 

- Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. Bert: Pre-training of deep bidirectional transformers for language understanding. _Computing Research Repository_ , arXiv:1810.04805. 

- Ivo Fernandes, Henrique Lopes Cardoso, and Eugenio Oliveira. 2018. Applying deep neural networks to named entity recognition in portuguese texts. In _2018 Fifth International Conference on Social Networks Analysis, Management and Security (SNAMS)_ , pages 284–289. IEEE. 

- Cl´audia Freitas, Paula Carvalho, Hugo Gonc¸alo Oliveira, Cristina Mota, and Diana Santos. 2010. Second harem: advancing the state of the art of named entity recognition in portuguese. In _quot; In Nicoletta Calzolari; Khalid Choukri; Bente Maegaard; Joseph Mariani; Jan Odijk; Stelios Piperidis; Mike Rosner; Daniel Tapias (ed) Proceedings of the International Conference on Language Resources and Evaluation (LREC 2010)(Valletta 17-23 May de 2010) European Language Resources Association_ . European Language Resources Association. 

- Jeremy Howard and Sebastian Ruder. 2018. Universal language model fine-tuning for text classification. In _Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 328–339. 

- Taku Kudo and John Richardson. 2018. Sentencepiece: A simple and language independent subword tokenizer and detokenizer for neural text processing. 

- Guillaume Lample, Miguel Ballesteros, Sandeep Subramanian, Kazuya Kawakami, and Chris Dyer. 2016. Neural architectures for named entity recognition. _Computing Research Repository_ , arXiv:1603.01360. Version 3. 

- Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma, and Radu Soricut. 2019. Albert: A lite bert for self-supervised learning of language representations. _arXiv preprint arXiv:1909.11942_ . 

- Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Doll´ar. 2017. Focal loss for dense object detection. In _Proceedings of the IEEE international conference on computer vision_ , pages 2980– 2988. 

- Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. Roberta: A robustly optimized bert pretraining approach. _arXiv preprint arXiv:1907.11692_ . 

- M´onica Marrero, Juli´an Urbano, Sonia S´anchezCuadrado, Jorge Morato, and Juan Miguel G´omezBerb´ıs. 2013. Named entity recognition: fallacies, challenges and opportunities. _Computer Standards & Interfaces_ , 35(5):482–489. 

- Matthew Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, and Luke Zettlemoyer. 2018. Deep contextualized word representations. In _Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers)_ , pages 2227– 2237. 

- Matthew E Peters, Sebastian Ruder, and Noah A Smith. 2019. To tune or not to tune? adapting pretrained representations to diverse tasks. In _Proceedings of the 4th Workshop on Representation Learning for NLP (RepL4NLP-2019)_ , pages 7–14. 

   - Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le, Mohammad Norouzi, Wolfgang Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al. 2016. Google’s neural machine translation system: Bridging the gap between human and machine translation. _Computing Research Repository_ , arXiv:1609.08144. Version 2. 

   - Vikas Yadav and Steven Bethard. 2018. A survey on recent advances in named entity recognition from deep learning models. In _Proceedings of the 27th International Conference on Computational Linguistics_ , pages 2145–2158. 

   - Zhilin Yang, Zihang Dai, Yiming Yang, Jaime Carbonell, Ruslan Salakhutdinov, and Quoc V Le. 2019. Xlnet: Generalized autoregressive pretraining for language understanding. _arXiv preprint arXiv:1906.08237_ . 

- Juliana Pirovani and Elias Oliveira. 2018. Portuguese named entity recognition using conditional random fields and local grammars. In _Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC-2018)_ . 

- Alec Radford, Karthik Narasimhan, Time Salimans, and Ilya Sutskever. 2018. Improving language understanding with unsupervised learning. Technical report, Technical report, OpenAI. 

- Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. 2019. Exploring the limits of transfer learning with a unified text-to-text transformer. _arXiv preprint arXiv:1910.10683_ . 

- Cicero Nogueira dos Santos and Victor Guimaraes. 2015. Boosting named entity recognition with neural character embeddings. _Computing Research Repository_ , arXiv:1505.05008. Version 2. 

- Diana Santos, Nuno Seco, Nuno Cardoso, and Rui Vilela. 2006. Harem: An advanced ner evaluation contest for portuguese. 

- Joaquim Santos, Bernardo Consoli, Cicero dos Santos, Juliano Terra, Sandra Collonini, and Renata Vieira. 2019a. Assessing the impact of contextual embeddings for portuguese named entity recognition. In _8th Brazilian Conference on Intelligent Systems, BRACIS, Bahia, Brazil, October 15-18_ , pages 437– 442. 

- Joaquim Santos, Juliano Terra, Bernardo Scapini Consoli, and Renata Vieira. 2019b. Multidomain contextual embeddings for named entity recognition. In _IberLEF@SEPLN_ . 

- Robyn Speer. 2019. ftfy. Zenodo. Version 5.5. 

- Jorge Wagner Filho, Rodrigo Wilkens, Marco Idiart, and Aline Villavicencio. 2018. The brwac corpus: A new open resource for brazilian portuguese. 

## **A Appendix** 

### **A.1 SentencePiece to WordPiece conversion** 

The generated SentencePiece vocabulary is converted to WordPiece following BERT’s tokenization rules. Firstly, all BERT special tokens are inserted ([CLS], [MASK], [SEP], and [UNK]) and all punctuation characters of the Multilingual vocabulary are added to Portuguese vocabulary. Then, since BERT splits the text at whitespace and punctuation prior to applying WordPiece tokenization in the resulting chunks, each SentencePiece token that contains punctuation characters is split at these characters, the punctuations are removed and the resulting subword units are added to the vocabulary<sup>7</sup> . Finally, subword units that do not start with “ ” are prefixed with “##” and “ ” characters are removed from the remaining tokens. 

### **A.2 HAREM Dataset preprocessing example** 

An example annotation of HAREM that contains multiple solutions, in XML format, is: 

<ALT><EM CATEG="PER|ORG">Governo de Cavaco Silva</EM>|<EM CATEG="ORG">Governo</EM> de <EM CATEG="PER" TIPO="INDIVIDUAL">Cavaco Silva </EM></ALT> 

where _<_ EM _>_ is a tag for Named Entity (NE) and “|” identifies alternative solutions. This annotation can be equally interpreted as containing the following NEs: 

1. 1 NE: Person ”Governo de Cavaco Silva” 

2. 1 NE: Organization ”Governo de Cavaco Silva” 

3. 2 NEs: Organization ”Governo” and Person ”Cavaco Silva” 

The rules described in 4.2.2 would select the third solution in the example above. 

> 7Splitting at punctuation implies no subword token can contain both punctuation and non-punctuation characters. 



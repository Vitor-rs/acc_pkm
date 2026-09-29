---
title: ANLS* -- a universal document processing metric for generative large language
  models
citekey: Peer2024
authors:
- David Peer
- Philemon Schöpf
- Volckmar Nebendahl
- Alexander Rietzler
- Sebastian Stabinger
year: 2024
date: '2024'
item_type: preprint
doi: 10.48550/ARXIV.2402.03848
url: https://arxiv.org/abs/2402.03848
zotero_key: W5J79WT6
collections:
- SA9KZ2CI
tags:
- Computer Science - Computation and Language
- Computer Science - Artificial Intelligence
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: Peer et al. - 2024 - ANLS -- a universal document processing metric
  for generative large language models.pdf
synced_at: '2026-09-29T17:55:53.049256'
---

# ANLS* -- a universal document processing metric for generative large language models

**Autores:** David Peer, Philemon Schöpf, Volckmar Nebendahl, Alexander Rietzler, Sebastian Stabinger
**DOI:** [10.48550/ARXIV.2402.03848](https://doi.org/10.48550/ARXIV.2402.03848)
**URL:** https://arxiv.org/abs/2402.03848

## 📄 Conteúdo Completo do Documento

# ANLS* - A Universal Document Processing Metric for Generative Large Language Models 

David¹ Philemon¹ Volckmar Alexander Sebastian Peer Sch¨opf Nebendahl Rietzler Stabinger 

DeepOpinion `https://deepopinion.ai` 

February 28, 2024 

##### **Abstract** 

Traditionally, discriminative models have been the predominant choice for tasks like document classification and information extraction. These models make predictions that fall into a limited number of predefined classes, facilitating a binary true or false evaluation and enabling the direct calculation of metrics such as the F1 score. However, recent advancements in generative large language models (GLLMs) have prompted a shift in the field due to their enhanced zero-shot capabilities, which eliminate the need for a downstream dataset and computationally expensive fine-tuning. However, evaluating GLLMs presents a challenge as the binary true or false evaluation used for discriminative models is not applicable to the predictions made by GLLMs. 

This paper introduces a new metric for generative models called ANLS* for evaluating a wide variety of tasks, including information extraction and classification tasks. The ANLS* metric extends existing ANLS metrics as a drop-in-replacement and is still compatible with previously reported ANLS scores. An evaluation of 7 different datasets and 4 different GLLMs using the ANLS* metric is also provided, demonstrating the importance of the proposed metric. 

We also benchmark a novel approach to generate prompts for documents, called SFT, against other prompting techniques such as LATIN. In 15 out of 21 cases, SFT outperforms other techniques and improves the state-of-the-art, sometimes by as much as 15 percentage points. Sources are available at `https://github.com/deepopinion/anls_star_metric` 

## **1 Introduction** 

The increases in model size, dataset size, and available compute have significantly advanced the state-of-the-art (SOTA) on many natural language processing (NLP) tasks [7, 4, 13, 12]. A unique and challenging domain within NLP is document processing, because documents contain text, images and tables and are, therefore, inherently multimodal. Additionally, the text is not strictly arranged in a linear fashion, but often has distinct positional structure within the 2D space of the document (i.e. the layout of the document). As such, document processing tasks are often addressed with specialized layout models [28, 27, 5] that improve the performance by encoding important 2D positional information of bounding boxes together with the text tokens. 

While discriminative models such as LayoutLMv3 [5] have significantly advanced the state-ofthe-art in document processing tasks, they still possess certain limitations. For instance, they are incapable of executing tasks that require additional synthesis, translation, or enhancement of text, 

> 1Equal contribution. Contact via `firstname.lastname@deepopinion.ai` 

> 2This paper was written with the assistance of GPT-4. 

1 

as they cannot generate tokens and usually only label tokens. For example, a task may require extracting the date-time and transforming it into the `YYYY-MM-DD` format. Consequently, generative large language models (GLLMs) have garnered considerable attention in this field in recent times [24] as they can solve these problems without the need for additional post-processing steps. Furthermore, these models are usually pre-trained on large datasets, eliminating the need for fine-tuning them on a specific downstream task as is usually done for classical deep learning models [28, 27, 5]. Simply altering the input prompt (zero-shot) or providing a few examples demonstrating the task (few-shot) is sufficient to accomplish a task with decent performance. This is particularly crucial for document processing tasks, as the number of available datasets is limited and the creation of new ones is costly. Consequently, the community is moving towards large generative models for document processing tasks [24, 25]. 

While the evaluation of discriminative models typically relies on measuring the F1 score by counting correctly labeled bounding boxes coming from an OCR solution, this method is not applicable for GLLMs since the extracted, and possibly already pre-processed, information is directly returned as generated text. I.e. there is no direct connection between the OCR bounding boxes and the extracted information anymore. Generated text may also contain minor errors such as typos, which should be penalized differently compared to completely wrong answers. GLLMs are, therefore, typically evaluated using the Average Normalized Levenshtein Similarity (ANLS) metric [3], which is a normalized form of the Levenshtein similarity, assessing the closeness of a generated answer to the expected output. A shortcoming of the ANLS metric is that it can only deal with strings and lists, but cannot be used for dictionaries or any combination of types that are often encountered when dealing with information extraction tasks. Additionally, some tasks require to extract information with a list structure such as line-item extraction [14], which requires the evaluation of complex output objects. 

In this paper, we introduce ANLS*, a metric that can be used to evaluate a wide variety of tasks such as information extraction or classification, even in cases where output values that may contain minor errors are generated. It is worth mentioning, that this metric can also be used for discriminative models which allows for direct comparison of both discriminative and generative models with one single metric in the future. Additionally, the ANLS* metric can be applied to unstructured as well as structured outputs or any combination of both which makes it a versatile tool for the evaluation of document processing tasks. The proposed metric extends all previously defined ANLS metrics [3]. That is, results that could be calculated using the ANLS metric remain unchanged under ANLS*, while simultaneously offering greater flexibility. Therefore, it serves as a plug-in replacement for existing ANLS metrics. 

Lastly, we provide qualitative as well as quantitative experiments using the proposed ANLS* metric to demonstrate the importance of the proposed metric. Various GLLMs and prompting methods across different datasets are evaluated with the proposed metric. Those results are not only provided for the community as a baseline for future experiments, but the scripts to reproduce the results are also publicly available. 

## **2 Related Work** 

**Metrics** The normalized Levenshtein similarity (NLS) was defined by Levenshtein et al. [10] to measure the similarity between words using the minimal distance between those words. Later, the Average Normalized Levenshtein Similarity (ANLS) was introduced by Biten et al. [3] for the evaluation of visual question-answering (VQA) tasks. The ANLS metric takes OCR errors into consideration, which makes it suitable for generative models. Tito et al. [19] further expanded the ANLS metric for the comparison of lists by using the Hungarian matching algorithm from Kuhn [9] to find the best match between the ground truth list and the predicted list. Finally, Van Landeghem et al. [21] extended the normalized Levenshtein similarity to account for predictions that should be null. This metric is not only useful for verifying the correct handling of unanswerable questions but also for penalizing hallucinations generated by GLLMs. 

2 

**LLMs for Document Processing** Xu et al. [28] introduced a novel layout-aware language model to encode bounding box information as well as visual information about the document in tokens in order to improve document processing tasks. They outperformed purely text-based models such as BERT [4] by a large margin. Novel developments with different attention layers and pre-training methods have later been introduced [27, 5]. A novel GLLM called DocLLM was introduced by Wang et al. [24] specifically for document processing tasks. This model captures cross-alignment between text and spatial modalities decomposing the attention mechanism of transformers. Although they could show significant improvements and novel pre-training methods, we will demonstrate that this model is still behind extremely large, purely text-based models, such as gpt-4 [2]. As a consequence, special prompting mechanisms that may encode OCR scanned documents in a way that is easier to understand by purely text-based models gained interest recently. Wang et al. [25] introduced such a prompting technique, called LATIN, to enhance the representation of documents for text-based GLLMs. Instead of directly encoding positional information in the tokens, they utilized layout-aware instruction prompts by using the positional information of the bounding boxes after the OCR scan. We developed a more advanced approach, called SFT that takes several properties of documents and LLMs into account. We will show that SFT is superior to LATIN and other prompting techniques. 

1 

Other approaches completely bypass the conversion from OCR to prompts by employing a multimodal model that directly processes documents without a separate OCR step. For instance, Kim et al. [8] developed an OCR-free document transformer architecture. Ye et al. [29] developed a generative multimodal model named MPlug-DocOWL that was trained on language-only, general vision-and-language, and document instruction tuning datasets. 

## **3 Metric Definition** 

In this section, we introduce ANLS*. The goal is to develop a metric that is not only compatible with the existing ANLS [3] and the ANLSL [19] metrics, but also penalizes unanswerable questions in case they are answered as proposed by Van Landeghem et al. [21]. Additionally, the ANLS* metric should be a tool that is applicable for a wide variety of tasks, including tasks with dictionary outputs, lists or any combination of those in order to handle e.g. line-item extraction [14] as well as simple question-answering tasks. As a result, the ANLS* metric serves as a direct drop-in replacement for all standard ANLS metrics defined by the community so far, and can additionally be used for evaluating all document-processing tasks. 

### **3.1 Supported data types** 

The ANLS* metric supports the following data types: 

1. `String` - To compare strings against each other using the normalized Levenshtein similarity. 

2. `None` - Sometimes questions are not answerable. With this type it can be checked, whether the model does not answer. Any answer other than None will be penalized. 

3. `Tuple` - Compare the given answer with each element in the tuple and select the element that produces the maximum ANLS* score. This is also provided by the classical ANLS metric [3]. 

4. `List` - Sometimes it is required to extract information in the form of lists from a document. For example, extracting all purchased items found in an invoice. While the order is not important, the list should contain all items. Note that the same item can occur multiple times in lists. Hungarian matching [9] is used to compare the ground truth and the predicted list against each other. Both, missing elements as well as hallucinated elements, are penalized as introduced by Tito et al. [19]. 

> 1The scope of this paper does not include an introduction of SFT. It may be introduced in a future publication. 

3 





<!-- Start of picture text -->
(a) Ground truth.<br><!-- End of picture text -->







<!-- Start of picture text -->
(b) Prediction with ANLS* = 1 . 0. (c) Prediction with ANLS*  <  1 . 0.<br><!-- End of picture text -->

Figure 1: Examples of how the ground truth, as well as predictions, are decomposed into a tree structure. A correct prediction is shown in Figure 1b, while Figure 1c visualizes a partially incorrect prediction. Its worth mentioning that any hallucination as well as incorrect types are penalized as well. More examples are given in Table 1. 

5. `Dict` - For document information extraction it is usually required to extract key-value pairs. For example, when extracting the date and total value from an invoice. Missing keys as well as hallucinated keys are penalized. 

It is worth mentioning that all combinations of the above types are supported as well. For example, a dictionary may contain lists of strings or the elements of a list may be dictionaries. The implementation of the ANLS* metric maps those complex structures into a tree and compares the ground truth tree against the predicted tree from the model. Figure 1a visualizes how the ground truth is decomposed into a tree structure that can then be compared against predictions for an example. 

Figure 1b demonstrates a prediction with ANLS* = 1 _._ 0 w.r.t Figure 1a. Finally, Figure 1c shows an example of a partially incorrect prediction. Note that the ANLS* metric is not only able to detect wrong strings but also wrong output structures. For example, the prediction may be a list, although a dictionary was expected. All these cases are correctly handled by the ANLS* metric. 

4 

### **3.2 Formal definition of the ANLS* metric** 

In the following, the ground truth is denoted as _g_ and the prediction as _p_ . Note that the type of the ground truth `type` ( _g_ ) may differ from the type of the prediction `type` ( _p_ ) in case the GLLM returns incorrect results. For example, the GLLM may answer with a sentence although a list was expected. The idea of the metric is to generate a tree from the ground truth as well as a tree from the prediction and to compute a matching between both trees. Additionally, the metric is normalized to account for different lengths of the ground truth and the prediction. Overall, the ANLS* metric is defined as follows: 



where _s_ is the score between the ground truth and the prediction and _l_ is the size of the trees _g_ and _p_ such that ANLS*( _g, p_ ) _∈_ [0 _,_ 1]. Additionally, it is worth noting that each prediction in this tree is given equal weight. This implies that leaf nodes of large sub-trees carry the same weight as leaf nodes that appear at the top level. 

#### **3.2.1 Definition of the score** _s_ 

The score _s_ is defined recursively to measure the similarity between the ground truth and the prediction. Note that in order to distinguish between the _one of_ semantic of a ground truth list used by the original ANLS metric, and the matching semantic implemented in the ANLSL metric, we introduced Tuples for the former and Lists for the latter. The score _s_ is defined as follows: 



with LD being the Levensthein distance and _τ_ being the normalized Levensthein distance threshold which is set to _τ_ = 0 _._ 5. _ψ_ is the Hungarian matching algorithm [9] performed according to the pairwise ANLS* of each ground truth and prediction element. This algorithm returns an optimal matching of elements between two lists w.r.t. a given score. The score for type mismatches (i.e., different subtrees) yields a score of 0 _._ 0. The function `keys` ( _x_ ) returns all keys of a dictionary _x_ , that are not None. It is important that `keys` ( _x_ ) ignores None values in order to penalize hallucinations correctly. 

5 

#### **3.2.2 Definition of the length** _l_ 

To normalize _s_ , we define the length _l_ of each type as follows: 



As can be seen, the length is weighted for all type matches accordingly. Nevertheless, it is not guaranteed that the prediction produced the correct output structure. On the other hand, a partially correct structure should not get a sore of 0 _._ 0. To this end, we match the subtree and penalize wrong types via another length function _lt_ . It can be seen that the maximum length is used between the ground truth and the prediction - max( _lt_ ( _g_ ) _, lt_ ( _p_ )) – such that both, missing subtrees, as well as hallucinated subtrees, are penalized equally. The length function _lt_ is defined as follows: 



where _x_ is either a (sub)tree of the prediction _p_ or a (sub)tree of the ground truth _g_ . 

Using the ANLS* metric we will next showcase some examples to demonstrate the behavior of the metric. In a quantitative study, we will later show that ANLS* is a suitable metric for a wide variety of tasks. 

## **4 Experimental Evaluation** 

In this section, we evaluate the performance of the ANLS* metric both qualitatively and quantitatively. The source code required to reproduce these results can be accessed at `https://github.c om/deepopinion/anls_star_metric` . 

### **4.1 Examples** 

Different ANLS* scores for various ground truths and predictions are provided below, to offer the reader some insight into which predictions are considered as good and which are considered as bad. We also show some limitations of the proposed method. Note that tuples are interpreted as _one of_ and lists are interpreted as _all of_ . 

Several cases for good and bad predictions including type mismatches are shown in Table 1. Additionally, we added some edge cases in Table 2 that may seem counter-intuitive at first, but they 

6 

Table 1: ANLS* scores for different predictions and ground truth types. 

|Id|Description|Ground Truth|Prediction|ANLS*|
|---|---|---|---|---|
|1|Correct String|`Hello World`|`Hello World`|1.0|
|2|Typo|`Hello World`|`Hello Wolrd`|0.82|
|3|Incorrect String|`Hello World`|`How are you?`|0.0|
|4|Hallucination|**None**|`Hello World!`|0.0|
|5|One of n|`tuple(Hello, World)`|`Hello`|1.0|
|6|Typo in one of n|`tuple(Hello, World)`|`Wolrd`|0.6|
|7|Expected String|`Hello World`|`list(Hello, World)`|0.0|
|8|Correct List|`list(Hello, World)`|`list(World, Hello)`|1.0|
|9|Missing Element|`list(Hello, World)`|`list(Hello)`|0.5|
|10|Correct Dict|_{_`a:Hello, b:World`_}_|_{_`b:World, a:Hello`_}_|1.0|
|11|Missig Key|_{_`a:Hello, b:World`_}_|_{_`a:Hello`_}_|0.5|
|12|Hallucinated Key|_{_`a:Hello, b:World`_}_|_{_`b:World, a:Hello, c:Great`_}_|0.67|
|13|Complex Object|_{_`a:Hello, b:list(W,r,l,d)`_}_|_{_`a:Hello, b:list(w,r,d)`_}_|0.8|



Table 2: ANLS* scores for edge cases. 

|Id|Description|Ground Truth|Prediction|ANLS*|
|---|---|---|---|---|
|14|`list` casted implicitly to `tuple`|`list(Hello, World)`|`Hello`|1.0|
|15|Comparison of numbers|`0.2`|0.199999999|0.0|
|16|Incorrect Format|`31.12.2023`|`31.Dec 2023`|0.58|
|17|Unanswerable Question - Incorrect Answer|`Yesterday`|`Last Week`|0.0|
|18|Unanswerable Question - No Answer|`Yesterday`|`None`|0.0|



are required in order to keep the metric consistent with the previously defined ANLS and ANLSL metrics. 

The first edge case #14 shown in Table 2 (list automatically casted to a tuple) is implemented to ensure compatibility with common datasets where possible answers are returned as lists, while the actual answer is a single string. According to the proposed semantics, all possible answers should be tuples. However, to ensure the reproducibility of experiments with classical QA datasets, we implemented this implicit casting in cases where the ground truth is a list and the prediction is a string. In case 15, it is evident that numbers are not interpreted as numbers, but a string comparison is performed instead. Case 16 illustrates that different formats may produce a high error, even though the semantics are the same. Lastly, cases 17 and 18 demonstrate that completely incorrect answers are weighted equally to missing answers. 

### **4.2 Experimental Evaluation** 

In this subsection, the quantitative evaluation of the ANLS* metric on many different datasets and different GLLMs is shown. More precisely, we evaluated two QA datasets (DocVQA [11], MPDocVQA [20]) and five information extraction datasets (Kleister Charity [15], Kleister NDA [15], SROIE [6], VRDU Ad Buy [26], VRDU Registration[26]). The following model versions were used for the evaluation: gpt-3.5-turbo-16k (Version gpt-3.5-turbo-16k-0613), gpt-4-turbo (Version gpt-4-1106-preview) [2], gemini-pro (Version 1.0) [16] and mistral-large (Feb. 2024) [17]. We used LangChain [1] for the implementation with the following system-prompts: 

7 

#### **QA prompt** 

`You are a world-class question answering system. You are given a document and a question. You must answer the question based on` _�→_ `the document. Precisely answer the question without any additional text. Its very important to NOT write full sentences! Note: Ensure that the answer is precisely contained in the original document. Here is the document: {document} Here is the question: {question}` 

#### **Information extraction prompt** 

`You are a document information extraction system. You are given a document and a json with keys that must be extracted from the` _�→_ `document. Here is the document: {document} {format_instructions}` 

Format extractions are automatically generated by LangChain according to the given dataset and keys that must be extracted. For representing the document itself, different prompting methods were evaluated (Simple, LATIN, SFT). More details can be found in the provided source code. 

The results are shown in Table 3. It can be seen that special prompt formatting improved scores in almost all cases. Our advanced SFT technique improved scores in 15 out of 21 cases sometimes by a large amount. For example for DocVQA SFT outperformed LATIN by as much as 15 percentage points. For cases similar to Kleister NDA, where documents contain only text and no positional encoding, we can see that there is no improvement for SFT. Nevertheless, in general documents that contain 2D structure show the importance of specialized prompt formatting techniques. It can also be seen that GPT models are superior to gemini-pro, mistral-large as well as to the custom trained DocLLM model. In one case, gemini-pro is outperformed by 60.5 percentage points. Especially mistral-large struggles with processing documents. We found that the safety filter of gemini-pro is too restrictive and filtered a lot of samples. Finally, it is worth mentioning that gpt-3.5-turbo-16k outperformed the newer gpt-4-turbo model in 2 cases, on DocVQA as well as SROIE. 

## **5 Conclusion & Discussion** 

In this paper, we introduce a novel metric called ANLS*, which serves as a plug-in replacement for existing ANLS metrics. This metric is not only applicable for traditional GLLM tasks such as QA, but also for information extraction tasks, and even for more complex outputs. We demonstrate that ANLS* is a versatile metric for a broad range of tasks. We evaluate the ANLS* metric using three different GLLMs on seven different datasets. We also demonstrate that more advanced methods such as SFT outperform prompting techniques, such as LATIN. We found that the GPT models outperform both gemini-pro and the custom-trained DocLLM model. We believe that DocLLM is still too small with 7B parameters to be competitive against GPT models. Unfortunately, it is not available at the time of writing such that combinations of prompting techniques with DocLLM can not be tested yet. 

We posit that ANLS* is a suitable metric for the evaluation of generative models and should be adopted for future use. We also claim that the ANLS* metric is suitable for discriminative models, allowing for a comparison of generative and discriminative models using a single metric. We hope that the ANLS* metric will be adopted by the community in the future. 

8 

#### Table 3: ANLS* score for different GLLMs and Datasets. 

Note that the values for DocLLM are copied from the paper [24] as the model is not available at the time of writing. 

|Dataset|Method<br>g|pt-3.5-turbo-16k|gpt-4-turbo|gemini-pro|mistral-large|DocLLM*|
|---|---|---|---|---|---|---|
|DocVQA|Simple|0.586|0.607|0.586|0.388||
||Latin Prompt|0.659|0.699|0.676|0.403|0.634|
||**SFT (Ours)**|**0.809**|0.790|0.741|0.540||
|MPDocVQA|Simple|0.348|0.389|0.389|0.239||
||Latin Prompt|0.413|0.463|0.467|0.289|-|
||**SFT (Ours)**|0.547|**0.548**|**0.548**|0.377||
|Kleister Charity|Simple|0.490|0.743|0.583|0.534||
||Latin Prompt|0.442|0.735|0.478|0.540|0.499|
||**SFT (Ours)**|0.476|**0.763**|0.633|0.600||
|Kleister NDA|Simple|0.343|0.695|0.623|0.608||
||Latin Prompt|0.434|**0.705**|0.599|0.643|-|
||**SFT (Ours)**|0.355|0.703|0.552|0.637||
|SROIE|Simple|0.874|0.835|0.263|0.877||
||Latin Prompt|0.849|0.851|0.371|0.858|-|
||**SFT (Ours)**|0.893|0.873|0.288|**0.931**||
|VRDU AdBuy|Simple|0.402|0.553|0.510|0.305||
||Latin Prompt|0.389|0.586|0.556|0.351|-|
||**SFT (Ours)**|0.661|**0.770**|0.685|0.243||
|VRDU Reg.|Simple|0.659|0.676|0.699|0.633||
||Latin Prompt|0.693|0.673|**0.740**|0.645|-|
||**SFT (Ours)**|0.723|0.711|0.720|0.687||



## **References** 

- [1] Langchain. `https://github.com/langchain-ai/langchain` . Accessed: 31-01-2024. 

- [2] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [3] Ali Furkan Biten, Ruben Tito, Andres Mafla, Lluis Gomez, Mar¸cal Rusinol, Ernest Valveny, CV Jawahar, and Dimosthenis Karatzas. Scene text visual question answering. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4291–4301, 2019. 

- [4] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deep bidirectional transformers for language understanding. In _Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ , pages 4171–4186, Minneapolis, Minnesota, June 2019. Association for Computational Linguistics. 

- [5] Yupan Huang, Tengchao Lv, Lei Cui, Yutong Lu, and Furu Wei. Layoutlmv3: Pre-training for document ai with unified text and image masking. In _Proceedings of the 30th ACM International Conference on Multimedia_ , pages 4083–4091, 2022. 

- [6] Zheng Huang, Kai Chen, Jianhua He, Xiang Bai, Dimosthenis Karatzas, Shijian Lu, and CV Jawahar. Icdar2019 competition on scanned receipt ocr and information extraction. In _2019 International Conference on Document Analysis and Recognition (ICDAR)_ , pages 1516– 1520. IEEE, 2019. 

9 

- [7] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. _arXiv preprint arXiv:2001.08361_ , 2020. 

- [8] Geewook Kim, Teakgyu Hong, Moonbin Yim, JeongYeon Nam, Jinyoung Park, Jinyeong Yim, Wonseok Hwang, Sangdoo Yun, Dongyoon Han, and Seunghyun Park. Ocr-free document understanding transformer. In _European Conference on Computer Vision_ , pages 498–517. Springer, 2022. 

- [9] Harold W Kuhn. The hungarian method for the assignment problem. _Naval research logistics quarterly_ , 2(1-2):83–97, 1955. 

- [10] Vladimir I Levenshtein et al. Binary codes capable of correcting deletions, insertions, and reversals. In _Soviet physics doklady_ , volume 10, pages 707–710. Soviet Union, 1966. 

- [11] Minesh Mathew, Dimosthenis Karatzas, and CV Jawahar. Docvqa: A dataset for vqa on document images. In _Proceedings of the IEEE/CVF winter conference on applications of computer vision_ , pages 2200–2209, 2021. 

- [12] David Peer, Bart Keulen, Sebastian Stabinger, Justus Piater, and Antonio Rodriguez-Sanchez. Improving the trainability of deep neural networks through layerwise batch-entropy regularization. _Transactions on Machine Learning Research_ , 2022. URL `https://openreview.net/for um?id=LJohl5DnZf` . 

- [13] David Peer, Sebastian Stabinger, Stefan Engl, and Antonio Rodr´ıguez-S´anchez. Greedy-layer pruning: Speeding up transformer models for natural language processing. _Pattern Recognition Letters_ , 157:76–82, 2022. 

- [14] Stˇep´an<sup>ˇ</sup> Simsa,<sup>ˇ</sup> Milan Sulc,<sup>ˇ</sup> Michal Uˇriˇc´aˇr, Yash Patel, Ahmed Hamdi, Matˇej Koci´an, Maty´aˇs Skalick`y, Jiˇr´ı Matas, Antoine Doucet, Micka¨el Coustaty, et al. Docile benchmark for document information localization and extraction. _arXiv preprint arXiv:2302.05658_ , 2023. 

- [15] Tomasz Stanis�lawek, Filip Grali´nski, Anna Wr´oblewska, Dawid Lipi´nski, Agnieszka Kaliska, Paulina Rosalska, Bartosz Topolski, and Przemys�law Biecek. Kleister: key information extraction datasets involving long documents with complex layouts. In _International Conference on Document Analysis and Recognition_ , pages 564–579. Springer, 2021. 

- [16] Gemini Team, Rohan Anil, Sebastian Borgeaud, Yonghui Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 

- [17] Mistral AI Team. Mistral large. `https://mistral.ai/news/mistral-large/` . Accessed: 27-02-2024. 

- [18] Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, and Christopher D Manning. Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. _arXiv preprint arXiv:2305.14975_ , 2023. 

- [19] Rub`en Tito, Dimosthenis Karatzas, and Ernest Valveny. Document collection visual question answering. In _Document Analysis and Recognition–ICDAR 2021: 16th International Conference, Lausanne, Switzerland, September 5–10, 2021, Proceedings, Part II 16_ , pages 778–792. Springer, 2021. 

- [20] Rub`en Tito, Dimosthenis Karatzas, and Ernest Valveny. Hierarchical multimodal transformers for multipage docvqa. _Pattern Recognition_ , 144:109834, 2023. 

10 

- [21] Jordy Van Landeghem, Rub`en Tito, �Lukasz Borchmann, Micha�l Pietruszka, Pawel Joziak, Rafal Powalski, Dawid Jurkiewicz, Micka¨el Coustaty, Bertrand Anckaert, Ernest Valveny, et al. Document understanding dataset and evaluation (dude). In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 19528–19540, 2023. 

- [22] Jordy Van Landeghem, Rub`en Tito, �Lukasz Borchmann, Micha�l Pietruszka, Pawel Joziak, Rafal Powalski, Dawid Jurkiewicz, Micka¨el Coustaty, Bertrand Anckaert, Ernest Valveny, et al. Document understanding dataset and evaluation (dude). In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 19528–19540, 2023. 

- [23] Ramakrishna Vedantam, C Lawrence Zitnick, and Devi Parikh. Cider: Consensus-based image description evaluation. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 4566–4575, 2015. 

- [24] Dongsheng Wang, Natraj Raman, Mathieu Sibue, Zhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, and Xiaomo Liu. Docllm: A layout-aware generative language model for multimodal document understanding. _arXiv preprint arXiv:2401.00908_ , 2023. 

- [25] Wenjin Wang, Yunhao Li, Yixin Ou, and Yin Zhang. Layout and task aware instruction prompt for zero-shot document image question answering, 2023. 

- [26] Zilong Wang, Yichao Zhou, Wei Wei, Chen-Yu Lee, and Sandeep Tata. Vrdu: A benchmark for visually-rich document understanding. In _Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , pages 5184–5193, 2023. 

- [27] Yang Xu, Yiheng Xu, Tengchao Lv, Lei Cui, Furu Wei, Guoxin Wang, Yijuan Lu, Dinei Florencio, Cha Zhang, Wanxiang Che, Min Zhang, and Lidong Zhou. LayoutLMv2: Multi-modal pre-training for visually-rich document understanding. pages 2579–2591, Online, August 2021. Association for Computational Linguistics. 

- [28] Yiheng Xu, Minghao Li, Lei Cui, Shaohan Huang, Furu Wei, and Ming Zhou. Layoutlm: Pretraining of text and layout for document image understanding. In _Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ , pages 1192–1200, 2020. 

- [29] Jiabo Ye, Anwen Hu, Haiyang Xu, Qinghao Ye, Ming Yan, Yuhao Dan, Chenlin Zhao, Guohai Xu, Chenliang Li, Junfeng Tian, et al. mplug-docowl: Modularized multimodal large language model for document understanding. _arXiv preprint arXiv:2307.02499_ , 2023. 

11 



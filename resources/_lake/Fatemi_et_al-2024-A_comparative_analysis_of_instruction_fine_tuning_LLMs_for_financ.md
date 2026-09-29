---
title: A comparative analysis of instruction fine-tuning LLMs for financial text classification
citekey: Fatemi2024
authors:
- Sorouralsadat Fatemi
- Yuheng Hu
- Maryam Mousavi
year: 2024
date: '2024'
item_type: preprint
doi: 10.48550/ARXIV.2411.02476
url: https://arxiv.org/abs/2411.02476
zotero_key: 8ZYYHRBS
collections:
- SA9KZ2CI
tags:
- Computer Science - Computation and Language
- Computer Science - Artificial Intelligence
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: a comparative analysis of instruction fine-tuning llms for financial
  text classification.pdf
synced_at: '2026-09-29T18:16:44.491729'
---

# A comparative analysis of instruction fine-tuning LLMs for financial text classification

**Autores:** Sorouralsadat Fatemi, Yuheng Hu, Maryam Mousavi
**DOI:** [10.48550/ARXIV.2411.02476](https://doi.org/10.48550/ARXIV.2411.02476)
**URL:** https://arxiv.org/abs/2411.02476

## 📄 Conteúdo Completo do Documento

# **A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text** 

# **Classification** 

SOROURALSADAT FATEMI, University of Illinois at Chicago, USA 

YUHENG HU, University of Illinois at Chicago, USA 

MARYAM MOUSAVI, Arizona State University, USA 

Large Language Models (LLMs) have demonstrated impressive capabilities across diverse Natural Language Processing (NLP) tasks, including language understanding, reasoning, and generation. However, general-domain LLMs often struggle with financial tasks due to the technical and specialized nature of financial texts. This study investigates the efficacy of instruction fine-tuning smaller-scale LLMs, including Mistral-7B, Llama3-8B, and Phi3-mini, to enhance their performance in financial text classification tasks. We fine-tuned both instruction-tuned and base models across four financial classification tasks, achieving significant improvements in task-specific performance. Furthermore, we evaluated the zero-shot capabilities of these fine-tuned models on three unseen complex financial tasks including argument classification, deal completeness classification and causal classification. Our results indicate while base model fine-tuning led to greater degradation, instruction-tuned models maintained more robust performance. To address this degradation, we employed model merging techniques, integrating single-task domain-specific fine-tuned models with the base model. Using this merging method resulted in significant enhancements in zero-shot performance, even exceeding the original model’s accuracy on certain datasets. Our findings underscore the effectiveness of instruction fine-tuning and model merging for adapting LLMs to specialized financial text classification tasks. 

## **1 INTRODUCTION** 

Large Language Models (LLMs) have revolutionized Natural Language Processing (NLP) by demonstrating exceptional capabilities in understanding, reasoning, and generating human-like text across various general-domain tasks. Prominent models like ChatGPT [4] and GPT-4 [36] have shown impressive versatility in following general human instructions and handling various tasks such as question answering [5], machine translation [67], information extraction [11], and grammar correction [35]. This broad proficiency has led to growing interest in leveraging LLMs for industry-specific applications including medicine and finance. For instance, Med-PaLM 2 [41] has been adapted for medical domains to provide accurate responses to medical queries, while Bloomberg’s financial LLM [50] supports various NLP tasks within the financial sector. 

In the finance industry, beyond quantitative data typically analyzed, the sentiment and tone of financial reports, earnings calls, news articles, and social media posts significantly influence investor decisions. Therefore, extracting and analyzing relevant textual information is critical for informed investment strategies and decision-making [12, 16]. Despite the advancements of general-domain LLMs, they often fall short when applied to specialized fields like finance due to complex terminologies and intricate concepts. This underscores a need for domain-specific adaptations to fully realize the potential of LLMs in financial applications. 

Existing research highlights the success of LLMs in financial tasks, such as predicting stock price movements [24, 28, 53] and performing advanced financial text analytics [13, 14, 52, 54]. However, significant challenges remain, particularly in tasks like financial relation extraction and numerical reasoning, which are crucial for making wellinformed decisions [24, 52]. The efficient market hypothesis [29] further underscores the importance of linking public 

Fameti et al. 

information with stock returns, emphasizing the need for sophisticated analysis tools [12, 16]. 

To address these limitations and enhance the capabilities of LLMs for specific domains, existing methods can be broadly classified into three main approaches: in-context learning, training models from scratch on domain-specific and general data, and fine-tuning existing models using supervised datasets. In-context learning, where LLMs generate results based on a few demonstration examples [24], can be costly, slow in inference, and limited by the model’s context window [2]. Moreover, these models can be sensitive to the quality and variability of the provided examples [21]. Training models from scratch, while effective, demands significant computational resources and vast domain-specific and general dataset. Fine-tuning existing models is promising alternative but faces challenges such as the need for high-quality datasets and the risk of catastrophic forgetting, where the model’s ability to perform general tasks degrades after domain-specific fine-tuning. Techniques like model merging can help mitigate these effects. 

Previous studies have demonstrated that instruction fine-tuning smaller open-source language models can significantly enhance their performance on domain-specific tasks across various fields, such as law and medicine. In many cases, these models have outperformed the zero-shot performance of proprietary LLMs and other state-of-the-art models [19, 23, 33, 61, 65]. Within the finance domain, one study fine-tuned the Llama2 model for sentiment analysis, outperforming the FinBERT [62]. Another study fine-tuned Llama2-7B and Llama2-13B models on a variety of financial tasks, including sentiment analysis, relation extraction, question answering, and stock market prediction [54]. However, much of the existing research has focused primarily on fine-tuning models from the Llama family. To address this gap, we explore fine-tuning other powerful, smaller LLMs, specifically Mistral-7B, Phi-3, and Llama2-8B, across four representative financial text classification tasks: sentiment analysis, news headline classification, relation extraction, and hawkish-dovish classification. 

One of the main challenges with fine-tuning LLMs for domain-specific tasks is the degradation of their zero-shot performance on unseen tasks [63]. To mitigate this, previous studies have incorporated general instruction data into domain-specific training datasets or augmented the data to reduce model sensitivity to semantically similar prompts [27, 46, 65]. While this approach improves generalizability, it also increases computation cost and training time. 

## **1.1 Our approach and Contributions** 

In our study, we aimed to address these challenges and improve the performance of smaller LLMs on specialized financial tasks by focusing on in-context learning, fine-tuning and model merging techniques. By leveraging these approaches, we aim to improve the performance of small LLMs in specialized financial tasks while maintaining their general capabilities on unseen tasks. We explored the potential of **Mistral-7B** , **Phi-3** , and **Llama2-8B** , which are powerful yet resource-efficient models, across seven representative financial text classification tasks: **sentiment analysis** , **news headline classification** , **relation extraction** , **hawkish-dovish classification** , **argument unit classification** , **deal completion classification** and **causal classification** . These models were selected to address the challenge of adapting LLMs to complex, domain-specific tasks while managing computational costs. By concentrating on smaller models, we aim to provide a more scalable solution that balances performance with efficiency in the financial sector. 

We first assessed the in-context learning capabilities of selected models on the specified tasks. We experimented with one-shot, five-shot and ten-shot examples and compared them against zero-shot performance of the models. The results 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

shows some improvement in the model prediction when providing the in-context examples. However, after a certain number of examples, increasing the number of demonstrations led to performance degradation in small instruct models. 

Next, we fine-tuned the models to improve task performance while maintaining the generalization capabilities of the models. Both base and instruction-tuned models were fine-tuned using the same set of finance-specific training data. Our approach differs from previous work by focusing on instruction-tuned models that had already been exposed to a diverse range of tasks, reducing the need for extensive general datasets. The results show that fine-tuning both base and instruct models leads to substantial improvements over zero-shot performance, including when compared to proprietary models such as GPT-4. In particular, the models excelled in tasks like relation extraction and hawkish-dovish classification, which are typically underrepresented in the pre-training data of most LLMs. We then evaluated the performance of fine-tuned models on three different unseen tasks and we observed that base fine-tuned models exhibited greater performance degradation compared to instruct fine-tuned models. These findings indicate that instruct fine-tuned models provide a more robust foundation for further fine-tuning on domain-specific tasks. 

To further address the performance degradation on unseen tasks, we leveraged the merging techniques using **MergeKit framework** . This allowed us to merge single-task fine-tuned models with the vanilla instruction model, helping to preserve the models’ zero-shot generalization abilities while enhancing their task-specific performance. Notably, the Mistral-7B model demonstrated results that were either on par with, or surpassed, its original zero-shot performance, highlighting the effectiveness of model merging techniques in maintaining robust performance across tasks. 

Our key contributions are as follows: 

- We experimented with in-context learning of small LLMs, including Llama3-8B, Mistral-7B, and Phi-3-mini, on four financial domain datasets. Our findings indicate that increasing the number of examples degrades the performance of small instruct models. 

- We fine-tuned smaller models such as Mistral-7B, Phi-3, and Llama2-8B on four key financial text classification tasks, showcasing the feasibility of using smaller, more efficient models for domain-specific financial tasks. 

- We demonstrated significant performance improvements across all models by fine-tuning both base and instruct models, with the instruct models proving more robust in handling complex financial tasks. 

- We introduced model merging techniques via the MergeKit framework, which learned the domain specific knowledge effectively, while mitigated the typical degradation of zero-shot performance on unseen tasks, notably improving results for the Mistral-7B model. 

- We highlight the advantages of fine-tuning smaller LLMs on specialized financial datasets, achieving strong performance without the extensive resource requirements typically associated with larger models. 

## **2 RELATED WORK** 

This section reviews recent studies that apply Large Language Models (LLMs) to domain-specific tasks. Prior to the rise of LLM-focused research, many studies concentrated on utilizing BERT, an encoder-only model, for improving performance through fine-tuning, developing self-attentive mechanisms, and incorporating multiple lexical knowledge sources to better capture semantic context, specially in the finance domain [10, 34, 39, 51, 59]. However, this paper 

Fameti et al. 

focuses on instruction fine-tuning, which leverages decoder-only LLM models optimized for generating text based on preceding context. 

## **2.1 Training from Scratch** 

Training domain-specific language models from scratch remains a straightforward method for achieving domain adaptation. BloombergGPT is an early example of large language models built specifically for the financial domain. It was trained on a blend of financial and general corpora, and showing high performance on financial tasks [50]. Similarly, other studies transformed large-scale raw domain-specific corpora into reading comprehension task, allowing LLMs to acquire domain knowledge and improve prompting capabilities [6]. However, training from scratch demands substantial computational resources and large dataset, making it less practical than other methods such as In-Context Learning (ICL) or fine-tuning, which require fewer resources [56]. 

## **2.2 In-context Learning** 

Scaling model size and leveraging extensive pre-training data have unlocked emergent capabilities in LLMs, such as In-Context Learning (ICL) [3, 8, 49]. This allows models to learn from a few in-context provided instructed examples without requiring full retraining [37]. Proprietary models like ChatGPT and GPT-4 have demonstrated strong performance across various general tasks [43, 64, 66]. However, when applied to specialized domains like finance and social media, their performance often lags behind that of fine-tuned models like BERT, particularly for tasks requiring deeper semantic understanding [48]. Increasing the number of in-context examples can also lead to performance degradation in certain domain-specific tasks [64]. 

In finance, Li et al. [24] examined the performance of ChatGPT and GPT-4 across several financial text analytics tasks. Another study enhanced financial sentiment analysis using semi-supervised learning and Chain-of-Thought reasoning to improve accuracy with minimal prompting [9]. Although these models outperform some domain-specific models in certain tasks, they struggle with tasks like named-entity recognition and headline classification, which require deeper semantic analysis. These limitations motivate our research into the performance of open-source instruction-tuned models in the finance domain. 

## **2.3 Instruction Fine-tuning** 

Instruction fine-tuning is a resource-efficient approach for adapting LLMs to specific tasks. It allows models to adjust to domain-specific needs without the need for extensive retraining [37, 63]. This technique has proven effective across domains like medicine, law, and social sciences, where fine-tuned models often outperform general-purpose models like GPT-4 [7, 19, 23, 27, 60, 65]. 

In the finance domain, several studies have applied instruction fine-tuning to models like LLaMA using financial datasets. Xie et al. [54] fine-tuned LLaMA on 136k task-specific instruction samples, including sentiment analysis, named-entity recognition, question answering, and stock movement prediction, achieving results comparable to GPT-4. Yang et al. [56] developed an end-to-end framework for training and deploying FinLLMs in the finance sector using Low-Rank Adaptation (LoRA) to fine-tune LLaMA and ChatGLM models using 50k data points from news articles, social media posts, Sec fillings and stock movement predictions. Zhang et al. [61] also applied fine-tuning to financial 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

classification tasks, focusing on sentiment analysis. 

However, these studies have mainly focused on fine-tuning the LLaMA model, often overlooking other smaller, open-source LLMs. Moreover, these studies focus on fine-tuning base models which typically require large supervised instruct-created datasets [45]. To overcome data scarcity limitations, Xie et al. [54] augmented the data by multiple instructions per sample to enhance training, though this increased computational costs. Recently released instructiontuned models, already trained on diverse tasks, may offer a more efficient alternative by bypassing the need for such extensive data augmentation. To address this research gap, our study fine-tunes both base and instruction-tuned variants of three robust small LLMs (Llama3, Mistral-7B, and Phi-3) on four financial classification tasks using a consistent amount of training data. 

## **2.4 Merging Models** 

In addition, previous studies show that fine-tuning on domain-specific data can degrade performance on unseen tasks. To address this, some researchers in non-financial domains have incorporated both generic and domain-specific instruction data, but this adds significant computational costs [46, 47]. In the finance domain, [54, 61] have shown that fine-tuning improves performance on trained datasets, however, these studies have not examined performance on unseen finance-related tasks. To fill this gap, we evaluate the performance of fine-tuned models on three unseen finance-related datasets. In contrast, our study takes a more efficient approach: rather than augmenting training data with generic datasets, we fine-tuned instruction models on each task individually and applied the MergeKit framework to combine the single-task fine-tuned models with the vanilla instruction model, thus preserving performance on unseen tasks while minimizing computational overhead. 

|**Dataset**|**Used for**|**Task**|**# Labels**|**Data size**|**Example labels**|
|---|---|---|---|---|---|
|FPB|Train, test of ICL, FT|Sentiment analysis|3|4,845|negative,<br>neutral,<br>positive|
|FiQA-SA|Train, test of ICL, FT|Sentiment analysis|3|1,173|negative,<br>neutral,<br>positive|
|Headline-Dir|Train, test of ICL, FT|News headline classi-<br>fication|3|9,277|up, down, stable|
|FinRED|Train, test of ICL, FT|Relation extraction|29|1,070|employer, industry,<br>owner|
|FOMC|Train, test of ICL, FT|Hawkish-dovish<br>classification|3|496|hawkish,<br>neutral,<br>dovish|
|FinArg-AUC-T1|Evaluation on un-<br>seen data|Argument unit clas-<br>sification|2|969|claim, premise|
|M&A|Evaluation on un-<br>seen data|Deal<br>completeness<br>classification|2|500|complete, rumour|
|FinCausual‘20-T1|Evaluation on un-<br>seen data|Causal classification|2|800|causal, noise|



Table 1. Dataset size and number of labels of datasets used in our experiments 

Fameti et al. 



<!-- Start of picture text -->
Sentiment AnalysisFPB, FISAQA LLM Answer Sentiment AnalysisFPB, FISAQA<br>Relation ExtractionFinred LLM Answer Relation ExtractionFinred<br>LLM Answer<br>Headline ClassificationNews Headline LLM Answer Headline ClassificationNews Headline<br>FOMC ClassificationFOMC LLM Answer FOMC ClassificationFOMC<br>a) b)<br>Sentiment AnalysisFPB, FISAQA LLM<br>Relation ExtractionFinred LLM<br>Headline ClassificationNews Headline LLM Merged LLM<br>FOMC ClassificationFOMC LLM<br>Base<br>c)<br><!-- End of picture text -->

Fig. 1. The three approaches used in this work a) single task fine-tuning, b)Multi-task fine-tuning c)Merging with vanilla models 

## **3 EXPERIMENT SETUP** 

In this section, we provide a detailed overview of the experimental setup used for both in-context learning (ICL) and fine-tuning experiments. This setup includes the selection of models, the configuration of training parameters, and the choice of datasets, all carefully designed to assess the effectiveness of various approaches in adapting large language models to domain-specific financial tasks. By standardizing these conditions, we aim to ensure a fair comparison between different techniques, ultimately highlighting the strengths and limitations of each method in enhancing model performance across specialized financial text classification tasks. 

## **3.1 Models** 

We conduct ICL and fine-tuning experiments using various open-source small models to examine the effects of different model sizes and pre-training datasets. All models employed in this study utilize a decoder-only transformer architecture. We selected three open-source models because they are among the most powerful small-size open-source models available. We fine-tune both the instruct and base models for the Llama3 and Mistral models, and only the instruct model for the Phi3 model since the base model was not available. It should be noted that ICL experiments were exclusively conducted on the instruct models. 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

- (1) **Llama3-8B** [17]: This latest version from the Llama family is pre-trained on 15 trillion tokens. Compared to its predecessor (e.g. Llama-2), it features a larger tokenizer and a higher-quality training dataset obtained through an enhanced data-filtering pipeline. The instruction-fine-tuned variant of this model has undergone a combination of supervised fine-tuning (SFT), rejection sampling, proximal policy optimization (PPO), and direct preference optimization (DPO). 

- (2) **Mistral-7B** [22]: The smallest model in the Mistral family, this 7-billion parameter model is fine-tuned to achieve performance surpassing that of all other models of similar size on the MT-Bench benchmark. 

- (3) **Phi-3-mini-Instruct** [1]: This model, with 3.8 billion parameters, is pre-trained on 3.3 trillion tokens. We utilized the instruction-fine-tuned version, which incorporates post-training processes like supervised fine-tuning and direct preference optimization to enhance instruction-following capabilities. 

## **3.2 Tasks and Datasets** 

We conduct ICL and fine-tuning experiments on four financial text classification tasks: sentiment analysis, relation extraction, news headline classification, and hawkish-dovish classification<sup>1</sup> . Details of the dataset are provided in Table 1, and splitting methods and statistics are presented in Table 22 in appendix .1. 

**Sentiment Analysis** is a critical tool in finance, used to predict market trends and investment behavior by analyzing news and social media data [24, 32]. Timely extraction of sentiment from these sources is crucial for decision-making by traders and investors. Following BloombergGPT’s method [50], we use two sentiment datasets, reserving 20% of the labeled data for testing. 

- (1) Financial PhraseBank [30]: Financial PhraseBank [30]: This dataset contains sentiment classifications (positive, negative, neutral) derived from financial news, annotated by 5-8 individuals. We focus on the subset with at least 50% agreement among annotators. 

- (2) FiQA Sentiment Analysis [58]: This dataset comprises 961 samples, each annotated with one of three labels: positive, neutral, or negative. 

**News Headlines Classification** focuses on extracting actionable information from news beyond basic sentiment analysis, which is valuable for investors, policymakers, and market practitioners. Utilizing the Headlines dataset [42] with 11,412 annotated news headlines about "gold" from 2000 to 2019, we extract additional dimensions like price movements. Specifically, we focus on a subset converting it into a three-class dataset identifying gold prices as Up, Down, or Stable. 

**Hawkish-Dovish Classification** involves categorizing Federal Open Market Committee (FOMC) monetary policy statements as either hawkish or dovish. This classification is significant due to its impact on financial market returns. Conventional sentiment analysis models, which typically categorize text as positive or negative, struggle to capture the nuanced policy stance in these texts accurately. As mentioned in the study, for example, a sentence containing the word "increase" could be either dovish or hawkish depending on context, without necessarily conveying negativity. To address this challenge, we utilized a dataset where FOMC statements were annotated as Hawkish, Dovish, or Neutral, following the splitting method outlined in the original study [38]. 

**Relation extraction** plays a crucial role in financial text analysis by identifying relationships between entities, which supports tasks like knowledge graph creation, question answering, and semantic search. FinRed dataset focuses on this task and identifys relationships in financial news and earnings transcripts. We transform the dataset into a 

1Some of these dataset were obtained from the HuggingFacehttps://huggingface.co/TheFinAI and https://huggingface.co/FinGPT 

Fameti et al. 

classification task that identifies the relationship between two entities in a sentence, categorizing 29 relation classes such as "subsidiary" and "manufacturer". We reserve 20% of the data for testing purposes [40]. 

## **3.3 Unseen Tasks and Datasets** 

To assess the generalizability of our fine-tuned models, we evaluated their performance on three unseen tasks. Details of the dataset are provided in Table 1, and in Table 22 in appendix .1 

**Argument Unit Classification** goes beyond sentiment analysis by exploring the detailed elements of market dynamics and financial events. It entails identifying and categorizing specific units or segments of arguments within earnings conference call data. This classification is fundamental for a detailed breakdown of financial narratives, facilitating better comprehension and analysis. We used FinArg AUC dataset to classify sentences as either claims or premises, facilitating a more nuanced analysis of financial narratives [44]. 

**Causal Classification** identifies implicit causal relationships within financial documents. Using the SC dataset, sentences from financial news and Securities and Exchange Commission (SEC) filings were classified as either causal or noise, highlighting the underlying causes that influence market trends [31]. 

**Deal Completeness Classification** focuses on determining the status of mergers and acquisitions (M&A) events, distinguishing between completed deals and ongoing rumors. The dataset includes news articles and tweets related to M&A events, with each instance describing a potential deal between an acquirer and a target company, including IPO rumors. Each instance is categorized as either complete (successful deal) or rumor (no deal materialized). This task is crucial due to the impact of M&A deal rumors on the share price volatility of target firms, influencing cumulative abnormal returns [57]. 

## **3.4 Methodology** 

In this section, we outline the methodologies employed in our study, beginning with a brief introduction to the setup of instruction tuning for both base and instruct models. Finally, we describe the merging framework that combines task-specific and base models to enhance generalizability. 

_3.4.1_ **Instruction Dataset for Instruct Models** _._ We adopt the methodology outlined in [47] to create detailed instructions that aid the model in understanding various tasks. Each task instance in our instruction dataset is structured with three main components: task instruction, input text, and output. 

The task instruction provides a guide for the task to be performed based on the input text, along with the expected labels for each task. A comprehensive list of task instructions for each task is provided in Table 25 in Appendix .1. We then create each sample from the original dataset by combining the instruction, input, and output in a specific format. 

For the Instruct models, we generate a prompt for each model by including the special tokens specified in Table 23 in Appendix .1. For test datasets, we enclose the instructions and input within the corresponding special tokens for each model, while using label delimiters like "label:" as suggested in [26]. 

_3.4.2_ **Instruction Dataset for Base Models** _._ Following the approach of [45], we designed an instruction scheme to aid the model in understanding the task. As detailed in Table 24 in Appendix .1, the instruction scheme includes a 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

generic instruction, an instruction field to guide task completion, and task-specific instructions as shown in Table 25 in Appendix .1. The scheme also features an input field and a response field that the LLMs are required to complete. 

_3.4.3_ **Instruction Fine-tuning** _._ We conducted instruction fine-tuning on all three models using HuggingFace Transformers with 2 epochs and the Adam-w torch fused optimizer. The batch size was set to 2, with an initial learning rate of 2e-4 and warm-up steps comprising 3% of all training steps. The maximum length of input texts was 1024 for the Phi-3 model and 2048 for the Mistral-7B and Llama3-8B models. All models were fine-tuned on 8 A100 40GB GPUs. 

To optimize the fine-tuning process and reduce the computational cost, we employed techniques such as Low-Rank Adaptation (LoRA) with a rank set to 32 and Lora alpha set to 46, alongside quantization [18]. LoRA enables fine-tuning the low-rank decomposed factors of the original weight matrices rather than the full matrices, significantly reducing trainable parameters. This approach allows training on less powerful hardware and shortens the total training time [25]. We experimented with two fine-tuning settings: 

- (1) **Single-Task Fine-Tuning** : Each model underwent separate fine-tuning on the dataset specific to each task, as depicted in Figure 1a, utilizing the specified training settings. These fine-tuned models are subsequently employed in the next section (Model Merging) to enhance the generalizability of the models on the unseen tasks. 

- (2) **Multi-Task Fine-Tuning** : Each base and instruct model underwent fine-tuning using a combination of instruction datasets, covering all tasks, as depicted in Figure 1b. The total dataset consists of 13,194 training examples, as outlined in Table 22 in Appendix .1. 

_3.4.4_ **Model Merging** _._ Further fine-tuning of pre-trained models can lead to catastrophic forgetting, degrading general capabilities and reducing performance across tasks [63, 65]. To mitigate this, leveraging existing pre-trained checkpoints is crucial. Model merging, combining parameters from multiple models trained on specific tasks into a unified model, has become essential. This strategy supports multi-task and continual learning, reducing catastrophic forgetting without retraining costs [15, 55]. 

Our study utilized MergeKit, a library for model merging, employing Task Arithmetic [20]. This technique involves arithmetic on task vectors, representing differences between fine-tuned models and a common base model. Task Arithmetic enhances generalizability and performance across diverse tasks, effectively mitigating catastrophic forgetting [15]. We utilize single-task fine-tuned models on LlaMA3-8B and Mistral-7B models, as described in the previous section, and merge them with the vanilla instruct models for the corresponding models (LlaMA3-8B and Mistral-7B) with equal 25% weight for each of the models<sup>2</sup> , as shown in Figure 1c. 

_3.4.5_ **Baseline Models** _._ We compare the fine-tuned and merged models against three baseline vanilla instruct models and three specialized financial models: 

- (1) FinMA-7B [54]: A 7B parameter model instruction-fine-tuned for financial tasks, including multiple NLP and forecasting tasks. 

- (2) AdaptLLM-7B [6]: A model continued pre-trained and fine-tuned on financial news. 

- (3) GPT-4<sup>3</sup> : A robust model from OpenAI. 

In the next section, we will review the results of our experiments in detail, focusing on the comparative performance of the models under different settings, including zero-shot, few-shot, and multi-task fine-tuning scenarios. We will also 

> 2we were unable to perform model merging for the Phi-3-Instruct model because the Language Model head was updated during fine-tuning and did not match the vanilla model. 

3We used the GPT-4 model from checkpoint preview of gpt-4-1106-preview and following website https://platform.openai.com/docs/models 

Fameti et al. 

analyze how these models handle unseen tasks and assess the impact of model merging techniques on improving their generalization capabilities. Our analysis will highlight key trends, identify strengths and weaknesses of each approach, and offer insights into the effectiveness of fine-tuning strategies for enhancing performance on domain-specific financial tasks. 

|**Model**|**# example**|**FP**|**B**|**FiQA**|**-SA**|**Headline-Dir**|**FOMC**|
|---|---|---|---|---|---|---|---|
|||**Acc**|**F1**|**Acc**|**F1**|**F1**|**F1**|
||One-shot|75.5|75.1|72.5|74.8|89.1|52.8|
|_l_|Five-shot|72.7|73.4|73.3|74.4|88.7|53.2|
|_Lama3-8B_|ten-shot|68.9|70.5|66.1|74.7|88.1|53.6|
||One-shot|74.8|72.7|48.4|57.3|86.5|59.6|
|_Mistral-7B_|Five-shot|74.9|71.4|47.9|54.1|85.6|54.1|
||ten-shot|68.5|69.9|37.1|53.4|84.5|49.9|
||One-shot|58.8|58.6|60.4|59.5|88.6|52.9|
|_Phi-3-mini_|Five-shot|49.8|47.7|53.6|47.|87.3|46.1|
||ten-shot|26.5|51.2|51.3|49.5|81.1|39.3|



Table 2. Few-shot experiment results on the FBP, FiQA-SA, Headline-Dir, and FOMC datasets using the Llama3-8B, Mistral-7B, and Phi-3-mini instruct models. Results for the FinRED dataset are excluded due to its large label space, which resulted in very low performance (below 5%). 

## **4 RESULTS AND ANALYSIS** 

In this section, we present a comprehensive analysis of the model performance across various experimental setups, including zero-shot, few-shot, multi-task fine-tuning, and model merging techniques. We also provide a detailed error analysis and summarize the key findings. 

_4.0.1_ **Evaluation Framework** _._ Following standard practices, We evaluate the models using standard classification metrics such as accuracy, and weighted F1 score to assess their performance on financial text classification tasks. The tasks include sentiment analysis, relation extraction, news headline classification, and hawkish-dovish classification. All results are compared against baseline models, including state-of-the-art models like GPT-4 and FinMA-7B, to provide a benchmark for evaluating improvements. We also report and discuss the results of based-fine-tuned, instruct-fine-tuned, and merged models compared to the baselines across four datasets. 

## **4.1 Zero-Shot Performance Analysis** 

As shown in Figure 3 and Table 3, the zero-shot performance of the vanilla instruct models (Phi-3, Mistral, and Llama3) was relatively strong on the Financial PhraseBank (FPB), FiQA Sentiment Analysis (FiQA-SA), and headline classification datasets. The Llama3 and Phi-3 models demonstrated notable accuracy in these tasks, while the Mistral model performed below 50% on datasets that included tweets, likely due to its pre-training corpus lacking similar data. 

However, all models struggled on the FOMC and FinRed datasets, showing suboptimal results. The FOMC dataset’s complex monetary policy texts and the FinRed dataset’s extensive label set of 29 categories posed significant challenges, even for the larger Llama3 model. This performance issue likely stems from the long-tail distributions and the intricate 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 



Fig. 2. Few-shot experiment results (Accuracy) on the FBP, FiQA-SA, Headline-Dir, and FOMC datasets using the Llama3-8B, Mistral7B, and Phi-3-mini instruct models. Results for the FinRED dataset are excluded due to its large label space, which resulted in a low performance (below 5%). 

nature of relation extraction tasks that are not well-represented in the models’ instruction-tuned training. These findings align with prior observations that such datasets require specialized fine-tuning for optimal performance [47, 48]. 

On both the FOMC and FinRed datasets, all models exhibited subpar performance. We attribute the poor performance on the FOMC dataset, which contains monetary policy texts, to the texts being more long-tailed compared to other 

, Fameti et al. 



Fig. 3. Performance comparison of vanilla models (zero-shot instruct models), multi-task fine-tuned instruct models, multi-task fine-tuned base models, and GPT-4 models on five financial classification datasets for Llama3-8B and Mistral-7B models. F1 score is reported. 



Fig. 4. Performance comparison of vanilla models (zero-shot instruct models), multi-task fine-tuned instruct models, and GPT-4 models on five financial classification datasets for Phi-3 model. F1 score is reported. 

datasets in the pre-training phase, thereby making the downstream task more challenging. This observation aligns with findings from [48]. The FinRed dataset, characterized by its large label space (29 labels) and intricate relation extraction tasks, presented substantial challenges. These difficulties likely stem from these tasks not being adequately covered in the instruction-tuned training, which is consistent with the findings of [47]. 

Notably, even the Llama3 model, despite its superior architecture and high-quality training data, performed below 10% on this dataset. This might be due to its strict adherence to instruction-tuned behavior, focusing solely on generating labels without the added contextual explanations that other models like Mistral-7B and Phi-3 provided alongside the labels, possibly due to their Chain-of-Thought (CoT) post-training. 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

|**Experiment**|**Model**|**F**|**PB**|**FiQ**|**A-SA**|**Headline-Dir**|**FinRED**|**FOMC**|**FinArg**|**M&A**|**SC**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||**Acc**|**F1**|**Acc**|**F1**|**F1**|**F1**|**F1**|**F1**|**F1**|**F1**|
||BloombergGPT|-|51.2|-|75.2|-|-|-|-|-|-|
|_Bli Mdl_|AdaptLLM-7B|-|62.5|-|72.1|-|-|-|-|-|-|
|_asene oes_|FinMA-7B|86.0|86.1|78.3|79.2|-|-|49.0|27.5|45.3|-|
||GPT-4|80.4|80.6|71.9|75.7|83.4|31.2|65.8|-|-|-|
||Llama3-8B|77.5|76.7|71.1|72.9|72.3|6.5|47.4|50.2|85.9|66.7|
|_Vanilla Models_|Mistral-7B|73.4|69.8|45.9|54.8|77.6|20.5|38.6|42.2|83.6|68.8|
||Phi-3-mini|72.8|72.9|72.7|74.8|87.1|24.8|48.5|54.1|80.1|66.5|
||Llama3-8B|79.1|79.4|87.2|85.3|95.3|69.1|68.7|23.4|72.5|52.6|
|_MT-Base-FT_|Mistral-7B|86.8|86.6|85.5|85.1|95.5|76.4|67.1|13.4|70.9|31.8|
||Llama3-8B|86.2|86.3|86.4|86.6|95.9|73.4|68.4|31.1|72.9|39.2|
|_MT-Instruct-FT_|Mistral-7B|86.3|86.2|85.1|83.9|95.2|69.4|70.2|35.1|76.1|57.6|
||Phi-3-mini|84.7|84.1|79.5|81.5|95.6|67.2|66.5|53.5|77.7|64.9|
|_Md Mdl_|Llama3-8B|80.6|80.7|75.3|78.3|93.2|44.6|60.9|54.6|74.3|65.5|
|_erge oes_|Mistral-7B|80.4|80.3|65.1|72.1|91.6|41.2|38.9|50.4|83.5|59.6|



Table 3. Main experimental results for four financial classification tasks and three unseen financial classification tasks (FinArg, M&A, Casual-SC). Vanilla models indicate the zero-shot performance of instruct models. MT-Base-FT refers to multi-task fine-tuned base models, and MT-Instruct-FT refers to multi-task fine-tuned instruct models. Baseline models’ results: BloombergGPT results are taken from [50], AdaptLLM-7B results are obtained from [6], and FinMA-7B results are taken from [54]. The best results are in **bold** . 

## **4.2 Few-Shot Results** 

To explore the impact of few-shot learning, we conducted experiments using 1-shot, 5-shot, and 10-shot setups, employing three different random seeds for sampling demonstration examples, following the methodology in [48] and reported the average performance. The few-shot results, compared against zero-shot results, are summarized in Figure **??** and Table 2. 

We observed that 1-shot prompting generally improved model performance across most datasets, except for the Phi3-mini model, where performance slightly decreased on sentiment analysis tasks due to the adverse effects of unrelated examples on smaller language models. Increasing the number of shots to 5 and 10 produced mixed results: while some models like Llama3-8B and Mistral-7B showed only slight declines, others, particularly Phi-3-mini, experienced high variability in performance, indicating its sensitivity to the number of examples used. 

Notably, all models demonstrated a significant drop in performance on the headline classification dataset when the number of demonstrations increased, even falling below the performance in the zeros-shot setting. This decline suggests that few-shot settings can sometimes introduce noise, leading to a decrease in model accuracy, particularly for smaller models [64]. 

However, models like Llama3-8B and Mistral-7B displayed only slight decreases on other datasets. Among all models, Phi-3-mini showed the highest performance variability when the number of demonstrations increased, underscoring the sensitivity of smaller models to few-shot settings, as previously highlighted in the literature [64]. Due to consistently 

Fameti et al. 

low performance on the FinRed dataset, which did not exceed 10%, we excluded these results from our analysis, aligning with findings that suggest an increase in input complexity can adversely affect model accuracy on tasks with large label sets[64]. 

## **4.3 Multi-Task Fine-Tuning** 

Our multi-task fine-tuning experiments demonstrated more stable behavior across models, as illustrated in Table 3 and Figures 3 and 4. Fine-tuning led to a substantial increase in model performance compared to zero-shot settings in both base and instruct models. Notably, the instruct fine-tuned Llama3-8B model showed a dramatic improvement from 6.5% to 73.4% on the relation extraction task (FinRED dataset), with similar gains observed in the Hawkish-Dovish classification tasks (FOMC dataset). Mistral-7B and Phi-3 models showed an average 40% performance improvement after fine-tuning on both base and instruct models. 

Additionally, all models outperformed GPT-4 on these finance-related tasks, highlighting the limitations of GPT-4 in specialized domains such as finance and the necessity for task-specific fine-tuning. In sentiment analysis tasks (FPB and FiQA-SA datasets), our models performed comparably to the state-of-the-art FinMA-7B model, surpassing other models like AdalpLLM-7B and BloombergGPT. 

The results indicated that multi-task fine-tuned instruct models outperformed their base counterparts across all datasets, except the Mistral-7B base model, which slightly outperformed the instruct variant on most tasks. This variance could be attributed to differences in the quality of supervised fine-tuning prompts, suggesting that starting with a robust instruction-tuned checkpoint may offer advantages for domain-specific fine-tuning. 

The results of the multi-task fine-tuned Phi-3 models also demonstrate performance on par with the other two models, despite having only 3.8 billion parameters. This highlights the potential of the Phi-3 model for fine-tuning downstream financial tasks. 

## **4.4 Generalization Multi-Task Fine-Tuned model to Unseen Tasks** 

The almost similar behavior observed in the multi-task fine-tuning of base and instruct models (using the same amount of data without incorporating generic instruction data) on seen tasks indicates that both models benefit nearly equally from fine-tuning on tasks present in the training corpus. However, our results on three unseen financial tasks, as shown in Table 3 and Figures 5 and 6, indicate that multi-task fine-tuned base models exhibit significantly greater performance declines compared to their instruct-tuned counterparts when generic instruction data is absent during fine-tuning. This highlights the risk of performance degradation for base models on tasks they haven’t encountered, a trend consistent with prior research on catastrophic forgetting [46, 65]. In contrast, instruct-tuned models retain stronger generalization capabilities, making them more robust in handling unseen tasks. 

For example, on the Argument Unit Classification task, the Llama3-8B model’s performance drops to 13.4%, while on the Causal Classification task, the Mistral-7B model experiences a decline to 31.8%. Notably, the Phi-3-mini model, despite its smaller size of 3.8 billion parameters, shows only a 2% performance drop, suggesting that it retains its general capabilities better than larger models after fine-tuning. These findings emphasize the effectiveness of instruct-tuned 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

## models in maintaining performance across unfamiliar tasks. 

Overall, while multi-task fine-tuning significantly improves performance on tasks within the training data, it can also increase the risk of overfitting and catastrophic forgetting, particularly when generic instruction data is not included in the training process. These results underscore the importance of diverse instruction data in enhancing a model’s ability to generalize effectively across unseen tasks. 



Fig. 5. Performance comparison of vanilla models (zero-shot instruct models), multi-task fine-tuned instruct models, multi-task fine-tuned base models, and merged models on three unseen datasets for Llama3-8B and Mistral-7B models. F1 score is reported. 



Fig. 6. Performance comparison of vanilla models (zero-shot instruct models) and multi-task fine-tuned instruct models on three unseen datasets for the Phi-3 model. F1 score is reported. 

Fameti et al. 

## **4.5 Merged Models** 

To mitigate the degradation of zero-shot performance on unseen tasks, we utilized the MergeKit framework (arithmetic method), which combines single-task fine-tuned models with the vanilla instruct model. The merging approach significantly enhances performance on unseen tasks, with results often surpassing the original zero-shot performance, significant for the FinArg dataset. 

The results for the Llama3-8B and Mistral-7B models are shown in Figure 5. For example, the merged models outperformed both the fine-tuned, base models and zero-shot in handling complex tasks, suggesting that the integration of diverse task knowledge leads to a more generalized and robust performance. The performance of single-task fine-tuning on both base and instruct models is presented in Appendix .2. 

The merging strategy helps to preserve the benefits of fine-tuning while reducing the risk of catastrophic forgetting on unseen datasets without incorporating a generic instruction dataset, which increases computational cost and time. While fine-tuning improves performance over base models, merging fine-tuned models further enhances their ability to handle unseen tasks by a) Combining diverse knowledge sources, b) Reducing overfitting, and c) Leveraging complementary strengths of different models. The regularization effect from merging also helps to produce a more generalized and robust model performance across diverse tasks. 

We can also observe that the performance drop of the Phi3 base model compared to its fine-tuned counterpart is not much compared to the other two models (Llama3 and Mistral), as indicated in 6. This could be due to the following reasons. 

- Model Architecture: Phi3 may have an architecture that is more resistant to overfitting during fine-tuning. It’s possible that Phi3 has better built-in regularization mechanisms or a structure that promotes better generalization. 

- Pre-training Approach: The pre-training approach used for Phi3 might result in more robust general knowledge that is less easily overwritten during fine-tuning. This could lead to better retention of broad capabilities even after task-specific training. 

- Model Size: If Phi3 is a smaller model compared to Mistral and Llama3, it might have less capacity to overfit to the fine-tuning data, paradoxically leading to better generalization on unseen tasks. 

The significant performance drops in Mistral and Llama3 suggest that these models might be more susceptible to overfitting during fine-tuning, possibly due to larger model sizes, different architectures, or fine-tuning approaches that allow for more dramatic changes to the model’s parameters. This difference highlights the importance of careful fine-tuning practices and the need to consider the trade-offs between task-specific performance and general capabilities when adapting large language models to specific tasks. It also demonstrates why techniques like model merging can be valuable in recovering and combining the strengths of different model versions. 

## **4.6 Error Analysis and Model Insights** 

Our error analysis reveals significant improvements in fine-tuned models across various tasks, particularly in financial sentiment detection, relation extraction, news headline classification, and hawkish-dovish classification. These enhancements stem from the models’ increased ability to capture domain-specific nuances, understand hierarchical corporate structures, and interpret economic indicators. In financial sentiment detection, fine-tuned models excel at identifying subtle cues and handling mixed sentiments more effectively. For relation extraction and news headline classification, fine-tuning leads to a better interpretation of corporate ties and financial movements. Similarly, in the hawkish-dovish 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

classification, the models display a stronger grasp of monetary policies and their economic implications. Below, we provide detailed case studies involving Phi-3, Mistral, and Llama3 models, highlighting performance improvements across these key areas. 

_4.6.1 Financial Sentiment Classification Result Analysis._ Fine-tuning yielded significant performance gains in financial sentiment classification, particularly in the following areas: 

_1. Domain-Specific Knowledge._ Fine-tuned models demonstrated improved comprehension of financial language and context. For example, in Table 4, fined-tuned models correctly interpreted growth statements in a financial context, where the base models failed to capture the nuance. 

**Sentence:** "Finnish Bore that is owned by the Rettig family has grown recently through the acquisition of smaller shipping companies." **Ground Truth Label:** Positive **Model Predictions:** Phi-3 Base: Neutral, Phi-3 Fine-tuned: Positive Mistral Base: Neutral, Mistral Fine-tuned: Positive Llama3 Base: Neutral, Llama3 Fine-tuned: Positive 

Table 4. Domain-Specific Knowledge Example - FPB dataset 

_2. Improved Sentiment Detection._ Fine-tuned models showed enhanced capability in detecting subtle sentiment cues within financial statements, such as recognizing negative sentiment related to financial losses, as illustrated in Table 5. 

**Sentence:** "Finnair said that the cancellation of flights would cause daily losses of<sup>=</sup> C2.5 million US$3 million." **Ground Truth Label:** Negative **Model Predictions:** Mistral Base: Neutral, Mistral Fine-tuned: Negative Llama3 Base: Neutral, Llama3 Fine-tuned: Negative Phi-3 Base: Neutral, Phi-3 Fine-tuned: Negative 

Table 5. Improved Sentiment Detection Example - FPB dataset 

_3. Better Handling of Mixed Sentiment._ When encountering statements containing positive and negative elements, fine-tuned models, particularly Mistral, identify the prevailing sentiment better, as shown in Table 6. 

**Sentence:** "Kalnapilio-Tauro Grupe, which is owned by Denmark’s Royal Unibrew, raised its market share... by 14.5 <u>percent</u> to 40.5 million liters." **Ground Truth Label:** Positive **Model Predictions:** Phi-3 Base: Positive, Phi-3 Fine-tuned: Positive Mistral Base: Neutral, Mistral Fine-tuned: Positive Llama3 Base: Positive, Llama3 Fine-tuned: Positive 

Table 6. Better Handling of Mixed Sentiment Example - FPB dataset 

Fameti et al. 

_4. Reduced Tendency to Default to Neutral._ Fine-tuned models show greater confidence in assigning sentiment to complex statements, often correctly identifying positive or negative impacts in financial contexts where base models defaulted to neutral, as demonstrated in Table 7. 

**Sentence:** "The transaction will have a positive impact of around EUR2m on earnings, which Ruukki will recognize during the fourth <u>quarter."</u> **Ground Truth Label:** Positive **Model Predictions:** Phi-3 Base: Neutral, Phi-3 Fine-tuned: Positive Mistral Base: Neutral, Mistral Fine-tuned: Positive Llama3 Base: Neutral, Llama3 Fine-tuned: Positive 

Table 7. Reduced Tendency to Default to Neutral Example - FPB dataset 

_5. Understanding of Financial Metrics._ Fine-tuned models exhibited an enhanced ability to interpret financial metrics and their implications, as evidenced in Table 8, where models accurately assessed financial performance indicators. 

**Sentence:** "Cash flow from operations rose to EUR 52.7 mn from EUR 15.6 mn in 2007." **Ground Truth Label:** Positive **Model Predictions:** Phi-3 Base: Positive, Phi-3 Fine-tuned: Positive Mistral Base: Neutral, Mistral Fine-tuned: Positive Llama3 Base: Positive, Llama3 Fine-tuned: Positive 

Table 8. Understanding of Financial Metrics Example - FPB dataset 

_4.6.2 FOMC Classification Result Analysis._ Fine-tuned models also showed marked improvements in interpreting monetary policy statements from the Federal Open Market Committee (FOMC). This was particularly evident in their ability to interpret economic indicators and broader economic contexts. 

_1. Understanding Economic Indicators._ Fine-tuned models better interpret the impact of economic indicators and the relationship between them like unemployment rates. 

For example, as illustrated in Table 9, the base models did not interpret the economic indicators correctly and classified this example as neutral. In contrast, fine-tuned models correctly identify it as Hawkish, recognizing that low unemployment and robust job gains typically lead to tighter monetary policy to prevent overheating. 

_2. Improved Contextual Interpretation._ Fine-tuned models show marked improvement in interpreting broader economic contexts. 

The example of table 10, indicates the base models often interpret the examples incorporating economic contexts as neutral, while fine-tuned models correctly identify it as Dovish, recognizing that “sustained expansion” typically implies a continuation of accommodative policy. 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

**Sentence:** "The unemployment rate edged down to 3.5 percent, and job gains have been robust in recent months." **Ground Truth Label:** Hawkish **Model Predictions:** Phi-3 Base: Neutral, Phi-3 Fine-tuned: Hawkish Mistral Base: Neutral, Mistral Fine-tuned: Hawkish Llama3 Base: Neutral, Llama3 Fine-tuned: Hawkish 

Table 9. Understanding Economic Indicators Example - FOMC dataset 

**Sentence:** "Inflation has been running persistently below the Committee’s longer-run <u>goal</u> of 2 <u>percent."</u> **Ground Truth Label:** Dovish **Model Predictions:** Phi-3 Base: Neutral, Phi-3 Fine-tuned: Dovish Mistral Base: Neutral, Mistral Fine-tuned: Dovish Llama3 Base: Neutral, Llama3 Fine-tuned: Dovish 

Table 10. Improved Contextual Interpretation Example - FOMC dataset 

**Sentence:** "Although household spending has been rising at a strong pace, business fixed investment and exports remain weak." **Ground Truth Label:** Dovish **Model Predictions:** Phi-3 Base: Neutral, Phi-3 Fine-tuned: Dovish Mistral Base: Neutral, Mistral Fine-tuned: Dovish Llama3 Base: Hawkish, Llama3 Fine-tuned: Dovish 

Table 11. Reduced Misclassification of Complex Statements Example - FOMC example 

_3. Reduced Misclassification of Complex Statements._ Fine-tuned models display improvement in handling statements with mixed signals. 

Table 11 illustrates that base models often struggle with such mixed signals in complex statements, frequently defaulting to Neutral. Fine-tuned models are better at weighing these factors, often correctly identifying this as a Dovish statement due to the emphasis on weak areas of the economy. 

_4. Handling of Edge Cases._ Fine-tuned models show improved performance on edge cases or unusual phrasings that might confuse base models. 

|**Sentence:**<br>"The<br>Committee<br>will<br>be<br>patient<br>as<br>it<br>determines<br>what|future|
|---|---|
|adjustments to the target range for the federal funds rate may be approp|riate."|
|**Ground Truth Label:** Dovish||
|**Model Predictions:**||
|Phi-3 Base: Neutral, Phi-3 Fine-tuned: Dovish||
|Mistral Base: Neutral, Mistral Fine-tuned: Dovish||
|Llama3 Base: Neutral, Llama3 Fine-tuned: Dovish||



Table 12. Handling of Edge Cases Example - FOMC dataset 

Fameti et al. 

Example of table 12 shows base models often interpret sentences with unusual phrases as Neutral, while fine-tuned models correctly identify it as Dovish, recognizing that “patience” in this context often implies a willingness to maintain accommodative policy. 

_4.6.3 FinRED Dataset Error and Improvement Analysis._ In the domain of relation extraction from financial texts, fine-tuned models displayed significant improvements across several dimensions: 

_1. Domain-Specific Knowledge Acquisition._ Fine-tuned models have been exposed to a large volume of financial and corporate relationship data, allowing them to learn domain-specific nuances that base models may not have encountered. 

**Sentence:** "For more than 25 years, Stratasys Ltd. ( SSYS ) has been a defining force and dominant player in 3D printing and additive manufacturing – shaping the way things are made." 

**Ground Truth Label:** Product/material produced **Model Predictions:** 

Phi-3 Base: Developer, Phi-3 Fine-tuned: Product/material produced Mistral Base: Manufacturer, Mistral Fine-tuned: Product/material produced Llama3 Base: Manufacturer, Llama3 Fine-tuned: Product/material <u>produced</u> 

Table 13. Domain-Specific Knowledge Acquisition Example - FinRED dataset 

In the example of table 13, in the Stratasys-3D printing relationship, the fine-tuned models correctly identify the "product/material produced" relationship, understanding that Stratasys is a company that produces 3D printing technologies. The base models, lacking this specific industry knowledge, misclassify the relationship as "developer" or "manufacturer", which are less precise in describing the company’s role in the 3D printing industry. This demonstrates how fine-tuned models have acquired domain-specific knowledge about the 3D printing industry and the relationships between companies and their core technologies. 

_2. Contextual Interpretation._ Fine-tuned models develop an enhanced ability to interpret contextual cues within 

sentences, leading to more accurate relationship classification. 

**Sentence:** "Miner Glencore surged 9 percent, having dropped 30 percent in the <u>previous</u> session to an all-time low." **Ground Truth Label:** Industry **Model Predictions:** Phi-3 Base: None, Phi-3 Fine-tuned: Industry Mistral Base: Industry, Mistral Fine-tuned: Industry Llama3 Base: Owned by, Llama3 Fine-tuned: Industry 

Table 14. Contextual Interpretation Example - FinRED dataset 

The example of table 14, in the Glencore-mining case, the fine-tuned model correctly interprets "mining and trading company" to classify Glencore’s relationship to mining as "industry". The base model, possibly confused by the complex sentence structure, and misclassified this as a corporate structure relationship ("parent organization" or "subsidiary"). 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

**Sentence:** "Gucci owner Kering (Swiss: KER.SW - news) published its financial report for the <u>quarter."</u> **Ground Truth Label:** parent organization **Model Predictions:** Phi-3 Base: owner of, Phi-3 Fine-tuned: parent organization Mistral Base: owner of, Mistral Fine-tuned: parent organization Llama3 Base: owned by, Llama3 Fine-tuned: owned by 

Table 15. Hierarchical Relationship Understanding Example - FinRED dataset 

_3. Hierarchical Relationship Understanding._ Through exposure to various corporate structures, fine-tuned models better understand the nuances of organizational hierarchies and roles. 

In the case presented in table 15, the fine-tuned models identified the nuanced hierarchical relationship ("parent organization") between Kering and Gucci, while the base models defaulted to "owner," failing to capture the specific corporate structure. This shows the improved ability of fine-tuned models to comprehend the complexities of organizational hierarchies. This examples shows how fine-tuned models develop a deeper understanding of hierarchical relationships, particularly in corporate structures, where roles and organizational layers are not always straightforward. 

_4. Entity-Relationship Mapping._ Fine-tuned models develop a more sophisticated understanding of how different entities (companies, products, people) typically relate to each other in the corporate world. 

**Sentence:** "First Eagle is currently owned by members of the founding families." **Ground Truth Label:** Industry **Model Predictions:** Phi-3 Base: Owner of, Phi-3 Fine-tuned: Industry Llama3 Base: Owner of, Llama3 Fine-tuned: Industry Mistral Base: Owner of, Mistral Fine-tuned: Industry 

Table 16. Entity-Relationship Mapping Example - FinRED dataset 

The example of table 16 shows that the fine-tuned models correctly understood the ownership structure of First Eagle, while the base models confused the relationship and wrongly focused on ownership, highlighting the fine-tuned models’ better grasp of corporate entity-relationship mapping. 

_5. Reduction of Overgeneralization._ Fine-tuned models learn to avoid defaulting to common but incorrect relationships when faced with ambiguity, a problem often seen in base models. 

**Sentence:** "Saudi Arabian budget carrier flynas, which made a name for itself as a low-cost airline." **Ground Truth Label:** Product/material produced **Model Predictions:** Phi-3 Base: Manufacturer, Phi-3 Fine-tuned: Product/material produced Mistral Base: Manufacturer, Mistral Fine-tuned: Product/material produced Llama3 Base: Manufacturer, Llama3 Fine-tuned: Product/material <u>produced</u> 

Table 17. Reduction of Overgeneralization Example - FinRED dataset 

Fameti et al. 

In this case showen in table 17, the relationship between flynas and the products or services it provides, with the ground truth label being "product/material produced." Here, the base models overgeneralized the relationship by assuming that flynas was a "manufacturer," which is a common but incorrect assumption, while the fine-tuned models correctly captured the nuanced relationship of flynas producing a service (low-cost flights). 

_6. Handling of Complex Sentences._ Financial texts often contain complex, information-dense sentences. Fine-tuned models learn to parse these more effectively. 

**Sentence:** "Excluding $4.4 million of costs associated with the strategic restructuring initiative recorded in the six months ended June 30, 2019, our selling, general and administrative expenses increased $6.4 million primarily due to increased selling and marketing expenses in connection with the commercial launch of ANJESO." **Ground Truth Label:** Industry **Model Predictions:** Phi-3 Base: Product/material produced, Phi-3 Fine-tuned: Industry Mistral Base: Marketing, Mistral Fine-tuned: Industry Llama3 Base: None, Llama3 Fine-tuned: Industry 

Table 18. Handling of Complex Sentences Example - FinRED dataset 

In the example of table 18, despite the complexity of this financial statement, the fine-tuned models correctly identify the relationship between the company and its industry. They focus on the relevant information about selling and marketing expenses, inferring an industry relationship. The base models either misclassify or fail to identify any relationship in this complex sentence. 

Through these case studies, it’s evident that fine-tuning significantly improves model performance across various financial and economic tasks. Fine-tuned models exhibit better sentiment detection, relationship extraction, and contextual understanding, leading to more accurate predictions and analyses. However, fine-tuning LLM models can lead to catastrophic forgetting and compromise the model performance on unseen tasks which can be improved by using techniques such as merging models. 

_4.6.4 Merging Models for Improved Performance on unseen tasks-datasets._ Merging models helps improve performance on unseen tasks for several reasons. 

_1. Diverse knowledge integration._ Merged models combine knowledge from multiple models trained on different tasks 

or datasets, allowing them to leverage a broader range of information and patterns. 

**Sentence from M&A dataset:** "Autodesk, a maker of design and architecture software, has reached an agreement to acquire construction technology start-up PlanGrid for USD 875.00 million net of cash." **Ground Truth Label:** Rumor **Model Predictions:** Llama3 Base: Complete, Llamma3 Fine-tuned: Rumor Mistral-Llama3 Merged: Complete 

Table 19. Example of Merging Models to Handle Unseen Tasks from M&A dataset 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

For the above entry, the Llama3 fine-tuned model incorrectly classified it as a rumor, while both the base and merged models correctly identified it as complete. This suggests that the fine-tuned model might have overfit to certain patterns, while the merged model was able to correct this error. 

_2. Reduced Overfitting and Regularization._ Merging can act as a form of regularization, helping to average out overspecialized patterns and less likely to overfit to specific patterns in the fine-tuning data. It promotes more general features, making the models more robust on unseen tasks. 

**Sentence from FinArg dataset:** "It’s a global number and we are very glad to have the success of the FBA <u>program."</u> **Ground Truth Label:** Claim **Model Predictions:** 

Llama3 Fine-tuned: Neutral, Llama3 Merged: Claim Mistral Fine-tuned: Premise, Mistral Merged: Claim 

Table 20. Reduced Overfitting and Regularization Example - FinArg dataset 

As shown in table 20, the merged model avoids the overfitting and classify the sentence correctly as “claim”, where the fine-tuned model misclassifies this example as a “premise”. 

_3. Complementary strengths._ Different models may excel at different aspects of the task. Merging allows the combined model to leverage the strengths of each constituent model as shown in table **??** 

**Sentence from SC dataset:** " Seth Golden, , Daily Articles, 0 The first trading day post the Saudi Arabia oil field bombings and speculative production slowdown pushed crude oil future (CLF) prices up roughly 15%, with equity <u>prices</u> moving lower Monday." **Ground Truth Label:** Causal **Model Predictions:** Llama3 Fine-tuned: Noise, Llama3 Merged: Causal Mistral Fine-tuned: Noise, Mistral Merged: Causal 

Table 21. Complementary strengths Example - SC dataset 

## **5 CONCLUSION AND FUTURE WORK** 

In this study, we evaluated the in-context learning (ICL) capabilities of three small instruct models—Llama3-8B, Mistral7B, and Phi-3—across various financial classification tasks. The results highlighted variability in model performance with increasing numbers of shots. Overall, ICL did not significantly enhance the models’ ability to learn downstream tasks from examples, particularly for smaller models. Among the three, Llama3-8B exhibited marginally better performance, though the gains were not substantial. 

Beyond ICL, our primary focus was on the instruct fine-tuning of both the base and instruct versions of these models for four key financial tasks: sentiment analysis, news headline classification, relation extraction, and hawkish-dovish classification. The results demonstrate that multi-task fine-tuning of instruct models significantly improves task-specific performance, particularly for complex tasks such as relation extraction and hawkish-dovish classification. These findings underscore the potential of fine-tuning smaller LLMs for domain-specific tasks in finance. 

Fameti et al. 

Notably, the study also revealed that multi-task fine-tuned base models, such as Mistral-7B and Llama3-8B, exhibited greater performance degradation on unseen tasks compared to their instruct-tuned counterparts. This suggests that starting with instruct models, which have already been fine-tuned on a variety of tasks, provides a more robust foundation for maintaining generalization capabilities. Notably, the Phi-3 model, despite its smaller size (3.8 billion parameters), showed minimal performance decline on unseen tasks, indicating that it remains highly capable after fine-tuning for specialized financial tasks. 

Looking ahead, we plan to extend this work by exploring more complex financial tasks, such as question answering, which involves retrieving numerical data from tables, and stock market prediction. These tasks will allow us to further investigate instruct fine-tuning on both small base and instruct models. Additionally, as model merging is gaining traction, we aim to experiment with advanced merging techniques like Dare and Tie to assess their effectiveness in mitigating performance degradation on unseen tasks, potentially leading to more versatile and resilient models. 

## **REFERENCES** 

- [1] Marah Abdin, Sam Ade Jacobs, Ammar Ahmad Awan, Jyoti Aneja, Ahmed Awadallah, Hany Awadalla, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Harkirat Behl, et al. 2024. Phi-3 technical report: A highly capable language model locally on your phone. _arXiv preprint arXiv:2404.14219_ (2024). 

- [2] Amanda Bertsch, Maor Ivgi, Uri Alon, Jonathan Berant, Matthew R Gormley, and Graham Neubig. 2024. In-Context Learning with Long-Context Models: An In-Depth Exploration. _arXiv preprint arXiv:2405.00200_ (2024). 

- [3] TB Brown, B Mann, N Ryder, M Subbiah, JD Kaplan, P Dhariwal, A Neelakantan, P Shyam, G Sastry, A Askell, et al. 2020. Language Models are Few-Shot Learners Advances in Neural Information Processing Systems 33. (2020). 

- [4] OpenAI ChatGPT. 2023. optimizing language models for dialogue. OpenAI. 2022. 

- [5] Qianglong Chen, Guohai Xu, Ming Yan, Ji Zhang, Fei Huang, Luo Si, and Yin Zhang. 2023. Distinguish before answer: Generating contrastive explanation as knowledge for commonsense question answering. _arXiv preprint arXiv:2305.08135_ (2023). 

- [6] Daixuan Cheng, Shaohan Huang, and Furu Wei. 2023. Adapting large language models via reading comprehension. _arXiv preprint arXiv:2309.09530_ (2023). 

- [7] Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E Gonzalez, et al. 2023. Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality. _See https://vicuna. lmsys. org (accessed 14 April 2023)_ 2, 3 (2023), 6. 

- [8] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. 2023. Palm: Scaling language modeling with pathways. _Journal of Machine Learning Research_ 24, 240 (2023), 1–113. 

- [9] Xiang Deng, Vasilisa Bashlovkina, Feng Han, Simon Baumgartner, and Michael Bendersky. 2023. What do llms know about financial markets? a case study on reddit market sentiment analysis. In _Companion Proceedings of the ACM Web Conference 2023_ . 107–110. 

- [10] Kelvin Du, Frank Xing, and Erik Cambria. 2023. Incorporating multiple knowledge sources for targeted aspect-based financial sentiment analysis. _ACM Transactions on Management Information Systems_ 14, 3 (2023), 1–24. 

- [11] Alexander Dunn, John Dagdelen, Nicholas Walker, Sanghoon Lee, Andrew S Rosen, Gerbrand Ceder, Kristin Persson, and Anubhav Jain. 2022. Structured information extraction from complex scientific text with fine-tuned large language models. _arXiv preprint arXiv:2212.05238_ (2022). 

- [12] Louis H Ederington and Jae Ha Lee. 1993. How markets process information: News releases and volatility. _The Journal of Finance_ 48, 4 (1993), 1161–1191. 

- [13] Sorouralsadat Fatemi and Yuheng Hu. 2023. A Comparative Analysis of Fine-Tuned LLMs and Few-Shot Learning of LLMs for Financial Sentiment Analysis. _arXiv preprint arXiv:2312.08725_ (2023). 

- [14] Georgios Fatouros, John Soldatos, Kalliopi Kouroumali, Georgios Makridis, and Dimosthenis Kyriazis. 2023. Transforming sentiment analysis in the financial domain with ChatGPT. _Machine Learning with Applications_ 14 (2023), 100508. 

- [15] Charles Goddard, Shamane Siriwardhana, Malikeh Ehghaghi, Luke Meyers, Vlad Karpukhin, Brian Benedict, Mark McQuade, and Jacob Solawetz. 2024. Arcee’s MergeKit: A Toolkit for Merging Large Language Models. _arXiv preprint arXiv:2403.13257_ (2024). 

- [16] Axel Groß-Klußmann and Nikolaus Hautsch. 2011. When machines read the news: Using automated text analytics to quantify high frequency news-implied market reactions. _Journal of Empirical Finance_ 18, 2 (2011), 321–340. 

- [17] Meta Group. 2024. LLaMA3 Model. https://ai.meta.com/blog/meta-llama-3/. Accessed: 2024-04-18. 

- [18] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ (2021). 

- [19] Quzhe Huang, Mingxu Tao, Chen Zhang, Zhenwei An, Cong Jiang, Zhibin Chen, Zirui Wu, and Yansong Feng. 2023. Lawyer llama technical report. _arXiv preprint arXiv:2305.15062_ (2023). 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

- [20] Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Suchin Gururangan, Ludwig Schmidt, Hannaneh Hajishirzi, and Ali Farhadi. 2022. Editing models with task arithmetic. _arXiv preprint arXiv:2212.04089_ (2022). 

- [21] Pranab Islam, Anand Kannappan, Douwe Kiela, Rebecca Qian, Nino Scherrer, and Bertie Vidgen. 2023. Financebench: A new benchmark for financial question answering. _arXiv preprint arXiv:2311.11944_ (2023). 

- [22] Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, et al. 2023. Mistral 7B. _arXiv preprint arXiv:2310.06825_ (2023). 

- [23] Qiang Li, Xiaoyan Yang, Haowen Wang, Qin Wang, Lei Liu, Junjie Wang, Yang Zhang, Mingyuan Chu, Sen Hu, Yicheng Chen, et al. 2023. From Beginner to Expert: Modeling Medical Knowledge into General LLMs. _arXiv preprint arXiv:2312.01040_ (2023). 

- [24] Xianzhi Li, Samuel Chan, Xiaodan Zhu, Yulong Pei, Zhiqiang Ma, Xiaomo Liu, and Sameena Shah. 2023. Are ChatGPT and GPT-4 General-Purpose Solvers for Financial Text Analytics? A Study on Several Typical Tasks. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: Industry Track_ . 408–422. 

- [25] Yinheng Li, Shaofei Wang, Han Ding, and Hang Chen. 2023. Large language models in finance: A survey. In _Proceedings of the Fourth ACM International Conference on AI in Finance_ . 374–382. 

- [26] Alisa Liu, Xiaochuang Han, Yizhong Wang, Yulia Tsvetkov, Yejin Choi, and Noah A Smith. 2024. Tuning language models by proxy. _arXiv preprint arXiv:2401.08565_ (2024). 

- [27] Tiedong Liu and Bryan Kian Hsiang Low. 2023. Goat: Fine-tuned llama outperforms gpt-4 on arithmetic tasks. _arXiv preprint arXiv:2305.14201_ (2023). 

- [28] Alejandro Lopez-Lira and Yuehua Tang. 2023. Can chatgpt forecast stock price movements? return predictability and large language models. _arXiv preprint arXiv:2304.07619_ (2023). 

- [29] Burton G Malkiel. 2011. The efficient-market hypothesis and the financial crisis. In _Rethinking finance: perspectives on the crisis (Proceedings of a conference). Russel Sage Foundation_ . Citeseer. 

- [30] Pekka Malo, Ankur Sinha, Pekka Korhonen, Jyrki Wallenius, and Pyry Takala. 2014. Good debt or bad debt: Detecting semantic orientations in economic texts. _Journal of the Association for Information Science and Technology_ 65, 4 (2014), 782–796. 

- [31] Dominique Mariko, Hanna Abi Akl, Estelle Labidurie, Stephane Durfort, Hugues De Mazancourt, and Mahmoud El-Haj. 2020. Financial document causality detection shared task (fincausal 2020). _arXiv preprint arXiv:2012.02505_ (2020). 

- [32] Kostadin Mishev, Ana Gjorgjevikj, Irena Vodenska, Lubomir T Chitkushev, and Dimitar Trajanov. 2020. Evaluation of sentiment analysis in finance: from lexicons to transformers. _IEEE access_ 8 (2020), 131662–131682. 

- [33] Maryam Mousavi, Hasan Davulcu, Mohsen Ahmadi, Robert Axelrod, Richard Davis, and Scott Atran. 2022. Effective messaging on social media: What makes online content go viral?. In _Proceedings of the ACM Web Conference 2022_ . 2957–2966. 

- [34] Maryam Mousavi, Elena Steiner, Steven R. Corman, Scott Ruston, Dylan Weber, and Hasan Davulcu. 2021. Stif: Semi-supervised taxonomy induction using term embeddings and clustering. In _Proceedings of the 2021 5th International Conference on Natural Language Processing and Information Retrieval_ . 115–123. 

- [35] Kostiantyn Omelianchuk, Andrii Liubonko, Oleksandr Skurzhanskyi, Artem Chernodub, Oleksandr Korniienko, and Igor Samokhin. 2024. Pillars of Grammatical Error Correction: Comprehensive Inspection Of Contemporary Approaches In The Era of Large Language Models. _arXiv preprint arXiv:2404.14914_ (2024). 

- [36] R OpenAI. 2023. Gpt-4 technical report. arxiv 2303.08774. _View in Article_ 2, 5 (2023). 

- [37] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ 35 (2022), 27730–27744. 

- [38] Agam Shah, Suvan Paturi, and Sudheer Chava. 2023. Trillion dollar words: A new financial dataset, task & market analysis. _arXiv preprint arXiv:2305.07972_ (2023). 

- [39] Raj Sanjay Shah, Kunal Chawla, Dheeraj Eidnani, Agam Shah, Wendi Du, Sudheer Chava, Natraj Raman, Charese Smiley, Jiaao Chen, and Diyi Yang. 2022. When flue meets flang: Benchmarks and large pre-trained language model for financial domain. _arXiv preprint arXiv:2211.00083_ (2022). 

- [40] Soumya Sharma, Tapas Nayak, Arusarka Bose, Ajay Kumar Meena, Koustuv Dasgupta, Niloy Ganguly, and Pawan Goyal. 2022. FinRED: A dataset for relation extraction in financial domain. In _Companion Proceedings of the Web Conference 2022_ . 595–597. 

- [41] Karan Singhal, Tao Tu, Juraj Gottweis, Rory Sayres, Ellery Wulczyn, Le Hou, Kevin Clark, Stephen Pfohl, Heather Cole-Lewis, Darlene Neal, et al. 2023. Towards expert-level medical question answering with large language models. _arXiv preprint arXiv:2305.09617_ (2023). 

- [42] Ankur Sinha and Tanmay Khandait. 2021. Impact of news on the commodity market: Dataset and results. In _Advances in Information and Communication: Proceedings of the 2021 Future of Information and Communication Conference (FICC), Volume 2_ . Springer, 589–601. 

- [43] Xiaofei Sun, Xiaoya Li, Jiwei Li, Fei Wu, Shangwei Guo, Tianwei Zhang, and Guoyin Wang. 2023. Text classification via large language models. _arXiv preprint arXiv:2305.08377_ (2023). 

- [44] Eugene Sy, Tzu-Cheng Peng, Shih-Hsuan Huang, Heng-Yu Lin, and Yung-Chun Chang. 2023. Fine-grained argument understanding with bert ensemble techniques: A deep dive into financial sentiment analysis. In _Proceedings of the 35th Conference on Computational Linguistics and Speech Processing (ROCLING 2023)_ . 242–249. 

- [45] Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois, Xuechen Li, Carlos Guestrin, Percy Liang, and Tatsunori B Hashimoto. 2023. Stanford alpaca: An instruction-following llama model. 

Fameti et al. 

- [46] Haochun Wang, Chi Liu, Nuwa Xi, Zewen Qiang, Sendong Zhao, Bing Qin, and Ting Liu. 2023. Huatuo: Tuning llama model with chinese medical knowledge. _arXiv preprint arXiv:2304.06975_ (2023). 

- [47] Xiao Wang, Weikang Zhou, Can Zu, Han Xia, Tianze Chen, Yuansen Zhang, Rui Zheng, Junjie Ye, Qi Zhang, Tao Gui, et al. 2023. InstructUIE: multi-task instruction tuning for unified information extraction. _arXiv preprint arXiv:2304.08085_ (2023). 

- [48] Zengzhi Wang, Qiming Xie, Yi Feng, Zixiang Ding, Zinong Yang, and Rui Xia. 2023. Is ChatGPT a good sentiment analyzer? A preliminary study. _arXiv preprint arXiv:2304.04339_ (2023). 

- [49] Jerry Wei, Jason Wei, Yi Tay, Dustin Tran, Albert Webson, Yifeng Lu, Xinyun Chen, Hanxiao Liu, Da Huang, Denny Zhou, et al. 2023. Larger language models do in-context learning differently. _arXiv preprint arXiv:2303.03846_ (2023). 

- [50] Shijie Wu, Ozan Irsoy, Steven Lu, Vadim Dabravolski, Mark Dredze, Sebastian Gehrmann, Prabhanjan Kambadur, David Rosenberg, and Gideon Mann. 2023. Bloomberggpt: A large language model for finance. _arXiv preprint arXiv:2303.17564_ (2023). 

- [51] Chunli Xiang, Junchi Zhang, Fei Li, Hao Fei, and Donghong Ji. 2022. A semantic and syntactic enhanced neural model for financial sentiment analysis. _Information Processing & Management_ 59, 4 (2022), 102943. 

- [52] Qianqian Xie, Weiguang Han, Zhengyu Chen, Ruoyu Xiang, Xiao Zhang, Yueru He, Mengxi Xiao, Dong Li, Yongfu Dai, Duanyu Feng, et al. 2024. The FinBen: An Holistic Financial Benchmark for Large Language Models. _arXiv preprint arXiv:2402.12659_ (2024). 

- [53] Qianqian Xie, Weiguang Han, Yanzhao Lai, Min Peng, and Jimin Huang. 2023. The wall street neophyte: A zero-shot analysis of chatgpt over multimodal stock movement prediction challenges. _arXiv preprint arXiv:2304.05351_ (2023). 

- [54] Qianqian Xie, Weiguang Han, Xiao Zhang, Yanzhao Lai, Min Peng, Alejandro Lopez-Lira, and Jimin Huang. 2024. PIXIU: A Comprehensive Benchmark, Instruction Dataset and Large Language Model for Finance. _Advances in Neural Information Processing Systems_ 36 (2024). 

- [55] Prateek Yadav, Derek Tam, Leshem Choshen, Colin Raffel, and Mohit Bansal. 2023. Resolving interference when merging models. _arXiv preprint arXiv:2306.01708_ 2 (2023). 

- [56] Hongyang Yang, Xiao-Yang Liu, and Christina Dan Wang. 2023. Fingpt: Open-source financial large language models. _arXiv preprint arXiv:2306.06031_ (2023). 

- [57] Linyi Yang, Eoin M Kenny, Tin Lok James Ng, Yi Yang, Barry Smyth, and Ruihai Dong. 2020. Generating plausible counterfactual explanations for deep transformers in financial text classification. _arXiv preprint arXiv:2010.12512_ (2020). 

- [58] Steve Yang, Jason Rosenfeld, and Jacques Makutonin. 2018. Financial aspect-based sentiment analysis using deep representations. _arXiv preprint arXiv:1808.07931_ (2018). 

- [59] Yi Yang, Mark Christopher Siy Uy, and Allen Huang. 2020. Finbert: A pretrained language model for financial communications. _arXiv preprint arXiv:2006.08097_ (2020). 

- [60] Li Yunxiang, Li Zihan, Zhang Kai, Dan Ruilong, and Zhang You. 2023. Chatdoctor: A medical chat model fine-tuned on llama model using medical domain knowledge. _arXiv preprint arXiv:2303.14070_ (2023). 

- [61] Boyu Zhang, Hongyang Yang, and Xiao-Yang Liu. 2023. Instruct-fingpt: Financial sentiment analysis by instruction tuning of general-purpose large language models. _arXiv preprint arXiv:2306.12659_ (2023). 

- [62] Boyu Zhang, Hongyang Yang, Tianyu Zhou, Muhammad Ali Babar, and Xiao-Yang Liu. 2023. Enhancing financial sentiment analysis via retrieval augmented large language models. In _Proceedings of the Fourth ACM International Conference on AI in Finance_ . 349–356. 

- [63] Shengyu Zhang, Linfeng Dong, Xiaoya Li, Sen Zhang, Xiaofei Sun, Shuhe Wang, Jiwei Li, Runyi Hu, Tianwei Zhang, Fei Wu, et al. 2023. Instruction tuning for large language models: A survey. _arXiv preprint arXiv:2308.10792_ (2023). 

- [64] Wenxuan Zhang, Yue Deng, Bing Liu, Sinno Jialin Pan, and Lidong Bing. 2023. Sentiment analysis in the era of large language models: A reality check. _arXiv preprint arXiv:2305.15005_ (2023). 

- [65] Yue Zhang, Leyang Cui, Deng Cai, Xinting Huang, Tao Fang, and Wei Bi. 2023. Multi-task instruction tuning of llama for specific scenarios: A preliminary study on writing assistance. _arXiv preprint arXiv:2305.13225_ (2023). 

- [66] Qihuang Zhong, Liang Ding, Juhua Liu, Bo Du, and Dacheng Tao. 2023. Can chatgpt understand too? a comparative study on chatgpt and fine-tuned bert. _arXiv preprint arXiv:2302.10198_ (2023). 

- [67] Wenhao Zhu, Hongyi Liu, Qingxiu Dong, Jingjing Xu, Shujian Huang, Lingpeng Kong, Jiajun Chen, and Lei Li. 2023. Multilingual machine translation with large language models: Empirical results and analysis. _arXiv preprint arXiv:2304.04675_ (2023). 

## **APPENDIX** 

## **.1 Appendix A** 

We present statistics regarding the datasets utilized for instruction fine-tuning of both base and instruct models. Subsequently, we provide descriptions of the instructions and prompt templates employed for each task during instruction fine-tuning. 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

|**Datasets**|**Train Set**|**Validation Set**|**Test Set**|
|---|---|---|---|
|FPB|3100|776|970|
|FiQA-SA|750|188|235|
|Headline-Dir|6493|928|1856|
|FinRED|5655|808|1616|
|FOMC|1785|199|496|
|FinArg-AUC-T1|-|-|969|
|M&A|-|-|500|
|FinCausual‘20-T1|-|-|800|



Table 22. Training, validation and test set statistics used for instruction fine-tuning base and instruct models. ‘-’ denotes that the dataset was not used in training. 

|**Model**|**Instruct Model Train Prompt Template**|**Instruct Model Test Prompt Template**|
|---|---|---|
|Llama3|<|user|> {instruction}<br>sentence: {input} <|end|><br><|assistant|><br>label: {output} <|end|>|<|user|> {instruction}<br>sentence: {input} <|end|><br><|assistant|><br>label:|
|Mistral|<s> [INST] «SYS» {instruction} «/SYS»<br>Sentence: {input} [/INST]<br>label: {output} </s>|<s> [INST] «SYS» {instruction} «/SYS»<br>Sentence: {input} [/INST]<br>label:|
|Phi-3|<|begin_of_text|><|start_header_id|><br>system<|end_header_id|>{instruction}<br><|eot_id|>|<|begin_of_text|><|start_header_id|><br>system<|end_header_id|>{instruction}<br><|eot_id|>|
||<|start_header_id|>user<|end_header_id|><br>Sentence:{input} <|eot_id|><br><|start_header_id|>assistant<|end_header_id<br>label: {output} <|eot_id|><|end_of_text|>||><br><|start_header_id|>user<|end_header_id|><br>Sentence:{input} <|eot_id|><br><|start_header_id|>assistant<|end_header_id|><br>label:|



Table 23. Prompt templates for instruct models used in our instruction fine-tuning and test experiments. Instructions are obtained from Table 25. 

## **.2 Appendix B** 

We present the results of single-task fine-tuning of base and instruct models in Table 25 and Figures 7, 8, and 9. The results indicate that single-task fine-tuning performs similarly to multi-task fine-tuning. In some datasets, single-task fine-tuning even relatively outperforms multi-task fine-tuning for base models. For merging the models, we utilized the single-task fine-tuned instruct models, which performed similarly to multi-task fine-tuned models, to alleviate the degradation of zero-shot performance of fine-tuned models on unseen tasks. 

Fameti et al. 



Fig. 7. Performance comparison of vanilla models (zero-shot instruct models), single-task fine-tuned base models, multi-task finetuned base models, single-task fine-tuned instruct models, and multi-task fine-tuned instruct models on five financial classification datasets for Llama3-8B model. F1 score is reported. 



Fig. 8. Performance comparison of vanilla models (zero-shot instruct models), single-task fine-tuned base models, multi-task finetuned base models, single-task fine-tuned instruct models, and multi-task fine-tuned instruct models on five financial classification datasets for Mistral-7B model. F1 score is reported. 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

## **Base Model Train Prompt Template** 

Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request. ###Instruction: {instruction} ###Input: {input} ###Response: 

{output} 

Table 24. Prompt templates for base models used in our instruction fine-tuning. Instructions are obtained from Table 25. 



Fig. 9. Performance comparison of vanilla models (zero-shot instruct models), single-task fine-tuned instruct models, and multi-task fine-tuned instruct models on five financial classification datasets for Phi-3 model. F1 score is reported. 

Fameti et al. 

|**Task**|**Dataset**|**Instruction**|
|---|---|---|
|Sentiment analysis|FPB, FiQA-SA|You are a skilled financial analyst specialized in detecting mar-<br>ket sentiment from news sources. Your task is to evaluate the<br>sentiment of the following sentence and assign it one of the<br>labels: Positive, Negative, or Neutral. Return only a single word,<br>either Positive or Negative or Neutral.|
|News headline classification|Headline-Dir|You are a skilled financial analyst. Analyze the provided data<br>to identify the trend in price movements of gold. Determine if<br>the price is going up, down, or remaining stable. Return ’up’ if<br>the price is increasing, ’down’ if it’s decreasing, or ’stable’ if<br>it’s remaining relatively unchanged. Return only a single word,<br>either up or down or stable.|
|Relation extraction|FinRED|You are a skilled financial analyst. Utilize the input text as a<br>context reference, choose the right relationship between ’en-<br>tity1’ and ’entity2’ from the options. Return only a single word<br>from the Options. Options: founded by, chief executive officer,<br>employer, product/material produced, industry, owned by, sub-<br>sidiary, parent organization, manufacturer, brand, owner of,<br>developer, headquarters location, distribution format, original<br>broadcaster, legal form, location of formation, creator, stock<br>exchange, operator, publisher, distributed by, platform, member<br>of, position held, currency, director/manager, chairperson, busi-<br>ness division.|
|Hawkish-dovish classification|FOMC|You are an expert financial analyst. Classify the following sen-<br>tence from FOMC into ’HAWKISH’, ’DOVISH’, or ’NEUTRAL’<br>class. Label HAWKISH if it is corresponding to tightening of<br>the monetary policy, DOVISH if it is corresponding to easing<br>of the monetary policy, or NEUTRAL if the stance is neutral.|
|Argument unit classification|FinArg-AUC-T1|You are an expert financial analyst. Analyze sentences from<br>earnings conference calls and identify their argumentative func-<br>tion. Each sentence is either a ’premise’, offering evidence or<br>reasoning, or a ‘claim’, asserting a conclusion or viewpoint. Re-<br>turn only a single word, either premise or claim.|
|Deal completeness classification|M&A|You are an expert financial analyst. In this task, you will be<br>given Mergers and Acquisitions (M&A) news articles or tweets.<br>Your task is to classify each article or tweet based on whether<br>the mentioned deal was completed or remained a rumour. Your<br>response should be a single word - either ‘complete’ or ‘rumour’<br>- representing the outcome of the deal mentioned in the provided<br>text. Return only a single word, either complete or rumour.|
|Causal classification|FinCausual’20-T1|You are an expert financial analyst. In this task, you are provided<br>with sentences extracted from financial news and SEC data.<br>Your goal is to classify each sentence into either ‘causal’ or<br>‘noise’ based on whether or not it indicates a causal relationship<br>between financial events. Return only a single word, either<br>causal or noise.|



Table 25. Example prompts for each task in our fine-tuning and test experiments 

A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification 

|**Experiment**|**Model**|**FP**|**B**|**FiQA**|**-SA**|**Headline-Dir**|**FinRED**|**FOMC**|**FinArg**|**M&A**|**SC**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||**Acc**|**F1**|**Acc**|**F1**|**F1**|**F1**|**F1**|**F1**|**F1**|**F1**|
||Llama3-8B|77.5|76.7|71.1|72.9|72.3|6.5|47.4|50.2|85.9|66.7|
|_Vanilla Models_|Mistral-7B|73.4|69.8|45.9|54.8|77.6|20.5|38.6|42.2|83.6|68.8|
||Phi-3-mini|72.8|72.9|72.7|74.8|87.1|24.8|48.5|54.1|80.1|66.5|
|_STBFT_|Llama3-8B|84.7|84.8|88.1|88.2|95.6|74.3|67.7|-|-|-|
|_-ase-_|Mistral-7B|85.2|85.3|85.9|86.5|95.3|70.1|71.1|-|-|-|
|_MT-B-FT_|Llama3-8B|79.1|79.4|87.2|85.3|95.3|69.1|68.7|23.4|72.5|52.6|
|_ase_|Mistral-7B|86.8|86.6|85.5|85.1|95.5|76.4|67.1|13.4|70.9|31.8|
||Llama3-8B|81.1|79.5|78.7|81.4|95.5|73.2|67.6|-|-|-|
|_ST-Instruct-FT_|Mistral-7B|84.6|84.8|85.5|83.9|95.4|67.3|68.3|-|-|-|
||Phi-3-mini|83.4|82.5|76.6|79.1|95.6|69.2|66.3|-|-|-|
||Llama3-8B|86.2|86.3|86.4|86.6|95|73.4|68.4|31.1|72.9|39.2|
|_MT-Instruct-FT_|Mistral-7B|86.3|86.2|85.1|83.9|95.2|69.4|70.2|35.1|76.1|57.6|
||Phi-3-mini|84.7|84.1|79.5|81.5|95.6|67.2|66.5|53.5|77.7|64.9|
|_Md Mdl_|Llama3-8B|80.6|80.7|75.3|78.3|93.2|44.6|60.9|54.6|74.3|65.5|
|_erge oes_|Mistral-7B|80.4|80.3|65.1|72.1|91.6|41.2|38.9|50.4|83.5|59.6|



Table 26. Main experimental results for four financial classification tasks and three unseen financial classification tasks (FinArg, M&A, Casual-SC). Vanilla models indicate the zero-shot performance of instruct models. ST-Base-FT refers to single-task fine-tuned base models, and ST-Instruct-FT refers to single-task fine-tuned instruct models. MT-Base-FT refers to multi-task fine-tuned base models, and MT-Instruct-FT refers to multi-task fine-tuned instruct models. 



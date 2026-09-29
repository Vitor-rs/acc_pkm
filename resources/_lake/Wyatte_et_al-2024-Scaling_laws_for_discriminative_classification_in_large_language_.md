---
title: Scaling laws for discriminative classification in large language models
citekey: Wyatte2024
authors:
- Dean Wyatte
- Fatemeh Tahmasbi
- Ming Li
- Thomas Markovich
year: 2024
date: '2024'
item_type: preprint
doi: 10.48550/ARXIV.2405.15765
url: https://arxiv.org/abs/2405.15765
zotero_key: ERZX36KZ
collections:
- SA9KZ2CI
tags:
- /novo
- Computer Science - Computation and Language
- Computer Science - Machine Learning
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: scaling laws for discriminative classification in large language models.pdf
synced_at: '2026-09-29T18:12:25.950284'
---

# Scaling laws for discriminative classification in large language models

**Autores:** Dean Wyatte, Fatemeh Tahmasbi, Ming Li, Thomas Markovich
**DOI:** [10.48550/ARXIV.2405.15765](https://doi.org/10.48550/ARXIV.2405.15765)
**URL:** https://arxiv.org/abs/2405.15765

## 📄 Conteúdo Completo do Documento

# **Scaling Laws for Discriminative Classification in Large Language Models** 

Dean Wyatte 

Cash App Boulder, Colorado, USA dwyatte@block.xyz 

Ming Li 

Cash App 

Bellevue, Washington, USA victorl@block.xyz 

## **ABSTRACT** 

Modern large language models (LLMs) represent a paradigm shift in what can plausibly be expected of machine learning models. The fact that LLMs can effectively generate sensible answers to a diverse range of queries suggests that they would be useful in customer support applications. While powerful, LLMs have been observed to be prone to hallucination which unfortunately makes their near term use in customer support applications challenging. To address this issue we present a system that allows us to use an LLM to augment our customer support advocates by re-framing the language modeling task as a discriminative classification task. In this framing, we seek to present the top-K best template responses for a customer support advocate to use when responding to a customer. We present the result of both offline and online experiments where we observed offline gains and statistically significant online lifts for our experimental system. Along the way, we present observed scaling curves for validation loss and top-K accuracy, resulted from model parameter ablation studies. We close by discussing the space of trade-offs with respect to model size, latency, and accuracy as well as and suggesting future applications to explore. 

## **CCS CONCEPTS** 

• **Applied computing** → _Document searching_ ; • **Computing methodologies** → **Supervised learning by classification** ; _Neural networks_ . 

## **KEYWORDS** 

Large Language Models, Discriminative Classification, Domain Adaptation, Scaling 

∗Corresponding Author 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _SIGKDD, June 03–05, 2018, Woodstock, NY_ 

© 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 978-1-4503-XXXX-X/18/06...$15.00 

https://doi.org/XXXXXXX.XXXXXXX 

Fatemeh Tahmasbi 

Cash App 

Woodbridge, Virginia, USA 

fatemeh@block.xyz 

Thomas Markovich<sup>∗∗</sup> 

Cash App 

Cambridge, Massachusetts, USA tmarkovich@block.xyz 

#### **ACM Reference Format:** 

Dean Wyatte, Fatemeh Tahmasbi, Ming Li, and Thomas Markovich. 2024. Scaling Laws for Discriminative Classification in Large Language Models. In _Proceedings of Make sure to enter the correct conference title from your rights confirmation emai (SIGKDD)._ ACM, New York, NY, USA, 11 pages. https://doi.org/XXXXXXX.XXXXXXX 

## **1 INTRODUCTION** 

Modern Large Language Models (LLMs) such as those in the GPT [3, 7, 29], LLaMA [34, 35], PaLM [10], and Pythia [6] families are decoder-only models employing the transformer architectures, and are trained to perform next token prediction through an autoregressive objective. These models work by using attention with a causal mask to learn a representation of a sequence of tokens that can then be used to predict the next best token. Because these models are decoder-only, they are significantly simpler and may be more sample efficient [33, 38] meaning that much larger models can be trained on drastically more data. It has been shown that LLM training exhibits strong scaling laws that relate the size of the model and the available data to the overall model quality on a variety of downstream tasks [3]. The existence of these scaling curves has shown that our current LLMs are not yet at risk of overfitting, causing us to conclude that we can improve both by just increasing the model size and amount of training data [16, 18]. To date, the vast majority of LLM work has been focused on open-domain tasks, but for industrial settings, closed domain tasks are more valuable in the near term. These are tasks for which the action and topic spaces are drastically reduced. Customer service applications are a common application for language modeling, because they typically involve extracting nuanced meaning from multi-turn text based conversations and are a common part of many corporate product offerings. Indeed, the customer service application market is projected to be as large as 58 billion dollars [1] with multiple existing offerings such as Google’s DialogFlow and Amazon’s Lex. 

Given the generative nature of LLMs, an autonomous customer support system is a natural application of an LLM. While LLMs seem uncontested in many applications, they are not without their problems. In generative settings, these models have been shown to hallucinate answers, and are susceptible to data exfiltration attacks. In customer support use cases, both of these failure modes preclude adoption. Beyond these concerns, LLMs can also have the potential to reply to focused queries from customers with off-topic or innane 

SIGKDD, June 03–05, 2018, Woodstock, NY 

Wyatte, et al. 

responses which would ultimately lead to degraded customer experience. Additionally, LLMs are also extremely computationally demanding which makes their deployment in high throughput product applications expensive or untenable. Solving these problems is the focus of intense research across the community. 

Rather than waiting for these problems to be solved, we ask the question **“How can we use LLMs to solve intermediate, industrially relevant, problems?”** We find this answer in using LLMs to perform next-reply classification given a set of pre-written replies for our chat support system as a way to augment and speed up our customer support representatives. We will refer to this problem as template classification, which we frame as a supervised machine learning task for a decoder-only LLM architecture that we fine-tune into a discriminative classifier. Framing the problem in this way allows us to enjoy the well documented benefits of modern language models while avoiding the well documented risks associated with model hallucination and data leakage. With this framing in hand, we construct a two phase training pipeline that first domain-adapts the LLM and then fine-tunes it into a discriminative classifier. As this is an industrial system, we consider the correspondence between offline machine learning metrics and online product metrics which we assess through rigorous online experimentation. We additionally explore the trade-off between accuracy, which generally correlates with model accuracy, and run-time performance through a model parameter ablation. In summary, this paper’s core contributions are: 

- (1) We detail to our knowledge the first industrial implementation of fine-tuning LLMs into discriminative classifiers. 

- (2) We detail to our knowledge the first scaling law on closed domain adaptation. 

- (3) We detail the relationship between language modeling performance and amenability to discriminative fine-tuning for a classification task with hundreds or thousands of classes. 

- (4) We discuss practical considerations associated with putting these models into production. 

While this system focuses on augmenting our customer advocates with LLMs, we view this as the first in a series of steps towards deploying a reliable, autonomous, customer support agent. The remainder of this paper is organized as follows. In Section 2, we review related work with a particular focus on scaling laws and using LLMs for classification. In Section 3, we review our system. We detail our Methods in Section 4. We present our offline and online experimental results in Section 5, and carefully discuss the practical considerations associated with implementing and deploying these models within our system. And finally, we present our conclusions and next steps in Section 6. 

## **2 RELATED WORK** 

In this section we situate our work within the large language model literature, which has rapidly evolved over the last few years. 

**Language Models and Customer Support.** Language modeling has frequently been used to construct chat interfaces that assist customers in handling common queries in a faster and cheaper way than human agents can provide, and in 2023 Gartner found that chatbots were used to resolve 58% of all billing disputes [2]. These chat systems are often built on a rigid set of rules and business logic, 

and language modeling is used for intent classification to navigate the tree. Because encoder-decoder models such as BERT provide a trained encoder which can be used for downstream classification, many of these intent classification systems were built with BERT as a backbone. In 2021 CS-BERT, BERTa\’u, and AVA were released, which are a BERT variants that were finetuned on customer support data, and provided significant improvements across a variety of customer support benchmarks [12, 37, 42]. Recently, generative language models have been explored within a customer support use case [26, 32], but are not without their very public failures due to hallucination of company policies [27] or PII leakage [8]. To the best of our knowledge, BERT-based models remain the state of the art for intent classification based systems. 

**Large Language Models.** Almost all modern language models use a transformer architecture [36]. At the heart of this architecture is the transformer block which is comprised of multi-head self attention [36], layer normalization units [4], a dense fully connected unit, and residual connections. Modern transformers are constructed by stacking many of these blocks, and in the instance of text, the transformer ingests input tokens and outputs predicted tokens based on some training objective. Most modern LLMs follow a causal decoder-only architecture, such that the LLM has no way to learn different representations for input and target sequences. Instead, through the use of causal masking, the decoder-only transformer predicts the next token conditioned on the previously observed tokens. Popular examples of this model structure include GPT [3, 7, 29], LLaMA [34, 35], PaLM [10], and Pythia [6]. 

**Model Scaling Behavior.** Scaling behaviors have long been observed in the training of language models. The authors of Kaplan et al. [18] were some of the first to empirically observe power-law scaling in dataset volume and model size from their training of GPT2 [18]. They additionally observed no instances of overfitting for 1 billion parameters and tokens. In the development of Chinchilla, the authors provided an empirical analytical formula that recommended the optimal model size and data volume for a fixed compute budget [16]. There has also been work focused on understanding the scaling behavior of language model fine-tuning. It has previously been observed that in domains with a fixed number of tokens, the optimal strategy is to take a pre-trained model and fine-tune it for the domain at hand [14, 15]. In Hernandez et al. [15], a relationship was derived to predict the loss reduction associated with fine-tuning when compared with training a transformer of the same size from scratch on the same data. 

**Domain Adaptation of Language Models.** There is a significant body of literature that is focused on applying language models to narrow domains through various domain adaptation schemes. An early version of this idea was presented as domain adaptive pre-training (DAPT), which found that a second phase of pre-training on domain-specific datasets led to significant performance gains [14]. Another early example is that of TOD-BERT, which performed domain adaptation through both dataset curation and loss function augmentation [40]. The dataset was curated from nine different human-human interaction or multi-turn tasks, and the pre-training used a combination of masked language modeling and contrastive loss that exploited the dialog-specific nature of the pre-training datasets. Using both of these strategies, they were 

Scaling Laws for Discriminative Classification in Large Language Models 

SIGKDD, June 03–05, 2018, Woodstock, NY 

able to realize significant performance gains. It was shown in CSBERT that in-domain pre-training on millions of customer support messages provided significant benefits on downstream customer support applications [37]. Similar results have been observed in the case of modern decoder-only architectures. In ChipNeMo the authors domain adapted a LLM for use in a chip design which is a highly technical domain [23]. Through domain adaptation, they found that they needed a 5-fold smaller model to achieve same level of performance across a range of downstream tasks [23]. Similar, models like CodeLLaMA [31] and StarCoder [20] have shown impressive accuracy on a range of programming tasks through a second round or pre-training for domain adaptation. Looking beyond simple domain adaptation, the authors of Cheng et al. [9] developed a language model fine-tuning process inspired by reading comprehension tests. These reading comprehension tests enable the authors to generate domain-specific 7B parameter models that have equivalent quality to 50B parameter models that have been domain adapted through two-phase pre-training. A portion of our work can be understood in this line of investigation because we perform a domain adaptation step. 

**Discriminative Fine-tuning.** There are relatively few example of using decoder transformer architectures for classification tasks through discriminative fine-tuning. Early work with the GPT architecture investigated the effect of language model pre-training on downstream fine-tuning tasks such as text classification, entailment, semantic similarity, and multiple choice question answering [28]. Subsequent work with the GPT architecture however focused on zero- and few-shot language generation in lieu of fine-tuning. Other similar fine tuning methods could include both Parameter Efficient Fine Tuning (PEFT) [41] and Supervised Fine Tuning (SFT) [25]. PEFT refers to a family of methods, such as LoRA [17], that seek to fine tune a much smaller set of parameters than exist in the original model. SFT seeks to align the original embeddings of the LLM for the target task through a supervised process that maps the LLM output to that of the target. For InstructGPT, this mapping consists of aligning input training text with multiple sequential output tokens. Our method can be understood as a SFT method with an output space that is of size _𝑁𝑐𝑙𝑎𝑠𝑠𝑒𝑠_ . Perhaps the most relevant work is the recent LS-LLaMA approach which systematically studied replacing the final transformer decoder with a classification layer and removing causal masks. In their experiments, they find reliable improvements upon BERT baselines while also outperforming LLMs an order of magnitude larger than LS-LLaMA. Their work however is limited to the LLaMA family of models and they do not quantify the effect of LLM size on discriminative fine-tuning ability. 

## **3 PRELIMINARIES** 

Cash App customer support advocates respond to customer queries in real time using a combination of freehand and template text that they further tailor to a specific customer’s query. The templates are used for common customer support actions including greeting the customer, requesting more information about a particular query (e.g., details associated with a financial transaction), troubleshooting steps, and providing status updates about an in-progress support case. Figure 1 illustrates typical use of these templates for troubleshooting. 



<!-- Start of picture text -->
Customer<br>Hi I’m having trouble accessing my account. can you please help me?<br>De t ails  +<br>Sen t  a t  Jun  1 8, 2023, 5: 1 2:49 PM (2 days ago)<br>Cash App (Automated)<br>Thanks for this information. We'll get you to someone who can help.<br>Sen t  a t  Jun  1 8, 2023, 5: 1 3:33 PM (2 days ago)<br>Cash App<br>Hi, I am Victor from Cash App! Thank you so much for your patience<br>during our delay Dean, I will be more than happy to assist you today<br>Te mpla t e: Cash  A pp  -  General Gree t ing<br>Sen t  by advoca t e  # 27 1 49 a t  Jun  1 8, 2023, 9:49: 1 6 PM (2 days ago)<br>Account Access - Login Trouble Shooting Suggested<br>Account Access  - New Device Suggested<br>Account Access  - New Phone Number Suggested<br>Feature Request Edge Case Suggested<br>General Greeting Already Used<br>It sounds like you are having trouble logging in. Can you try the following to troubleshoot�<br>�# XX�<br>7# YYY<br>If you're still having difficulty logging in to your account, please let us know and we'll try a<br>different route.<br>English (Uni t ed S t a t es) Send<br><!-- End of picture text -->

**Figure 1: Example customer support case with most relevant template responses.** 

Advocates are trained to choose appropriate templates during a support case, which presents us with an opportunity to automatically suggest the most appropriate ones using a machine learning model that considers the current support case context. To augment the advocates, we have designed a machine learning system that selects the top-k most likely templates that would address the customer’s message. In this setting, it is only the advocate who sees the top-k signals. Advocates can then further tailor the suggested templates before responding, dismiss them to manually search for a more appropriate template, or respond completely in freehand text. We describe our modeling approaches to this problem in the following section followed by a broader study of this online system in Section 5.2. 

## **4 METHODS** 

The overall training pipeline is depicted in Figure 2 and consists of two steps: 1) domain adaptation with an autoregressive language modeling objective and 2) discriminative fine-tuning with discrete labels. In the domain adaptation step, we start with a pre-trained LLM and continue pre-training it on data from our target domain consisting of Cash App customer support transcripts. We use the Pythia suite of LLMs [6] which build on the GPTNeoX architecture, and are closely related to the original GPT-3 paper, [13] with parameter counts from 70M to 12B pre-trained on approximately 300B tokens of domain general web data from The Pile [5, 13]. This choice of pre-trained LLM allows us to leverage the effectiveness of transfer learning [15] while still studying their scaling laws using a range of parameter counts within a closed domain. For this 

SIGKDD, June 03–05, 2018, Woodstock, NY 

Wyatte, et al. 



<!-- Start of picture text -->
Classification Models<br>Pythia(410m, 1.4b, 2.8b)<br>Foundation Models  Cash App Customer Support<br>Foundation Models<br>Pythia(410m, 1.4b, 2.8b)<br>Pythia(410m, 1.4b, 2.8b)<br><!-- End of picture text -->

**Figure 2: Training pipeline for domain adaptation and discriminative fine-tuning.** 

study, we focus on the 410 million (410m), 1.4 billion (1.4b), and 2.8 billion (2.8b) parameter variants to provide a comparison to BERT-large [11] (340M parameters), which is commonly used in discriminative fine-tuning while documenting scaling effects for domain adaptation with higher parameter counts. 

In the discriminative fine-tuning step, we initialize a new linear layer of size _𝑁ℎ𝑖𝑑𝑑𝑒𝑛_ × _𝑁𝑐𝑙𝑎𝑠𝑠𝑒𝑠_ on top of the final transformer block of one of our domain adapted models. We fine-tune the model end-to-end on a smaller dataset of Cash App customer support transcripts labeled with support advocates template response selections to produce our final classifier. 

## **4.1 Customer Support Dataset** 

Our customer support dataset consists of tens of billions of tokens of customer support transcripts collected using an in-app messaging interface over the course of Cash App’s operational history. These transcripts have been processed to remove PII using an industry standard redaction pipeline. The cases are initiated by a message from a customer and contain a combination of automated system responses and human responses as the support advocate works to resolve the customer’s query. Examples of how the dataset is formatted in each phase of our training pipeline are shown in the Appendix. 

Even though we redact our data, PII leakage is a common risk with LLMs in deployed applications but it is not a risk for our 

system as designed for two reasons. The first is that we are using our LLM as a classifier to select the correct template to respond to a customer with; and the second is that all responses are routed through a customer service advocate. 

## **4.2 Domain Adaptive Pre-training** 

We annotate each message in the aforementioned customer support transcripts with a "<CUSTOMER>", "<SYSTEM>", or "<ADVOCATE>" prefix to indicate the participant and join the annotated messages together with newlines. For tokenization, we employ the same BPE tokenizer used in the pre-trained Pythia model opposed to any domain-specific tokenization such as in [23]. Documents shorter than 2048 tokens are packed together into full length sequences to increase throughput. Shorter documents within the sequence are separated with a special end-of-text token to give the model indication that these documents are unrelated. 

During domain adaptation, we generally follow the original pretraining configuration for the model sizes reported in [6] including the use of the AdamW optimizer with _𝛽_ 1 and _𝛽_ 2 values of 0.9 and 0.95, and weight decay of 0.01, learning rate based on the model size, and batch size of 2 million tokens. We employ a linear warmup for 1% of our total training steps followed by cosine decay to zero. Our complete hyperparameters are shown in Table 1. Additionally, we use the Zero Redundancy Optimizer (ZeRO) [30] to efficiently scale training to multiple GPUs. 

Scaling Laws for Discriminative Classification in Large Language Models 

SIGKDD, June 03–05, 2018, Woodstock, NY 

|**Model**|**Configuration Key**|**Value**|
|---|---|---|
|Pythia 410m, 1.4b, 2.8b|||
||fp16.enabled<br>lr-decay-style|True<br>cosine|
||max-position-embeddings|2048|
||optimizer.params.betas|[0.9, 0.95]|
||optimizer.type|AdamW|
||warmup|0.01|
||weight-decay|0.01|
||max-steps|14500|
||eval-steps|0.1|
||save-steps|0.1|
|Pythia 410m|learning rate|3e-4|
|Pythia 1.4b|learning rate|2e-4|
|Pythia 2.8b|learningrate|1.6e-4|



**Table 1: Configuration details for Pythia models domain adaptation. Common configurations are listed above the middle line, with model-specific configurations below.** 

We pre-train for up to 14500 steps of 2M tokens, reserving 1B tokens for evaluation although due to computational constraints and time considerations, we interrupted the larger models late in training. We save checkpoints every 1450 steps (2.9B tokens) which we use for discriminative fine-tuning. 

## **4.3 Discriminative Fine-tuning** 

In this step we fine-tune the domain-adapted Pythia models from the previous step for a sequence classification task. We select 250K random messages on which a customer support advocate chose to use a template reply and consider that as our label. We use a 50% train/test split at the support case level to prevent leakage if selecting multiple messages from the same support case. The label set comprises 640 unique template responses. 

We consider the support case up to the labeled message as the context. We are interested in comparing our domain adapted models with BERT-large which has a maximum context of 512 tokens, so we use a rolling window with an earliest-first truncation strategy to select the most recent whole messages up to the maximum of 512 tokens. We omit the "<CUSTOMER>", "<SYSTEM>", and "<ADVOCATE>" annotations in this case to give more room for support case context based on previous unpublished work that shows these annotations provide minimal information in this task. 

We initialize a new linear layer of 640 classes and select the right-most token of each sequence in the batch to pool as input as in [22] and implemented in the transformers library [39]. We fine-tune for one epoch as we have observed additional fine-tuning quickly overfits and evaluate the result with Top-1, Top-3, and Top-5 accuracy. 

Fine-tuning hyperparameters are shown in Table 2 

## **4.4 Model Updates** 

Our model training pipeline is composed of two phases – domain adaptation and discriminative fine tuning. The domain adaptation phase requires billions of tokens and can take multiple days to 

|**Model**|**Configuration Key**|**Value**|
|---|---|---|
|BERT-large,|||
|Pythia 410m, 1.4b, 2.8b|||
||fp16.enabled|True|
||lr-decay-style|linear|
||max-position-embeddings|512|
||optimizer.params.betas|[0.9, 0.99]|
||optimizer.type|AdamW|
||warmup|0.1|
||weight-decay|0.0|
||learning rate|1e-5|
||batch size|128|
|BERT-large|num-train-epochs|10|
|Pythia 410m, 1.4b, 2.8b|num-train-epochs|1|



**Table 2: Configuration details for discriminative fine-tuning. Common configurations are listed above the middle line, with model-specific configurations below.** 

train while discriminative fine tuning requires orders of magnitude fewer tokens and only takes hours. Because domain adaptation is trained using the standard causal autoregressive objective, we find that we are able to reuse domain adapted models across different discriminative fine tuning jobs. We anticipate performing further domain adaptation after 10 billion additional tokens have been acquired, but otherwise update models via discriminative fine tuning to accommodate changes to template usage. 

## **4.5 Baseline Models** 

As a baseline, we fine-tune BERT-large as well as customer support domain-adapted variant using the approach described in [14] that is used in several of our other online systems. For details of our domain adaptation using BERT’s masked language modeling objective, we refer readers to [21]. Given BERT-large generally takes several epochs to converge [11], we fine-tune for a maximum of 10 epochs and report the epoch with the highest test set performance which which in practice, was epoch 9. 

## **5 EXPERIMENTS** 

## **5.1 Offline Training and Evaluation** 

Given our two-stage training pipeline, our goal in studying scaling laws is to predict how well a model adapted to a domain using a language modeling objective (stage 1) will perform when discriminatively fine-tuned as a classifier (stage 2). We evaluate this scaling behavior using various metrics that offer insights into performance, efficiency, and behavior across different scales, including 

**FLOPs (Floating Point Operations):** The number of floating point operations executed during the language modeling stage. It provides insights into the computational complexity of the LLM and how it scales with model and dataset size. 

**Language Modeling Loss:** The cross entropy between the model’s predicted next token and the actual next token in training data, directly optimized by the language modeling objective. Monitoring the loss ensures that the model is converging toward an optimal language model of the data. 

SIGKDD, June 03–05, 2018, Woodstock, NY 

Wyatte, et al. 



<!-- Start of picture text -->
2.10 2.10 2.10<br>2.05 2.05 2.05<br>2.00 2.00 2.00<br>1.95 Pythia-410m 1.95 Pythia-410m 1.95 Pythia-410m<br>Pythia-1.4b Pythia-1.4b Pythia-1.4b<br>1.90 Pythia-2.8b 1.90 Pythia-2.8b 1.90 Pythia-2.8b<br>1.85 1.85 1.85<br>1.80 1.80 1.80<br>1.75 1.75 1.75<br>1017 1018 5.0B 10.0B 15.0B 20.0B 25.0B 30.0B 0.38 0.39 0.40 0.41 0.42 0.43 0.44 0.45<br>Domain Adaptation FLOPs Domain Adaptation Tokens Domain Adaptation Loss<br>(a) Domain Adaptation FLOPs vs Classification Loss (b) Domain Adaptation Tokens vs Classification Loss (c) Domain Adaptation Loss vs Classification Loss<br>Classification Loss<br><!-- End of picture text -->

**Figure 3: Discriminative fine-tuning empirical scaling properties across different model sizes.** 

**Classification Loss:** The cross entropy between the model’s predicted class probabilities and the ground truth label, directly optimized by the discriminative fine-tuning objective. It provides a measure of how well the classifier can differentiate between classes. 

Figure 3 depicts properties of the scaling laws observed in our experiments. In Figure 3 (a) we plot classification loss as a function of language modeling FLOPs for each of the model sizes we adapted. We observe overlap across the three model sizes tested such that for a given compute budget such as 10<sup>18</sup> FLOPs, larger models exhibit lower training loss, suggesting their ability to learn complex patterns and structure within the training data. While we do not fit a formal scaling law here, the observation is consistent with compute optimal language modeling [16, 18] applied to discriminative finetuning. 

In Figure 3 (b), we plot the classification loss as a function of number of tokens seen during our domain adaptation stage. We observe scaling as a function of number of training tokens with larger models exhibiting lower classification loss for the same number of training tokens. We also observe a linear relationship between supervised classification loss and the number of training tokens across model sizes. These results suggest that even the largest model we trained will still benefit from more data. We find this encouraging because it means we are able to produce better classifiers when discriminatively fine-tuned, despite our practical parameterlimitations [15, 18]. 

We relate language modeling loss to classification loss in Figure 3 (c). We observe a linear relationship between language modeling loss during domain adaptation and classification loss during discriminative fine-tuning across model sizes. This means despite the different training objectives in these two stages of our pipeline, we can easily predict how amenable a particular LLM is to discriminative fine-tuning from its language modeling abilities. One reason for this may be due to our choice of pooling during discriminative fine-tuning using the right-most token of the input sequence. This makes our fine-tuning objective to minimize _𝑝_ ( _𝑦𝑖_ | _𝑥_ 0 _...𝑥𝑛_ −1). If we 

consider class _𝑦𝑖_ to be a special "class token", the fine-tuning objective reduces to the standard language modeling objective assuming all other regular subword tokens _𝑥_ are masked. 

In Table 3 we compare the classification accuracy for different model sizes with BERT-large serving as a baseline. The results span a wide accuracy range of more than 10% between the weakest model (BERT-large) and the strongest model (Domain Adapted Pythia2.8b), highlighting the impact of scaling data used for language modeling as well as increasing model size. Domain adaptation regularly improves the accuracy of a model by approximately 4-5%, which is a larger uplift than that which results from increasing the model size at the scales tested here. We observe that the Pythia models outperform BERT in the roughly parameter equivalent case of BERT-large (310m) compared to Pythia 410m with Pythia 1.4b outperforming BERT-large with domain adaptation. This comparison not only underscores the impact of model and dataset size on accuracy, but may also point to the nature of the language modeling objective in determining discriminative fine-tuning performance. BERT-based models are pre-trained with a masked language modeling objective that only covers 15% of tokens while the causal language modeling objective used in the Pythia models predicts every token in the sequence which may make language modeling more sample efficient [33, 38] and allow use of larger datasets. Finally, while we limit the sequence length to 512 tokens during discriminative fine-tuning to ensure a fair comparison between BERT-large and Pythia models, the Pythia models can make use of up to 2048 tokens of context during language modeling to learn longer-range dependencies. 

We also quantify the latency of a typical forward pass for the model sizes we consider which is important for deployed use cases that contain a human in the loop like customer support. While transformer latencies are well-described by the model architecture itself including number of parameters [19], we compute them empirically for our observed sequences via load test in our production environment. We optimize each model using TensorRT on an NVIDIA A10 GPU with FP16 support and then conduct a load test for five minutes sampling from a distribution of 10000 input sequences. 

Scaling Laws for Discriminative Classification in Large Language Models 

SIGKDD, June 03–05, 2018, Woodstock, NY 

The load test makes requests of batch size 1 at a given rate to our end-to-end inference service that includes truncation to a maximum length of 512 tokens. Table 4 lists the peak 1-minute average, P99, and max latencies in milliseconds observed during the load test. We observe that Pythia-2.8b quickly saturates a single GPU at higher levels of concurrency leading to increased tail latency. Because our production system contains a human in the loop that is shown the model’s predictions, we establish a latency budget as to not negatively impact their workflow. For a latency budget of 100 ms, Pythia-2.8b will need to be scaled to an additional GPU for each additional request per second, which we view as impractical for most industrial use cases. In contrast, Pythia-1.4b on a single GPU can handle 5-10 requests per second and Pythia-410m fails to saturate a single GPU at the request rates considered here. While larger models may thus appear to be less well-suited for use cases with low latency budgets, we see promise in the relatively smooth linear scaling of classification loss with number of training tokens (Figure 3, for example Pythia-1.4b trained over approximately 27B tokens has approximately the same classification loss as Pythia-2.8 trained over approximately 3B tokens). Therefore domains with a large amount of unlabeled data may be able to utilize smaller models trained for longer or even by repeating data [24]. 

|**Model**|**Top-1**<br>**Acc.(%)**|**Top-3**<br>**Acc.(%)**|**Top-5**<br>**Acc.(%)**|
|---|---|---|---|
|BERT-large|46.39|66.68|74.24|
|_+ Domain Adaptation_|49.24|70.51|78.04|
|Pythia-410m|45.43|66.96|75.02|
|_+ Domain Adaptation_|51.09|73.31|80.71|
|Pythia-1.4b|48.64|70.87|78.89|
|_+ Domain Adaptation_|53.75|76.59|83.95|
|Pythia-2.8b|49.96|72.33|80.31|
|_+ Domain Adaptation_|**55.12**|**78.02**|**85.10**|



**Table 3: Comparison of classification accuracy across different models after discriminative fine-tuning.** 

## **5.2 Online Case Study** 

We now turn to experiments that we have performed in our online system that uses the models described in preceding sections to surface the most appropriate templates to customer support advocates. Whenever a new message is sent during a customer support case, the model considers the most recent conversation context (up to its maximum context length) and returns the top-5 highest probability templates that are part of its training set as candidate classifications. To evaluate the effectiveness of the system, we remove these predictions from a randomly selected 2% of advocate-support case interactions which allows us to determine how often an advocate would choose one of our predicted templates when they are working on a given support case as well as the effects of the system on other business metrics. 

Our primary metrics of interest are related to customer support efficiency that do not affect our customer-facing support experience in any noticeable way. A simple first order metric to optimize for is the amount of time it takes an advocate to choose the correct 

|**Requests/Sec**|**Pythia-410m**|**Pythia-1.4b**|**Pythia-2.8b**|
|---|---|---|---|
|1|Avg: 14.29|Avg: 28.80|Avg: 45.92|
||P99: 30.72|P99: 40.95|P99: 70.66|
||Max: 32.37|Max: 41.45|Max: 72.08|
|2|Avg: 13.97|Avg: 31.64|Avg: 51.42|
||P99: 28.90|P99: 59.91|P99: 111.43|
||Max: 29.58|Max: 67.07|Max: 118.84|
|5|Avg: 13.66|Avg: 30.96|Avg: 52.72|
||P99: 26.21|P99: 60.65|P99: 121.27|
||Max: 33.85|Max: 66.67|Max: 149.56|
|10|Avg: 14.05|Avg: 33.02|Avg: 63.89|
||P99: 31.84|P99: 79.86|P99: 183.26|
||Max: 59.33|Max: 116.40|Max: 222.36|
|20|Avg: 15.03|Avg: 40.42|Avg: 122.38|
||P99: 34.55|P99: 110.96|P99: 371.90|
||Max: 46.92|Max: 178.11|Max: 482.43|



**Table 4: Peak 1-minute average, P99, and max latencies across models.** 

template response based on their training. We find that we have reduced the selection time by 7.38 seconds on average over the lifetime of the system and in general, are able to continually improve on these savings (Figure 4). These selection time savings correspond to a 3.56% total time reduction over the course of an entire support case, a substantial savings when considering the support footprint required for Cash App’s tens of millions of active users. During the initial launch of the system, we conducted an internal audit and found no evidence that this time reduction affected customer support standards. 



<!-- Start of picture text -->
9.5<br>Average Difference: 7.38 sec<br>9.0<br>8.5<br>8.0<br>7.5<br>7.0<br>6.5<br>6.0<br>Week<br>Jan 2023 Apr 2023 Jul 2023 Oct 2023 Jan 2024<br>Time Difference (s)<br><!-- End of picture text -->

**Figure 4: Weekly absolute difference in selection time between holdout and treatment groups.** 

New response templates are frequently introduced and existing ones are deprecated, so we need to retrain our model in a discriminative manner. To date, we have retrained our model four time and before releasing the model, we A/B test over a shorter two-week period to determine the effect on our efficiency metrics.<sup>1</sup> Over the 

1At time of writing, we have A/B tested our fourth model but have not yet released it. 

SIGKDD, June 03–05, 2018, Woodstock, NY 

Wyatte, et al. 

lifetime of each model, we find that we are consistently able to keep the time it takes to select the correct template with our predictions at approximately 13 seconds, in contrast to 19 seconds without templates (Figure 5). A/B tests indicate that we are able to significantly decrease selection time as a function of retraining (Table 5). Together these results are consistent with the overall increase in selection time savings over the total system lifetime (Figure 4). 



<!-- Start of picture text -->
Cohort<br>25<br>Holdout<br>Treatment<br>20<br>15<br>10<br>5<br>0<br>model-v1 model-v2 model-v3<br>Model Version<br>Selection Time (s)<br><!-- End of picture text -->

**Figure 5: Selection time between holdout and treatment groups over model lifetime** 

|**A/B Test**|**Selection Time (seconds)**|_𝑝_**-value**|
|---|---|---|
||**A**<br>**B**||
|model-v1/model-v2|13.78<br>**13.33**|4.76e-10|
|model-v2/model-v3|12.98<br>**12.52**|9.09e-10|
|model-v3/model-v4|11.64<br>**10.91**|3.67e-27|



**Table 5: A/B tests between existing and retrained models over a two-week period.** 

During the training phase of our model, we prioritize accuracy as an offline evaluation metric. However, in the online phase, we aim to optimize response selection time. Therefore, we seek a simple relationship between the two to inform model selection. To investigate this, we computed the accuracy of our model in our holdout that removes model predictions and compare it to the selection time savings between treatment and holdout groups for the (top 300) response templates by volume. We observe a clear positive relationship validated by Mann-Kendall test such that as the prediction accuracy improves, the average time saved on selection tends to increase (Figure 6). Accurately predicting the most frequently occuring response templates is expected to significantly reduce our selection time. However, accurately predicting new response templates shortly after their introduction, as customer support advocates familiarize themselves with them, is also important for optimizing selection time. 

## **6 CONCLUSION** 

In this work, we have described scaling laws for LLMs over closed domain adaptation with applications to a customer support use 



<!-- Start of picture text -->
Mann-Kendall Test<br>14 Trend: Increasing<br>p:  1.20e-14<br>12<br>10<br>8<br>6<br>4<br>2<br>0<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Accuracy (%)<br>Selection Time Saved (s)<br><!-- End of picture text -->

**Figure 6: Average selection time saving versus accuracy for highest volume response templates.** 

case. While most prior works on scaling laws has focused on the generative abilities of LLMs, we detail the effect on discriminative fine-tuning. Because existing deployed systems in industry are likely to involve a discrete classification, they can immediately benefit from the recent progress in LLMs including domain adaptation. Furthermore, this approach obviates safety concerns of LLMs in deployed systems such as hallucination by avoiding text generation altogether. In scenarios, where safety can be managed, such as those with a human in the loop to verify generated responses, practitioners can develop a domain-specific backbone. This backbone can be shared across across text classification and text generation deployments, or it can be gradually integrated into business operations as generative applications are adopted. 

Using our experimental system, we show the benefit of more accurate models in our online case study, which is commonly a result of scaling up model size. However, for use cases with a human in the loop, larger models may introduce latency that negatively affects business operations. Given the relatively smooth linear scaling we observe with number of tokens in our domain adaptation experiments, smaller domain-specific LLMs are an attractive solution to increase accuracy without negatively affecting latency. 

While our work has focused on customer support applications, we believe that our system is applicable in any situation where structured conversations or text classifications might occur. Furthermore, Our system would be applicable to open-domain settings with a fixed set of classification categories through the removal of the domain-adaptation step. Therefore, while the method was developed with the customer support use-case in mind, it is applicable to a wide variety of situations. 

## **REFERENCES** 

> [1] [n. d.]. Customer Service Software Market Size to Touch USD 58.1 Billion By 2030, According to Acumen Research and Consulting. https: //www.globenewswire.com/news-release/2023/01/11/2586848/0/en/CustomerService-Software-Market-Size-to-Touch-USD-58-1-Billion-By-2030According-to-Acumen-Research-and-Consulting.html. Accessed: 202404-15. 

Scaling Laws for Discriminative Classification in Large Language Models 

SIGKDD, June 03–05, 2018, Woodstock, NY 

- [2] [n. d.]. Gartner Survey Reveals Only 8% of Customers Used a Chatbot During their Most Recent Customer Service Interaction. https://web.archive.org/web/ 20231116150840/https://www.gartner.com/en/newsroom/press-releases/202306-15-gartner-survey-reveals-only-8-percent-of-customers-used-a-chatbotduring-their-most-recent-customer-service-interaction. Accessed: 2024-04-15. 

- [3] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ (2023). 

- [4] Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. 2016. Layer normalization. _arXiv preprint arXiv:1607.06450_ (2016). 

- [5] Stella Biderman, Kieran Bicheno, and Leo Gao. 2022. Datasheet for the pile. _arXiv preprint arXiv:2201.07311_ (2022). 

- [6] Stella Biderman, Hailey Schoelkopf, Quentin Gregory Anthony, Herbie Bradley, Kyle O’Brien, Eric Hallahan, Mohammad Aflah Khan, Shivanshu Purohit, USVSN Sai Prashanth, Edward Raff, et al. 2023. Pythia: A suite for analyzing large language models across training and scaling. In _International Conference on Machine Learning_ . PMLR, 2397–2430. 

- [7] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. _Advances in Neural Information Processing Systems_ 33 (2020), 1877–1901. 

- [8] Matt Burgess. 2023. OpenAI’s custom chatbots are leaking their secrets. https://www.wired.com/story/openai-custom-chatbots-gpts-promptinjection-attacks/ 

- [9] Daixuan Cheng, Shaohan Huang, and Furu Wei. 2023. Adapting large language models via reading comprehension. _arXiv preprint arXiv:2309.09530_ (2023). 

- [10] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. 2023. Palm: Scaling language modeling with pathways. _J. Machine Learning Research_ 24, 240 (2023), 1–113. 

- [11] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. Bert: Pre-training of deep bidirectional transformers for language understanding. _arXiv preprint arXiv:1810.04805_ (2018). 

- [12] Paulo Finardi, José Dié Viegas, Gustavo T Ferreira, Alex F Mansano, and Vinicius F Caridá. 2021. BERTa\’u: Ita\’u BERT for digital customer service. _arXiv preprint arXiv:2101.12015_ (2021). 

- [13] Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster, Jason Phang, Horace He, Anish Thite, Noa Nabeshima, et al. 2020. The pile: An 800gb dataset of diverse text for language modeling. _arXiv preprint arXiv:2101.00027_ (2020). 

- [14] Suchin Gururangan, Ana Marasović, Swabha Swayamdipta, Kyle Lo, Iz Beltagy, Doug Downey, and Noah A Smith. 2020. Don’t stop pretraining: Adapt language models to domains and tasks. _arXiv preprint arXiv:2004.10964_ (2020). 

- [15] Danny Hernandez, Jared Kaplan, Tom Henighan, and Sam McCandlish. 2021. Scaling laws for transfer. _arXiv preprint arXiv:2102.01293_ (2021). 

- [16] Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, et al. 2022. Training compute-optimal large language models. _arXiv preprint arXiv:2203.15556_ (2022). 

- [17] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ (2021). 

- [18] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. 2020. Scaling laws for neural language models. _arXiv preprint arXiv:2001.08361_ (2020). 

- [19] Vijay Anand Korthikanti, Jared Casper, Sangkug Lym, Lawrence McAfee, Michael Andersch, Mohammad Shoeybi, and Bryan Catanzaro. 2023. Reducing activation recomputation in large transformer models. _Proceedings of Machine Learning and Systems_ 5 (2023). 

- [20] Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, et al. 2023. StarCoder: may the source be with you! _arXiv preprint arXiv:2305.06161_ (2023). 

- [21] Victor Li and Dean Wyatte. 2023. Improving customer support intent classification with additional language model pretraining. https://ai.cash.app/supportpretraining. (2023). [Accessed 25-01-2024]. 

   - [25] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ 35 (2022), 27730–27744. 

   - [26] Keivalya Pandya and Mehfuza Holia. 2023. Automating Customer Service using LangChain: Building custom open-source GPT Chatbot for organizations. _arXiv preprint arXiv:2310.05421_ (2023). 

   - [27] Jason Proctor. 2024. How can I mislead you? Air Canada found liable for chatbot’s bad advice on bereavement rates | CBC News. https://www.cbc.ca/news/canada/ british-columbia/air-canada-chatbot-lawsuit-1.7116416 

   - [28] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. 2018. Improving language understanding by generative pre-training. (2018). 

   - [29] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. 2019. Language models are unsupervised multitask learners. _OpenAI blog_ 1, 8 (2019), 9. https://insightcivic.s3.us-east-1.amazonaws.com/language-models.pdf 

   - [30] Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. 2020. Zero: Memory optimizations toward training trillion parameter models. In _SC20: International Conference for High Performance Computing, Networking, Storage and Analysis_ . IEEE, 1–16. 

   - [31] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Tal Remez, Jérémy Rapin, et al. 2023. Code llama: Open foundation models for code. _arXiv preprint arXiv:2308.12950_ (2023). 

   - [32] Mohammad Shahin, F Frank Chen, and Ali Hosseinzadeh. 2024. Harnessing customized AI to create voice of customer via GPT3. 5. _Advanced Engineering Informatics_ 61 (2024), 102462. 

   - [33] Yi Tay, Mostafa Dehghani, Vinh Q Tran, Xavier Garcia, Dara Bahri, Tal Schuster, Huaixiu Steven Zheng, Neil Houlsby, and Donald Metzler. 2022. Unifying language learning paradigms. _arXiv preprint arXiv:2205.05131_ (2022). 

   - [34] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. 2023. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ (2023). 

   - [35] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ (2023). 

   - [36] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. _Advances in Neural Information Processing Systems_ 30 (2017). 

   - [37] Peiyao Wang, Joyce Fang, and Julia Reinspach. 2021. CS-BERT: a pretrained model for customer service dialogues. In _Proceedings of the 3rd Workshop on Natural Language Processing for Conversational AI_ . 130–142. 

   - [38] Thomas Wang, Adam Roberts, Daniel Hesslow, Teven Le Scao, Hyung Won Chung, Iz Beltagy, Julien Launay, and Colin Raffel. 2022. What language model architecture and pretraining objective works best for zero-shot generalization?. In _International Conference on Machine Learning_ . PMLR, 22964–22984. 

   - [39] Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin Lhoest, and Alexander M. Rush. 2020. Transformers: State-of-the-Art Natural Language Processing. In _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations_ . Association for Computational Linguistics, Online, 38–45. https://www.aclweb.org/anthology/2020.emnlpdemos.6 

   - [40] Chien-Sheng Wu, Steven Hoi, Richard Socher, and Caiming Xiong. 2020. TODBERT: Pre-trained natural language understanding for task-oriented dialogue. _arXiv preprint arXiv:2004.06871_ (2020). 

   - [41] Lingling Xu, Haoran Xie, Si-Zhao Joe Qin, Xiaohui Tao, and Fu Lee Wang. 2023. Parameter-efficient fine-tuning methods for pretrained language models: A critical review and assessment. _arXiv preprint arXiv:2312.12148_ (2023). 

   - [42] Shi Yu, Yuxin Chen, and Hussain Zaidi. 2021. AVA: A financial service chatbot based on deep bidirectional transformers. _Frontiers in Applied Mathematics and Statistics_ 7 (2021), 604842. 

- [22] Zongxi Li, Xianming Li, Yuzhang Liu, Haoran Xie, Jing Li, Fu-lee Wang, Qing Li, and Xiaoqin Zhong. 2023. Label supervised llama finetuning. _arXiv preprint arXiv:2310.01208_ (2023). 

- [23] Mingjie Liu, Teodor-Dumitru Ene, Robert Kirby, Chris Cheng, Nathaniel Pinckney, Rongjian Liang, Jonah Alben, Himyanshu Anand, Sanmitra Banerjee, Ismet Bayraktaroglu, et al. 2023. Chipnemo: Domain-adapted llms for chip design. _arXiv preprint arXiv:2311.00176_ (2023). 

- [24] Niklas Muennighoff, Alexander M Rush, Boaz Barak, Teven Le Scao, Aleksandra Piktus, Nouamane Tazi, Sampo Pyysalo, Thomas Wolf, and Colin Raffel. 2023. Scaling Data-Constrained Language Models. _arXiv preprint arXiv:2305.16264_ (2023). 

## **APPENDICES** 

## **Dataset Formatting** 

Here we show how transcripts from our customer support dataset are formatted. Figure 7 depicts how raw text is formatted for the pre-training and discriminative fine-tuning phases of our training pipeline. 

SIGKDD, June 03–05, 2018, Woodstock, NY 

Wyatte, et al. 

### **Raw Text:** 

**Customer:** What are the balances on my accounts? **System:** Hi <NAME>, I’ll get you to someone who can help. You don’t have to wait. We’ll notify you when they reply. 

**Customer:** Ty 

**Customer:** Just a general question... What are the totals of all my accounts with cash app? 

**Advocate:** Is there anything else that I can do for you? **Customer:** No, that’s it, Thanks! 

### **Pre-training Sample:** 

<CUSTOMER>: What are the balances on my accounts? \n <SYSTEM>: Hi <NAME>, I’ll get you to someone who can help. ... \n <ADVOCATE>: Is there anything else that I can do for you? \n <CUSTOMER>: No, that’s it, Thanks! 

### **Discriminative Fine-tuning Sample:** 

**Input:** What are the balances on my accounts? Hi <NAME>, I’ll get you to someone who can help. ... the totals of all my accounts with cash app? 

**Classification Label:** <VIEW_BALANCE_TEMPLATE> 

**Figure 7: Dataset Formatting for Pre-training and Discriminative Fine-tuning.** 

## **Domain Adaptation Scaling Results** 

Here we look at the scaling properties of the domain adaptation step within our pipeline. Figure 9 shows the training and validation loss of various models across different steps of pre-training. 

Scaling Laws for Discriminative Classification in Large Language Models 

SIGKDD, June 03–05, 2018, Woodstock, NY 



<!-- Start of picture text -->
0.85 0.85 0.85<br>0.84 0.84 0.84<br>0.83 0.83 0.83<br>Pythia-410m Pythia-410m Pythia-410m<br>0.82 PythiaPythia-2.8b-1.4b 0.82 PythiaPythia-2.8b-1.4b 0.82 PythiaPythia-2.8b-1.4b<br>0.81 0.81 0.81<br>0.80 0.80 0.80<br>0.79 17 18 0.79 0.79<br>10 10 5.0B 10.0B 15.0B 20.0B 25.0B 30.0B 0.38 0.39 0.40 0.41 0.42 0.43 0.44 0.45<br>Domain Adaptation FLOPs Domain Adaptation Tokens Domain Adaptation Loss<br>(a) Domain Adaptation FLOPs vs Top-5 Accuracy (b) Domain Adaptation Tokens vs Top-5 Accuracy (c) Domain Adaptation Loss vs Top-5 Accuracy<br>Figure 8: Discriminative fine-tuning empirical scaling properties across different model sizes.<br>0.70 Classification Accuracy in Scaling Results<br>0.65 Pythia-410m Figure 8 depicts properties of the scaling laws observed in<br>0.60 Pythia-1.4b Pythia-2.8b experiments with regard to classification accuracy instead of loss<br>in Figure 3.<br>0.55<br>0.50<br>0.45<br>0.40<br>0.35<br>0 2000 4000 6000 8000 10000 12000 14000<br>Step<br>(a) Domain adaptation training Loss on different steps<br>0.48<br>Pythia-410m<br>0.46 Pythia-1.4b<br>Pythia-2.8b<br>0.44<br>0.42<br>0.40<br>0.38<br>2000 4000 6000 8000 10000 12000 14000<br>Step<br>(b) Domain adaptation validation loss on different steps<br>Top-5 Classification Accuracy (%)<br>Training Loss<br>Validation Loss<br><!-- End of picture text -->

Figure 8 depicts properties of the scaling laws observed in our experiments with regard to classification accuracy instead of loss in Figure 3. 

**Figure 9: Domain adaptation emprical scaling results across different model sizes.** 



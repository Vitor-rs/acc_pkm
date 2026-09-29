---
title: 'Embedding in recommender systems: a survey'
citekey: Wang2026
authors:
- Maolin Wang
- Xinjian Zhao
- Wanyu Wang
- Sheng Zhang
- Jiansheng Li
- Bowen Yu
- Binhao Wang
- Shucheng Zhou
- Dawei Yin
- Qing Li
- Ruocheng Guo
- Xiangyu Zhao
year: 2026
date: '2026-05-07'
item_type: journalArticle
doi: 10.1145/3812652
url: https://dl.acm.org/doi/10.1145/3812652
zotero_key: U8DW2KUH
collections:
- SA9KZ2CI
tags:
- Computer Science - Information Retrieval
- Computer Science - Artificial Intelligence
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: embedding in recommender systems a survey.pdf
synced_at: '2026-09-29T18:18:44.448888'
---

# Embedding in recommender systems: a survey

**Autores:** Maolin Wang, Xinjian Zhao, Wanyu Wang, Sheng Zhang, Jiansheng Li, Bowen Yu, Binhao Wang, Shucheng Zhou, Dawei Yin, Qing Li, Ruocheng Guo, Xiangyu Zhao
**DOI:** [10.1145/3812652](https://doi.org/10.1145/3812652)
**URL:** https://dl.acm.org/doi/10.1145/3812652

## 📄 Conteúdo Completo do Documento

# **Embedding in Recommender Systems: A Survey** 

XIANGYU ZHAO<sup>∗</sup> , MAOLIN WANG<sup>∗</sup> , and XINJIAN ZHAO<sup>∗</sup> , City University of Hong Kong, China JIANSHENG LI, City University of Hong Kong, China 

SHUCHENG ZHOU, City University of Hong Kong, China DAWEI YIN, Baidu Inc., China 

QING LI, Hong Kong Polytechnic University, China 

JILIANG TANG, Michigan State University, USA 

RUOCHENG GUO<sup>†</sup> , ByteDance Research, UK 

Recommender systems have become an essential component of many online platforms, providing personalized recommendations to users. A crucial aspect is embedding techniques that coverts the high-dimensional discrete features, such as user and item IDs, into low-dimensional continuous vectors and can enhance the recommendation performance. Applying embedding techniques captures complex entity relationships and has spurred substantial research. In this survey, we provide an overview of the recent literature on embedding techniques in recommender systems. This survey covers embedding methods like collaborative filtering, self-supervised learning, and graph-based techniques. Collaborative filtering generates embeddings capturing user-item preferences, excelling in sparse data. Self-supervised methods leverage contrastive or generative learning for various tasks. Graph-based techniques like node2vec exploit complex relationships in networkrich environments. Addressing the scalability challenges inherent to embedding methods, our survey delves into innovative directions within the field of recommendation systems. These directions aim to enhance performance and reduce computational complexity, paving the way for improved recommender systems. Among these innovative approaches, we will introduce Auto Machine Learning (AutoML), hash techniques, and quantization techniques in this survey. We discuss various architectures and techniques and highlight the challenges and future directions in these aspects. This survey aims to provide a comprehensive overview of the state-of-the-art in this rapidly evolving field and serve as a useful resource for researchers and practitioners working in the area of recommender systems. To facilitate the development, evaluation and comparison of embedding-based recommender systems, we provide an open-source algorithm index<sup>1</sup> . 

### CCS Concepts: • **Computer science** → **Recommender Systems** . 

### **ACM Reference Format:** 

Xiangyu Zhao, Maolin Wang, Xinjian Zhao, Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, and Ruocheng Guo. 2023. Embedding in Recommender Systems: A Survey. 1, 1 (December 2023), 42 pages. https://doi.org/XXXXXXX.XXXXXXX 

∗Xiangyu Zhao, Maolin Wang and Xinjian Zhao contributed equally to this paper. 

†Corresponding author. 

1https://github.com/Applied-Machine-Learning-Lab/Embedding-in-Recommender-Systems 

Authors’ addresses: Xiangyu Zhao; Maolin Wang; Xinjian Zhao, City University of Hong Kong, Hong Kong, China; Jiansheng Li, City University of Hong Kong, Hong Kong, China; Shucheng Zhou, City University of Hong Kong, Hong Kong, China; Dawei Yin, Baidu Inc., China; Qing Li, Hong Kong Polytechnic University, Hong Kong, China; Jiliang Tang, Michigan State University, USA; Ruocheng Guo, ByteDance Research, London, UK. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. 

© 2023 Association for Computing Machinery. XXXX-XXXX/2023/12-ART $15.00 

https://doi.org/XXXXXXX.XXXXXXX 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

2 

Recommender systems have become an integral part of online platforms, providing personalized suggestions to users based on their preferences and behavior [181]. One of the key components of a recommender system is the representation of high-dimensional discrete features in a lowdimensional continuous vector space, known as embeddings. Embeddings have been shown to improve the performance of recommender systems by capturing the complex relationships between entities (e.g. items and users). Although embeddings have been widely employed in recommender systems, there has been a burgeoning body of research dedicated to investigation of them. Various methodologies have been proposed to generate entity embeddings, with the aim of capturing intricate relationships between entities. These methods include collaborative filtering [1, 19, 118], self-supervised learning [175], and graph-based techniques [31]. Additionally, Auto Machine Learning (AutoML) [85], hashing techniques [35, 62], and quantization techniques [96, 117] have also been explored as ways to improve the performance and efficiency of embedding-based recommender systems. 

Collaborative filtering (CF) is a widely adopted technique in recommender systems [70]. This method hinges on generating embeddings, which are compact, low-dimensional representations of users and items. These embeddings serve as a means to capture the underlying preferences and intrinsic characteristics of users and items alike. Within collaborative filtering, two prominent strategies for generating embeddings emerge: matrix factorization and factorization machines [118]. The allure of CF lies in its ability to provide accurate recommendations by discerning intricate relationships and interactions among users and items. It notably excels in handling sparse data and effectively tackling the challenge of the cold-start problem, where limited information about new items or users is available [70]. However, generating embeddings through collaborative filtering (CF) requires extensive training on large datasets, potentially imposing a significant computational burden. Moreover, it is worth noting that CF approaches might exhibit suboptimal performance when dealing with data that is inherently limited or predisposed to biases. 

In response to some of the limitations traditional CF poses, self-supervised learning-based techniques have arisen as a promising solution for embedding the learning of recommender systems [52] with limited data. These methodologies commonly harness the power of contrastive learning or generative learning techniques to derive entity embeddings. By capitalizing on expansive datasets and tapping into non-linear relationships, these methods aptly capture the latent semantics embedded within the data [155]. This equips them with remarkable generalizability across various tasks and domains. Yet, the success of self-supervised learning pivots significantly on the meticulous crafting of data augmentation methodologies, alongside the judicious selection of model architectures, loss functions, and pre-trained models. These factors wield considerable influence over the stability and convergence of the training process. It is important to note that self-supervised learning places particular emphasis on the graph and sequence structures of data, which will be a central focus of this survey. 

Graph-based methods, such as node2vec [38] and graph autoencoders [27, 127], harness the rich structural intricacies inherent in item-item and user-user relationships to create embeddings that capture these connections. By adeptly capturing the multifaceted network patterns and associations present in recommendation scenarios, these methods yield embeddings that elegantly encapsulate the existing intricate relationships between entities. These techniques assume particular significance in the settings where there exist an intricate underlying graph structure, as witnessed in social network environments. Furthermore, they furnish a conduit for incorporating auxiliary information through item-item and user-user relationships [12, 29]. 

One of the main challenges in the field of embeddings in recommender systems is the scalability of the methods. As the number of items and users in a recommender system becomes massive, the computational cost of generating embeddings can be a concern. To enhance efficiency and reduce 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

3 

complexity, various research directions have been explored for embedding-based recommender systems. At the forefront of this evolution within recommendation systems stand auto machine learning, hashing, and quantization techniques. Auto machine learning (AutoML) automates optimal machine learning solutions, streamlining tasks like model architecture design and hyperparameter tuning. In recommendation systems, AutoML aids in selecting suitable embedding sizes, boosting performance while mitigating challenges [195]. Hashing techniques [154] address the sparsity challenges of one-hot encodings by leveraging hashing functions for dimension reduction, minimizing storage, and computation. Quantization compresses high-dimensional embeddings into compact codes, curbing memory demands and enhancing efficiency. This process reconstructs original embeddings with minimal distortion, offering an efficient solution [34, 55, 81]. 

Overall, this survey seeks to offer a thorough panoramic view of embedding applications for recommender systems. We will delve into three categories of widely utilized techniques for embedding generation, encompassing (1) collaborative filtering, (2) self-supervised learning, and (3) graphbased approaches. Furthermore, we will scrutinize integrating (a) AutoML, (b) hashing techniques, and (c) quantization methodologies into the embedding framework. Moreover, in each chapter, we demonstrate existing tools and unveil prospective pathways for future advancement. Finally, we will briefly showcase how embeddings are practically applied in different real-world recommender systems, providing a practical outlook on the methods discussed. To the best of our knowledge, this paper represents the first systematic review of embedding techniques in recommendation systems. 

## **1 COLLABORATIVE FILTERING EMBEDDING** 

In this section, we will introduce the strategy of Collaborative Filtering (CF), which is a conventional embedding method in recommender systems. Generally, CF is to learn the similarity between users and items as well as user behavior, then predict potential preferred items for recommendation. There are two typical methods to implement embeddings in CF, Matrix Factorization (MF) scheme and the Factorization Machine (FM) scheme. MF is to factorize the user rating matrix into generalized product of the user feature matrix and item feature matrix, then achieve recommendation according to the preference of users to items, which can be calculated by corresponding user embeddings vectors and item embeddings vectors. However, for simple MF methods, the sparsity of the rating matrix is always a hard issue due to the large amount of one-hot encoded categorical features, and auxiliary features about users and items can not be adopted. To address these issues, FM [118] is proposed as the initial learning strategy that learns the prediction performance with respect to the similarity of feature embeddings between different features, based on the feature embedding transformed from one-hot embedding. 

## **1.1 Matrix Factorization Scheme** 

The singular value decomposition (SVD) is the most common kind of method for matrix factorization, for which the SVD is introduced as a pseudo form in FunkSVD model [30]. Intuitively, it involves an approximate factorization of the original rating matrix R ∈ R<sup>_𝑚_×</sup><sup>_𝑛_</sup> ( _𝑚_ users and _𝑛_ items) to obtain smaller user matrix U ∈ R<sup>_𝑚_×</sup><sup>_𝑑_</sup> and item matrix V ∈ R<sup>_𝑛_×</sup><sup>_𝑑_</sup> , with a hidden embedding dimension _𝑑_ : 



U and V represent unexplainable latent features of the users and the items respectively. The final optimization object is designed as 



, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

4 



<!-- Start of picture text -->
n d<br>Item 1 Item 2 Item 3 Item 4  · · ·  Item n<br>User 1 3.1 2.5 ? ? · · ·  2.7 n<br>User 2  ? 4.4 ? 3.9 · · · ?<br>m User 3 2.6 ? 4.7 ? · · · ? m U V T d<br>User 4  ? 3.5 ? ? · · ·  4.2<br>· · · · · · · · · · · · · · · · · · · · · Item  Matrix<br>User m 3.8 4.6 ? ? · · · ?<br>Rating  Matrix User  Matrix<br><!-- End of picture text -->

Fig. 1. FunkSVD model [30]. It involves an approximate factorization on matrix R ∈ R<sup>_𝑚_×</sup><sup>_𝑛_</sup> to obtain smaller user matrix U ∈ R<sup>_𝑚_×</sup><sup>_𝑑_</sup> and item matrix V ∈ R<sup>_𝑛_×</sup><sup>_𝑑_</sup> , with a hidden embedding dimension _𝑑_ . 

where u _𝑖_ and v _𝑗_ are the latent feature vectors of user _𝑖_ and item _𝑗_ in d-dimensional space respectively. u _𝑖_ and v _𝑗_ are aslo _𝑖_ -th and _𝑗_ -th column vector of U and V respectively. And the corresponding rating is predicted as u<sup>_𝑇_</sup> _𝑖_<sup>v</sup><sup>_𝑗_,</sup> 

Since then, many methods with improvements and variations based on FunkSVD [30] were gradually presented. For user factor reduction, NSVD [111] combines the item factors in a linear way to represent users. SVD++ [67] then replaces representing step with feeding latent user factors to optimize NSVD [111] by rating through a sparse weight matrix. Then SVDfeature [18] was presented as a toolkit that combines rank-model. DELF [23] implements the attention [134] to automatically differentiate interacted items whose importance is different. BiasSVD [69], adds a bias part: user-independent or item-independent factors, to FunkSVD [30]. TimeSVD [68] adds time weights by learning a parameter in each period and training with related data. 

Beyond direct modification of the FunkSVD framework, several frameworks have also been proposed through SLIM [108]. SLIM [108] introduces a user behavior matrix whose values _𝑟𝑢𝑖_ are binary: 1 for rated item _𝑖_ by user _𝑢_ , 0 otherwise. Then replace one of the factorized small matrices. But SLIM [108] lacks the ability to compare the similarity of either two items rated by one user at the same time. FISM [60] solves this by learning the low-dimensional latent vector space without the detailed rating information. But it considers that all the items rated by a user are equal for further prediction. NAIS [48] uses attention to select items with more important interactions automatically, which fixes this issue well. SGNS [74] implements skip-gram [104] and negative sampling techniques to factorize a shifted PMI matrix. ConvMF [64] integrates the CNN into PMF [105] and captures contextual information about the document to improve the performance of rating prediction. 

## **1.2 Factorization Machines** 

A solution to address classification challenges with large-scale sparse data lies in feature combination. Factorization Machines (FM) [118] effectively compress numerous sparse features, reduce parameter magnitude, and maintain performance simultaneously. Fundamentally, FM substitutes the interaction term in regular logistic regression with the dot product of latent factors. A strategy involves concatenating one-hot vectors representing user and item IDs to create the input feature vector x. Alternatively, auxiliary feature vectors linked to users and items can also be combined. Second-order feature combinations are then considered. For input feature vector x, the output value expression ΦFM (x) of degree _𝑑_ = 2 in factorization machines is given by: 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

5 

Embedding in Recommender Systems: A Survey 



where computation time is linear due to the concept of introducing high-order interactions based on linear regression. The dot product of _𝑘_ -dimensional vectors v _𝑖_ and v _𝑗_ is computed as: 



Parameters w = ( _𝑤_ 1 _,_ · · · _,𝑤𝑛_ )<sup>_𝑇_</sup> ∈ R<sup>_𝑛_</sup> and V = (v1 _,_ · · · _,_ v _𝑘_ )<sup>_𝑇_</sup> ∈ R<sup>_𝑛_×</sup><sup>_𝑘_</sup> are used, where _𝑤_ 0 and _𝑤𝑖_ represent bias and parameter for the _𝑖_ -th variable respectively. _𝑘_ signifies the dimension of learned latent embeddings, while _𝑛_ denotes the dimension of the original feature vector. FM facilitates model resolution by replacing _𝑤𝑖,𝑗_ with the dot product of vectors _𝑣𝑖_ and _𝑣 𝑗_ , effectively achieving the factorization process. When FM exclusively uses user and item IDs with binary interaction outputs, its prediction process aligns with FunkSVD [190]. Nonetheless, FM extends its reach by incorporating the embedding mechanism’s features and extending to diverse feature sets, bolstering flexibility and applicability. 

Deep Neural Networks (DNNs) excel in capturing high-order feature interactions [118]. Factorization Neural Networks (FNNs) [188] enhance this capability by integrating DNNs as the lower layer, enabling the learning of complex interactions that FM’s linear approach lacks. It reduces the need for feature engineering, enhances model expressiveness, and offers inspiration for FM-MLP combinations. Product-based Neural Networks (PNN) [116] introduces a product layer comprising linear and nonlinear segments to explicitly calculate the product expression of 2-dimensional feature interactions, while it may perform well with MLPs like FNN [188]. 

Neural Factorization Machines (NeuFM) [45] follow a similar linear and nonlinear composition, fusing 2-dimensional linear features (derived from a general matrix factorization layer) with high-dimensional nonlinear features from DNNs. Attentional Factorization Machines (AFM) [164] introduce an attention mechanism, learning attention score for feature interaction importance through a neural network. This mechanism reflects varying feature importance, enhancing model sensitivity. 

Contrasting the aforementioned method, a fusion of factorization machines (FM) and deep neural networks (DNNs) provides an avenue for alleviating the manual feature engineering burden inherent in certain DNNs. Notably, Google’s Wide & Deep [21] represents a significant advancement in recommendation systems. This model effectively tackles the challenges of memorization and generalization by capturing interactions between low-dimensional and high-dimensional features. However, it still requires artificial feature engineering for the Wide component’s input. Huawei’s DeepFM [40] builds upon the Wide & Deep framework, replacing the Wide component with FM. By sharing the embedding part between FM and Deep components, training efficiency improves. Importantly, DeepFM dispenses with pre-training FM and artificial feature engineering, achieving simultaneous learning of low-dimensional and high-dimensional feature interactions. 

Further progress, building upon Wide & Deep [21] and DeepFM [40], centers on enhancing explicit higher-dimensional feature interactions, particularly through cross-product computations. Deep & Cross Network (DCN) [145], an initial approach in this direction, adopts a cross-network instead of FM, replacing the Wide component. While promising, DCN might not universally suit all scenarios. xDeepFM [82] achieves simplification by presenting a compressed interaction network (CIN) based on DCN [145], and the way of learning feature interaction is changed to a vector-wise idea referred to FM [118], which means calculating dot-product and then learning the explicit 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

6 

interactions. AutoInt [128] shares similarities with models like DCN [145] and xDeepFM [82], all aimed at capturing explicit high-dimensional feature interactions. However, AutoInt differentiates itself by sidestepping the combination of a cross-network and deep neural network. Instead, it directly integrates an interacting layer after the embedding phase. 

## **1.3 Survey and Tool** 

**Survey:** Abdi et al.[1] focuses on the field of context-aware recommendation based on matrix factorization, while Chen et al. [19] analyzes and concludes the theory of nonnegative matrix factorization with DNN. 

**Tool:** LibFM<sup>2</sup> [119] is a famous toolkit to achieve FM [118]. LibFFM<sup>3</sup> and xlearn<sup>4</sup> are used to achieve FFM [59]. For other algorithms, corresponding toolkits can also be found. Such as DeepCTR<sup>5</sup> , which can achieve various CTR prediction models including DeepFM [40]. 

## **1.4 Future Direction** 

**Synergistic Model Fusion for Complex Scenarios** An interesting avenue for future exploration lies in the synergy between different models. Instances like CAT-E and CAT-NT, as proposed by Zhao et al. [193], creatively combine SVD, FM, and gradient boosting, showcasing the potential of model fusion. These approaches cater to highly specialized scenarios, often tied to the designs of MF models based on SVD and FM. Investigating and expanding upon such combinations could yield even more tailored solutions for intricate use cases. 

## **2 SELF-SUPERVISED LEARNING FOR EMBEDDINGS** 



<!-- Start of picture text -->
Augmented<br>data<br>Raw Data  Encoder  Decoder<br>Augmented<br>data<br>(a)Architecture of Contrastive methods<br>Raw Data  Augmented<br>Encoder  Decoder<br>data<br>(b)Architecture of Generative methods<br><!-- End of picture text -->

Fig. 2. Data flow of SSL recommendation model 

Self-supervised learning (SSL) makes use of enormous unlabeled data to train machine learning models. The preliminary idea of SSL is that use pretext tasks to collect useful and transferable 

> 2libFM: https://github.com/srendle/libfm 

> 3LibFFM: https://github.com/ycjuan/libffm 

> 4xlearn: https://github.com/aksnzhy/xlearn 

> 5DeepCTR: https://github.com/shenweichen/DeepCTR 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

7 

information from the massive unlabeled data and leverage the pre-learned knowledge to achieve better performance on target tasks, which is formalized as follows: 



where _𝑆_ is the original data, and _𝑆_<sup>ˆ</sup> is the corrupted data (a.k.a augmented data). _𝑧𝜃_ is the encoder parameter to generate the node embedding vector, which is specific for the input type. _𝑑𝜙_ is the decoder to learn its own parameter _𝜙_ and refine the encoder parameter _𝜃_ for the main recommendation task. 

Based on Eq. 5, learning embedding parameters is a part process of the self-supervised learning recommendation (SSR) model which is conducted on both pretext tasks and recommendation tasks, and the supervised signals are produced from the raw data semi-automatically. Based on the type of auxiliary tasks, we divide the SSL methods into two categories: contrastive and generative. From Fig 2, we can preliminarily see the whole picture of the SSL-based recommendation model. Furthermore, within this section, contrastive and generative methods work with either sequence data or graph data as their input. Note that this section concentrates solely on graph self-supervised learning and does not explore other graph representation learning methods. In the next section, we will offer a more comprehensive discussion of graph embedding in recommender systems. 

## **2.1 Contrastive Learning for Embeddings** 

Contrastive learning (CL) is a vital research line in self-supervised learning, which aims to generate the self-supervised signal by minimizing the distance between views of the same sample and maximizing that between views of different samples in the embedding space. Different views can be generated by performing data augmentation on the training data. Corresponding to the Eq. 5, _𝑆_<sup>ˆ</sup> is the set of corrupted data processed by data augmentation techniques (i.e., _𝑆_<sup>ˆ</sup> = A( _𝑆_ )) which will be presented in the following paragraph. 

In summary, it contains three components including 1) data augmentation (i.e., S<sup>ˆ</sup> ); 2) sample encoder (i.e., _𝑧𝜃_ (·)) which is particular for the type of input (e.g., graph encoder and sequence encoder); 3) CL loss (i.e., L _𝐶𝐿_ ). The SSR model utilizes augmentation methods on the original data and the encoder formalizes the original data and corrupted data as vectors. Finally, to discriminate the augmented data and original data, it maximizes the mutual information between the positive pairs (i.e., augmented data from the same sample) and the negative pairs (i.e., augmented data from a different sample) via the CL loss. We first introduce the augmentation techniques of graph and sequence, then demonstrate CL methods based on the type of inputs, which typically are graphs and sequences. 

_2.1.1 Graph Data._ In the context of a graph G = ( _𝑉, 𝐸_ ) and adjacent matrix A, as shown in Fig 3, three common augmentation techniques are applied as follows: **Node/Edge Dropout** involves removing nodes or edges with a probability _𝛼_ , aiming to identify influential components for the recommendation task and enhance system robustness. **Graph Diffusion** introduces user-item similarity through new edges generated by weighted neighbor edge sums to model potential preferences, often selecting top-K similarities. **Subgraph Sampling** fabricates an augmented graph by the selection of nodes and edges, shaping a subgraph that accentuates local connectivity. These augmentation methods contribute to the self-supervision signal for learning high-quality embeddings. 

SGL [155] focuses on learning the user node and item node embedding in the user-item bipartite graph, which is the first work utilizing contrastive learning for recommendation by designing an auxiliary task to supplement the recommendation model. In particular, it first uses edge dropout, 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

8 

node dropout, and random walk to generate three views of the samples (e.g., user nodes or item nodes). Then, it creates positive pairs (i.e., ��A _𝑠_ ′<sup>_,_A</sup> _𝑠_<sup>′′</sup> � | _𝑠_ ∈S� ) using views of the same sample and negative pairs (i.e., ��A _𝑠_ ′1<sup>_,_A</sup> _𝑠_<sup>′′</sup> 1 � | _𝑠_ 1 _,𝑠_ 2 ∈S _,𝑠_ 1 ≠ _𝑠_ 2�) by views of different samples. The auxiliary task ensures that different views of the same nodes are similar in the embedding space. In other words, it aims to maximize the similarity between positive pairs and minimize that of negative pairs to learn the node embeddings. Thus, following SimCLR [15], it adopts the InfoNCE loss [110], which could maximize the agreement between positive samples and minimize the agreement between negative samples. Moreover, the node embeddings are computed by a LightGCN [46], a graph neural network (GNN) acting as the embedding layer. _𝜏_ is the hyper-parameter known as the temperature in the softmax function. _𝑠_ ∈S is the sample node from the user nodes or the item nodes. Finally, SGL combines the user and item contrastive loss. It jointly optimizes the InfoNCE loss (i.e., for the CL task) and the Bayesian personalized ranking (BPR) loss (i.e., for the recommendation task). 

HHGR [185] recommends items for groups in a user-item graph and tackles the issue of distorted local structures due to random node dropout. They propose a dual-scale node-dropping strategy: coarse-grained node dropout eliminates nodes across groups, while fine-grained node dropout targets nodes within the same preference group. Their approach shares similarities with the SGL method, focusing on mutual information between distinct node perspectives. In the realm of cross-domain recommendation utilizing CL, methods like CCDR [169] transfer valuable node embeddings from a well-equipped source domain to a less-equipped target domain. CCDR employs both intra-domain and inter-domain CL tasks for knowledge transfer. In the intra-domain CL task, two neighbor sets of node _𝑖_ are obtained, and GNN aggregation focuses on different neighbors of _𝑖_ to obtain two embeddings ( _𝑒𝑖_ , _𝑒_ ′( _𝑖_ ) ). The InfoNCE loss is then computed using the positive pair ( _𝑒_ ′( _𝑖_ ) _,𝑒𝑖_ ). The inter-domain CL task transfers knowledge across domains by conducting CL on nodes with identical properties (e.g., users and taxonomies) in both domains. Similarly, PCRec [137] addresses cross-domain tasks in two phases. The first phase involves pre-training on the source domain to extract knowledge, and the second phase employs target domain knowledge to transfer insights to the recommendation model. DCL [95] challenges the assumption of interest in only sampled negative items by conducting subgraph sampling through perturbation of the _𝐿_ -hop ego network of a given node. 

_2.1.2 Sequence Data._ In the context of sequence data, this section introduces four primary techniques to generate corrupted sequences to facilitate sequence augmentation. **Item Cropping** , inspired by image cropping in computer vision, is applied to contrastive learning in the sequential recommendation. **Item Masking** , borrowed from language models, involves masking elements in a sequence to prevent overfitting and encourage learning of high-order structures among tokens. Similarly, **Item Reordering** is proposed to ensure predictions remain invariant to item order, training recommendation models on augmented data with varying item sequences. **Item Substitution** enhances recommendation models by maintaining the original sequence’s structure while substituting highly correlated yet possibly redundant items. Item Insertion, akin to substitution, involves adding related items before each original item in a subset of the sequence. Specific details are shown in Fig. 4. 

Following the general pipeline of CL, the CL for sequences first generates different views of each sequence by the augmentation methods mentioned above. Then train the recommendation model with contrastive loss (e.g., SimCLR [15]). CL4SRec [170] deals with the sequential recommendation task. It adopts three augmentation methods: item cropping, masking, and reordering. Given a minibatch of _𝑁_ users, it generate 2 _𝑁_ augmented sequences { _𝑆𝑢_<sup>_𝑎_</sup> 1<sup>_𝑖,𝑆_</sup> _𝑢_<sup>_𝑎_</sup> 1<sup>_𝑗,𝑆_</sup> _𝑢_<sup>_𝑎_</sup> 2<sup>_𝑖,𝑆_</sup> _𝑢_<sup>_𝑎_</sup> 2<sup>_𝑗, . . . ,𝑆_</sup> _𝑢_<sup>_𝑎_</sup> _𝑁_<sup>_𝑖,𝑆_</sup> _𝑢_<sup>_𝑎_</sup> _𝑁_<sup>_𝑗_}, where</sup> _𝑆𝑢_<sup>_𝑎_</sup> _𝑛_<sup>_𝑖_denotes the sequence interacted by user</sup><sup>_𝑢_</sup> _𝑛_<sup>augmented by the augmentation method</sup><sup>_𝑎_</sup> _𝑖_<sup>(e.g.,</sup> 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

9 



<!-- Start of picture text -->
(a)Edge Dropout (b)Node Dropout<br>(c)Subgraph Diffusion (d)Subgraph Sampling<br><!-- End of picture text -->

Fig. 3. Augmentation methods of Graph 



Fig. 4. Augmentation methods of Sequence 

item cropping). Then, for each user _𝑢𝑖_ , it regards _𝑆𝑢_<sup>_𝑎_</sup> _𝑖_<sup>_𝑖,𝑆_</sup> _𝑢_<sup>_𝑎_</sup> _𝑖_<sup>_𝑗_</sup> as the positive pair, and other 2( _𝑁_ − 1) � � elements as negative samples. In addition, it applies the transformer encoder to compute the sequence embeddings. Eventually, the softmax cross entropy loss is used to discriminate the positive pairs from the negative ones. Similar to CL4SRec, CoSeRec [94] uses item substitution and insertion for data augmentation, while ContraRec [138] defines positive pairs from both the same sequence and different sequences with the same target item. 

Contrastive methods utilize the CL loss with augmented data to enhance embeddings by capturing latent patterns. However, selecting augmentation techniques is difficult, as there’s no fixed rule for their choice. This makes it necessary for researchers to choose data augmentation strategies carefully. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

10 

## **2.2 Generative Self-supervised Learning Methods** 

Inspired by the Mask language model (MLM) such as BERT [114], generative methods take advantage of their powerful ability to process the sequence data when reconstructing corrupted data (i.e., sequences with masked items) to learn the embedding. In this scenario, _𝑆_<sup>ˆ</sup> in the Eq. 5 usually is the set of data processed by the item masking method, and _𝐿𝑠𝑠𝑙_ is the BERT-like loss function (e.g., Eq. 6). we categorize these methods based on their input types, with the majority of them designed to work with sequences, while only a limited subset is tailored for graph-based data. 

_2.2.1 Graph-based Generative Methods._ It is difficult to directly conduct generative self-supervised learning using graph data. Thus, most existing work obtains sequences from graph data and then employs generative methods using the sequence data. For example, G-BERT [123] deals with the training data such that diagnosis and medical ontology are represented by a tree structure. The model utilizes the graph attention network [135] to learn the ontology embedding from diagnosis and medical tree-like graphs in order to make medication recommendations. Then, it feeds the ontology embeddings into a BERT-like model and pre-trains it with MLM-based tasks, which include the self-prediction task and the dual-prediction task. The former task is to predict the masked codes from the same type (i.e., medication or diagnosis) of ontology embeddings and the latter is to reconstruct the masked codes from different types of ontology embeddings. 

PMGT [92] focuses on multimodal recommendations, handling nodes with diverse information in a multimodal graph (e.g., item descriptions and images). They propose MCNSampling, a novel method to select neighboring nodes using importance scores and use BERT-Like patterns for node embedding learning. PT-GNN [43], instead of reconstructing masked nodes or items, addresses cold-start nodes with few neighbors using a meta-learning approach. It first pre-trains a transformer encoder on the embeddings of the first _𝐾_ neighboring nodes to simulate cold-start scenarios. Then, a GCN model is pre-trained, incorporating the meta embedding in each convolution step. It finally maximizes cosine similarity between the predicted embedding and the ground-truth embedding generated by NCF [49] using all neighbor nodes. 

_2.2.2 Sequence-based Generative Methods._ BERT4Rec [129] utilizes the BERT [26] encoder for sequential recommendation. It uses BERT to model sequential user behaviors. BERT4Rec first applies item masking on the sample sequence, where the masked items are replaced with the special token ’[mask]’. Then it trains the model to predict the original item being masked based on the items nearby in the sequence. Its loss is defined as: 



where S<sup>ˆ</sup> _𝑢_ is obtained by applying item masking on the original user behavior sequence S _𝑢_ . V _𝑢_<sup>_𝑚_</sup> is the set of masked items. _𝑣𝑚_<sup>∗is the original item for the masked item</sup><sup>_𝑣𝑚_, and</sup><sup>_𝑃_(</sup><sup>_𝑣𝑚_|Sˆ</sup><sup>_𝑢_)is the</sup> conditional probability calculated by the decoder of BERT. In the training phase, we can compute the item embedding through the encoder of BERT. There are several extensions of BERT4Rec for different tasks. For example, UNBERT [187] extends the BERT model for news recommendation. U-BERT [114] aims to learn user embeddings of the target domains by transferring knowledge from content-rich source domains. UPRec [163] explores extending the BERT4Rec model to handle heterogeneous information such as user attributes and social networks. 

Another line of research focuses on learning general item embeddings that are suitable for various recommendation tasks through generative methods. PeterRec [179] is to conduct learningto-learn idea [6] on cross-domain recommendation task. Dissimilar to traditional cross-domain methods [137, 169] which update the parameters of the whole model during the fine-tuning 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

11 

Table 1. Summary of Self-supervised Embedding learning. ’GCNs’ denotes that the method indicates that the graph encoder could be instantiated as various GCN such as lightGCN [46], graph attention network. 

|Pretext Task|Input|Methods|Data Augmentation|Sample Encoder|Recommendation Task|
|---|---|---|---|---|---|
||Graph|SGL [155]<br>HHGR [185]<br>CCDR [169]|Edge/Node Dropout, Random Walk<br>Node Dropout<br>Subgraph Sampling|GCN<br>GCNs<br>GAT|User Embedding/Node Embedding<br>Group Recommendation<br>Cross-domain Recommendation|
|||PCRec [137]|Subgraph Sampling|GIN|Cross-domain Recommendation|
|Contrastive||DCL [95]|Subgraph Sampling|GCNs|Next-item Recommendation|
|||CL4SRec [129]|Item Cropping/Reordering/Masking|Transformer based Encoder|Sequential Recommendation|
||Sequence|CoSeRec [94]<br>ContraRec [138]<br>H<sup>2</sup>SeqRec [78]|Item Substitution/Insertion<br>Item Masking/Reordering<br>Item Cropping/Reordering/Masking|Transformer based Encoder<br>Transformer based Encoder<br>Transformer based Encoder|Sequential Recommendation<br>Sequential Recommendation<br>Sequential Recommendation|
|||G-BERT [123]|Item Masking|GCN/Transformer based Encoder|Medical diagnosis Recommendation|
||Graph|PMGT [92]<br>PT-GNN [43]|Subgraph Sampling/Item Masking<br>Subgraph Sampling|Transformer-based Graph Encoder<br>GraphSAGE|Multimodal based Recommendation<br>Cold-Start Problem|
|Generative|Sequence|BERT4Rec [129]<br>UNBERT [187]<br>U-BERT [114]<br>UPRec [163]|Item Masking<br>Word Masking<br>Word Masking<br>Item Masking|Transformer based Encoder<br>Transformer based Encoder<br>Transformer based Encoder<br>Transformer based Encoder|Sequential Recommendation<br>News Recommendation<br>Cross-domain Recommendation<br>Multimodal based Recommendation|



phase, it subtly inserts small neural network modules into the backbone of the original model and only trains the small neural networks to adapt to the downstream tasks. Like the application of BERT [114] for learning the general words embedding, ShopperBERT [126] take advantage of the rich user behaviors to pre-train the BERT model based on nine auxiliary tasks for the general embedding. The experiment shows that it outperforms the model designed for one specific downstream recommendation task and indicates learning the general embedding is feasible. 

In conclusion, generative methods take advantage of the successful paradigm of the MLM and the fitting ability of the transformer encoder resulting in learning the high performance and capacity of embedding. Although it is suitable for the sequence data naturally, researchers extend the methods to deal with graph embedding learning by transforming the graph data into the sequence data. 

We summarize the data augmentation strategy, encoder, and recommendation task of all the self-supervised embedding learning methods mentioned in this section in Table 1. 

## **2.3 Surveys and Tools** 

**Surveys.** Unlike this section only focuses on embedding learning for recommendation systems, Yu et al. [175] demonstrates self-supervised learning methods for the entire recommendation system. Furthermore, it provides a fine-grained taxonomy in SSL to introduce the recommendation methods. It also develops a toolkit for easy implementation of SSR methods. 

**Tools.** SELFRec<sup>6</sup> is a framework for Self-supervised recommendation (SSR). It integrates multiple data augmentation techniques, popular datasets, and evaluation methods. Moreover, SELFRec is highly modularized and computationally efficient. It is also adaptable to the new SSR models. 

## **2.4 Future direction** 

**The choice of augmentation methods** : Augmenting the data with a suitable and effective view is able to generate a strong self-supervised signal to optimize the model effectively. However, to search for workable augmentation techniques, scientists usually test many strategies randomly resulting in the waste of labor force and sub-optimal model performance. Several works [167], [63] has studied the theory of augmentation selection in contrastive learning but less in recommendation task. Thus, principles to guide the choice of augmentation methods in recommendation tasks are waiting for exploration. 

> 6https://github.com/Coder-Yu/SELFRec 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

12 

**On-device embedding for recommendation model** : Recommendation models handle extensive user and item data, requiring substantial embedding capacity and memory. Traditional on-device deployment poses challenges due to device limitations. However, knowledge distillation has shown promise in shrinking model size, as demonstrated in works like [151] and [178]. Integrating selfsupervised learning methods could potentially compensate for performance loss in these compact models, an area with limited exploration. 

## **3 GRAPH BASED EMBEDDING** 

Recent advancements in graph machine learning have enabled off-the-shelf models to effectively capture complex relationships within graphs, producing node and graph embeddings that can be utilized for various downstream tasks. In recommender systems, users, items, attributes, and other auxiliary information can be used to create a variety of graph structures (e.g., social networks [44], user-item bipartite graphs [47], and knowledge graphs [140]). Recently, graph-based embeddings in recommender systems have received a lot of attention. As graph embeddings can leverage the topology information in graph data, they are shown to be effective in various tasks in recommender systems. This section classifies methods for learning graph embeddings in recommender systems based on the categories of graph data structures: 1) Embedding of Homogeneous Graphs; 2) Embedding of Bipartite Graphs; 3) Embedding of Heterogeneous Graphs; 4) Embedding of Hypergraphs. 



<!-- Start of picture text -->
(a)Homogeneous Graph (b)Bipartite Graph<br>(c)Heterogeneous Graph (d)Hypergraph<br><!-- End of picture text -->

Fig. 5. Graph types in the recommendation system 

## **3.1 Embedding of Homogeneous Graphs** 

Homogeneous graphs are the most basic graph structures, where all nodes in a homogeneous graph are of the same type. In recommender systems, user social relationships or potential connections of items can be naturally modeled as homogeneous graphs, where nodes can be represented as users or items, and edges between nodes can represent the friendship between users or denote different items purchased by the same user. Homogeneous graph-based graph learning algorithms (e.g., DeepWalk) can often be extended to more complex graph structures. Deepwalk [112] is one of 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

13 

the most fundamental graph learning algorithms, which is based on the random walk algorithm to sample a sequence of nodes in the graph and encode them using skip-gram [102]. Skip-gram is a classical word2vec model that maximizes the likelihood of central words to generate context words. In Deepwalk, the central and context words represent a node _𝑣𝑖_ and _𝑘_ nodes that co-occur with node _𝑣𝑖_ , where _𝑘_ is the window size of the skip-gram model. The objective function of Deepwalk can be formulated as follows: 



Where _ℎ𝑣𝑖_ denotes the embedding of node _𝑣𝑖_ , _𝜃_ denotes the parameters of the neural network. In this way, Deepwalk captures the structural information of the graph and generates similar embeddings for neighboring nodes. Asymmetric Proximity Preserving (APP) graph embedding [197] points out that in many downstream recommender system applications, the nodes in the graph do not have symmetry. For example, the probability of observing a user purchasing a computer _𝑖𝑐_ before buying a mouse _𝑖𝑚_ is much higher than that of seeing a user buying a mouse _𝑖𝑚_ before purchasing a computer _𝑖𝑐_ . Deepwalk is based on skip-gram needs to predict the context of each node and cannot capture the asymmetry of the nodes, and APP graph embedding only allows gradient updates in the direction of the sampled path. InfoWalk [200] pointed out that there are nodes without in-degree in the directed graph, that is, dangling nodes, which cannot be handled by APP graph embedding because it cannot access such nodes. 

However, as the graph size increases the number of possible different node sequences generated by random walk-based methods becomes not handleable. Some works try to solve this problem, such as LINE [130] and GNNs (e.g., GCN [65], GAT [136]), which are widely used in recommender systems. GNNs do not need to sample node sequences, they can be directly applied to the whole graph. To learn high-quality graph embedding that can be applied to downstream tasks of recommender systems, GNNs need to be extended to take the special properties of recommender system tasks. HyperSoRec [139] proposes that the user-user graph can be approximated as a structure of an _𝑛_ -order tree graph. Chami et al. [10] show that tree graph embedding in hyperbolic space can achieve better performance than its counterpart in Euclidean space which may suffer from severe distortion. HyperSoRec develops a hyperbolic mapping layer to map graph embedding in euclidean space to hyperbolic space. M2GRL [144] proposes to combine homogeneous graphs of multiple views to enhance sparse features and enrich node information. It constructs catalog view, instance view and shop view, then adopts random walk and SGNS [74] to learn an independent embedding of each view, and finally, map them to a shared embedding space and align them separately. DGENN [42] also uses more than one view of homogeneous graphs to learn embeddings jointly. It first learns embeddings from the user-user and item-item homogeneous graphs. Then it leverages the user-item graph as a regularization to ensure the learned embeddings are smooth. 

## **3.2 Embedding of Bipartite Graphs** 

The bipartite graph is a unique structure with two node sets, where edges connect nodes from different sets. This is commonly used in recommendation systems (e.g. user-item interaction graphs), represented as G = (V _𝐴_ ∪V _𝐵,_ E), with V _𝐴_ and V _𝐵_ as node sets, and E denoting the edges. 

Graph Convolutional Matrix Completion (GC-MC) [5] predicts ratings using a graph encoder to aggregate information from neighboring nodes with uniform weight. It aggregates user embeddings from one-hot embeddings based on interacted items, and item embeddings from one-hot vectors of interacting users. A bilinear decoder then reconstructs user-item ratings. However, GC-MC has drawbacks: 1) It employs one-hot encoding, hindering new node processing and becoming 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

14 

inefficient as the graph size grows. 2) GC-MC overlooks node features. STAR-GCN [186] resolves these by end-to-end learning of low-dimensional node embeddings. It simulates embedding new nodes with a masked vector, training the model to reconstruct embeddings. NGCF [149] overcomes the second drawback of GC-MC by considering the node features, and it learns embeddings as follows: 





Where N _𝑢_ and N _𝑖_ denote the number of neighbor nodes of user _𝑢_ and item _𝑖_ . The h _𝑢_<sup>(</sup><sup>_𝑙_)</sup> and h _𝑖_<sup>(</sup><sup>_𝑙_)</sup> denote the node embeddings of user _𝑢_ and item _𝑖_ in layer _𝑙_ . _𝑊_ stands for linear transformation, which can be a fully connected layer. 

LightGCN [46] argues that as the inputs of the user and item stem from ID embeddings lacking semantic information, there is no need for nonlinear transformations. Therefore, LightGCN introduces a straightforward and efficient aggregation method: 



Where N _𝑢_ and N _𝑖_ denote the number of neighbor nodes of user _𝑢_ and item _𝑖_ .The h _𝑢_<sup>(</sup><sup>_𝑙_)</sup> and h _𝑖_<sup>(</sup><sup>_𝑙_)</sup> denote the node embeddings of user _𝑢_ and item _𝑖_ in layer _𝑙_ . 

Although LightGCN greatly simplifies GCN, it still requires a long training time because multilayer message passing dominates the training of the model. The relatively slow training limits the application of LightGCN in real recommendation scenarios. UltraGCN [100] further removes the multi-layer messaging process by directly optimizing the cosine similarity of nodes and neighbors to capture the higher-order collaborative signals between users and items, and it uses a negative sampling strategy to avoid oversmoothing. 

Recognizing the inherent sparsity within user-item interaction graphs, Collaborative Similarity Embedding (CSE) [12] suggests enhancing embeddings by incorporating higher-order similarities among nodes of the same type. CSE introduces two modules, namely DSEmbed and NSEmbed, to capture user-item similarity and inter-item/inter-user similarity within a user-item bipartite graph. DSEmbed employs an optimization scheme based on rating data, aiming to model the proximity between users and items. This is achieved by maximizing the log-likelihood function of positive and negative samples. The optimization objective of DSEmbed can be formulated as: 



where _𝑝_<sup>�</sup> _𝑣 𝑗 >𝑖 𝑣𝑘_ | h<sup>�</sup> is calculated as follows: 



Conversely, NSEmbed employs random walks and CBOW [102] to predict central nodes, enabling the modeling of higher-order neighbor relationships among users or items. Another approach, GE [168], proposes joint training to address the sparsity observed in user-POI bipartite graphs. This is achieved by incorporating multiple graph perspectives, where supplementary bipartite graphs (e.g., POI-POI, POI-Region) augment the model’s efficacy by providing enriched information. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

15 

## **3.3 Embedding of Heterogeneous Graphs** 

The heterogeneous graph is a more realistic representation of many real-world graphs than simplified graphs like homogeneous and bipartite graphs. These graphs encompass diverse node categories that can be interconnected. In contrast to homogeneous graphs with just one node type, heterogeneous graphs are more intricate and contain more abundant information. In the context of recommender systems, incorporating diverse relationships can lead to more accurate learned entity embeddings. For instance, combining a user-item bipartite graph with a social network of users can enhance the precision of predicting user preferences. 

Recent research focuses on enhancing user embeddings in recommender systems by incorporating social influence modeling. DiffNet [158] and GraphRec [29] tackle social and user-item networks separately. DiffNet oversimplifies social influence modeling by assuming uniform influence among a user’s neighbors. In contrast, GraphRec employs GAT [136] to better model real-world social influence by weighing friends’ influence based on the similarity of their initial embeddings. DiffNet++ [157] builds upon DiffNet by introducing a unified framework that considers both social networks and user-item bipartite graphs. It addresses the limitation of DiffNet’s inability to distinguish varying degrees of influence from different neighbors through a multi-level attention mechanism. GES [142] leverages related side information like brand to aggregate nodes’ embeddings for obtaining item embeddings in heterogeneous graphs. However, these methods primarily account for static social influence. DANSER [161] introduces a dual GAT to capture both static and dynamic influence, acknowledging that a user’s impact on friends can vary based on items, leading to more realistic embeddings. 

The knowledge graph is also a type of heterogeneous graph that is widely used in recommender systems. Nodes in the knowledge graph represent entities, edges represent the relationships between entities, and edge attributes describe the nature of these relationships. By accurately describing real-world relationships, the knowledge graph provides rich semantic information that can improve interpretability and alleviate the sparsity problem in recommender systems. To learn entity embeddings in the knowledge graph, several translation-based models such as TransE [8], TransH [152], and TransR [84] have been utilized. However, these approaches fail to fully utilize the topological and semantic information in the knowledge graph, which is precisely what GNNs excel at. To overcome this, methods like KGCN [141] and KGAT [148] apply GCN and GAT respectively to produce higher-quality embeddings. Nevertheless, these methods disregard users’ diverse intents when modeling user-item relationships, thus constraining embedding learning quality. Addressing this, KGIN [150] introduces an intent layer between users and their interacted items for finer-grained relationship modeling. 

## **3.4 Embedding of Hypergraphs** 

The hypergraph is a graph structure in which an edge can connect arbitrarily many nodes, and edges in a hypergraph are called hyperedges. In recommender systems, hypergraphs can be used to model complex entity relationships. A hypergraph can be represented as G = (V _,_ E _,_ H), where V represents the set of nodes, E represents the set of hyperedges, and H represents the incidence matrix. 

IHGNN [20] enhances node embeddings through hypergraphs, revealing higher-order interaction patterns in user query histories. It introduces hyperedges ( _𝑢,𝑞, 𝑝_ ) for user query and product, employing three high-order feature interactions for hyperedge embedding aggregation. HyperGroup [41] targets group recommendation, addressing potential misalignment between user and group preferences by representing groups as hyperedges. It aggregates neighboring hyperedges 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

16 

Table 2. Summary of Graph Embedding Methods 

|Graph type|Method|Message Passing|
|---|---|---|
|Homogeneous Graph|DeepWalk [112], APP [197], InfoWalk [200]<br>M2GRL [144], SGNS [74], DG-ENN [42]<br>LINE [130]|Random walk<br>Multiple view graphs + GCN<br>GCN|
||PGE [79]|Time decayweighted|
|Bipartite Graph|GC-MC [5], STAR-GCN [186], NGCF [149]<br>LightGCN [46]<br>CSE [12], FBNE [13]<br>GE [168]|Average neighbor embedding<br>Normalized summation<br>Random Walk<br>Multiple viewgraphs + LINE|
||DiffNet [158]<br>GraphRec [29], DiffNet++ [157], DANSER [161]|Average neighbor embedding<br>GAT|
|Heterogeneous Graph|GES [142]|GAT+Side Information|
||TransGRec [159]<br>GHL [109]|GCN<br>Gated GNN|
|Hyper Graph|IHGNN [20], HyperGroup [41]<br>HEMR [72]|Weighted average of Hyperedge<br>Hyperedge random walk|



to capture group similarity. HEMR [72] focuses on music recommendation using hypergraph embeddings. It employs hyperedge-level random walks, followed by skip-gram for node embedding learning. The jump probability _𝑝𝑒_ to each node, is defined as follows: 



Where _𝐷_ ( _𝑒_ ) denotes the degree of the current hyperedge _𝑒_ , _𝛼_ and _𝛽_ are hyperparameters. This approach encourages jumping out of low-degree hyperedges and exploring the complex relationships of nodes in the hypergraph. 

The graph embedding methods mentioned above are summarized in Table 2. We classify the graph embedding methods according to the way they aggregate information in the graph. For example, random walk denotes aggregation of information through a sequence of nodes sampled by random walk. 

## **3.5 Surveys & Tools** 

**Surveys.** Unlike our discussion focusing on learning graph embedding in recommender systems, Wang et al. [146] focuses on the design of graph neural networks in different types of graph structures, while they do not consider the application of hypergraphs in recommender systems. Gao et al. [31] focuses on the application of graph neural networks in different recommender scenarios such as sequence recommendation and multi-behavior recommendation. 

**Tools.** We also collected some high quality tools [146]<sup>7</sup> and repositories<sup>89</sup> on graph-based recommendation systems. 

> 7https://github.com/maenzhier/GRecX 

> 8https://github.com/tsinghua-fib-lab/GNN-Recommender-Systems 

> 9https://github.com/DLUTElvis/GNN4Rec-Papers 

> , Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

17 

## **3.6 Future Direction** 

**Dynamic Graph Embedding for Recommendation.** In graph-based recommender systems, dynamic graph evolution is vital. Embeddings from static graphs can result in uninteresting recommendations for users. Current research has rarely tackled dynamic graph embedding in recommender systems. While PGE [79] considers temporal decay for item weights, it still treats graphs as static and overlooks evolving network structures. Leveraging dynamic graph neural networks [99, 174] for effective recommender system applications is a critical area for future exploration. 

**Fair Graph Embedding for Recommendation.** Fair machine learning has recently emerged as a prominent area of focus in the machine learning community. Its primary objective is to alleviate bias of various forms in models developed through data-driven techniques. Within the domain of graph recommendation systems, the emphasis is on preventing models from relying on biased signals as patterns and subsequently propagating these biases throughout the graph. Given the profound societal impact of recommendation systems, it is crucial to ensure the acquisition of fair embeddings. While prior studies (e.g., GEAR [98] and FairGo [156]) can apply to this, fair graph embedding remains underexplored. Also, benchmarking fairness in graph-based recommendation systems is a key research avenue. For a comprehensive understanding of fair machine learning, you can refer to the survey [101]. 

**Edge Embedding for Recommendation.** Existing generic GNN frameworks seldom place a strong emphasis on handling edge features. GNNs that do incorporate edge features often adopt domain-specific strategies, customizing their approaches to address particular tasks. Examples of such tasks include quantum chemistry [36], circuit design [184], and graph matching [176]. However, this specialized focus has contributed to a notable gap in research when it comes to exploring the significance of edge features within GNN-based recommender systems. Within the context of recommender systems, the majority of research efforts have traditionally centered on node features, user-item interactions, and graph structures, largely overlooking the potential wealth of information that edge features can provide. This oversight is surprising given that edges in recommender systems can encode essential information, such as the strength of useritem connections, the temporal dynamics of interactions, or the trustworthiness of user reviews. Neglecting edge features in the context of recommender systems not only limits our understanding of the nuances within user-item interactions but also hampers the development of more accurate and context-aware recommendation models. To address this gap, there is a growing need for research that delves into the role of edge features within GNN-based recommender systems. Investigating how to effectively incorporate and leverage edge features, alongside node features and graph structures. 

## **4 HASH EMBEDDING** 

In recommender systems, an alternative to the prevalent one-hot encoding for representing categorical attributes is hashing. Hashing embeddings were introduced to address the limitations associated with one-hot encoding. One-hot encoding often results in high-dimensional and extremely sparse feature matrices, posing significant scalability challenges, especially within complex deep recommendation systems. Hashing embeddings provide an effective solution to these challenges, offering benefits for both scalability enhancement and complexity reduction. Hashing embedding involves the application of one or more hash functions to the original sparse encoding, effectively curbing storage demands and computational overhead. Compared to raw one-hot encodings, hash embeddings manage to maintain recommendation effectiveness while substantially reducing the complexity of training and inference. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

18 

Considering various hash embedding methods based on factors like the number of hash functions, their utilization, and post-processing steps, we categorize the literature into three groups: 1) single function hash embedding; 2) multiple functions hash embedding; 3) dense hash embedding. 

## **4.1 Single Function Hash Embedding** 

The hashing trick, initially introduced by Yahoo [154], uses a single hash function to map the features into hash values. This method is particularly relevant in collaborative filtering scenarios, exemplified by matrix factorization (M = UV<sup>_𝑇_</sup> ∈ R<sup>_𝑚_×</sup><sup>_𝑛_</sup> ), where U ∈ R<sup>_𝑚_×</sup><sup>_𝑑_</sup> and V ∈ R<sup>_𝑛_×</sup><sup>_𝑑_</sup> are factorized matrices of the sparse M. The hashing trick diminishes the dimensions of these matrices through a binary encoding function _𝑓𝐸_ and hash function _𝑓𝐻_ . In this context, with feature index ( _𝑗,𝑘_ ), and position index _𝑝_ , _𝑓𝐸_ transforms ( _𝑗,𝑘_ ) into values in {0 _,_ 1}, effectively positioning the feature in hash table position _𝑖_ using hash function _𝑓𝐻_ . This leads to U<sup>′</sup> ∈ R<sup>_𝑚_′×</sup><sup>_𝑑_</sup> and V<sup>′</sup> ∈ R<sup>_𝑛_′×</sup><sup>_𝑑_</sup> , where _𝑚_<sup>′</sup> ≪ _𝑚_ and _𝑛_<sup>′</sup> ≪ _𝑛_ , as follows: 



Here, _𝑓𝐸_<sup>′and</sup><sup>_𝑓_</sup> _𝐻_<sup>′are separate functions. The hashing function maps feature values to {0</sup><sup>_,_1</sup><sup>_,_2</sup><sup>_, ...,𝑚_′ −</sup> 1} _,𝑚_<sup>′</sup> ≪ _𝑚_ , while _𝑓𝐸_ ( _𝑗,𝑘_ ) = 0 if _𝑓𝐻_ ( _𝑗,𝑘_ ) ≠ _𝑝_ , and 1 otherwise. It is equivalent to its matrix representation. For instance, consider the compression of U ∈ R<sup>_𝑚_×</sup><sup>_𝑑_</sup> into W ∈ R<sup>_𝑚_′×</sup><sup>_𝑑_</sup> , where _𝑚_<sup>′</sup> ≪ _𝑚_ . This reduction simplifies the computation of the final hash embedding, as exemplified by the user vector U _𝑝,_ ·: 



In this equation, H ∈{0 _,_ 1}<sup>_𝑚_′×</sup><sup>_𝑚_</sup> is a hash matrix, and e _𝑝_ is a _𝑑_ -dimensional one-hot vector with its _𝑝_ -th element equals to 1. _ℎ𝑖𝑗_ of the hash matrix H ∈{0 _,_ 1}<sup>_𝑚_′×</sup><sup>_𝑚_</sup> is defined as: 



The hashing trick has profoundly impacted the field of hash embedding within recommendation systems. This approach stands as the pioneer of simple, yet powerful techniques that markedly enhance the efficiency of original one-hot embeddings, particularly when dealing with highdimensional features. 

## **4.2 Multiple Functions Hash Embedding** 

To counteract the information loss stemming from hash collisions, approaches utilizing multiple hash functions have been devised. These methods can be categorized based on their encoding functions. The concept behind Embeddings with Multiple Hash Functions aligns with the hashing trick’s modulus hashing and hash embedding table. 

A notable technique is the Bloom filter [7], which employs multiple hash functions to map features into an embedding space. This process generates a binary embedding through multiple hash values, enabling intermediate products to be recovered or mapped back from the embedding to the final product without compromising information integrity. Another innovation, hash embedding [132], merges word embedding and the hashing trick. It entails computing the hash embedding as the product of embedding vectors and the corresponding element in the weight vector for each token. Unlike the hashing trick, which employs a solitary hash function, hash embedding deploys 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

19 

multiple functions. It initially queries the relevant embedding based on the feature index and subsequently employs a weighted sum of these embeddings. 

Hybrid hashing [183], introduced by Twitter, follows a similar premise. It employs two hash functions but applies them exclusively to infrequent feature values. For frequent feature values, the one-hot full embedding method is employed. This approach divides the embedding space considering feature frequencies, ensuring that vital information from the top- _𝐾_ frequent features is retained. By employing a combination of one-hot full embedding and hybrid hashing, Facebook’s Q-R trick [125] adopts the complementary partition idea with multiple hash functions to avert hash collisions. Q-R trick introduces complementary hash functions through two embedding tables: W1 ∈ R<sup>_𝑙_×</sup><sup>_𝑑_</sup> and W2 ∈ R _<u>𝑎𝑙</u>_<sup>×</sup><sup>_𝑑_</sup> for each categorical feature with _𝑎_ distinct values. The final embedding results from pooling the outputs of each hash function. The hash embedding combines two components: W1 represents the coarse-grained aspect where multiple values can map to the same row, while W2 functions as the fine-grained counterpart, compensating for collisions in W1. The ultimate hash embedding is computed as: 



Here, H and H<sup>′</sup> denote corresponding hash matrices, and ⊙ signifies element-wise multiplication. This design employing complementary hash functions ensures representation uniqueness. 

## **4.3 DHE: Dense Hash Embeddings** 

In contrast to the aforementioned methods, Google’s Dense Hash Embedding (DHE) [62] introduces several significant innovations. This approach focuses on enhancing hash functions to generate denser embedding vectors. Notably, DHE deploys a DNN-based decoding layer in lieu of conventional embedding tables, leading to markedly superior performance compared to other hash embedding techniques. Remarkably, its performance can even rival that of one-hot encoding. However, it’s worth noting that this enhancement comes at the trade-off of a larger model size relative to other hash embedding methods. 

DHE employs a multitude of hash functions, approximately 1 _,_ 000 in number, along with a DNN. These hash functions map categorical features like IDs to high-dimensional vectors (e.g., 1 _,_ 024 dimensions), with vector elements in the range of {1 _,_ 2 _, ...,𝑚_ }. These vectors can be left normalized, drawn from a uniform distribution, or subjected to transformation into a normal distribution via the Box-Muller method [9]. Moreover, a DNN with _ℎ_ layers and dropout regularization serves as a decoder. It maps the identity-encoded vectors of dimension _𝑘_ to the final hash embedding vectors of dimension _𝑑_ . DHE stands out in its ability to maintain the uniqueness of representations compared to other original hash embedding methods. Furthermore, it addresses the out-of-vocabulary challenge by ensuring the feature embedding is influenced by changes in embedding net parameters. DHE also offers a mechanism for enhancing generalization. This involves concatenating different series of categorical features to the ID-type feature during the decoding process, further improving generalization capabilities. 

Finally, We summarize the hash function numbers, hash model size, etc., of all the hash embedding methods mentioned in this section in Table 3. 

## **4.4 Survey and Tool** 

**Survey:** Kang et al. [62] mention many hashing embedding methods with various techniques in different application scenarios. Ghaemmaghami et al. [35] and Li et al. [77] present an overview of popular hash embedding models in deep recommendation systems. They mainly discuss the initial purpose of hash functions: compressing the models while controlling the hash collision. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

20 

Table 3. Summary of Hash Embedding Models 

|**Model**|**Embedding Vec**|#**Hash Func**<br>#**Decoding NN Layer**|**Model Size**|
|---|---|---|---|
|Hashing Trick [154]|One-hot|1<br>1|_𝑂_(_𝑚𝑑_)|
|Bloom Embed [122]|(Multi) One-hot|2∼4<br>1|_𝑂_(_𝑚𝑑_)|
|Hash Embed [132]|(Multi) One-hot|2<br>1|_𝑂_(_𝑛𝑘_+_𝑚𝑑_)|
|Hybrid Hashing [183]|(Multi) One-hot|2<br>–|_𝑂_(_𝑚𝑑_)|
|Q-R Trick [125]|(Multi) One-hot|2<br>3|_𝑂_(_𝑚𝑑_+ <sup>_𝑛𝑑_2</sup><br>_𝑚_<sup>)</sup><br>|
|BH [172]|(Multi) One-hot & Binary|Multi (e.g. 4)<br>–|∼_𝑂_( <sup>_𝑛𝑑_</sup><br>1000<sup>)</sup>|
|DHE [62]|Dense|∼1000<br>Deep|_𝑂_(_𝑘𝑑_NN+ (_ℎ_−1)_𝑑_<sup>2</sup><br>NN <sup>+</sup><sup>_𝑑𝑑_NN)</sup>|



**Tool:** MurmurHash3<sup>10</sup> is a widely used version of the hash function MurMurHash. It can provide 32-bit and 128-bit hash. Then CityHash<sup>11</sup> (64, 128, and 256-bit output) and SpookyHash<sup>12</sup> (128-bit output) are both inspired by MurmurHash3 and perform better in terms of compotational efficiency. 

## **4.5 Future Directions** 

**Enhancing Hash Embedding with Multiple Functions** In stark contrast to employing a solitary hash function, leveraging multiple hash functions or embracing binary encoding has proven to exert superior control over the scale of the embedding matrix, concurrently reducing the loss of information. Recent innovative designs highlight [62] the beneficial impact of incorporating an augmented number of hash functions. Such a framework possesses the potential to seamlessly replace the extensive and costly hash embedding tables utilized in preceding methodologies, presenting a notably more efficient storage alternative. 

## **5 AUTOML & EMBEDDING** 

Auto machine learning (AutoML) is a process that automatically generates optimal machine learning solutions for those tasks that are repetitive and time-consuming. In the embedding learning scenario, it could search for the best size of the embedding layer. Concretely, the traditional deep learning approach employs a fixed, uniform embedding size for all features, disregarding the varying importance of each feature in recommendation tasks, which inevitably leads to suboptimal performance. Additionally, the use of excessively large embedding sizes contributes to inflated storage usage and elevated computational expenses. To counter these issues, the AutoML framework introduces the concept of tailoring appropriate embedding sizes for each feature. Neural Architecture Search (NAS) plays a pivotal role in addressing this concern within the realm of AutoML. NAS’s substantial advancements now enable efficient exploration of optimal configurations, including embedding sizes, for recommendation systems within a feasible timeframe. 

The methods discussed in this section will be classified by the kinds of the search strategy in NAS which contains reinforcement learning [61], gradient-based algorithm [121], evolutionary algorithm [113]. In addition, considering that there are a few papers on the evolutionary algorithm, we introduce this category with other unique methods together. 

## **5.1 Reinforcement learning based method** 

Reinforcement learning is quite simple to grasp. Think of it like improving your game strategy: if a move or tactic leads to a higher score, reinforcing it enhances your performance. This learning approach involves five main parts: the environment (like a game scenario), the controller or 

> 10MurmurHash3: https://github.com/hajimes/mmh3 

> 11CityHash: https://github.com/google/cityhash 

> 12SpookyHash: http://burtleburtle.net/bob/hash/spooky.html 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

21 

player, actions, rewards, and status. In the case of embedding dimension search (EDS), consider a recommendation model as the setting, evaluating performance to determine rewards. The player, often represented by a policy network, decides what move to make. Rewards are based on how well the model performs. The player uses these rewards to decide how to adjust the current embedding size. The status refers to the player’s situation, like the network parameters. 

NIS [57] initiates Embedding Dimension Search (EDS) by organizing features based on frequency, creating an embedding E that assigns larger sizes to frequent features. It divides E into matrices using a fixed search grid. Within this reinforcement learning framework, a recommendation model computes rewards, and a neural network-based player selects actions through soft-max probabilities. The reward integrates memory costs and target objectives into a composite loss function. Asynchronous Advantage Actor-critic (A3C) [106] trains the player and recommendation model alternately. ESAPN [88] dynamically searches for suitable embedding sizes for users and items in stream recommendation. At first, It establishes potential embedding size ranges. Using a recommendation model tailored for stream recommendations, it employs a reinforcement learning approach. The controller, comprising user and item multilayer perceptrons, uses frequency and current embedding size as inputs for the policy network. The controller’s action decides whether to increase or maintain embedding sizes. The reward reflects its predictive capability and guides its decision-making process, which can be calculated from losses of the stream recommendation model as follows: 



where the input is a loss sequence of users or items with length _𝑇_ , _𝐿𝑡_<sup>(</sup><sup>_𝑢_/</sup><sup>_𝑖_)</sup> represents the _𝑡_ -th prediction loss of user _𝑢_ or item _𝑖_ , and _𝐿_ is the loss of the current item or user. The specific loss function is suitable for the typical recommendation task. To optimize the parameter of the policy network according to the reward, the bell-man equation is formulated as follows: 



where Φ is the parameter of the policy network for the user or item, _𝑎_ , and _𝑠_ denotes the action and state, respectively. However, it is hard to calculate its gradient in practice, thus it uses Monte-Carlo sampling to evaluate the ∇Φ _𝐽_ (Φ). In the end, inspired by ENAS, it uses sampled validation data to optimize the policy network and train the recommendation model based on training data. 

In summary, reinforcement algorithm-based methods solve the non-differentiable problem of the hard selection in discrete search space and are an efficient and effective search strategy to significantly reduce the search space in embedding size. However, the controller takes a hard selection in a pre-defined embedding candidate size which is likely to achieve a sub-optimal performance. To get higher performance in embedding size selection, the soft selection strategy is widely adopted in gradient-based methods. 

## **5.2 Gradient-based Method** 

With the introduction of the Differentiable Neural Architecture Search (DARTS) method proposed by Liu et al. [87], gradient-based methods have gained attention. These methods enable the transformation of the search space from discrete to continuous, and the optimization process is guided by gradient calculations or inspired by DARTS. For example, DNIS [22] argues that a pre-defined discrete search space could poor the flexibility of the searching model. Thus, it optimizes the NIS approach by leveraging a soft selection layer to relax the search space to continuous space for performance improvement. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

22 

To be specific, it denotes an embedding _𝐸_ with max dimension K by a multi-hot embedding index vectors set D = { _𝑑_ 1 _,_ · · · _,𝑑𝑁_ } and a values vectors set V = { _𝑣_ 1 _,_ · · · _, 𝑣𝐾_ } with the search space of 2<sup>_𝑁𝐾_</sup> size. As same as the NIS, it divides the features into _𝑆_ blocks based on the descending order of frequency. Thus, the search space is reduced from 2<sup>_𝑁𝐾_</sup> to 2<sup>_𝑆𝐾_</sup> . After that, it defines the soft selection layer as a numerical matrix _𝛼_ ∈ R<sup>_𝑆_×</sup><sup>_𝐾_</sup> with elements in the range [0 _,_ 1], which aims to shrink the elements in embedding within a small number. Subsequently, the approach defines the soft selection layer as a numerical matrix A ∈ R<sup>_𝑆_×</sup><sup>_𝐾_</sup> , where the elements are constrained to the range of [0 _,_ 1]. The purpose of this layer is to reduce the values within the embedding to a smaller range. The soft selection operation can be calculated as follow: 



where � _𝑒𝑖_ is the _𝑖_ -th row of output embedding and _𝛼𝑖_ is _𝑖_ -th row of A matrix. In addition, matrix A is gained through learning. By inserting a soft selection layer between the embedding layer and interaction layer, it could be optimized jointly like the DARTS method. In particular, it defines a bi-level optimization problem that has been solved by DARTS. Similar to DNIS, autoSrh [153] follows the pipeline of DNIS to make tabular Data prediction. The difference is that it debates the idea that setting a pruning threshold could satisfy the requirement of limited memory usage. 

Moreover, to improve the hard selection in ESAPN, AutoEMB [195] also designed the soft selection layer as a weighted sum operation. Concretely, similar to ESAPN, it defines some candidate embedding sizes for users and items, and employs matrices to transform user and item embedding of candidate sizes into a uniform embedding size for plugging into deep learning-based recommendation models. However, the author noted that thesimple linear transformation process results in significant variation in the values of embeddings with different sizes, rendering them incomparable. To address this issue, the approach applies Batch-Norm with Tanh activation to normalize the transformed user and item embedding vectors. Subsequently, it introduces two multiple perceptron networks to select the embedding size. For an end-to-end differentiable framework, it takes a soft selection layer to calculate the final embedding size. 

However, there is another approach called AutoDim [194] that addresses the issue of nondifferentiability by employing Gumbel-softmax tricks as a soft selection layer. AutoDim builds upon AutoEMB by extending its input from just users and items to various feature fields such as gender, age, and more. This expansion allows for broader and more comprehensive embeddings that can capture additional contextual information for improved performance. 

Another gradient-based idea to find the optimal embedding size is to prune the original embedding through a mask matrix which is learned from train data. For example, AMTL [173] utilizes an Adaptively-Masked Twins-based layer (AMTL) to generate the mask vector. Specifically, the input of AMTL is the frequency attribute of features such that the rank of frequency in a given feature field and AMTL consists of two multiple perceptrons (i.e., h-AML and l-AML) for high-frequency and low-frequency data respectively to avoid the parameter update dominated by high-frequency sample. Then, the final output is the weighted sum to fuse the output of two branch AMLs. Lastly, the approach applies a differentiable temperature softmax function to the output, generating a probability mask vector for selecting an embedding size for high or low-frequency features. However, considering the high training costs of AMTL, SSEDS [115] introduces a saliency criterion to determine the significance of each element in the embedding matrix. The saliency score is obtained through a single forward-backward propagation. Using the saliency score, the mask matrix is generated by retaining the top-K important parameters in the embedding, taking into account memory constraints. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

23 

Table 4. Summary of AutoML Embedding, N, K represents # of features and the original length of the feature vector. S and T denote # of the block of the feature and the feature vector, and F _𝐺_ denotes # of the feature group. U and I indicate # of user and item samples. 

|Search Strategy|Methods|Search Space|Search space Continuity|Storage space Limitation|
|---|---|---|---|---|
|Rif li|NIS [57]|(_𝑆_+1)<sup>_𝑇_</sup>|Discrete|✓|
|enorcement earnng|ESAPN [88]|2<sup>(</sup><sup>_𝑈_+</sup><sup>_𝐼_)</sup><sup>_𝑇_</sup>|Discrete|�|
||DNIS [22]|2<sup>_𝑆𝐾_</sup>|Continuous|�|
||AutoEMB [195]|2<sup>(</sup><sup>_𝑈_+</sup><sup>_𝐼_)</sup><sup>_𝑇_</sup>|Continuous|�|
|Gditbd|AutoDim [194]|_𝑇_<sup>|F</sup><sup>_𝐺_|</sup>|Continuous|�|
|raen-ase|AMTL [173]|-|Continuous|✓|
||AutoSrh [66]|2<sup>_𝑆𝐾_</sup>|Continuous|✓|
||SSEDS [115]|2<sup>_𝑁𝐾_</sup>|Continuous|✓|
|Evolutionaryalgorithm|RULE [17]|(2<sup>_𝑁_</sup>−1)<sup>|F</sup><sup>_𝐺_|</sup>|Discrete|✓|
|Parameter Regularization|PEP [91]|2<sup>_𝑁𝐾_</sup>|Continuous|✓|
|Ah bddi bii|ANT [83]|2<sup>_𝑆𝐾_</sup>|Continuous|�|
|ncor emengs comnaton|AutoDis [39]|2<sup>_𝑆𝐾_</sup>|Continuous|�|



## **5.3 Other methods** 

Evolutionary algorithms, inspired by natural evolution, have been used for optimizing neural network parameters since the twentieth century. In Neural Architecture Search (NAS), these algorithms involve creating an initial set of architectural designs (seed), combining and mutating them, and evaluating the performance of resulting designs. For instance, RULE [17] employs an evolutionary algorithm to learn adaptable embeddings with distinct sizes for different items, akin to NIS. In RULE, an estimator decides which designs to eliminate based on mixed embedding block data. The estimator is trained using these compositions and evaluated using metrics like recall. Evolution proceeds by selecting a parent model and generating a child model through mutations. Two strategies are used: swapping embedding blocks between item groups and selecting blocks for one group. Importantly, only one mutation occurs per round. The child model is added to both the seed set and the cache set. Meanwhile, the poorest performing design is removed from the seed set to maintain a constant size. This process of creating child models and updating sets continues for a finite number of rounds. At the end of the evolution, the cache set holds the best-performing models, offering a collection of designs with superior performance. 

Another unique thought regards the embedding matrix size selection as a regularization problem. Inspired by Soft Threshold Reparameterzation [71], different from AMTL, PEP [91] directly prune the embedding matrix E by learning a threshold automatically. Before training the recommendation model, it is argued, according to the Lottery Ticket hypothesis, that the parameters can be initialized by performing an element-wise product with E0 and _𝑚_ , where _𝑚_ ∈{0 _,_ 1}<sup>_𝑁_×</sup><sup>_𝐷_</sup> represents the mask matrix generated from E<sup>ˆ</sup> , and E0 denotes the unpruned embedding parameters. 

There is also a research line of combining learnable anchor embedding matrices to form an optimal embedding matrix. ANT [83] and autoDis [39] follow this idea to search for a suitable embedding size. ANT firstly learn meta embedding _𝐴_ ∈ R<sup>|</sup><sup>_𝐴_|×</sup><sup>_𝑑_</sup> containing a set of anchor embedding _𝐴_ = { _𝑎_ 1 _,_ · · · _,𝑎_ | _𝐴_ | } _,_ | _𝐴_ | _<<_ | _𝑉_ |, where | _𝑉_ | is the number of rows in original embedding _𝐸_ . Then, it integrates the set of anchor embedding by using a trainable sparse transformation from _𝐴_ to _𝐸_ . However, different from the hard selection of anchor embedding in ANT, autoDis designs a differentiable automatic discretization network to execute a soft selection of meta-embeddings (i.e., anchor embeddings in ANT). 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

24 

## **5.4 Survey and Tool** 

**Survey** : In terms of Deep Recommender Systems (DRS), Zheng et al. [196] and Chen et al. [11] both demonstrate how to perform the autoML technique on each component of DRS including feature selection, feature embedding, and feature interaction with a different taxonomy of method. **Tools** : EasyRec<sup>13</sup> provides a convenient tool for users to develop and customize the recommendation model. The novel part of EasyRec is that it integrates the autoML API from Alibaba Cloud, which supplies lots of autoML-related services including auto feature selection, and auto feature interaction. 

## **5.5 Future Direction** 

**Progressive NAS in EDS** : Progressive NAS (PNAS) is a novel neural architecture search (NAS) scheme that leverages the shortest path algorithm to discover the most efficient path between a start and target node within the search space. Considering the extensive search space involved in embedding size, PNAS holds significant promise for its application in the search for optimal embedding sizes in the field of EDS. 

**Unsupervised NAS in embedding** : Conventionally, the best model architecture is determined based on human-labeled data. However, [85] proposed a new unsupervised scheme of NAS called UnNAS in visual tasks. The performance of the sampled architecture needs to be evaluated in an unsupervised manner. In addition, the model selected by UnNAS has comparable performance with that chosen by the supervised NAS method. Thus, it is a promising pattern in NAS where we could explore an efficient method of EDS. 

## **6 QUANTIZATION** 

Quantization, a fundamental technique in information theory, emerges as a promising avenue to bolster the scalability of deep recommender systems. It aims to compress continuous _highdimensional vectors_ into _low-dimensional discrete codes_ . In deep recommender systems, there can be tens of thousands of categorical features that are encoded into dense embeddings. The huge memory cost caused by the embeddings poses a challenge to the deployment of deep recommender systems. In this context, quantization offers a strategic pathway to alleviate the memory burden associated with embeddings, thereby contributing to the enhanced scalability and operational efficiency of recommendation systems. 

Quantization compresses the original embedding into a set of codes. The length of this set of codes will be much smaller than the original embedding. One can either (1) use such discrete codes as new embeddings or (2) reconstruct the original embedding with a small distortion. Therefore, quantization allows us to discard the original embedding, leading to pronounced reductions in memory consumption and offering an effective way to address the scalability challenges in recommender systems. 

In this section, we classify quantization methods into: (a) binary quantization and (b) codebook quantization based on the form of quantization embedding. In particular, we additionally discuss the application of quantization embedding on online recommender systems. 

## **6.1 Binary Quantization** 

Binary quantization converts the embedding into a binary code b ∈{±1}<sup>_𝑟_</sup> , where _𝑟_ denotes the length of the binary code. In the binary code representation, the similarity _𝑥𝑢𝑖_ between user _𝑢_ and item _𝑖_ can be written as: 

> 13https://github.com/alibaba/EasyRec 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

25 

Embedding in Recommender Systems: A Survey 



<!-- Start of picture text -->
D-dimensional<br>Vector<br>PQ codebooks C oncat<br>M-dimensional PQ Embedding:  [1,2,2,3]<br>AQ codebooks<br>AQ Embedding:  [1,2,3,3]<br><!-- End of picture text -->

Fig. 6. Comparison of PQ-based and AQ-based methods 



where b _𝑢_ , d _𝑖_ denote the binary quantization embedding of user _𝑢_ and item _𝑖_ , respectively. 

Discrete Personalized Ranking (DPR) [191] maps embeddings to binary codes by optimizing AUC. However, AUC is typically utilized as an evaluation metric instead of an optimization objective, and optimizing its ranking can be an NP-hard combinatorial optimization problem. To address this, DPR follows OPAUC [32] by approximately optimizing AUC through a least-squares surrogate loss function, instead of directly optimizing AUC rank. The optimization objective of DDL can be formulated as: 



Where | _𝐼𝑢_<sup>+|denotes the number of user-item interactions that exist in the dataset,|</sup><sup>_𝐼_</sup> _𝑢_<sup>−|denotes</sup> the number of all user-item without interactions, | _𝑈_ | denotes the number of users, and _𝐷_ = �( _𝑢,𝑖, 𝑗_ )| _𝑢_ ∈ _𝑈,𝑖_ ∈ _𝐼𝑢_<sup>+</sup><sup>_, 𝑗_∈</sup><sup>_𝐼_</sup> _𝑢_<sup>−</sup> �. 

In particular, to obtain more compact and high-quality codes, DPR adds the balance constraint and the irrelevant constraint. The balance constraint encourages maximizing the entropy of the code, and the irrelevant constraint encourages the bits in the code to be as independent as possible. The objective function of DPR can be formulated as the following: 



Where B and D denote the matrices of _𝑏_ and _𝑑_ stacked by columns. For this discrete optimization problem, DPR solves it with softening constraints and alternating optimization. However, DPR does not impose a constraint on the gap between the binary code and the initial embedding, which is improved by Discrete Deep Learning (DDL) [192]. DDL uses a bag-of-words model to learn the embedding of the text of an item and minimizes the gap between it and the corresponding binary code. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

26 

While binary quantization is theoretically sound and interpretable, it limits the scalability of quantization embeddings by making them discrete. Compact embeddings may lose vital information. In contrast, codebook quantization is a preferable approach, as it condenses features into a set of codes. Each code can possess multiple potential values. Moreover, codebook quantization fits better with deep learning techniques. It trains continuous codebook elements rather than discrete ones. We’ll delve into codebook quantization in the next section. 

## **6.2 Codebook Quantization** 

Codebook quantization is a family of methods that compress the original embedding matrix into a set of codebooks and indexes so that we can reconstruct the embedding that will eventually be used for downstream recommendation tasks with codebooks and indexes that only require a small memory footprint. Here, we present three types of codebook quantization methods: unsupervised and supervised codebook quantization. 

Most of the existing codebook quantization methods are variations and extensions of Product Quantization (PQ) [55], PQ decomposes the high-dimensional feature space R<sup>_𝐷_</sup> into a cartesian product C = _𝐶_<sup>1</sup> × · · · × C<sup>_𝑀_</sup> ∈ R<sup>_𝑀_×</sup><sup>_𝐾_</sup> of lower-dimensional subspaces. So the high-dimensional vector can be compressed into a compositional representation of _𝑀_ codebooks, and the quantization embedding can be obtained by concatenating the _𝑀_ sets of codewords. The objective function of Vanilla PQ can be formulated as follows: 



Where x denotes the sample features and _𝑖_ (x) denotes the quantization encoder that encodes the features into the indexes. 

Vanilla PQ does not optimize the objective directly, it applies K-means clustering to each of the _𝑀_ subspaces and compresses each subspace into _𝐾_ codewords, so that each feature vector is compressed into quantization embedding _𝑖_ (x) = {1 _, ..., 𝐾_ }<sup>_𝑀_</sup> . By computing the Euclidean distance, Vanilla PQ can be applied to the nearest neighbor search. However, Vanilla PQ has a serious problem in that it directly divides the features into different subspaces with equal spacing in an ordered manner and may ignore the possibility of a high correlation between subspaces, which can substantially degrade the performance of quantization. Optimized Product Quantization (OPQ) [34] uses the rotation matrix _𝑅_ ∈ R<sup>_𝑀_×</sup><sup>_𝑀_</sup> to optimize the decomposition of subspaces to reduce the correlation between subspaces, so the objective function is modified as: 



Since the above objective function is difficult to optimize, OPQ adopts the strategy of fixing _𝑅_ and codebook _𝐶_ one at a time to optimize them alternatively. 

The PQ-based approach requires decomposing the embedding space into independent subspaces, so this approach leads to large information loss when the subspace embeddings are strongly correlated. Additive Quantization (AQ) [3] adopts a different strategy from PQ, it directly assigns _𝑀_ codebooks to the whole high-dimensional space, and the _𝑀_ compressed vectors are summed to obtain the quantization embedding. 



, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

27 

Since optimizing the above equation is a complex combinatorial optimization problem, AQ chooses beam search [124] as the approximation algorithm to select the appropriate codewords for the codebook to complete the quantization. 

Both PQ and AQ-based quantization methods work in an unsupervised manner, employing unsupervised k-means clustering or heuristic beam search algorithms to optimize their objective functions. However, these methods fail to address the distortion of embeddings caused by quantization, leading to a partial loss of original embedding information. Consequently, obtaining high-quality embedding becomes challenging. Differentiable Product Quantization (DPQ) [16] proposes softmax-based and centroid-based methods to minimize reconstruction loss approximately between raw embeddings and quantization embeddings. This approach leads to higher-quality quantization embeddings compared to unsupervised PQ algorithms. 

Supervised methods [16, 180] enhance quantization via reconstruction loss, but recent research [80, 166, 182] shows it’s insufficient. Tailoring objectives for specific tasks in recommender systems proves more effective. Product Quantized Collaborative Filtering (PQCF) [81] challenges separate user and item quantization using PQ. Misaligned coordinates make this suboptimal. PQCF minimizes rating prediction loss, moving from Euclidean to the inner product space. It rotates C _𝑈_ and C _𝑉_ with orthogonal matrix H, aligning spaces and addressing PQ-based methods issues. The rating estimated by PQCF can be written as: 



where b _𝑢_ , d _𝑖_ denote the quantization embedding of user _𝑖_ and item _𝑗_ , respectively. PQCF adds regularization to the rating prediction loss to form the objective function: 



Alongside optimizing downstream recommendations, new optimization goals have emerged. DistillVQ [165], inspired by knowledge distillation, sets its objective as a similarity function measuring differences in relevance score distributions between teacher and student models (e.g., KL divergence). Another innovation, LightRec [80], enhances reconstruction loss with two functions, minimizing differences in user-item ratings pre- and post-quantization, as well as alterations in recommendation ranking. Matching-oriented Product Quantization (MoPQ) [166] shows that better quantization reconstruction doesn’t always mean better downstream performance. MoPQ improves accuracy through contrastive learning, modeling query-quantization matching via multinoulli process. 

## **6.3 Online Quantization** 

Modern recommender systems face constant influxes of new users, and traditional quantization methods (PQ, AQ) lack the capacity to manage streaming data, thus presenting challenges in realworld applications. Similarly, prior online hash algorithms require recalculating all user embeddings upon new user arrivals, which is often impractical in recommendation systems. To tackle this, Online PQ [171] posits that the impact of new data on the codebook is minimal due to the smaller size of incremental data. It updates only codewords for new data points without altering quantization embedding for original data. Online PQ maintains a sliding window for data processing, continuously applying K-means clustering for new codewords. However, being unsupervised, Online PQ doesn’t optimize quantization error, risking information loss and low-quality embedding. To address this, Online OPQ [86] extends to streaming data by solving the orthogonal procrustes problem to ensure subspace orthogonality during codebook updates. Online AQ [90] extends AQ, maintaining consistent objective functions. For streaming data adaptability, Online AQ derives codebook update 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, 28 Ruocheng Guo. 

strategies and related regret bounds via linear regression closed solutions and matrix inversion lemma [133]. Unlike AQ’s beam search for codeword selection, Online AQ introduces an efficient block beam search, a trade-off between hill climbing and beam search. 

Finally, we summarize all the quantization algorithms mentioned in this section in Table 5, where you can find the objective function, training method, and whether the algorithm is feasible for online quantization, etc. 

Table 5. Summary of Quantization Embedding Methods. QD=Quantization Distortion; RPL=Rating Prediction Loss; BPR=Bayesian Personalized Ranking Loss; BCE=Binary CrossEntropy; MCL=Multinoulli Contrastive Loss; KDL=Knowledge Distillation Loss. 

|**Type**|**Method**|**Codebook size**|**Supervised/Unsupervised**|**Objective function**|
|---|---|---|---|---|
|Binar Quantization|DPR [191]|No codebook|Supervised|AUC averaged|
|y|DDL [192]|No codebook|Supervised|QD+RPL|
||PQ [55], OPQ [34]|D/M|Unsupervised|QD|
||AQ [3]|D|Unsupervised|QD|
||DPQ [16]|D/M|Supervised|QD|
|Codebook Qantization|PQCF [81]|D/M|Supervised|QD+RPL|
||LightRec [80]|D/M|Supervised|QD+BPR+KDL|
||xLightFM [56]|Learnable|Supervised|QD+BCE|
||MOPQ [166]|D/M|Unsupervised|QD+MCL|
||Distill-VQ[165]|D/M|Unsupervised|QD+KDL|
|Oli titi|Online PQ [171]|D/M|Unsupervised|QD|
|nne Qanzaon|Online OPQ [86]|D/M|Unsupervised|QD|
||Online AQ [90]|D|Unsupervised|QD|



## **6.4 Survey and Tool** 

**Survey** To the best of our knowledge, no survey on quantization embedding for recommender systems has been conducted prior to this. A concurrent study [77] during the same period discussed vector quantization in the context of compressing embeddings in recommender systems. However, their primary focus was on the precision of embedding compression, whereas our emphasis lies in discussing the applications of quantized embeddings across various scenarios within recommender systems, including quantization embedding learning in online recommendation contexts, along with specific quantization techniques. Moreover, existing surveys on quantization either concentrate on image coding [107] or are restricted to product quantization [2]. Some existing reviews on codebooks also belong to the scope of quantization. For example, [96] discusses a variety of VQ Codebook Generation algorithms, and [117] discusses codebook design in the field of object recognition. **Tool** NEQ [25] provides various implementations of quantization algorithms (e.g. PQ, AQ, and OPQ). We also refer the reader to a vector quantization repository<sup>14</sup> that implements some novel quantization algorithms(e.g. Residual VQ [73]). 

## **6.5 Future Direction** 

**Multi-task Quantization** Previous studies [80, 166, 182] have highlighted that optimizing solely for reconstruction loss is inadequate for producing high-quality quantization embeddings. For better quantization, tailoring learning tasks to specific downstream recommendation contexts 

> 14https://github.com/lucidrains/vector-quantize-pytorch 

> , Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

29 

can enhance pattern capture. Introducing multi-task learning objectives alongside quantization distortion minimization as a new objective empowers models to grasp more valuable patterns, potentially leading to improved generalization. 

**Dynamic Codebook Quantization** In online recommender systems, accommodating changing user preferences is crucial. Accurate quantization is essential for domain features that exert a significant impact on user preferences, like user interaction features. However, less impactful domain features like user location may need smaller codebooks. Exploring methods for capturing changes in user preferences and dynamically adjusting the codebook size for each domain feature accordingly is a promising research direction that warrants attention. Such research could considerably enhance the efficiency and effectiveness of online recommender systems. 

## **7 APPLICATIONS OF EMBEDDING IN DEEP RECOMMENDATION SYSTEM** 

## **7.1 Embedding-based method for CTR tasks** 

With the advancement of various Embedding techniques, the capacity for expressive embedding has seen significant improvements. Embedding can now encode a wide range of features, rendering it a highly valuable technique. Moreover, mastering large-capacity embedding presents a formidable challenge. Consequently, it is advantageous to separate the training of embeddings from that of deep recommendation models. These attributes have made embedding pre-training an increasingly favored approach. Specifically, the typical procedure involves initially learning the dense vectors during the pre-training phase, followed by the incorporation of the well-trained embedding layer into the deep model for training the remaining parts of the model. Below are some practical examples of embedding pre-training in the context of industry applications, particularly in the domain of click-through rate (CTR) prediction. 

**Embedding pre-training with machine learning methods** : The Factorisation-machine supported neural network (FNN) [189] represents a classic feed-forward neural network, with its foundational layer being an embedding layer initialized using parameters pre-trained on the factorization machine (FM) [120]. Additionally, FNN has experimented with training the embedding layer through methods like Boltzmann machines(RBM) [51] or denoising auto-encoders (DAE) [4]. However, experiments in the realm of click-through prediction tasks demonstrate that the FNN model outperforms alternative techniques, including logistic regression, FM, RBM, or DAE-based embedding models. Facebook [50], on the other hand, employs a logistic regression model, with its input encoded via embeddings generated from a gradient-boosting decision tree, to accomplish ad click predictions. In this approach, the classification tree components function similarly to individual embedding layers that can be independently trained. 

**Embedding pre-training with deep neural network methods** : Beyond initializing embeddings with machine learning models, the industry has achieved significant performance via end-to-end deep neural network (DNN) methods. For instance, the word2vec model [103], introduced by Google utils a single-hidden layer neural network to pre-train the word embedding. Furthermore, Alibaba [142] delves into graph embeddings through the Deepwalk [112] technique, facilitating large-scale e-commerce recommendations. Addressing the challenge of cold-start items lacking historical interaction data, Alibaba initializes cold-start item embeddings using side information from neighboring similar items with substantial user interaction. Beyond the two-tower architecture, attention mechanisms and transformer encoders present alternative architectures for embedding pre-training. For example, in Fig. 7, Alibaba [198] combines the embedding layer and the welldesigned MLP layer to make CTR prediction. In this method, DIN uses the attention mechanism to calculate the attention scores between the candidate ad and the goods the users bought. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

30 



<!-- Start of picture text -->
Output<br>DIN Architecture<br>MLP<br>concat & flatten<br>weighted SUM<br>X X X<br>attention score attention score attention score<br>single attention single attention single attention<br>embedding layer<br>user features items1 items2 items3 target item<br><!-- End of picture text -->

Fig. 7. The Architecture of DIN 

While pre-training embeddings can enhance industrial deep learning models, it’s crucial to recognize that neural networks often require frequent or real-time training to adapt to the latest positive examples, especially in CTR prediction scenarios. This demand places a significant strain on computation resources and time. Therefore, it becomes essential to research and explore various training frequencies and strategies to strike a balance between training costs and model performance. 

## **7.2 Embedding-based method for retrieval tasks** 

Modern recommender systems consist of three core components: the recall layer, ranking model, and re-ranking model. Due to computational limitations, real-world recommendation systems can not consider all items for ranking. Instead, the recall layer narrows down the selection to a smaller set of items, facilitating real-time recommendations. The re-ranking model, positioned closest to users, identifies relationships among ranked items from the ranking model and rearranges the candidate item sequence. Concurrently, the recall layer significantly impacts recommendation accuracy by reducing the candidate pool compared to the full set. However, if irrelevant items are included, it could degrade recommendation quality, making the recall layer a notable performance bottleneck in real-time systems. This section delves into embedding applications within the recall layer, encompassing single-tower and two-tower models. 

**Single-tower Model** A prominent example of a single-tower recall model is the YouTube DNN video recall model [24]. This model involves pre-learned embeddings for videos and search tokens. The recall process computes the average of watched video and search token embeddings, generating the user’s historical embedding. Furthermore, the user’s profile and contextual features combine with the historical embedding, forming input for an MLP. This input is condensed into a lowerdimensional space, yielding the final user embedding, known as the recall vector. During training, 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

31 

the softmax function gauges user-class probabilities and minimizes cross-entropy against the relevant label. To mitigate class imbalance and minimize the vast number of classes, negative sampling akin to Word2vec [102] is employed. For recall, the nearest neighbor algorithm, e.g., Faiss [58], retrieves _𝐾_ video embeddings most akin to the user embedding. 

**Two-tower Model** The single-tower model combines the user and item features and inputs them into an MLP to learn the user embedding for recall. However, this approach incurs a high computational cost for online computation. The two-tower model utilizes two separate neural networks to generate the user and item embeddings and then computes their similarity using the inner product. The two-tower model offers the advantage of being able to calculate the item embedding offline and only requires a calculation of the user embedding and similarity online. Additionally, the inner product operation in the two-tower model is more efficient compared to the softmax in the single-tower model, making it suitable for building recommendation systems with high real-time performance. The DSSM [54], introduced by Microsoft for computing semantic similarity, is one of the earliest two-tower models. It inputs a query and document and employs an MLP to learn the embeddings. The cosine similarity of the embeddings represents the semantic similarity between the query and the document, and the DSSM can be adapted for use as a recommendation model by replacing the query and document with user and item. 

Both the DSSM and YouTube DNN Video Recall Models create negative samples through random sampling, but this approach is prone to generating false negative examples. This limitation could impact the performance of the recommendation system. The MOBIUS [28], a two-tower model was proposed by Baidu to address the limitations of random sampling in creating negative samples. This model employs a teacher network to calculate the relevance score of the samples and selects those with low relevance scores as negative samples, thus providing a more effective strategy for mining difficult negative samples. The EBR model [53] proposed by Facebook uses the simplest two-tower structure, which uses the same hard negative sample mining strategy as MOBIUS. Further, EBR designs an embedding ensemble, which trains multiple models using different negative samples and integrates the output of the models using weighted or concatenated embedding. This design allows the model to effectively capture the diverse preferences and behaviors of users, leading to improved recommendation accuracy. EBR also finds that merging location features and social relationships into embedding has a significant impact on recommendation performance, which can also be used in subsequent studies. 

Although the above-mentioned two-tower model has excellent processing speed, the intersection of user and item features in the two-tower model only occurs when the similarity between user embedding and item embedding is calculated, leading to a loss of information in the embeddings. As a result, this approach to decoupling the user and item in the two-tower model can greatly improve the speed of the recommendation system, but may also limit its accuracy. To perform feature intersection in the two-tower model, the DAT [177] proposed by Meituan concatenates two augmented vectors onto the user and item feature vectors as the input to the two towers. The enhancement vectors are designed to capture the positive interactions of the other tower. Specifically, DAT calculates the MSE between the enhancement vector and the embedding of the other tower as the loss of feature interaction learning when the training sample is positive. When the training sample is negative, this part of the loss is ignored. To alleviate the sample category imbalance problem in industrial scenarios, DAT proposes category alignment loss to constrain the distance between the main category covariance matrix and other category covariance matrices. **Multi-interest Embedding Model** Capturing multiple interests of users is one of the keys to recall, which prevents the recommendation system from being dominated by a single interest of users. The MIND model [75], applied at Tmall, alleviates the limitation of recall ability for niche content in the recommender system by incorporating a multi-interest extraction layer to capture users’ 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

32 

potential multiple interests in the user-item click sequence. It designs a capsule network-based multi-interest extraction layer in the recall layer, which decomposes the embedding interactions of sequential items into multiple embeddings. The SDM [97] applied to Taobao sequence recall utilizes a self-attention mechanism to capture multiple interests of users within a session, and a gated neural network to fuse the long-term and short-term interests of users. Specifically, SDM defines a session based on the time window of the interaction (e.g., an interaction belongs to the same session if the interaction difference is below a certain threshold, with a maximum session length limit). The most recent session is considered a short-term behavior, while earlier sessions are considered long-term behaviors. Since the shorter sequence of items visited by short-term behavior allows for designing a more complex model, SDM uses LSTM and self-attention mechanism to learn its embedding, while long-term behavior applies attention mechanism and simple fully connected layer to learn the embedding, and finally, the recall vector is obtained by fusing long-term and short-term interests through the gated neural net. The Airbnb listing recommendation system [37] generates embeddings of users and listings for recall or ranking based on user click sessions and booking sessions. It utilizes a skip-gram model to encode the sequence of clicked listings to capture users’ short-term interests and make real-time, personalized recommendations within a session. Meanwhile, Airbnb wants to capture users’ long-term interests from their historical booking session sequences, but due to the sparse booking behavior of users, the recommendation system faces a serious cold-start problem, which makes it difficult to learn meaningful embeddings. To alleviate this problem, Airbnb proposes an embedding learning method based on similar users and similar listings. Specifically, Airbnb clusters user and item separately and treats user type as user id, generates a booking session consisting of listing type, and learns the embedding of user type and item type, this idea is similar to group recommendation. 

**Approximate Near Neighbor Embedding Search** The above-mentioned model aims to train the user embeddings for recall, and after getting the user embeddings use an approximate near neighbor embedding search algorithm to recall the item ID. Most of the existing work uses Faiss [58], Facebook’s open-source similarity search library that can compute efficiently on GPU, to complete the recall task. Milvus [143] integrates the functionality of several vector similarity search libraries (e.g. Faiss [58], Microsoft SPTAG [14]) to develop a high-performance vector similarity search system for distributed systems and dynamic data. 

## **7.3 Empowering Recommendation Systems with Enhanced Embeddings Using Large Language Models** 

Recently, there has been a notable surge of interest in the incorporation of Large Language Models (LLMs) into embedding-based recommendation systems [160]. For the enhancement of embeddings in recommendation systems with LLMs, two prevalent strategies emerge: 

**Direct Inference of Embeddings Utilizing LLMs.** In this strategy, using LLMs, we can extract embedding vectors from textual descriptions of users, items, and user-item interactions. This is particularly effective in scenarios with limited data for user-item interactions. For example, ChatRec [33] generates embeddings through prompting a LLM with prompts generated by a multiinput prompt constructor module. The module forms a natural language paragraph that captures user intent and item details by considering various inputs, such as user-item history interactions, user profiles, specific user queries, and dialog history. GeneRec [147] uses user profiles, historical feedback, and collected Web data (e.g., common facts and knowledge from Wikipedia) to create personalized embeddings through LLMs. Specifically, it can generate personalized embeddings by analyzing user instructions (e.g., fusing images, audio, and natural languages) and feedback (e.g., clicks), resulting in tailored content like landscape micro-videos in the chosen style. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

33 

**Fine-tuning Embeddings with LLMs.** LLMs can leverage user-item interactions through selfsupervised fine-tuning, enhancing the quality of embeddings and subsequently boosting the overall performance of the system. This approach treats user or item IDs as distinct untrained tokens and optimizes them with a self-supervised fine-tuning process, such as generative retrieval tasks [162]. For example, in the case of PEPLER [76], it successfully embedded IDs into a semantic space for better embedding explanation ability. PEPLER utilizes a two-stage approach for fine-tuning embedding vectors and model parameters. In the first stage, the task of generating recommendation explanations relies on a sequential fine-tuning procedure for next-token prediction, using a negative log-likelihood (NNL) loss. Initially, the ID embedding vectors are trained with the LLM frozen, followed by a fine-tuning procedure that updates both the LLM and the vector parameters. In the second stage, two tasks including next-token prediction by minimizing the NNL loss and rating prediction minimizing the mean square error, are both employed to improve the generated explanation along with recommendation performance. PPR [162] incorporates contrastive loss as auxiliary losses by employing two unique data augmentation techniques: prompt-level augmentation involves randomly masking elements in user embedding vectors, and behavior-level augmentation that masks some items in the user-item interaction sequence. This allows for the learning of personalized embedding vectors that harness the information from user profiles. 

LLMs can play an important role in recommendation systems by extracting features and enhancing embeddings through the incorporation of the rich semantic information embedded in the pretrained and fine-tuned LLMs. LLM-enhanced embeddings have demonstrated their potential in enhancing performance in applications like video recommendation [89] and recommendation explanation generation [199]; however, the challenge of effectively integrating LLMs with recommendation systems remains an open problem [160]. For example, LLMs demand substantial computational resources and time, which may be unfeasible in resource-constrained and real-time recommendation scenarios. Additionally, LLMs have exhibited biases [93], like gender bias [131], which can potentially lead to untrustworthy recommendations. 

Although there have been notable improvements in the integration of LLMs with recommendation systems, research on embedding techniques is still in its nascent phase. As far as we know, there have been no comprehensive attempts to summarize and investigate the role of embedding approaches in recommendation systems that depend on large language models. This subsection, therefore, presents a preliminary groundwork. We anticipate that there will be a significant focus on exploring embeddings in the context of LLM-based recommendation systems. 

## **8 CONCLUSION** 

In summary, the use of embeddings in recommender systems has shown great promise in recent years. These methods can capture complex relationships between items and users, leading to better performance compared to traditional approaches. However, there are still challenges to overcome, such as scalability and understandability. This survey aims to provide a comprehensive overview of how embeddings are used in recommender systems, including the different techniques employed, their effectiveness, and the current issues and future directions in the field. By sharing recent advancements, this survey paves the way for future exploration and improvements in the ever-evolving landscape of recommendation systems. 

## **REFERENCES** 

> [1] Mohamed Hussein Abdi, George Okeyo, and Ronald Waweru Mwangi. 2018. Matrix factorization techniques for context-aware collaborative filtering recommender systems: A survey. (2018). 

> [2] S Twareque Ali and Miroslav Engliš. 2005. Quantization methods: a guide for physicists and analysts. _Reviews in Mathematical Physics_ 17, 04 (2005), 391–490. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, 34 Ruocheng Guo. 

- [3] Artem Babenko and Victor Lempitsky. 2014. Additive quantization for extreme vector compression. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition_ . 931–938. 

- [4] Yoshua Bengio, Li Yao, Guillaume Alain, and Pascal Vincent. 2013. Generalized denoising auto-encoders as generative models. _Advances in neural information processing systems_ 26 (2013). 

- [5] Rianne van den Berg, Thomas N Kipf, and Max Welling. 2017. Graph convolutional matrix completion. _arXiv preprint arXiv:1706.02263_ (2017). 

- [6] Luca Bertinetto, João F Henriques, Jack Valmadre, Philip Torr, and Andrea Vedaldi. 2016. Learning feed-forward one-shot learners. _Advances in neural information processing systems_ 29 (2016). 

- [7] Flavio Bonomi, Michael Mitzenmacher, Rina Panigrahy, Sushil Singh, and George Varghese. 2006. An improved construction for counting bloom filters. In _European Symposium on algorithms_ . Springer, 684–695. 

- [8] Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko. 2013. Translating embeddings for modeling multi-relational data. _Advances in neural information processing systems_ 26 (2013). 

- [9] George EP Box. 1958. A note on the generation of random normal deviates. _Ann. Math. Statist._ 29 (1958), 610–611. 

- [10] Ines Chami, Zhitao Ying, Christopher Ré, and Jure Leskovec. 2019. Hyperbolic graph convolutional neural networks. _Advances in neural information processing systems_ 32 (2019). 

- [11] Bo Chen, Xiangyu Zhao, Yejing Wang, Wenqi Fan, Huifeng Guo, and Ruiming Tang. 2022. Automated Machine Learning for Deep Recommender Systems: A Survey. _ArXiv_ abs/2204.01390 (2022). 

- [12] Chih-Ming Chen, Chuan-Ju Wang, Ming-Feng Tsai, and Yi-Hsuan Yang. 2019. Collaborative similarity embedding for recommender systems. In _The World Wide Web Conference_ . 2637–2643. 

- [13] Hongxu Chen, Hongzhi Yin, Tong Chen, Weiqing Wang, Xue Li, and Xia Hu. 2020. Social boosted recommendation with folded bipartite network embedding. _IEEE Transactions on Knowledge and Data Engineering_ (2020). 

- [14] Qi Chen, Haidong Wang, Mingqin Li, Gang Ren, Scarlett Li, Jeffery Zhu, Jason Li, Chuanjie Liu, Lintao Zhang, and Jingdong Wang. 2018. _SPTAG: A library for fast approximate nearest neighbor search_ . https://github.com/Microsoft/ SPTAG 

- [15] Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. 2020. A simple framework for contrastive learning of visual representations. In _International conference on machine learning_ . PMLR, 1597–1607. 

- [16] Ting Chen, Lala Li, and Yizhou Sun. 2020. Differentiable product quantization for end-to-end embedding compression. In _International Conference on Machine Learning_ . PMLR, 1617–1626. 

- [17] Tong Chen, Hongzhi Yin, Yujia Zheng, Zi Huang, Yang Wang, and Meng Wang. 2021. Learning elastic embeddings for customizing on-device recommenders. In _Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining_ . 138–147. 

- [18] Tianqi Chen, Weinan Zhang, Qiuxia Lu, Kailong Chen, Zhao Zheng, and Yong Yu. 2012. SVDFeature: a toolkit for feature-based collaborative filtering. _The Journal of Machine Learning Research_ 13, 1 (2012), 3619–3622. 

- [19] Wen-Sheng Chen, Qianwen Zeng, and Binbin Pan. 2022. A survey of deep nonnegative matrix factorization. _Neurocomputing_ 491 (2022), 305–320. 

- [20] Dian Cheng, Jiawei Chen, Wenjun Peng, Wenqin Ye, Fuyu Lv, Tao Zhuang, Xiaoyi Zeng, and Xiangnan He. 2022. IHGNN: Interactive Hypergraph Neural Network for Personalized Product Search. In _Proceedings of the ACM Web Conference 2022_ . 256–265. 

- [21] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra, Hrishi Aradhye, Glen Anderson, Greg Corrado, Wei Chai, Mustafa Ispir, et al. 2016. Wide & deep learning for recommender systems. In _Proceedings of the 1st workshop on deep learning for recommender systems_ . 7–10. 

- [22] Weiyu Cheng, Yanyan Shen, and Linpeng Huang. 2020. Differentiable neural input search for recommender systems. _arXiv preprint arXiv:2006.04466_ (2020). 

- [23] Weiyu Cheng, Yanyan Shen, Yanmin Zhu, and Linpeng Huang. 2018. DELF: A Dual-Embedding based Deep Latent Factor Model for Recommendation.. In _IJCAI_ , Vol. 18. 3329–3335. 

- [24] Paul Covington, Jay Adams, and Emre Sargin. 2016. Deep neural networks for youtube recommendations. In _Proceedings of the 10th ACM conference on recommender systems_ . 191–198. 

- [25] Xinyan Dai, Xiao Yan, Kelvin KW Ng, Jie Liu, and James Cheng. 2019. Norm-Explicit Quantization: Improving Vector Quantization for Maximum Inner Product Search. _arXiv preprint arXiv:1911.04654_ (2019). 

- [26] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. Bert: Pre-training of deep bidirectional transformers for language understanding. _arXiv preprint arXiv:1810.04805_ (2018). 

- [27] Yue Ding, Yuxiang Shi, Bo Chen, Chenghua Lin, Hongtao Lu, Jie Li, Ruiming Tang, and Dong Wang. 2021. Semideterministic and contrastive variational graph autoencoder for recommendation. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 382–391. 

- [28] Miao Fan, Jiacheng Guo, Shuai Zhu, Shuo Miao, Mingming Sun, and Ping Li. 2019. MOBIUS: towards the next generation of query-ad matching in baidu’s sponsored search. In _Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ . 2509–2517. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

35 

- [29] Wenqi Fan, Yao Ma, Qing Li, Yuan He, Eric Zhao, Jiliang Tang, and Dawei Yin. 2019. Graph neural networks for social recommendation. In _The world wide web conference_ . 417–426. 

- [30] Simon Funk. 2006. Netflix update: Try this at home. 

- [31] Chen Gao, Yu Zheng, Nian Li, Yinfeng Li, Yingrong Qin, Jinghua Piao, Yuhan Quan, Jianxin Chang, Depeng Jin, Xiangnan He, et al. 2021. Graph Neural Networks for Recommender Systems: Challenges, Methods, and Directions. _arXiv preprint arXiv:2109.12843_ (2021). 

- [32] Wei Gao, Rong Jin, Shenghuo Zhu, and Zhi-Hua Zhou. 2013. One-pass AUC optimization. In _International conference on machine learning_ . PMLR, 906–914. 

- [33] Yunfan Gao, Tao Sheng, Youlin Xiang, Yun Xiong, Haofen Wang, and Jiawei Zhang. 2023. Chat-rec: Towards interactive and explainable llms-augmented recommender system. _arXiv preprint arXiv:2303.14524_ (2023). 

- [34] Tiezheng Ge, Kaiming He, Qifa Ke, and Jian Sun. 2013. Optimized product quantization. _IEEE transactions on pattern analysis and machine intelligence_ 36, 4 (2013), 744–755. 

- [35] Benjamin Ghaemmaghami, Mustafa Ozdal, Rakesh Komuravelli, Dmitriy Korchev, Dheevatsa Mudigere, Krishnakumar Nair, and Maxim Naumov. 2022. Learning to Collide: Recommendation System Model Compression with Learned Hash Functions. _arXiv preprint arXiv:2203.15837_ (2022). 

- [36] Justin Gilmer, Samuel S Schoenholz, Patrick F Riley, Oriol Vinyals, and George E Dahl. 2017. Neural message passing for quantum chemistry. In _International conference on machine learning_ . PMLR, 1263–1272. 

- [37] Mihajlo Grbovic and Haibin Cheng. 2018. Real-time personalization using embeddings for search ranking at airbnb. In _Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ . 311–320. 

- [38] Aditya Grover and Jure Leskovec. 2016. node2vec: Scalable feature learning for networks. In _Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining_ . 855–864. 

- [39] Huifeng Guo, Bo Chen, Ruiming Tang, Weinan Zhang, Zhenguo Li, and Xiuqiang He. 2021. An embedding learning framework for numerical features in ctr prediction. In _Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining_ . 2910–2918. 

- [40] Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, and Xiuqiang He. 2017. DeepFM: a factorization-machine based neural network for CTR prediction. _arXiv preprint arXiv:1703.04247_ (2017). 

- [41] Lei Guo, Hongzhi Yin, Tong Chen, Xiangliang Zhang, and Kai Zheng. 2021. Hierarchical hyperedge embedding-based representation learning for group recommendation. _ACM Transactions on Information Systems (TOIS)_ 40, 1 (2021), 1–27. 

- [42] Wei Guo, Rong Su, Renhao Tan, Huifeng Guo, Yingxue Zhang, Zhirong Liu, Ruiming Tang, and Xiuqiang He. 2021. Dual graph enhanced embedding neural network for ctr prediction. In _Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining_ . 496–504. 

- [43] Bowen Hao, Jing Zhang, Hongzhi Yin, Cuiping Li, and Hong Chen. 2021. Pre-training graph neural networks for cold-start users and items representation. In _Proceedings of the 14th ACM International Conference on Web Search and Data Mining_ . 265–273. 

- [44] Jianming He and Wesley W Chu. 2010. A social network-based recommender system (SNRS). In _Data mining for social network data_ . Springer, 47–74. 

- [45] Xiangnan He and Tat-Seng Chua. 2017. Neural factorization machines for sparse predictive analytics. In _Proceedings of the 40th International ACM SIGIR conference on Research and Development in Information Retrieval_ . 355–364. 

- [46] Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, and Meng Wang. 2020. Lightgcn: Simplifying and powering graph convolution network for recommendation. In _Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval_ . 639–648. 

- [47] Xiangnan He, Ming Gao, Min-Yen Kan, and Dingxian Wang. 2016. Birank: Towards ranking on bipartite graphs. _IEEE Transactions on Knowledge and Data Engineering_ 29, 1 (2016), 57–71. 

- [48] Xiangnan He, Zhankui He, Jingkuan Song, Zhenguang Liu, Yu-Gang Jiang, and Tat-Seng Chua. 2018. Nais: Neural attentive item similarity model for recommendation. _IEEE Transactions on Knowledge and Data Engineering_ 30, 12 (2018), 2354–2366. 

- [49] Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, and Tat-Seng Chua. 2017. Neural collaborative filtering. In _Proceedings of the 26th international conference on world wide web_ . 173–182. 

- [50] Xinran He, Junfeng Pan, Ou Jin, Tianbing Xu, Bo Liu, Tao Xu, Yanxin Shi, Antoine Atallah, Ralf Herbrich, Stuart Bowers, et al. 2014. Practical lessons from predicting clicks on ads at facebook. In _Proceedings of the eighth international workshop on data mining for online advertising_ . 1–9. 

- [51] Geoffrey E Hinton. 2012. A practical guide to training restricted Boltzmann machines. In _Neural networks: Tricks of the trade_ . Springer, 599–619. 

- [52] Chao Huang, Xiang Wang, Xiangnan He, and Dawei Yin. 2022. Self-supervised learning for recommender system. In _Proceedings of the 45th international ACM SIGIR conference on research and development in information retrieval_ . 3440–3443. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

36 

- [53] Jui-Ting Huang, Ashish Sharma, Shuying Sun, Li Xia, David Zhang, Philip Pronin, Janani Padmanabhan, Giuseppe Ottaviano, and Linjun Yang. 2020. Embedding-based retrieval in Facebook search. In _Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ . 2553–2561. 

- [54] Po-Sen Huang, Xiaodong He, Jianfeng Gao, Li Deng, Alex Acero, and Larry Heck. 2013. Learning deep structured semantic models for web search using clickthrough data. In _Proceedings of the 22nd ACM international conference on Information & Knowledge Management_ . 2333–2338. 

- [55] Herve Jegou, Matthijs Douze, and Cordelia Schmid. 2010. Product quantization for nearest neighbor search. _IEEE transactions on pattern analysis and machine intelligence_ 33, 1 (2010), 117–128. 

- [56] Gangwei Jiang, Hao Wang, Jin Chen, Haoyu Wang, Defu Lian, and Enhong Chen. 2021. xLightFM: Extremely Memory-Efficient Factorization Machine. In _Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval_ . 337–346. 

- [57] Manas R Joglekar, Cong Li, Mei Chen, Taibai Xu, Xiaoming Wang, Jay K Adams, Pranav Khaitan, Jiahui Liu, and Quoc V Le. 2020. Neural input search for large scale recommendation models. In _Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ . 2387–2397. 

- [58] Jeff Johnson, Matthijs Douze, and Hervé Jégou. 2019. Billion-scale similarity search with GPUs. _IEEE Transactions on Big Data_ 7, 3 (2019), 535–547. 

- [59] Yuchin Juan, Yong Zhuang, Wei-Sheng Chin, and Chih-Jen Lin. 2016. Field-aware factorization machines for CTR prediction. In _Proceedings of the 10th ACM conference on recommender systems_ . 43–50. 

- [60] Santosh Kabbur, Xia Ning, and George Karypis. 2013. Fism: factored item similarity models for top-n recommender systems. In _Proceedings of the 19th ACM SIGKDD international conference on Knowledge discovery and data mining_ . 659–667. 

- [61] Leslie Pack Kaelbling, Michael L Littman, and Andrew W Moore. 1996. Reinforcement learning: A survey. _Journal of artificial intelligence research_ 4 (1996), 237–285. 

- [62] Wang-Cheng Kang, Derek Zhiyuan Cheng, Tiansheng Yao, Xinyang Yi, Ting Chen, Lichan Hong, and Ed H Chi. 2020. Learning to embed categorical features without embedding tables for recommendation. _arXiv preprint arXiv:2010.10784_ (2020). 

- [63] Wang-Cheng Kang, Derek Zhiyuan Cheng, Tiansheng Yao, Xinyang Yi, Ting Chen, Lichan Hong, and Ed H Chi. 2020. Learning to embed categorical features without embedding tables for recommendation. _arXiv preprint arXiv:2010.10784_ (2020). 

- [64] Donghyun Kim, Chanyoung Park, Jinoh Oh, Sungyoung Lee, and Hwanjo Yu. 2016. Convolutional matrix factorization for document context-aware recommendation. In _Proceedings of the 10th ACM conference on recommender systems_ . 233–240. 

- [65] Thomas N Kipf and Max Welling. 2016. Semi-supervised classification with graph convolutional networks. _arXiv preprint arXiv:1609.02907_ (2016). 

- [66] Shuming Kong, Weiyu Cheng, Yanyan Shen, and Linpeng Huang. 2022. AutoSrh: An Embedding Dimensionality Search Framework for Tabular Data Prediction. _IEEE Transactions on Knowledge and Data Engineering_ (2022). 

- [67] Yehuda Koren. 2008. Factorization meets the neighborhood: a multifaceted collaborative filtering model. In _Proceedings of the 14th ACM SIGKDD international conference on Knowledge discovery and data mining_ . 426–434. 

- [68] Yehuda Koren. 2009. Collaborative filtering with temporal dynamics. In _Proceedings of the 15th ACM SIGKDD international conference on Knowledge discovery and data mining_ . 447–456. 

- [69] Yehuda Koren, Robert Bell, and Chris Volinsky. 2009. Matrix factorization techniques for recommender systems. _Computer_ 42, 8 (2009), 30–37. 

- [70] Yehuda Koren, Steffen Rendle, and Robert Bell. 2021. Advances in collaborative filtering. _Recommender systems handbook_ (2021), 91–142. 

- [71] Aditya Kusupati, Vivek Ramanujan, Raghav Somani, Mitchell Wortsman, Prateek Jain, Sham Kakade, and Ali Farhadi. 2020. Soft threshold weight reparameterization for learnable sparsity. In _International Conference on Machine Learning_ . PMLR, 5544–5555. 

- [72] Valerio La Gatta, Vincenzo Moscato, Mirko Pennone, Marco Postiglione, and Giancarlo Sperlí. 2022. Music Recommendation via Hypergraph Embedding. _IEEE Transactions on Neural Networks and Learning Systems_ (2022). 

- [73] Doyup Lee, Chiheon Kim, Saehoon Kim, Minsu Cho, and Wook-Shin Han. 2022. Autoregressive Image Generation using Residual Quantization. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 11523–11532. 

- [74] Omer Levy and Yoav Goldberg. 2014. Neural word embedding as implicit matrix factorization. _Advances in neural information processing systems_ 27 (2014). 

- [75] Chao Li, Zhiyuan Liu, Mengmeng Wu, Yuchi Xu, Huan Zhao, Pipei Huang, Guoliang Kang, Qiwei Chen, Wei Li, and Dik Lun Lee. 2019. Multi-interest network with dynamic routing for recommendation at Tmall. In _Proceedings of the 28th ACM International Conference on Information and Knowledge Management_ . 2615–2623. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

37 

- [76] Lei Li, Yongfeng Zhang, and Li Chen. 2023. Personalized prompt learning for explainable recommendation. _ACM Transactions on Information Systems_ 41, 4 (2023), 1–26. 

- [77] Shiwei Li, Huifeng Guo, Xing Tang, Ruiming Tang, Lu Hou, Ruixuan Li, and Rui Zhang. 2023. Embedding Compression in Recommender Systems: A Survey. _Comput. Surveys_ (2023). 

- [78] Yicong Li, Hongxu Chen, Xiangguo Sun, Zhenchao Sun, Lin Li, Lizhen Cui, Philip S Yu, and Guandong Xu. 2021. Hyperbolic hypergraphs for sequential recommendation. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 988–997. 

- [79] Yuqi Li, Weizheng Chen, and Hongfei Yan. 2017. Learning graph-based embedding for time-aware product recommendation. In _Proceedings of the 2017 ACM on Conference on Information and Knowledge Management_ . 2163–2166. 

- [80] Defu Lian, Haoyu Wang, Zheng Liu, Jianxun Lian, Enhong Chen, and Xing Xie. 2020. Lightrec: A memory and search-efficient recommender system. In _Proceedings of The Web Conference 2020_ . 695–705. 

- [81] Defu Lian, Xing Xie, Enhong Chen, and Hui Xiong. 2020. Product quantized collaborative filtering. _IEEE Transactions on Knowledge and Data Engineering_ 33, 9 (2020), 3284–3296. 

- [82] Jianxun Lian, Xiaohuan Zhou, Fuzheng Zhang, Zhongxia Chen, Xing Xie, and Guangzhong Sun. 2018. xdeepfm: Combining explicit and implicit feature interactions for recommender systems. In _Proceedings of the 24th ACM SIGKDD international conference on knowledge discovery & data mining_ . 1754–1763. 

- [83] Paul Pu Liang, Manzil Zaheer, Yuan Wang, and Amr Ahmed. 2020. Anchor & transform: Learning sparse embeddings for large vocabularies. _arXiv preprint arXiv:2003.08197_ (2020). 

- [84] Yankai Lin, Zhiyuan Liu, Maosong Sun, Yang Liu, and Xuan Zhu. 2015. Learning entity and relation embeddings for knowledge graph completion. In _Proceedings of the AAAI conference on artificial intelligence_ , Vol. 29. 

- [85] Chenxi Liu, Piotr Dollár, Kaiming He, Ross Girshick, Alan Yuille, and Saining Xie. 2020. Are labels necessary for neural architecture search?. In _European Conference on Computer Vision_ . Springer, 798–813. 

- [86] Chong Liu, Defu Lian, Min Nie, and Xia Hu. 2020. Online optimized product quantization. In _2020 IEEE International Conference on Data Mining (ICDM)_ . IEEE, 362–371. 

- [87] Hanxiao Liu, Karen Simonyan, and Yiming Yang. 2018. Darts: Differentiable architecture search. _arXiv preprint arXiv:1806.09055_ (2018). 

- [88] Haochen Liu, Xiangyu Zhao, Chong Wang, Xiaobing Liu, and Jiliang Tang. 2020. Automated embedding size search in deep recommender systems. In _Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval_ . 2307–2316. 

- [89] Junling Liu, Chao Liu, Peilin Zhou, Qichen Ye, Dading Chong, Kang Zhou, Yueqi Xie, Yuwei Cao, Shoujin Wang, Chenyu You, et al. 2023. Llmrec: Benchmarking large language models on recommendation task. _arXiv preprint arXiv:2308.12241_ (2023). 

- [90] Qi Liu, Jin Zhang, Defu Lian, Yong Ge, Jianhui Ma, and Enhong Chen. 2021. Online Additive Quantization. In _Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining_ . 1098–1108. 

- [91] Siyi Liu, Chen Gao, Yihong Chen, Depeng Jin, and Yong Li. 2021. Learnable embedding sizes for recommender systems. _arXiv preprint arXiv:2101.07577_ (2021). 

- [92] Yong Liu, Susen Yang, Chenyi Lei, Guoxin Wang, Haihong Tang, Juyong Zhang, Aixin Sun, and Chunyan Miao. 2021. Pre-training graph transformer with multimodal side information for recommendation. In _Proceedings of the 29th ACM International Conference on Multimedia_ . 2853–2861. 

- [93] Yang Liu, Yuanshun Yao, Jean-Francois Ton, Xiaoying Zhang, Ruocheng Guo Hao Cheng, Yegor Klochkov, Muhammad Faaiz Taufiq, and Hang Li. 2023. Trustworthy LLMs: a Survey and Guideline for Evaluating Large Language Models’ Alignment. _arXiv preprint arXiv:2308.05374_ (2023). 

- [94] Zhiwei Liu, Yongjun Chen, Jia Li, Philip S Yu, Julian McAuley, and Caiming Xiong. 2021. Contrastive self-supervised sequential recommendation with robust augmentation. _arXiv preprint arXiv:2108.06479_ (2021). 

- [95] Zhuang Liu, Yunpu Ma, Yuanxin Ouyang, and Zhang Xiong. 2021. Contrastive learning for recommender system. _arXiv preprint arXiv:2101.01317_ (2021). 

- [96] Tzu-Chuen Lu and Chin-Chen Chang. 2010. A Survey of VQ Codebook Generation. _J. Inf. Hiding Multim. Signal Process._ 1, 3 (2010), 190–203. 

- [97] Fuyu Lv, Taiwei Jin, Changlong Yu, Fei Sun, Quan Lin, Keping Yang, and Wilfred Ng. 2019. SDM: Sequential deep matching model for online large-scale recommender system. In _Proceedings of the 28th ACM International Conference on Information and Knowledge Management_ . 2635–2643. 

- [98] Jing Ma, Ruocheng Guo, Mengting Wan, Longqi Yang, Aidong Zhang, and Jundong Li. 2022. Learning fair node representations with graph counterfactual fairness. In _Proceedings of the Fifteenth ACM International Conference on Web Search and Data Mining_ . 695–703. 

- [99] Franco Manessi, Alessandro Rozza, and Mario Manzo. 2020. Dynamic graph convolutional networks. _Pattern Recognition_ 97 (2020), 107000. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

38 

- [100] Kelong Mao, Jieming Zhu, Xi Xiao, Biao Lu, Zhaowei Wang, and Xiuqiang He. 2021. UltraGCN: ultra simplification of graph convolutional networks for recommendation. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 1253–1262. 

- [101] Ninareh Mehrabi, Fred Morstatter, Nripsuta Saxena, Kristina Lerman, and Aram Galstyan. 2021. A survey on bias and fairness in machine learning. _ACM Computing Surveys (CSUR)_ 54, 6 (2021), 1–35. 

- [102] Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013. Efficient estimation of word representations in vector space. _arXiv preprint arXiv:1301.3781_ (2013). 

- [103] Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013. Efficient estimation of word representations in vector space. _arXiv preprint arXiv:1301.3781_ (2013). 

- [104] Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S Corrado, and Jeff Dean. 2013. Distributed representations of words and phrases and their compositionality. _Advances in neural information processing systems_ 26 (2013). 

- [105] Andriy Mnih and Russ R Salakhutdinov. 2007. Probabilistic matrix factorization. _Advances in neural information processing systems_ 20 (2007). 

- [106] Volodymyr Mnih, Adria Puigdomenech Badia, Mehdi Mirza, Alex Graves, Timothy Lillicrap, Tim Harley, David Silver, and Koray Kavukcuoglu. 2016. Asynchronous methods for deep reinforcement learning. In _International conference on machine learning_ . PMLR, 1928–1937. 

- [107] Nasser M Nasrabadi and Robert A King. 1988. Image coding using vector quantization: A review. _IEEE Transactions on communications_ 36, 8 (1988), 957–971. 

- [108] Xia Ning and George Karypis. 2011. Slim: Sparse linear methods for top-n recommender systems. In _2011 IEEE 11th international conference on data mining_ . IEEE, 497–506. 

- [109] Xichuan Niu, Bofang Li, Chenliang Li, Rong Xiao, Haochuan Sun, Honggang Wang, Hongbo Deng, and Zhenzhong Chen. 2020. Gated Heterogeneous Graph Representation Learning for Shop Search in E-commerce. In _Proceedings of the 29th ACM International Conference on Information & Knowledge Management_ . 2165–2168. 

- [110] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2018. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ (2018). 

- [111] Arkadiusz Paterek. 2007. Improving regularized singular value decomposition for collaborative filtering. In _Proceedings of KDD cup and workshop_ , Vol. 2007. 5–8. 

- [112] Bryan Perozzi, Rami Al-Rfou, and Steven Skiena. 2014. Deepwalk: Online learning of social representations. In _Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining_ . 701–710. 

- [113] A Kai Qin, Vicky Ling Huang, and Ponnuthurai N Suganthan. 2008. Differential evolution algorithm with strategy adaptation for global numerical optimization. _IEEE transactions on Evolutionary Computation_ 13, 2 (2008), 398–417. 

- [114] Zhaopeng Qiu, Xian Wu, Jingyue Gao, and Wei Fan. 2021. U-BERT: Pre-training user representations for improved recommendation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 35. 4320–4327. 

- [115] Liang Qu, Yonghong Ye, Ningzhi Tang, Lixin Zhang, Yuhui Shi, and Hongzhi Yin. 2022. Single-shot Embedding Dimension Search in Recommender System. _arXiv preprint arXiv:2204.03281_ (2022). 

- [116] Yanru Qu, Han Cai, Kan Ren, Weinan Zhang, Yong Yu, Ying Wen, and Jun Wang. 2016. Product-based neural networks for user response prediction. In _2016 IEEE 16th International Conference on Data Mining (ICDM)_ . IEEE, 1149–1154. 

- [117] Amirthalingam Ramanan and Mahesan Niranjan. 2012. A review of codebook models in patch-based visual object recognition. _Journal of Signal Processing Systems_ 68, 3 (2012), 333–352. 

- [118] Steffen Rendle. 2010. Factorization machines. In _2010 IEEE International conference on data mining_ . IEEE, 995–1000. 

- [119] Steffen Rendle. 2012. Factorization machines with libfm. _ACM Transactions on Intelligent Systems and Technology (TIST)_ 3, 3 (2012), 1–22. 

- [120] Steffen Rendle. 2012. Factorization machines with libfm. _ACM Transactions on Intelligent Systems and Technology (TIST)_ 3, 3 (2012), 1–22. 

- [121] Sebastian Ruder. 2016. An overview of gradient descent optimization algorithms. _arXiv preprint arXiv:1609.04747_ (2016). 

- [122] Joan Serrà and Alexandros Karatzoglou. 2017. Getting deep recommenders fit: Bloom embeddings for sparse binary input/output networks. In _Proceedings of the Eleventh ACM Conference on Recommender Systems_ . 279–287. 

- [123] Junyuan Shang, Tengfei Ma, Cao Xiao, and Jimeng Sun. 2019. Pre-training of graph augmented transformers for medication recommendation. _arXiv preprint arXiv:1906.00346_ (2019). 

- [124] Stuart C Shapiro. 1992. Encyclopedia of artificial intelligence second edition. _New Jersey: A Wiley Interscience Publication_ (1992). 

- [125] Hao-Jun Michael Shi, Dheevatsa Mudigere, Maxim Naumov, and Jiyan Yang. 2020. Compositional embeddings using complementary partitions for memory-efficient recommendation systems. In _Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ . 165–175. 

- [126] Kyuyong Shin, Hanock Kwak, Kyung-Min Kim, Minkyu Kim, Young-Jin Park, Jisu Jeong, and Seungjae Jung. 2021. One4all user representation for recommender systems in e-commerce. _arXiv preprint arXiv:2106.00573_ (2021). 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

39 

- [127] Martin Simonovsky and Nikos Komodakis. 2018. Graphvae: Towards generation of small graphs using variational autoencoders. In _Artificial Neural Networks and Machine Learning–ICANN 2018: 27th International Conference on Artificial Neural Networks, Rhodes, Greece, October 4-7, 2018, Proceedings, Part I 27_ . Springer, 412–422. 

- [128] Weiping Song, Chence Shi, Zhiping Xiao, Zhijian Duan, Yewen Xu, Ming Zhang, and Jian Tang. 2019. Autoint: Automatic feature interaction learning via self-attentive neural networks. In _Proceedings of the 28th ACM International Conference on Information and Knowledge Management_ . 1161–1170. 

- [129] Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou, and Peng Jiang. 2019. BERT4Rec: Sequential recommendation with bidirectional encoder representations from transformer. In _Proceedings of the 28th ACM international conference on information and knowledge management_ . 1441–1450. 

- [130] Jian Tang, Meng Qu, Mingzhe Wang, Ming Zhang, Jun Yan, and Qiaozhu Mei. 2015. Line: Large-scale information network embedding. In _Proceedings of the 24th international conference on world wide web_ . 1067–1077. 

- [131] Vishesh Thakur. 2023. Unveiling gender bias in terms of profession across LLMs: Analyzing and addressing sociological implications. _arXiv preprint arXiv:2307.09162_ (2023). 

- [132] Dan Tito Svenstrup, Jonas Hansen, and Ole Winther. 2017. Hash embeddings for efficient word representations. _Advances in neural information processing systems_ 30 (2017). 

- [133] Daniel J Tylavsky and Guy RL Sohie. 1986. Generalization of the matrix inversion lemma. _Proc. IEEE_ 74, 7 (1986), 1050–1052. 

- [134] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. _Advances in neural information processing systems_ 30 (2017). 

- [135] Petar Veličković, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Lio, and Yoshua Bengio. 2017. Graph attention networks. _arXiv preprint arXiv:1710.10903_ (2017). 

- [136] Petar Veličković, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Lio, and Yoshua Bengio. 2017. Graph attention networks. _arXiv preprint arXiv:1710.10903_ (2017). 

- [137] Chen Wang, Yueqing Liang, Zhiwei Liu, Tao Zhang, and S Yu Philip. 2021. Pre-training Graph Neural Network for Cross Domain Recommendation. In _2021 IEEE Third International Conference on Cognitive Machine Intelligence (CogMI)_ . IEEE, 140–145. 

- [138] Chenyang Wang, Weizhi Ma, and Chong Chen. 2022. Sequential Recommendation with Multiple Contrast Signals. _ACM Transactions on Information Systems (TOIS)_ (2022). 

- [139] Hao Wang, Defu Lian, Hanghang Tong, Qi Liu, Zhenya Huang, and Enhong Chen. 2021. Hypersorec: Exploiting hyperbolic user and item representations with multiple aspects for social-aware recommendation. _ACM Transactions on Information Systems (TOIS)_ 40, 2 (2021), 1–28. 

- [140] Hongwei Wang, Fuzheng Zhang, Jialin Wang, Miao Zhao, Wenjie Li, Xing Xie, and Minyi Guo. 2018. Ripplenet: Propagating user preferences on the knowledge graph for recommender systems. In _Proceedings of the 27th ACM international conference on information and knowledge management_ . 417–426. 

- [141] Hongwei Wang, Fuzheng Zhang, Mengdi Zhang, Jure Leskovec, Miao Zhao, Wenjie Li, and Zhongyuan Wang. 2019. Knowledge-aware graph neural networks with label smoothness regularization for recommender systems. In _Proceedings of the 25th ACM SIGKDD international conference on knowledge discovery & data mining_ . 968–977. 

- [142] Jizhe Wang, Pipei Huang, Huan Zhao, Zhibo Zhang, Binqiang Zhao, and Dik Lun Lee. 2018. Billion-scale commodity embedding for e-commerce recommendation in alibaba. In _Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ . 839–848. 

- [143] Jianguo Wang, Xiaomeng Yi, Rentong Guo, Hai Jin, Peng Xu, Shengjun Li, Xiangyu Wang, Xiangzhou Guo, Chengming Li, Xiaohai Xu, et al. 2021. Milvus: A Purpose-Built Vector Data Management System. In _Proceedings of the 2021 International Conference on Management of Data_ . 2614–2627. 

- [144] Menghan Wang, Yujie Lin, Guli Lin, Keping Yang, and Xiao-ming Wu. 2020. M2GRL: A multi-task multi-view graph representation learning framework for web-scale recommender systems. In _Proceedings of the 26th ACM SIGKDD international conference on knowledge discovery & data mining_ . 2349–2358. 

- [145] Ruoxi Wang, Bin Fu, Gang Fu, and Mingliang Wang. 2017. Deep & cross network for ad click predictions. In _Proceedings of the ADKDD’17_ . 1–7. 

- [146] Shoujin Wang, Liang Hu, Yan Wang, Xiangnan He, Quan Z Sheng, Mehmet Orgun, Longbing Cao, Nan Wang, Francesco Ricci, and Philip S Yu. 2020. Graph learning approaches to recommender systems: A review. _arXiv preprint arXiv:2004.11718_ (2020). 

- [147] Wenjie Wang, Xinyu Lin, Fuli Feng, Xiangnan He, and Tat-Seng Chua. 2023. Generative recommendation: Towards next-generation recommender paradigm. _arXiv preprint arXiv:2304.03516_ (2023). 

- [148] Xiang Wang, Xiangnan He, Yixin Cao, Meng Liu, and Tat-Seng Chua. 2019. Kgat: Knowledge graph attention network for recommendation. In _Proceedings of the 25th ACM SIGKDD international conference on knowledge discovery & data mining_ . 950–958. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

40 

- [149] Xiang Wang, Xiangnan He, Meng Wang, Fuli Feng, and Tat-Seng Chua. 2019. Neural graph collaborative filtering. In _Proceedings of the 42nd international ACM SIGIR conference on Research and development in Information Retrieval_ . 165–174. 

- [150] Xiang Wang, Tinglin Huang, Dingxian Wang, Yancheng Yuan, Zhenguang Liu, Xiangnan He, and Tat-Seng Chua. 2021. Learning intents behind interactions with knowledge graph for recommendation. In _Proceedings of the Web Conference 2021_ . 878–887. 

- [151] Yuening Wang, Yingxue Zhang, and Mark Coates. 2021. Graph Structure Aware Contrastive Knowledge Distillation for Incremental Learning in Recommender Systems. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 3518–3522. 

- [152] Zhen Wang, Jianwen Zhang, Jianlin Feng, and Zheng Chen. 2014. Knowledge graph embedding by translating on hyperplanes. In _Proceedings of the AAAI conference on artificial intelligence_ , Vol. 28. 

- [153] Zhikun Wei, Xin Wang, and Wenwu Zhu. 2021. Autoias: Automatic integrated architecture searcher for click-trough rate prediction. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 2101–2110. 

- [154] Kilian Weinberger, Anirban Dasgupta, John Langford, Alex Smola, and Josh Attenberg. 2009. Feature hashing for large scale multitask learning. In _Proceedings of the 26th annual international conference on machine learning_ . 1113–1120. 

- [155] Jiancan Wu, Xiang Wang, Fuli Feng, Xiangnan He, Liang Chen, Jianxun Lian, and Xing Xie. 2021. Self-supervised graph learning for recommendation. In _Proceedings of the 44th international ACM SIGIR conference on research and development in information retrieval_ . 726–735. 

- [156] Le Wu, Lei Chen, Pengyang Shao, Richang Hong, Xiting Wang, and Meng Wang. 2021. Learning fair representations for recommendation: A graph-based perspective. In _Proceedings of the Web Conference 2021_ . 2198–2208. 

- [157] Le Wu, Junwei Li, Peijie Sun, Richang Hong, Yong Ge, and Meng Wang. 2020. Diffnet++: A neural influence and interest diffusion network for social recommendation. _IEEE Transactions on Knowledge and Data Engineering_ (2020). 

- [158] Le Wu, Peijie Sun, Yanjie Fu, Richang Hong, Xiting Wang, and Meng Wang. 2019. A neural influence diffusion model for social recommendation. In _Proceedings of the 42nd international ACM SIGIR conference on research and development in information retrieval_ . 235–244. 

- [159] Le Wu, Yonghui Yang, Lei Chen, Defu Lian, Richang Hong, and Meng Wang. 2020. Learning to transfer graph embeddings for inductive graph based recommendation. In _Proceedings of the 43rd international ACM SIGIR conference on research and development in information retrieval_ . 1211–1220. 

- [160] Likang Wu, Zhi Zheng, Zhaopeng Qiu, Hao Wang, Hongchao Gu, Tingjia Shen, Chuan Qin, Chen Zhu, Hengshu Zhu, Qi Liu, et al. 2023. A Survey on Large Language Models for Recommendation. _arXiv preprint arXiv:2305.19860_ (2023). 

- [161] Qitian Wu, Hengrui Zhang, Xiaofeng Gao, Peng He, Paul Weng, Han Gao, and Guihai Chen. 2019. Dual graph attention networks for deep latent representation of multifaceted social effects in recommender systems. In _The World Wide Web Conference_ . 2091–2102. 

- [162] Yiqing Wu, Ruobing Xie, Yongchun Zhu, Fuzhen Zhuang, Xu Zhang, Leyu Lin, and Qing He. 2022. Personalized prompts for sequential recommendation. _arXiv preprint arXiv:2205.09666_ (2022). 

- [163] Chaojun Xiao, Ruobing Xie, Yuan Yao, Zhiyuan Liu, Maosong Sun, Xu Zhang, and Leyu Lin. 2021. UPRec: User-Aware Pre-training for Recommender Systems. _arXiv preprint arXiv:2102.10989_ (2021). 

- [164] Jun Xiao, Hao Ye, Xiangnan He, Hanwang Zhang, Fei Wu, and Tat-Seng Chua. 2017. Attentional factorization machines: Learning the weight of feature interactions via attention networks. _arXiv preprint arXiv:1708.04617_ (2017). 

- [165] Shitao Xiao, Zheng Liu, Weihao Han, Jianjin Zhang, Defu Lian, Yeyun Gong, Qi Chen, Fan Yang, Hao Sun, Yingxia Shao, et al. 2022. Distill-VQ: Learning Retrieval Oriented Vector Quantization By Distilling Knowledge from Dense Embeddings. _arXiv preprint arXiv:2204.00185_ (2022). 

- [166] Shitao Xiao, Zheng Liu, Yingxia Shao, Defu Lian, and Xing Xie. 2021. Matching-oriented Product Quantization For Ad-hoc Retrieval. _arXiv preprint arXiv:2104.07858_ (2021). 

- [167] Tete Xiao, Xiaolong Wang, Alexei A Efros, and Trevor Darrell. 2020. What should not be contrastive in contrastive learning. _arXiv preprint arXiv:2008.05659_ (2020). 

- [168] Min Xie, Hongzhi Yin, Hao Wang, Fanjiang Xu, Weitong Chen, and Sen Wang. 2016. Learning graph-based poi embedding for location-based recommendation. In _Proceedings of the 25th ACM international on conference on information and knowledge management_ . 15–24. 

- [169] Ruobing Xie, Qi Liu, Liangdong Wang, Shukai Liu, Bo Zhang, and Leyu Lin. 2022. Contrastive cross-domain recommendation in matching. In _Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ . 4226–4236. 

- [170] Xu Xie, Fei Sun, Zhaoyang Liu, Shiwen Wu, Jinyang Gao, Jiandong Zhang, Bolin Ding, and Bin Cui. 2022. Contrastive learning for sequential recommendation. In _2022 IEEE 38th International Conference on Data Engineering (ICDE)_ . IEEE, 1259–1273. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

Embedding in Recommender Systems: A Survey 

41 

- [171] Donna Xu, Ivor W Tsang, and Ying Zhang. 2018. Online product quantization. _IEEE Transactions on Knowledge and Data Engineering_ 30, 11 (2018), 2185–2198. 

- [172] Bencheng Yan, Pengjie Wang, Jinquan Liu, Wei Lin, Kuang-Chih Lee, Jian Xu, and Bo Zheng. 2021. Binary code based hash embedding for web-scale applications. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 3563–3567. 

- [173] Bencheng Yan, Pengjie Wang, Kai Zhang, Wei Lin, Kuang-Chih Lee, Jian Xu, and Bo Zheng. 2021. Learning Effective and Efficient Embedding via an Adaptively-Masked Twins-based Layer. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 3568–3572. 

- [174] Jiaxuan You, Tianyu Du, and Jure Leskovec. 2022. ROLAND: graph learning framework for dynamic graphs. In _Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ . 2358–2366. 

- [175] Junliang Yu, Hongzhi Yin, Xin Xia, Tong Chen, Jundong Li, and Zi Huang. 2022. Self-Supervised Learning for Recommender Systems: A Survey. _arXiv preprint arXiv:2203.15876_ (2022). 

- [176] Tianshu Yu, Runzhong Wang, Junchi Yan, and Baoxin Li. 2019. Learning deep graph matching with channelindependent embedding and hungarian attention. In _International conference on learning representations_ . 

- [177] Yantao Yu, Weipeng Wang, Zhoutian Feng, and Daiyue Xue. 2021. A dual augmented two-tower model for online large-scale recommendation. _DLP-KDD_ (2021). 

- [178] Yang Yu, Fangzhao Wu, Chuhan Wu, Jingwei Yi, Tao Qi, and Qi Liu. 2021. Tiny-NewsRec: Efficient and Effective PLM-based News Recommendation. _arXiv preprint arXiv:2112.00944_ (2021). 

- [179] Fajie Yuan, Xiangnan He, Alexandros Karatzoglou, and Liguang Zhang. 2020. Parameter-efficient transfer from sequential behaviors for user modeling and recommendation. In _Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval_ . 1469–1478. 

- [180] Cao Yue, M Long, J Wang, Zhu Han, and Q Wen. 2016. Deep quantization network for efficient image retrieval. In _Proc. 13th AAAI Conf. Artif. Intell._ 3457–3463. 

- [181] Eva Zangerle and Christine Bauer. 2022. Evaluating recommender systems: survey and framework. _Comput. Surveys_ 55, 8 (2022), 1–38. 

- [182] Jingtao Zhan, Jiaxin Mao, Yiqun Liu, Jiafeng Guo, Min Zhang, and Shaoping Ma. 2021. Jointly optimizing query encoder and product quantization to improve retrieval performance. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 2487–2496. 

- [183] Caojin Zhang, Yicun Liu, Yuanpu Xie, Sofia Ira Ktena, Alykhan Tejani, Akshay Gupta, Pranay Kumar Myana, Deepak Dilipkumar, Suvadip Paul, Ikuhiro Ihara, et al. 2020. Model size reduction using frequency based double hashing for recommender systems. In _Fourteenth ACM Conference on Recommender Systems_ . 521–526. 

- [184] Guo Zhang, Hao He, and Dina Katabi. 2019. Circuit-GNN: Graph neural networks for distributed circuit design. In _International conference on machine learning_ . PMLR, 7364–7373. 

- [185] Junwei Zhang, Min Gao, Junliang Yu, Lei Guo, Jundong Li, and Hongzhi Yin. 2021. Double-scale self-supervised hypergraph learning for group recommendation. In _Proceedings of the 30th ACM International Conference on Information & Knowledge Management_ . 2557–2567. 

- [186] Jiani Zhang, Xingjian Shi, Shenglin Zhao, and Irwin King. 2019. STAR-GCN: Stacked and Reconstructed Graph Convolutional Networks for Recommender Systems. In _IJCAI_ . 

- [187] Qi Zhang, Jingjie Li, Qinglin Jia, Chuyuan Wang, Jieming Zhu, Zhaowei Wang, and Xiuqiang He. 2021. UNBERT: User-News Matching BERT for News Recommendation.. In _IJCAI_ . 3356–3362. 

- [188] Weinan Zhang, Tianming Du, and Jun Wang. 2016. Deep learning over multi-field categorical data. In _European conference on information retrieval_ . Springer, 45–57. 

- [189] Weinan Zhang, Tianming Du, and Jun Wang. 2016. Deep learning over multi-field categorical data. In _European conference on information retrieval_ . Springer, 45–57. 

- [190] Yuefeng Zhang. 2022. An Introduction to Matrix factorization and Factorization Machines in Recommendation System, and Beyond. _CoRR_ abs/2203.11026 (2022). https://doi.org/10.48550/arXiv.2203.11026 arXiv:2203.11026 

- [191] Yan Zhang, Defu Lian, and Guowu Yang. 2017. Discrete personalized ranking for fast collaborative filtering from implicit feedback. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 31. 

- [192] Yan Zhang, Hongzhi Yin, Zi Huang, Xingzhong Du, Guowu Yang, and Defu Lian. 2018. Discrete deep learning for fast content-aware recommendation. In _Proceedings of the eleventh ACM international conference on web search and data mining_ . 717–726. 

- [193] Qian Zhao, Yue Shi, and Liangjie Hong. 2017. Gb-cent: Gradient boosted categorical embedding and numerical trees. In _Proceedings of the 26th international conference on world wide web_ . 1311–1319. 

- [194] Xiangyu Zhao, Haochen Liu, Hui Liu, Jiliang Tang, Weiwei Guo, Jun Shi, Sida Wang, Huiji Gao, and Bo Long. 2021. Autodim: Field-aware embedding dimension searchin recommender systems. In _Proceedings of the Web Conference 2021_ . 3015–3022. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 

42 

#### Xiangyu Zhao<sup>∗</sup> , Maolin Wang<sup>∗</sup> , Xinjian Zhao<sup>∗</sup> , Jiansheng Li, Shucheng Zhou, Dawei Yin, Qing Li, Jiliang Tang, Ruocheng Guo. 

- [195] Xiangyu Zhaok, Haochen Liu, Wenqi Fan, Hui Liu, Jiliang Tang, Chong Wang, Ming Chen, Xudong Zheng, Xiaobing Liu, and Xiwang Yang. 2021. Autoemb: Automated embedding dimensionality search in streaming recommendations. In _2021 IEEE International Conference on Data Mining (ICDM)_ . IEEE, 896–905. 

- [196] Ruiqi Zheng, Liang Qu, Bin Cui, Yuhui Shi, and Hongzhi Yin. 2022. AutoML for Deep Recommender Systems: A Survey. _arXiv preprint arXiv:2203.13922_ (2022). 

- [197] Chang Zhou, Yuqiong Liu, Xiaofei Liu, Zhongyi Liu, and Jun Gao. 2017. Scalable graph embedding for asymmetric proximity. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 31. 

- [198] Guorui Zhou, Xiaoqiang Zhu, Chenru Song, Ying Fan, Han Zhu, Xiao Ma, Yanghui Yan, Junqi Jin, Han Li, and Kun Gai. 2018. Deep interest network for click-through rate prediction. In _Proceedings of the 24th ACM SIGKDD international conference on knowledge discovery & data mining_ . 1059–1068. 

- [199] Joyce Zhou and Thorsten Joachims. 2023. GPT as a Baseline for Recommendation Explanation Texts. _arXiv preprint arXiv:2309.08817_ (2023). 

- [200] Sheng Zhou, Xin Wang, Martin Ester, Bolang Li, Chen Ye, Zhen Zhang, Can Wang, and Jiajun Bu. 2021. Directionaware user recommendation based on asymmetric network embedding. _ACM Transactions on Information Systems (TOIS)_ 40, 2 (2021), 1–23. 

, Vol. 1, No. 1, Article . Publication date: December 2023. 



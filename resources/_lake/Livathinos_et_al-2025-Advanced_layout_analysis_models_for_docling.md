---
title: Advanced layout analysis models for docling
citekey: Livathinos2025
authors:
- Nikolaos Livathinos
- Christoph Auer
- Ahmed Nassar
- Rafael Teixeira de Lima
- Maksym Lysak
- Brown Ebouky
- Cesar Berrospi
- Michele Dolfi
- Panagiotis Vagenas
- Matteo Omenetti
- Kasper Dinkla
- Yusik Kim
- Valery Weber
- Lucas Morin
- Ingmar Meijer
- Viktor Kuropiatnyk
- Tim Strohmeyer
- A. Said Gurbuz
- Peter W. J. Staar
year: 2025
date: '2025'
item_type: preprint
doi: 10.48550/ARXIV.2509.11720
url: https://arxiv.org/abs/2509.11720
zotero_key: VUPRZQ8Y
collections:
- SA9KZ2CI
tags:
- Computer Science - Computer Vision and Pattern Recognition
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: Livathinos et al. - 2025 - Advanced layout analysis models for docling.pdf
synced_at: '2026-09-29T17:58:45.000400'
---

# Advanced layout analysis models for docling

**Autores:** Nikolaos Livathinos, Christoph Auer, Ahmed Nassar, Rafael Teixeira de Lima, Maksym Lysak, Brown Ebouky, Cesar Berrospi, Michele Dolfi, Panagiotis Vagenas, Matteo Omenetti, Kasper Dinkla, Yusik Kim, Valery Weber, Lucas Morin, Ingmar Meijer, Viktor Kuropiatnyk, Tim Strohmeyer, A. Said Gurbuz, Peter W. J. Staar
**DOI:** [10.48550/ARXIV.2509.11720](https://doi.org/10.48550/ARXIV.2509.11720)
**URL:** https://arxiv.org/abs/2509.11720

## 📄 Conteúdo Completo do Documento

# **Advanced Layout Analysis Models for Docling** 

## **Nikolaos Livathinos, Christoph Auer, Ahmed Nassar, Rafael Teixeira de Lima, Maksym Lysak, Brown Ebouky, Cesar Berrospi, Michele Dolfi, Panagiotis Vagenas, Matteo Omenetti, Kasper Dinkla, Yusik Kim, Valery Weber, Lucas Morin, Ingmar Meijer, Viktor Kuropiatnyk, Tim Strohmeyer, A.Said Gurbuz, Peter W. J. Staar** 

_{_ nli,cau,ahn,mly,ceb,dol,pva,dkl,vwe,inm,vku,taa _}_ @zurich.ibm.com, 

- _{_ rtdl,Brown.Ebouky,Matteo.Omenetti1,Yusik.Kim,Tim.Strohmeyer1,abdurrahman.said.guerbuez _}_ @ibm.com IBM Research, R¨uschlikon, Switzerland 

### **Abstract** 

This technical report documents the development of novel Layout Analysis models integrated into the Docling document-conversion pipeline. We trained several state-ofthe-art object detectors based on the RT-DETR, RT-DETRv2 and DFINE architectures on a heterogeneous corpus of 150,000 documents (both openly available and proprietary). Post-processing steps were applied to the raw detections to make them more applicable to the document conversion task. We evaluated the effectiveness of the layout analysis on various document benchmarks using different methodologies while also measuring the runtime performance across different environments (CPU, Nvidia and Apple GPUs). We introduce five new document layout models achieving 20.6% - 23.9% mAP improvement over Docling’s previous baseline, with comparable or better runtime. Our best model, “heron101”, attains 78% mAP with 28 ms/image inference time on a single NVIDIA A100 GPU. Extensive quantitative and qualitative experiments establish best practices for training, evaluating, and deploying document-layout detectors, providing actionable guidance for the document conversion community. All trained checkpoints, code, and documentation are released under a permissive license on HuggingFace. 

## **Introduction** 

The heterogeneity in the styling and representation formats of documents together with the vast amounts of information stored collectively in documents make it imperative to use specialized software that converts documents into a structured format suitable for any further data analysis. 

The Document Layout Analysis task identifies document elements, classifies them according to a predefined taxonomy and locates their bounding box on the page. This is an essential part in conversion pipelines such as Docling (DeepSearchTeam 2024; Livathinos et al. 2024), Corpus Conversion Service (Auer et al. 2022), MinerU (Wang et al. 2024), unstructured.io (Unstructured.io Team 2024), Marker (Paruchuri 2024), Pix2Text (breezedeus 2025). The same is also true for multi-stage expert models like LayoutLM (Feng et al. 2025), Dolphin (Feng et al. 2025), MonkeyOCR (Li et al. 2025), or NanonetsOCR (Mandal 2025). 

Docling is a well recognized open source<sup>1</sup> document conversion pipeline with a permissive license, based on top of 

1https://github.com/docling-project/docling 



Figure 1: Models mAP scores vs inference times. Docling’s new default model “heron”, delivers a 23.5% mAP gain. 

expert AI models that we developed and presented in the recent past (Nassar et al. 2025, 2022; Lysak et al. 2023; Livathinos et al. 2021; Morin et al. 2023). Docling can recognize a wide range of document formats (PDF, MS Word, MS PowerPoint, Images, HTML, etc.) and convert them into an internal representation (DoclingDocument) which enables easy access to all document elements via a Python API, supports integrations with popular AI Frameworks (DataPrepKit 2023; InstructLab 2023; BeeAI 2023; Liu 2022; LangChain 2023), exposes a Model Context Protocol interface (Hou et al. 2025) and exports the document in structured formats like JSON, HTML, Markdown, etc. 

In this technical report we present the steps we have taken to develop the family of Layout Models used by Docling. More specifically, we outline how to: 

- Compile a dataset of 150k documents. 

- Train a variety of different backbones. 

- Apply various post-processing techniques and evaluation methodologies. 

All layout models are publicly available in our Hugging Face space: https://huggingface.co/ds4sd/models 

## **Data** 

We have trained the models using a diverse dataset of 150’000 single-page documents, which include a total of 

2.3M document layout elements. This dataset unifies a post-processed version of the DocLayNet (Pfitzmann et al. 2022) document dataset together with the proprietary dataset DocLayNet-v2 and documents from the WordScape (Weber et al. 2023) dataset. The unified dataset consists of 17 layout classes as presented in Table 1. The annotations contain bounding boxes in COCO format and the document pages are available both as PDF files and as PNG images in 150 dpi resolution. 

|**Category**|**train**|**val**|**test**|**total**|
|---|---|---|---|---|
|Caption|37,680|4,252|3,860|45,792|
|Checkbox-Selected|3,071|455|451|3,977|
|Checkbox-Unselected|45,260|5,827|6,261|57,348|
|Code|6,185|760|727|7,672|
|Document Index|1,587|179|208|1,974|
|Footnote|9,818|1,168|1,200|12,186|
|Form|12,521|1,625|1,566|15,712|
|Formula<br>|29,101<br>|2,704<br>|2,923<br>|34,728<br>|
|Key-Value Region|20,649|2,665|2,683|25,997|
|List-item|421,845|47,552|47,426|516,823|
|Page-footer<br>|107,761|11,321<br>|11,304<br>|130,386|
|Page-header<br>|92,304<br>|10,636<br>|10,251<br>|113,191<br>|
|Picture|128,603|14,697|14,530|157,830|
|Section-header|293,021|34,368|31,212|358,601|
|Table|31,877|2,964|2,941|37,782|
|Text|1,042,044|118,863|115,479|1,276,386|
|Title|7,120|838|848|8,806|
|**Total**|**2,290,447 **|**260,874 **|**253,870 **|**2,805,191**|



Table 1: Distribution of the 17 canonical document element categories across dataset splits (train, validation, test) and total counts. 

_DocLayNet_ (Pfitzmann et al. 2022) is a large-scale dataset for document layout analysis, offering bounding-box annotations for 80,863 unique pages across six diverse document categories. The dataset provides multilingual documents in a variety of layouts, annotated in COCO format with 150 DPI PNG images. However, a key limitation is that it includes only 11 out of the 17 canonical layout classes defined in Table 1, omitting six important categories: “Document Index”, “Code”, “Checkbox-Selected”, “CheckboxUnselected”, “Form”, and “Key-Value Region” - collectively referred to as the “delta” classes. This omission creates a critical inconsistency for training models designed to recognize all canonical classes. Specifically, pages that do contain delta class elements are either mislabeled (e.g., a “Form” annotated as a “Table”) or lack annotations altogether for those elements. As a result, these samples introduce incorrect supervision during training, which can confuse the model and degrade its ability to distinguish between similar classes. This issue becomes especially problematic in fine-grained layout tasks, where accurate class boundaries are essential for model performance. 

To mitigate the negative impact of incomplete or incorrect annotations, we adopted a filtering-based approach to produce a reduced version of DocLayNet suitable for training models on all 17 canonical classes. As part of this strategy, 

we trained a filtering object detector—based on RT-DETRv2 on a small, curated dataset that includes all canonical categories. This detector was then applied to the full DocLayNet corpus to scan each page for the potential presence of delta class elements. Pages flagged with high likelihood of containing any of the missing classes were marked for exclusion to eliminate sources of annotation noise. To ensure high recall of delta class occurrences, we experimented with low confidence thresholds of 0.3, 0.4, and 0.5, resulting in the exclusion of 32%, 25%, and 20% of the samples, respectively. Following manual inspection of the filtered outputs, we selected a threshold of 0.3, which provided the most reliable filtering performance. This process yielded a curated version of DocLayNet consisting of 22,101 training samples, 2,804 validation samples, and 1,574 test samples—ensuring that retained pages do not contain elements from the delta classes and are therefore suitable for training models targeting the complete canonical taxonomy. We call this version of DocLayNet “canonical-DocLayNet”. 

_WordScape_ (Weber et al. 2023) is an open-source pipeline that harvests Microsoft Word documents from the Common Crawl<sup>2</sup> web corpus and converts them into a multimodal dataset suitable for training layout-aware models. Its conversion workflow comprises three main stages: first, it extracts URLs pointing to Microsoft Word files; second, it downloads each document via HTTP requests; third, it renders every page as an image, extracts the raw text, and generates bounding-box annotations for semantic entities such as headings and tables. We have incorporated WordScape documents from the 2013 CommonCrawl snapshot into our data mix. However, a detailed inspection of the annotations revealed a significant semantic mismatch: WordScape’s “Table” label is frequently applied to entire full-page entities which in our own classification belong to the distinct “Form”. Because these mislabeled instances would result to incorrect supervision during model training, we have decided to excise all WordScape documents that contain any table annotations from our dataset. 

_DocLayNet-v2_ is an improved, proprietary version of the original dataset. It covers the full set of “canonical” categories listed in Table 1 and offers a larger and more comprehensive test split comprising 7,613 single-page documents. 

## **Object Detectors** 

In this work, we focus on Transformer-based object detectors, emphasizing fast architectures capable of real-time performance. Because of legal constraints, we exclusively picked models released under permissive open-source licenses. This excludes the very popular family of YOLO (Redmon et al. 2016) object detectors. 

Within the DETR model family (Carion et al. 2020), we examined RT-DETRv1 (Zhao et al. 2023) with a ResNet-50 (He et al. 2016) backbone and RT-DETRv2 (Lv et al. 2024) with ResNet-50 and ResNet-101 backbones. Additionally, we assessed the DFINE detector (Peng et al. 2024), which is based on the HGNet-V2 backbone and is examined in three configurations: medium, large, and xlarge. 

2https://commoncrawl.org/ 

Multiple implementations are available for the RTDETRv1, RT-DETRv2, and DFINE models, including PyTorch-based versions from the original GitHub repositories, as well as implementations built on top of the Hugging Face Transformers framework (Wolf et al. 2020). We trained the models with their native code implementations, then leveraged the Hugging Face utilities to convert the checkpoints from pickle into the safetensors format. Final evaluations were then carried out using the Hugging Face inference pipeline with the converted safetensors checkpoints. 

The RT-DETRv2-based models have been trained for 72 epochs with a learning rate of 10<sup>_−_4</sup> using an AdamW[0.9, 0.999] optimizer with weight decay 10<sup>_−_4</sup> . The D-FINE models have been trained for 132, 80 and 80 epochs for the medium, large and x-large sizes, while the learning rates were 2 _∗_ 10<sup>_−_4</sup> , 2 _._ 5 _∗_ 10<sup>_−_4</sup> , 2 _._ 5 _∗_ 10<sup>_−_4</sup> respectively. The training for the D-FINE models use an AdamW[0.9, 0.999] optimizer with weight decays 1 _∗_ 10<sup>_−_4</sup> , 1 _._ 25 _∗_ 10<sup>_−_4</sup> , 1 _._ 25 _∗_ 10<sup>_−_4</sup> . The backbones (ResNet-50, ResNet-101, HGNet-V2) have been initialized with pre-trained weights. 

The training images have been augmented by a sequence of transformations. That includes randomized distortions, zoom out, horizontal flips and image resizing to 640x640. Table 2 summarizes the backbones and the number of parameters of our models. 

|Model|Backbone|Parameters (M)|
|---|---|---|
|egret-m|DFINE-m|19.5|
|egret-l|DFINE-l|31.2|
|egret-x|DFINE-x|62.7|
|old-docling|RT-DETRv1-r50vd|42.9|
|heron (Docling v2.50.0)|RT-DETRv2-r50vd|42.9|
|heron-101|RT-DETRv2-r101vd|76.7|



Table 2: Backbones and millions of parameters for Docling’s layout models. Docling v2.50.0 uses “heron” as the default layout model. 

## **Evaluation Methods** 

The models were evaluated on the respective test splits of the DocLayNet (Pfitzmann et al. 2022) (original and canonical) and the DocLayNet-v2 dataset. The predicted bounding boxes where evaluated once for all detections, and once for detections filtered by a minimum confidence score. Specific evaluations for Docling’s output also include a set of postprocessing steps. 

The image input to all models were PNG images, yet the subsequent post-processing stage also makes use of the original PDF documents by intersecting the predicted bounding box with the native PDF cells. Each predicted label is first mapped to a minimum score; any bounding box whose confidence falls below this threshold is omitted from further analysis. The label then determines how the remaining boxes will be handled. Depending on whether it represents a “Picture”, a wrapping document element (such as a “Form”, “Key Value Region”, “Table” or “Document Index”), or a 

regular element, different processing rules apply. 

For regular elements, each bounding box is matched to the best overlapping PDF cells. The bounding boxes are then adjusted so that they exactly include their assigned PDF cells, and overlapping regular clusters are eliminated. 

Special elements undergo additional treatment. Pictures that cover more than 90% of a page are discarded outright. If a regular element overlaps with a special element, it is assigned as a child to the latter. The bounding boxes for “Form” and “Key Value Region” elements are expanded to fully enclose all their children. Overlaps involving pictures or other special types are removed. 

Finally, when any group of elements overlap, only the best proposal in that group is retained; this element inherits all PDF cells from the overlapping set. The algorithm for selecting the best proposal follows a rule-based approach that prefers certain labels, takes into account element size and confidence score, and applies different thresholds for area and confidence depending on whether the element is classified as regular, picture, or wrapper. 

After applying post-processing, the results are assessed using two distinct methodologies. The first methodology relies on the COCO-Tools package (Blumenfeld et al. 2014), which computes standard metrics such as Average Precision (AP) and Average Recall (AR) for each document element class at varying Intersection over Union (IoU) thresholds of 0.50, 0.75, and 0.95, as well as the mean Average Precision (mAP) averaged over a range of IoUs from 0.50 to 0.95 in increments of 0.05. Additionally, AP metrics were separately reported for small, medium, and large objects. The second evaluation approach utilized the docling-eval<sup>3</sup> package, which is part of the Docling project, providing an alternative benchmarking framework for document layout analysis. 

Contrary to the COCO-tools which are applicable for generic object detection tasks, the docling-eval package evaluates the object detection in a way more targeted for documents. First, a prediction-score threshold is applied so that only bounding boxes whose confidence lies above 0.50 are retained. Next, all remaining scores are set to 1.0. The test dataset is then scanned to identify the intersection of labels present in both the predictions and the ground truth. For each sample, only those bounding boxes whose labels belong to this intersecting set are kept; any samples where the number of predicted boxes differs from the number of ground-truth boxes are skipped. Finally, mean Average Precision is computed over a range of Intersection-over-Union thresholds ranging from 0.50 to 0.95 in steps of 0.05. 

## **Results** 

The evaluation results are organized along four dimensions: (1) the evaluation dataset used, (2) the score-threshold filter applied to predictions (3) the type of post-processing applied to the model outputs, and (4) the evaluation methodology employed (COCO-tools vs. docling-eval). The runtime performance measurements vary on the inference device and batch size. 

3https://github.com/docling-project/docling-eval 

|Dataset|Model|Post Proc.|mAP-50:95|AP-50|AP-75|AP-large|AP-medium|AP-small|
|---|---|---|---|---|---|---|---|---|
|||docling|0.549|0.659|0.566|0.515|0.428|0.455|
||egret-m|direct-th50|0.645|0.791|0.698|0.670|0.484|0.419|
|||direct-th0|0.686|0.848|0.742|0.705|0.555|0.484|
|||docling|0.553|0.663|0.571|0.519|0.440|0.432|
||egret-l|direct-th50|0.636|0.799|0.688|0.667|0.493|0.370|
|||direct-th0|0.672|0.851|0.725|0.699|0.558|0.451|
|||docling|0.558|0.671|0.577|0.520|0.444|0.440|
|DLN|egret-x|direct-th50|0.631|0.792|0.680|0.665|0.479|0.369|
|ocayet||direct-th0|0.671|0.848|0.723|0.698|0.552|0.417|
|||docling|0.454|0.558|0.463|0.442|0.361|0.397|
||old-docling|direct-th50|0.469|0.677|0.467|0.502|0.420|0.241|
|||direct-th0|0.505|0.733|0.503|0.539|0.465|0.314|
|||docling|0.564|0.674|0.585|0.521|0.461|0.457|
||heron|direct-th50|0.660|0.805|0.703|0.678|0.525|0.440|
|||direct-th0|0.699|0.859|0.743|0.712|0.591|0.519|
|||docling|0.571|0.683|0.591|0.529|0.471|0.484|
||heron-101|direct-th50|0.657|0.799|0.693|0.672|0.526|0.447|
|||direct-th0|0.696|0.851|0.734|0.707|0.583|0.478|
|||docling|0.232|0.376|0.197|0.264|0.135|0.069|
||egret-m|direct-th50|0.673|0.758|0.726|0.697|0.530|0.324|
|||direct-th0|0.725|0.818|0.785|0.751|0.581|0.370|
|||docling|0.229|0.373|0.194|0.262|0.133|0.068|
||egret-l|direct-th50|0.673|0.771|0.737|0.703|0.539|0.307|
|||direct-th0|0.724|0.830|0.796|0.753|0.587|0.395|
|||docling|0.229|0.371|0.195|0.261|0.131|0.072|
||egret-x|direct-th50|0.673|0.762|0.731|0.702|0.530|0.318|
|DocLayNet-v2||direct-th0|0.727|0.825|0.791|0.755|0.583|0.383|
|||docling|0.196|0.319|0.166|0.226|0.110|0.070|
||old-docling|direct-th50|0.611|0.676|0.648|0.638|0.466|0.313|
|||direct-th0|0.667|0.744|0.708|0.696|0.517|0.360|
|||docling|0.184|0.298|0.156|0.208|0.109|0.055|
||heron|direct-th50|0.703|0.779|0.746|0.724|0.573|0.346|
|||direct-th0|0.751|0.832|0.799|0.771|0.620|0.416|
|||docling|0.240|0.391|0.202|0.274|0.144|0.072|
||heron-101|direct-th50|0.709|0.779|0.747|0.727|0.591|0.377|
|||direct-th0|0.758|0.834|0.801|0.775|0.640|0.465|
||egret-m|direct-th0|0.765|0.913|0.828|0.732|0.688|0.531|
||egret-l|direct-th0|0.747|0.912|0.808|0.721|0.668|0.515|
|DocLayNet|egret-x|direct-th0|0.753|0.914|0.815|0.729|0.680|0.514|
|canonical|old-docling|direct-th0|0.541|0.755|0.543|0.541|0.488|0.308|
||heron|direct-th0|0.776|0.917|0.826|0.736|0.707|0.582|
||**heron-101**|**direct-th0**|**0.780**|**0.916**|**0.825**|**0.738**|**0.712**|**0.589**|



Table 3: COCO-tools evaluation on DocLayNet, DocLayNet-v2 and DocLayNet-canonical with and without post-processing. The post-processed results consider only scores above 0.5. The direct results are computed for scores above 0.5 and for all scores without any additional post-processing. 

Table 3 presents the evaluation results using COCO-Tools on the original DocLayNet, on DocLayNetv2 and on the canonical DocLayNet. The output of each model was evaluated either directly or after applying some post-processing. When no post-processing is applied we present the options either to evaluate on all generated predictions or to select only the ones with confidence score over 0.5. In the case where post-processing is applied, we 

always keep the boxes with score over 0.5. 

The evaluation with COCO-tools on DocLayNet shows that heron has the maximum mAP score 0.699 when no post-processing is applied and all predicted boxes are taken into account. On the second rank, we find heron-101 with an mAP of 0.696. All variants of post-processing damage the mAP score by more than 10% and to a lesser extend the removal of boxes with low score. When evaluating on 

DocLayNet-v2, the best mAP score is seen with heron-101 (0.758) and the second best with heron (0.751). 

As already discussed, the annotations of the original DocLayNet dataset contain mismatches with our canonical classes. These inconsistencies penalize our metrics and lower the AP scores for the examples that contain the delta classes. To address this, we performed evaluations on the canonical version of DocLayNet with COCO-tools without any post-processing. As evident in Table 3 the canonical DocLayNet improves the mAP by 7.5% to 8.4% in comparison to the original DocLayNet. This benchmark allows heron-101 to achieve the highest mAP score 0.780. 

The evaluation results from the docling-eval package are presented in Table 4 for DocLayNet and DocLayNetv2. In this case some type of post-processing is always applied. heron ranks first for both datasets while heron-101 and the egret models are slightly behind. The substantial score gap between DocLayNet and DocLayNet-v2 across all models reflects both the higher document layout complexity in DocLayNet-v2 and the evaluation approach employed by docling-eval. 

|Model|DocLayNet|DocLayNet-v2|
|---|---|---|
|egret-m|0.59|0.35|
|egret-l|0.59|0.35|
|egret-x|0.60|0.35|
|old-docling|0.47|0.31|
|**heron**|**0.61**|**0.36**|
|heron-101|0.61|0.35|



Table 4: mAP scores on DocLayNet and DocLayNet-v2 using docling-eval with post-processing 

In addition to the quantitative evaluation presented above, we have run qualitative analysis based on visualizations of the predictions versus the ground truth. Figure 2 depicts on the left side the ground-truth image, in the middle the raw model predictions without any post-processing and on the right side the predictions with scores over 0.50. According to the results of Table 3 the mAP score is maximized when no post-processing or score filtering is applied. However, as it is clearly evident in Figure 2, the raw predictions (in the middle) are very noisy with many overlapping bounding boxes. On the other hand, the filtered predictions look much closer to the ground-truth, regardless of yielding lower mAP scores. 

Next, we compare the predictions with scores over 0.50 with the post-processed model outputs. Figure 3 presents the ground truth (left), the model output with scores over 0.50 (middle) and the post-processed predictions, which is the default option for Docling. As one can see, the postprocessing has improved the raw predictions by clustering together fragmented document elements and removing overlapping bounding boxes. This has clearly improved the layout geometry of the end-result but the assigned labels do not always match the ground truth. For example in the example of the top row of Figure 3, the generated cluster is assigned the label “Picture” but the annotation is “Table”. 

The high complexity of document layouts often yields ambiguous annotations. Figure 4 presents cases where it is not clear if the ground truth data or the model predictions are correct or maybe _both_ are valid layout resolutions. In the first example the main body of the page has been annotated as one big “Picture”, but the model predicts a more detailed classification where textual elements have been identified as “Section-Header”, “Text” and “List Item” and the bounding boxes of the pictures have been reduced to cover only the visual content. Such discrepancies suggest that alternative layouts differing both in geometry and classification may be acceptable. 

The mean Average Precision (mAP) score, originally developed to evaluate general-purpose object detection, has been widely adopted as a standard metric for document layout analysis tasks. Based on the observations of this study and our overall experience with Docling, we conclude that mAP may not always be a suitable metric to evaluate the layouts of documents. 

Lastly we have measured the runtime performance of our models in 3 hardware configurations: a single AMD EPYC 7763 64-Core, a single Nvidia A100-80GB and an Apple MacBook M3 with MPS enabled. We have measured the min, max, median, mean seconds needed to run the models on the test split of DocLayNet without counting the I/O operations. The measurements have been divided over the split size to show the amortized inference time per image as shown in Table 5. The lightest model, egret-m, is the fastest across all testing environments achieving 0.024 sec/image when running on A100 with batch size 200. The runtime of our most accurate model, heron-101, is 0.028 sec/image. On a typical server CPU with 4 threads, egret-m is three times faster than heron-101 when using batch size 32, whereas GPU performance is similar across all models Notably, the relatively small sizes of our models pose a challenge to saturate the A100 GPU. To mitigate this, we employed large batch sizes and parallelized data loading to the GPU using 32 CPU threads. 

## **Conclusion** 

In this technical report we presented the new family of Layout Models used by Docling. We explained how we built a diverse dataset of 150k documents, how we trained the models and which evaluation methods were used. Our best model, heron-101, achieves a 23.9% improvement over Docling’s prior layout model with 78% mAP score when measured on the canonical DocLayNet dataset and is based on RT-DETRv2 architecture with a ResNet101 backbone. Nevertheless, the inference runtime stays on par with what Docling’s earlier model with 0.028 sec/image when measured on a single Nvidia A100 GPU. The fastest model, egret-m, achieves 0.024 sec/image. Our analysis showed that keeping only the elements with high prediction score and applying post-processing can improve the quality of the layout resolution, however without this improvement being reflected on the mAP score. Our observations imply that the mean Average Precision may not be the best metric for the layout analysis on documents. You are very welcome to explore our publicly available models. 





Figure 2: Predictions made by the “heron” model. The ground truth, the predictions without score filtering and the predictions with score over 0.5 are visualized from left to right. Although the filtered predictions have lower mAP, they contain fewer overlapping bounding boxes and look closer to the ground truth. 





Figure 3: Predictions made by the “heron” model with post-processing. The ground truth, the predictions with score over 0.5 and the predictions with the standard Docling postprocessing are visualized from left to right. Post-processing eliminates misidentified “List-item” elements and corrects a full-page “Table” from detections that were mistakenly recognized as separate document items. 





Figure 4: Sometimes alternative layout resolutions also look reasonable. Selected predictions of the “heron” model with score above 0.5 

|Device|Batch-Size|Model|mean|median|min|max|
|---|---|---|---|---|---|---|
|||egret-m|0.334|0.329|0.075|0.440|
|||egret-l|0.472|0.463|0.099|0.682|
|CPU|32|egret-x|0.808|0.797|0.170|1.070|
|||old-docling|0.603|0.596|0.138|0.783|
|||heron|0.643|0.639|0.141|0.826|
|||heron-101|0.988|0.983|0.216|1.322|
|||egret-m|0.024|0.023|0.022|0.043|
|||egret-l|0.027|0.026|0.025|0.048|
||100|egret-x|0.030|0.029|0.027|0.047|
|||old-docling|0.025|0.024|0.024|0.039|
|||heron|0.030|0.027|0.026|0.099|
|||heron-101|0.174|0.168|0.162|0.259|
|CUDA||egret-m|0.024|0.023|0.023|0.034|
|||egret-l|0.026|0.025|0.025|0.037|
||200|egret-x|0.031|0.028|0.027|0.087|
|||old-docling|0.028|0.027|0.026|0.040|
|||heron|0.031|0.029|0.027|0.068|
|||heron-101|0.028|0.028|0.027|0.038|
|||egret-m|0.026|0.026|0.025|0.026|
||500|old-docling|0.029|0.029|0.027|0.031|
|||heron|0.026|0.027|0.026|0.027|
|||egret-m|0.033|0.033|0.030|0.042|
|||egret-l|0.040|0.039|0.036|0.070|
||50|egret-x|0.094|0.090|0.062|0.138|
|||old-docling|0.072|0.072|0.070|0.080|
|||heron|0.044|0.044|0.041|0.051|
|MPS||heron-101|0.062|0.062|0.057|0.076|
|||egret-m|0.038|0.034|0.033|0.078|
|||egret-l|0.110|0.108|0.049|0.170|
||100|egret-x|1.131|1.216|0.069|1.381|
|||old-docling|0.087|0.083|0.072|0.118|
|||heron|0.060|0.053|0.041|0.091|
|||heron-101|0.167|0.150|0.071|0.376|



Table 5: Inference runtime per image in seconds for various devices and batch sizes. CPU=AMD EPYC 7763 (4 threads). GPU=A100 80GB. MPS=M3 Max, 40 cores, 64GB. 

## **References** 

Auer, C.; Dolfi, M.; Carvalho, A.; Ramis, C. B.; and Staar, P. W. 2022. Delivering Document Conversion as a Cloud Service with High Throughput and Responsiveness. In _2022 IEEE 15th International Conference on Cloud Computing (CLOUD)_ , 363–373. IEEE. 

BeeAI. 2023. BeeAI: AI framework. 

Blumenfeld, R. S.; Bliss, D. P.; Perez, F.; and D’Esposito, M. 2014. CoCoTools: open-source software for building connectomes using the CoCoMac anatomical database. _Journal of Cognitive Neuroscience_ , 26(8): 1745–1754. 

breezedeus. 2025. Pix2Text: Open-Source Image-toMarkdown OCR with Layout, Table, Formula Recognition. GitHub repository. Version v1.0+; supports layout analysis, table recognition, text and math formula (LaTeX) OCR. Carion, N.; Massa, F.; Synnaeve, G.; Usunier, N.; Kirillov, A.; and Zagoruyko, S. 2020. End-to-End Object Detection with Transformers. In _ECCV_ , 213–229. 

DataPrepKit. 2023. DataPrepKit: Data preparation toolkit. DeepSearchTeam. 2024. Docling Technical Report. Technical report. 

Feng, H.; Wei, S.; Fei, X.; Shi, W.; Han, Y.; Liao, L.; Lu, J.; Wu, B.; Liu, Q.; Lin, C.; et al. 2025. Dolphin: Document Image Parsing via Heterogeneous Anchor Prompting. _arXiv preprint arXiv:2505.14059_ . 

He, K.; Zhang, X.; Ren, S.; and Sun, J. 2016. Deep Residual Learning for Image Recognition. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 770–778. 

Hou, X.; Zhao, Y.; Wang, S.; and Wang, H. 2025. Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions. _arXiv preprint arXiv:2503.23278_ . 

InstructLab. 2023. InstructLab: Framework for instructionbased learning. 

LangChain. 2023. LangChain: A framework for developing applications powered by language models. 

Li, Z.; Liu, Y.; Liu, Q.; Ma, Z.; Zhang, Z.; Zhang, S.; Guo, Z.; Zhang, J.; Wang, X.; and Bai, X. 2025. MonkeyOCR: Document Parsing with a Structure-Recognition-Relation Triplet Paradigm. arXiv:2506.05218. 

Liu, J. 2022. LlamaIndex. https://github.com/jerryjliu/ llama ~~i~~ ndex. 

Livathinos, N.; Auer, C.; Lysak, M.; Nassar, A.; Dolfi, M.; Vagenas, P.; Berrospi, C.; Omenetti, M.; Dinkla, K.; Kim, Y.; Gupta, S.; de Lima, R. T.; Weber, V.; Morin, L.; Meijer, I.; Kuropiatnyk, V.; and Staar, P. W. J. 2024. Docling Technical Report. Accessed: 2025-07-03, arXiv:arXiv:2408.09869v4. 

Livathinos, N.; Berrospi, C.; Lysak, M.; Kuropiatnyk, V.; Nassar, A.; Carvalho, A.; Dolfi, M.; Auer, C.; Dinkla, K.; and Staar, P. 2021. Robust PDF Document Conversion using Recurrent Neural Networks. _Proceedings of the AAAI Conference on Artificial Intelligence_ , 35(17): 15137–15145. Lv, W.; Zhao, Y.; Chang, Q.; Huang, K.; Wang, G.; and Liu, Y. 2024. RT-DETRv2: Improved Baseline 

with Bag-of-Freebies for Real-Time Detection Transformer. arXiv:2407.17140. 

Lysak, M.; Nassar, A.; Livathinos, N.; Auer, C.; and Staar, P. 2023. Optimized Table Tokenization for Table Structure Recognition. In _Document Analysis and Recognition - ICDAR 2023: 17th International Conference, San Jos´e, CA, USA, August 21–26, 2023, Proceedings, Part II_ , 37– 50. Berlin, Heidelberg: Springer-Verlag. ISBN 978-3-03141678-1. 

Mandal, S. 2025. Nanonets-OCR-s: A State-of-the-Art Image-to-Markdown OCR Model with Semantic Understanding. Online; research announcement on Nanonets website. Transforms documents into structured markdown with semantic tagging, supporting LaTeX equations, image descriptions, signatures, watermarks, checkboxes, tables. Morin, L.; Danelljan, M.; Agea, M. I.; Nassar, A.; Weber, V.; Meijer, I.; Staar, P.; and Yu, F. 2023. MolGrapher: Graph-based Visual Recognition of Chemical Structures. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 19552–19561. 

Nassar, A.; Livathinos, N.; Lysak, M.; and Staar, P. 2022. Tableformer: Table structure understanding with transformers. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 4614–4623. 

Nassar, A.; Marafioti, A.; Omenetti, M.; Lysak, M.; Livathinos, N.; Auer, C.; Morin, L.; Teixeira de Lima, R.; Kim, Y.; Gurbuz, A. S.; Dolfi, M.; Farr´e, M.; and Staar, P. W. J. 2025. SmolDocling: An ultra-compact visionlanguage model for end-to-end multi-modal document conversion. _arXiv preprint arXiv:2503.11576_ . Paruchuri, V. 2024. Marker: Convert PDF to Markdown Quickly with High Accuracy. https://github.com/VikParuchuri/marker. Peng, Y.; Li, H.; Wu, P.; Zhang, Y.; Sun, X.; and Wu, F. 2024. D-FINE: Redefine Regression Task in DETRs as Finegrained Distribution Refinement. arXiv:2410.13842. 

Pfitzmann, B.; Auer, C.; Dolfi, M.; Nassar, A. S.; and Staar, P. W. J. 2022. DocLayNet: A Large Human-Annotated Dataset for Document-Layout Analysis. 

Redmon, J.; Divvala, S.; Girshick, R.; and Farhadi, A. 2016. You Only Look Once: Unified, Real-Time Object Detection. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 779–788. 

Unstructured.io Team. 2024. Unstructured.io: OpenSource Pre-Processing Tools for Unstructured Data. https://unstructured.io. Accessed: 2024-11-19. Wang, B.; Xu, C.; Zhao, X.; Ouyang, L.; Wu, F.; Zhao, Z.; Xu, R.; Liu, K.; Qu, Y.; Shang, F.; Zhang, B.; Wei, L.; Sui, Z.; Li, W.; Shi, B.; Qiao, Y.; Lin, D.; and He, C. 2024. MinerU: An Open-Source Solution for Precise Document Content Extraction. arXiv:2409.18839. 

Weber, M.; Siebenschuh, C.; Butler, R. M.; Alexandrov, A.; Thanner, V. R.; Tsolakis, G.; Jabbar, H.; Foster, I.; Li, B.; Stevens, R.; and Zhang, C. 2023. WordScape: a Pipeline to extract multilingual, visually rich Documents with Layout Annotations from Web Crawl Data. In _Advances in Neural Information Processing Systems_ . 

Wolf, T.; Debut, L.; Sanh, V.; Chaumond, J.; Delangue, C.; Moi, A.; Cistac, P.; Rault, T.; Louf, R.; Funtowicz, M.; Davison, J.; Shleifer, S.; von Platen, P.; Ma, C.; Jernite, Y.; Plu, J.; Xu, C.; Scao, T. L.; Gugger, S.; Drame, M.; Lhoest, Q.; and Rush, A. M. 2020. Transformers: State-of-the-Art Natural Language Processing. In _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations_ , 38–45. Online: Association for Computational Linguistics. 

Zhao, Y.; Lv, W.; Xu, S.; Wei, J.; Wang, G.; Dang, Q.; Liu, Y.; and Chen, J. 2023. DETRs Beat YOLOs on Real-time Object Detection. arXiv:2304.08069. 



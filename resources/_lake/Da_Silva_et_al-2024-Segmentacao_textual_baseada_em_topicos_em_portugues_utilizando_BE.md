---
title: Segmentação textual baseada em tópicos em português utilizando BERTimbau
citekey: Silva2024
authors:
- Luciano A. C. Da Silva
- Maiara S. F. Rodrigues
- Adriana P. Archanjo
- Luis Pessoa
- Miguel L. Silva
- Thiago F. De Almeida
- Leonardo Silveira
year: 2024
date: '2024-11-17'
item_type: conferencePaper
doi: 10.5753/stil.2024.245080
url: https://sol.sbc.org.br/index.php/stil/article/view/31113
zotero_key: 2RLCAYI3
collections:
- SA9KZ2CI
tags: []
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: segmentação textual baseada em tópicos em português utilizando bertimbau.pdf
synced_at: '2026-09-29T18:35:20.557413'
---

# Segmentação textual baseada em tópicos em português utilizando BERTimbau

**Autores:** Luciano A. C. Da Silva, Maiara S. F. Rodrigues, Adriana P. Archanjo, Luis Pessoa, Miguel L. Silva, Thiago F. De Almeida, Leonardo Silveira
**DOI:** [10.5753/stil.2024.245080](https://doi.org/10.5753/stil.2024.245080)
**URL:** https://sol.sbc.org.br/index.php/stil/article/view/31113

## 📄 Conteúdo Completo do Documento

# **Segmentac¸˜ao Textual Baseada em T´opicos em Portuguˆes Utilizando BERTimbau** 

**Luciano A. C. da Silva**<sup>1</sup> **, Maiara S. F. Rodrigues**<sup>1</sup> **, Adriana P. Archanjo**<sup>1</sup> **, Luis Pessoa**<sup>1</sup> **, Miguel L. Silva**<sup>1</sup> **, Thiago F. de Almeida**<sup>1</sup> **, Leonardo Silveira**<sup>2</sup> **,** 

1CPQD - Centro de Pesquisa e Desenvolvimento, Campinas, SP, Brasil 

2Pontif´ıcia Universidade Cat´olica de Campinas, SP, Brasil 

luciano.augusto.silva@usp.br, maiara.frodrigues2000@gmail.com, prestoarch@hotmail.com, _{_ luisp, mfilho, tfelipea _}_ @cpqd.com.br, leonardo.silveira@ga.ita.br 

**_Abstract._** _In this work, we explore text segmentation for Portuguese using the BERTimbau model, with datasets derived from machine translation and online news sources. We obtained Pk_ = 6 _._ 89 _for an in-domain evaluation, but worse results in out-of-domain evaluations, highlighting the importance of a diverse training set to improve generalization across multiple domains._ 

**_Resumo._** _Neste trabalho, exploramos a segmentac¸˜ao textual para o portuguˆes utilizando o modelo BERTimbau, com bases de dados constru´ıdas usando traduc¸˜ao autom´atica e a partir de not´ıcias online. Obtivemos Pk_ = 6 _,_ 89 _para uma avaliac¸˜ao dentro do dom´ınio, mas resultados piores em avaliac¸˜oes fora do dom´ınio, destacando a importˆancia de uma base de treinamento diversificada para melhorar a generalizac¸˜ao em m´ultiplos dom´ınios._ 

## **1. Introduc¸˜ao** 

Com o aumento na gerac¸˜ao de conte´udo textual n˜ao estruturado, como transcric¸˜oes autom´aticas de not´ıcias, aulas e reuni˜oes, h´a tamb´em um crescente interesse em extrair de forma eficiente informac¸˜oes relevantes desse material [Retkowski and Waibel 2024, Gklezakos et al. 2024]. Por exemplo, pode ser desafiador encontrar o in´ıcio de um determinado t´opico discutido na transcric¸˜ao de uma longa reuni˜ao, a menos que essa transcric¸˜ao esteja devidamente estruturada. A segmentac¸˜ao textual baseada em t´opicos ´e uma tarefa de Processamento de Linguagem Natural (PLN) que divide um texto longo em segmentos n˜ao sobrepostos, de acordo com as mudanc¸as de t´opico [Hearst 1997]. Essa ferramenta permite estruturar e compreender melhor grandes volumes de dados, facilitando a busca e a extrac¸˜ao de informac¸˜oes. 

H´a poucos trabalhos recentes sobre segmentac¸˜ao textual em portuguˆes [Cardoso et al. 2017, Francisco 2018]. Neste artigo, exploramos a segmentac¸˜ao textual baseada em t´opicos para o portuguˆes, aplicando a abordagem proposta em [Yu et al. 2023], utilizando o modelo BERTimbau [Souza et al. 2023]. Constru´ımos os conjuntos de dados de treinamento e teste por meio de traduc¸˜ao autom´atica para o portuguˆes, e utilizando not´ıcias extra´ıdas da internet. 

## **2. Metodologia** 

Neste trabalho, utilizamos a abordagem proposta por [Yu et al. 2023] que trata a segmentac¸˜ao textual como um problema de classificac¸˜ao de uma sequˆencia de sentenc¸as, 

em que se deseja identificar a ´ultima sentenc¸a de cada t´opico, ou seja, identificar as fronteiras dos segmentos. O componente principal ´e um modelo de linguagem pr´e-treinado do tipo _Transformer encoder_ [Vaswani et al. 2023], que produz a representac¸˜ao contextual das sentenc¸as do texto de entrada. Cada representac¸˜ao de sentenc¸a ´e usada na classificac¸˜ao de fronteira do segmento, conforme mostrado na Figura 1. 



**Figura 1. Estrutura do modelo de segmentac¸ ˜ao proposto por [Yu et al. 2023]** 

Em [Yu et al. 2023], al´em da tarefa principal de segmentac¸˜ao baseada em t´opicos, s˜ao definidas duas tarefas auxiliares adicionais, _Topic-aware Sentence Structure Prediction_ (TSSP) e _Contrastive Semantic Similarity Learning_ (CSSL), com o objetivo de modelar a coerˆencia textual e obter melhores resultados na segmentac¸˜ao. O modelo ´e treinado de forma supervisionada, otimizando a soma das perdas das trˆes tarefas definidas, sobre um conjunto de treinamento devidamente anotado. 

Neste trabalho, utilizamos _datasets_ para o treinamento e a avaliac¸˜ao obtidos por meio de traduc¸˜ao autom´atica para portuguˆes ou constru´ıdos a partir de not´ıcias em portuguˆes extra´ıdas da internet. Os _datasets_ WikiSection e WIKI-50 foram usados por [Yu et al. 2023] e passaram pelo processo de traduc¸˜ao autom´atica usando a _API_ de traduc¸˜ao da Google. O _dataset_ WikiSection [Arnold et al. 2019] foi usado para treinamento e avaliac¸˜ao, e consiste num conjunto de 38K artigos em inglˆes e alem˜ao, nos dom´ınios de doenc¸as e cidades. Ap´os a traduc¸˜ao, restaram 3.590 documentos no dom´ınio de doenc¸as e 19.539 documentos no dom´ınio de cidades. O _dataset_ WIKI-50 [Koshorek et al. 2018] foi usado apenas para avaliac¸˜ao, e consiste originalmente em um conjunto de 50 amostras em inglˆes, provenientes da Wikipedia. 

Para a avaliac¸˜ao dos modelos, utilizamos tamb´em _datasets_ em portuguˆes constru´ıdos a partir de not´ıcias extra´ıdas com _webscrapping_ do portal G1<sup>1</sup> (portal de not´ıcias do Grupo Globo de Comunicac¸˜ao), e do canal de not´ıcias do IBGE<sup>2</sup> (Instituto Brasileiro de Geografia e Estat´ıstica). Os documentos de texto foram formados pela concatenac¸˜ao aleat´oria de not´ıcias, sendo cada not´ıcia considerada um segmento de t´opico diferente. No caso do _dataset_ G1, foram gerados 454 documentos a partir de 1.300 not´ıcias. Para o _dataset_ IBGE, foram gerados 1.517 documentos a partir de 3.376 not´ıcias. 

> 1https://g1.globo.com/tecnologia/noticia/2012/11/siga-o-g1-por-rss.html 

> 2https://servicodados.ibge.gov.br/api/docs/noticias?versao=3 

Como o nosso objetivo ´e aplicar a segmentac¸˜ao para o portuguˆes, substitu´ımos o modelo usado em [Yu et al. 2023] pelo modelo BERTimbau [Souza et al. 2023], pr´etreinado para o portuguˆes do Brasil. Utilizamos as vers˜oes BERTimbau Base (110M de parˆametros) e BERTimbau Large (335M de parˆametros)<sup>3</sup> . 

O treinamento foi realizado em uma GPU NVIDIA T4, usando BERTimbau Base e Large, com 70% do _dataset_ WikiSection em portuguˆes, por 5 ´epocas, com _learning rate_ de 5 _×_ 10<sup>_−_5</sup> , _batch size_ de 2 e gradiente acumulado de 2. Criamos sempre um modelo treinado com WiKiSection/cidades e o outro modelo treinado com WiKiSection/doenc¸as. No caso do BERTimbau Large, o treinamento durou aproximadamente 2 dias e 5 horas para o conjunto de cidades e pouco mais de 11 horas para o conjunto de doenc¸as. 

A avaliac¸˜ao dos modelos seguiu a mesma linha de [Yu et al. 2023]. Usamos trˆes m´etricas usuais para avaliac¸˜ao de segmentac¸˜ao textual: _F_ 1, _Pk_ [Beeferman et al. 1999], e _WindowDiff_ [Pevzner and Hearst 2002]. No caso das m´etricas _Pk_ e _WindowDiff_ , quanto menor o valor, melhor o desempenho. No caso da m´etrica _F_ 1, quanto maior o valor, melhor o desempenho. A avaliac¸˜ao dentro do dom´ınio de treinamento foi realizada com 20% do _dataset_ WikiSection em portuguˆes. Os _datasets_ WIKI-50, G1 e IBGE s˜ao usados apenas para avaliac¸˜ao fora do dom´ınio de treinamento. 

## **3. Resultados** 

As Tabelas 1 e 2 apresentam os resultados de avaliac¸˜ao dos modelos usando BERTimbau, criados e avaliados para o portuguˆes, dentro do mesmo dom´ınio, com os _datasets_ WikiSection/cidades e WikiSection/doenc¸as. Tamb´em s˜ao apresentados os resultados para o inglˆes correspondentes ao modelo BERT Base [Devlin et al. 2018], obtidos por [Yu et al. 2023]. 

|**Modelo**|**_F_1**|**_Pk_**|**_WD_**|
|---|---|---|---|
|(en) BERT Base [Yu et al. 2023]|80,16|8,22|10,19|
|(pt) BERTimbau Base|87,41|7,07|8,55|
|(pt)BERTimbau Large|87,59|6,89|8,37|



### **Tabela 1. Resultados dos modelos criados e avaliados com o** **_dataset_ WikiSection / cidades. BERT Base avaliado em inglˆes, BERTimbau em portuguˆes.** 

|**Modelo**|**_F_1**|**_Pk_**|**_WD_**|
|---|---|---|---|
|(en) BERT Base [Yu et al. 2023]|68,26|18,29|22,06|
|(pt) BERTimbau Base|76,91|17,16|19,45|
|(pt)BERTimbau Large|77,77|16,55|18,76|



### **Tabela 2. Resultados dos modelos criados e avaliados com o** **_dataset_ WikiSection / doenc¸as. BERT Base avaliado em inglˆes, BERTimbau em portuguˆes.** 

As m´etricas de avaliac¸˜ao obtidas com os modelos BERTimbau para o portuguˆes s˜ao melhores e pr´oximas `aquelas apresentadas por [Yu et al. 2023] em inglˆes. Neste caso, devemos considerar tamb´em que o modelo criado para o portuguˆes usando BERTimbau Large ´e maior que o modelo usado em [Yu et al. 2023]. 

3https://huggingface.co/neuralmind/bert-base-portuguese-cased 

A Tabela 3 apresenta os resultados da avaliac¸˜ao de dois modelos criados para o portuguˆes nos dom´ınios de cidades e doenc¸as, usando o BERTimbau Large, e avaliados fora do dom´ınio de treinamento, nos _datasets_ WIKI-50, G1 e IBGE. 

|**Dataset**|**Mod**|**elo / cid**|**ades**|**Mod**|**elo / doe**|**nc¸as**|
|---|---|---|---|---|---|---|
||**_F_1**|**_Pk_**|**_WD_**|**_F_1**|**_Pk_**|**_WD_**|
|Wiki50|15,43|35,01|35,36|12,97|35,98|36,02|
|G1|64,66|13,62|17,28|54,81|25,61|32,42|
|IBGE|43,12|20,12|21,06|43,36|23,40|26,55|



**Tabela 3. Avaliac¸ ˜ao fora do dom´ınio de treinamento. Modelos com o BERTimbau Large criados com o** **_dataset_ WikiSection/cidades e WikiSection/doenc¸as.** 

O desempenho do modelo fora do dom´ınio de treinamento foi inferior ao desempenho dentro do dom´ınio. Os resultados foram melhores para o modelo treinado com o _dataset_ WiKiSection/cidades. De fato, segundo [Arnold et al. 2019], o conte´udo do _dataset_ WikiSection apresenta caracter´ısticas distintas para cada dom´ınio: WiKiSection/doenc¸as ´e de dom´ınio cient´ıfico restrito com linguagem espec´ıfica, enquanto WiKiSection/cidades ´e de dom´ınio geral mais diverso, mais pr´oximo de um conte´udo de not´ıcias. Isso sugere que a composic¸˜ao de dados de treinamento pode ajudar a obter um modelo para segmentac¸˜ao textual que generalize melhor para m´ultiplos dom´ınios. 

## **4. Conclus˜ao** 

Neste trabalho, exploramos a segmentac¸˜ao textual para o portuguˆes, seguindo a abordagem de [Yu et al. 2023], mas utilizando o modelo pr´e-treinado para o portuguˆes BERTimbau [Souza et al. 2023]. Empregamos bases de treinamento e teste constru´ıdas usando a traduc¸˜ao autom´atica de bases existentes, al´em de bases de teste constru´ıdas a partir de not´ıcias em portuguˆes recuperadas da internet. Obtivemos ´otimos resultados na segmentac¸˜ao de texto dentro do mesmo dom´ınio para o portuguˆes, semelhante ao que foi obtido por [Yu et al. 2023] para o inglˆes. Nossos resultados sugerem a efic´acia do m´etodo empregado para a criac¸˜ao do modelo em portuguˆes e a importˆancia de usar uma base de treinamento de dom´ınio diversificado para obter um modelo que generalize melhor para m´ultiplos dom´ınios. 

Para trabalhos futuros, pretendemos explorar modelos diferentes e buscar uma composic¸˜ao mais variada de dados de treinamento para obter um modelo que generalize melhor para v´arios dom´ınios. Al´em disso, desejamos estudar a segmentac¸˜ao textual de transcric¸˜oes autom´aticas obtidas com reconhecimento de fala, e explorar a segmentac¸˜ao de textos muito longos, considerando a t´ıpica limitac¸˜ao do contexto de entrada de modelos baseados em _Transformer_ [Vaswani et al. 2023]. 

## **Agradecimentos** 

Este projeto foi apoiado pelo Minist´erio da Ciˆencia, Tecnologia e Inovac¸˜oes, com recursos da Lei no 8.248, de 23 de outubro de 1991, no ˆambito do PPI-SOFTEX, coordenado pela Softex e publicado PDI 03, DOU 01245.023862/2022-14. 

## **Referˆencias** 

- Arnold, S., Schneider, R., Cudr´e-Mauroux, P., Gers, F. A., and L¨oser, A. (2019). Sector: A neural model for coherent topic segmentation and classification. _Transactions of the Association for Computational Linguistics_ , 7:169–184. 

- Beeferman, D., Berger, A. L., and Lafferty, J. D. (1999). Statistical models for text segmentation. _Machine Learning_ , 34:177–210. 

- Cardoso, P. C., Pardo, T. A., and Taboada, M. (2017). Subtopic annotation and automatic segmentation for news texts in brazilian portuguese. _Corpora_ , 12(1):23–54. 

- Devlin, J., Chang, M., Lee, K., and Toutanova, K. (2018). BERT: pre-training of deep bidirectional transformers for language understanding. _CoRR_ , abs/1810.04805. 

- Francisco, O. J. (2018). Recuperac¸˜ao de informac¸˜ao em atas de reuni˜ao utilizando segmentac¸˜ao textual e extrac¸˜ao de t´opicos. Dissertac¸˜ao de mestrado, Universidade Federal de S˜ao Carlos, Sorocaba. 

- Gklezakos, D. C., Misiak, T., and Bishop, D. (2024). Treeseg: Hierarchical topic segmentation of large transcripts. _arXiv preprint arXiv:2407.12028_ . 

- Hearst, M. A. (1997). Text tiling: Segmenting text into multi-paragraph subtopic passages. _Computational linguistics_ , 23(1):33–64. 

- Koshorek, O., Cohen, A., Mor, N., Rotman, M., and Berant, J. (2018). Text segmentation as a supervised learning task. In _Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 2 (Short Papers)_ , pages 469–473. 

- Pevzner, L. and Hearst, M. A. (2002). A critique and improvement of an evaluation metric for text segmentation. _Computational Linguistics_ , 28(1):19–36. 

- Retkowski, F. and Waibel, A. (2024). From text segmentation to smart chaptering: A novel benchmark for structuring video transcriptions. In _Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 406–419. 

- Souza, F., Nogueira, R., and Lotufo, R. (2023). Bert models for brazilian portuguese: Pretraining, evaluation and tokenization analysis. _Applied Soft Computing_ , 149:110901. 

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., and Polosukhin, I. (2023). Attention is all you need. 

- Yu, H., Deng, C., Zhang, Q., Liu, J., Chen, Q., and Wang, W. (2023). Improving long document topic segmentation models with enhanced coherence modeling. In Bouamor, H., Pino, J., and Bali, K., editors, _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , pages 5592–5605, Singapore. Association for Computational Linguistics. 



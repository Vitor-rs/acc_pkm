---
title: Etiquetagem morfossintática multigênero para o português do brasil segundo
  o modelo "universal dependencies"
citekey: Silva2023
authors:
- Emanuel Huber Silva
- Thiago Alexandre Salgueiro Pardo
- Norton Trevisan Roman
year: 2023
date: '2023-09-25'
item_type: conferencePaper
doi: 10.5753/stil.2023.233848
url: https://sol.sbc.org.br/index.php/stil/article/view/25438
zotero_key: LCPFXTFS
collections:
- SA9KZ2CI
tags: []
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: etiquetagem morfossintática multigênero para o português do brasil
  segundo o modelo universal dependencies.pdf
synced_at: '2026-09-29T18:42:34.746263'
---

# Etiquetagem morfossintática multigênero para o português do brasil segundo o modelo "universal dependencies"

**Autores:** Emanuel Huber Silva, Thiago Alexandre Salgueiro Pardo, Norton Trevisan Roman
**DOI:** [10.5753/stil.2023.233848](https://doi.org/10.5753/stil.2023.233848)
**URL:** https://sol.sbc.org.br/index.php/stil/article/view/25438

## 📄 Conteúdo Completo do Documento

# **Etiquetagem morfossint´atica multigˆenero para o portuguˆes do Brasil segundo o modelo “Universal Dependencies”** 

**Emanuel Huber Silva**<sup>1</sup><sup>_,_3</sup><sup>_,_4</sup> **, Thiago Alexandre Salgueiro Pardo**<sup>1</sup> **, Norton Trevisan Roman**<sup>2</sup> 

1N´ucleo Interinstitucional de Lingu´ıstica Computacional (NILC), Instituto de Ciˆencias Matem´aticas e de Computac¸˜ao - Universidade de S˜ao Paulo (USP) 

2Escola de Artes, Ciˆencias e Humanidades - Universidade de S˜ao Paulo (USP) 

3Centro de Inovac¸˜ao CESAR 

4Departamento de Engenharia da Computac¸˜ao - Facens 

emanuel.huber@usp.br, taspardo@icmc.usp.br, norton@usp.br 

**_Abstract._** _Part of speech tagging is a process that seeks to identify the grammatical classes of words and symbols (tokens) in a sentence. For Brazilian Portuguese, there is a variety of approaches using corpora of the journalistic genre with different tagsets. In this paper, we present results better than the current state of the art, investigating tagging methods and evaluating their ability to perform multi-genre analysis in corpora of journalistic, academic and user-generated content genres. To do so, we use the Universal Dependencies model. Finally, we present a qualitative assessment of the systematic tagging errors made in the process._ 

**_Resumo._** _A etiquetagem morfossint´atica ´e um processo que busca identificar as classes gramaticais de palavras e s´ımbolos (tokens) em uma sentenc¸a. Para o portuguˆes brasileiro, h´a uma variedade de trabalhos utilizando corpora de gˆenero jornal´ıstico com diferentes conjuntos de etiquetas. Neste artigo, apresentamos resultados que superam o estado da arte atual, investigando m´etodos de etiquetagem e avaliando sua capacidade de an´alise multigˆenero em corpora dos gˆeneros jornal´ıstico, acadˆemico e de “user-generated content”. Para tanto, usamos o modelo “Universal Dependencies”. Por fim, apresentamos uma avaliac¸˜ao qualitativa dos erros sistem´aticos cometidos pelo modelo._ 

## **1. Introduc¸˜ao** 

A ´area de Processamento de L´ınguas Naturais (PLN) busca automatizar tarefas que envolvam a interpretac¸˜ao e a gerac¸˜ao de l´ıngua natural [Jurafsky e Martin 2009]. Em v´arias dessas tarefas, faz-se necess´ario utilizar caracter´ısticas lingu´ısticas dos documentos, como as classes gramaticais de palavras e s´ımbolos (ou etiquetas morfossint´aticas dos _tokens_ – do inglˆes, _part of speech tags_ ) e a estruturac¸˜ao sint´atica das sentenc¸as. 

Apesar da dominˆancia atual das abordagens neurais e dos grandes modelos de l´ıngua, que na maioria das vezes processam textos em suas formas originais sem anotac¸˜ao lingu´ıstica sofisticada, h´a muitas evidˆencias da importˆancia de informac¸˜oes lingu´ısticas em PLN. Por exemplo, [Lin et al. 2021] combinam etiquetas morfossint´aticas com representac¸˜oes vetoriais para aprimorar um analisador de opini˜oes baseado em aspectos. [Zhao et al. 2019], na frente de sumarizac¸˜ao autom´atica, demostram a importˆancia 

de utilizar informac¸˜oes lexicais e de etiquetas morfossint´aticas em conjunto com mecanismos de atenc¸˜ao. [Cabral et al. 2022], por sua vez, fazem uso desses conhecimentos no desenvolvimento de um sistema de extrac¸˜ao de informac¸˜ao aberta para o portuguˆes. [Garimella et al. 2019], em um estudo socio-lingu´ıstico, demonstram que h´a diferenc¸as gramaticais em textos escritos por homens e mulheres. 

Motivadas pela importˆancia desse tipo de conhecimento em PLN, h´a v´arias iniciativas cl´assicas e mais recentes para o desenvolvimento de recursos e ferramentas relacionados para o processamento computacional da l´ıngua portuguesa. Pode-se citar, por exemplo, a amplamente conhecida Floresta Sint´a(c)tica [Afonso et al. 2002] e o _treebank_ Porttinari [Pardo et al. 2021], o l´exico de l´ıngua geral PortiLexiconUD [Lopes et al. 2022], o etiquetador morfossint´atico LX-Tagger [Branco e Silva 2004] e o etiquetador do estado da arte de [Fonseca et al. 2015] treinado com o corpus de referˆencia Mac-Morpho [Alu´ısio et al. 2003], assim como o conhecido _parser_ PALAVRAS [Bick 2000], entre muitas outras pesquisas relevantes. 

Visando a contribuir nesta frente e avanc¸ar a fronteira do conhecimento, este artigo foca na tarefa de etiquetagem morfossint´atica para o portuguˆes, mas trazendo ambic¸˜oes maiores. Por um lado, s˜ao investigados m´etodos variados e do estado da arte para conjuntos de dados de referˆencia em portuguˆes, avaliando-se a capacidade de an´alise multigˆenero dos m´etodos. Objetiva-se, com isso, o desenvolvimento de um etiquetador de alta acur´acia e de amplo uso, possibilitando o desenvolvimento de aplicac¸˜oes de PLN mais robustas. Para tanto, utilizam-se os corpora Porttinari [Pardo et al. 2021], DANTEStocks [Di Felippo et al. 2021] e PetroGold [Souza et al. 2021], dos gˆeneros jornal´ıstico, gerado por usu´ario (do inglˆes, _User-Generated Content_ - UGC) e acadˆemico (do dom´ınio de ´oleo e g´as), respectivamente. Por outro lado, explora-se o modelo _Universal Dependencies_ (UD) [de Marneffe et al. 2021], de ampla aceitac¸˜ao, inclusive para o portuguˆes [Rademaker et al. 2017]. Mostramos que nossos melhores resultados ultrapassam 99% de acur´acia e que ´e poss´ıvel produzir um etiquetador morfossint´atico multigˆenero de alta acur´acia, superando o estado da arte. Mais do que isso, na an´alise qualitativa realizada, evidencia-se que muitos dos erros remanescentes s˜ao linguisticamente plaus´ıveis. 

O restante desse trabalho est´a organizado como segue. Na Sec¸˜ao 2, os trabalhos relacionados s˜ao sucintamente apresentados. Na Sec¸˜ao 3, os corpora utilizados s˜ao introduzidos. Os experimentos realizados e os resultados atingidos s˜ao relatados nas Sec¸˜oes 4 e 5. Por fim, a Sec¸˜ao 6 conclui esse trabalho. 

## **2. Trabalhos relacionados** 

H´a v´arios trabalhos em etiquetagem morfossint´atica para o portuguˆes, dos quais destacamos alguns. [Fonseca et al. 2015] utilizam uma rede neural com representac¸˜oes vetoriais das palavras e atributos lingu´ısticos adicionais (como capitalizac¸˜ao e sufixos) para prever suas etiquetas. Os autores utilizam diferentes vers˜oes do corpus jornal´ıstico MacMorpho [Alu´ısio et al. 2003], atingindo 97 _,_ 57% de acur´acia (ou seja, a proporc¸˜ao de _tokens_ corretamente classificados). Utilizando o mesmo corpus, [de Sousa e Lopes 2019] avaliam as Redes Neurais Recorrentes (RNRs) bidirecionais com representac¸˜oes vetoriais em n´ıvel de palavra e caractere. Essa abordagem alcanc¸ou 97 _,_ 36% de acur´acia. [Domingues 2011] apresenta um etiquetador que utiliza o aprendizado baseado em transformac¸˜oes para os gˆeneros jornal´ıstico e acadˆemico. Foram utilizados um l´exico 

**Tabela 1. Exemplos dos corpora selecionados** 

|Corpus|Exemplo|
|---|---|
|Porttinari-base|Foram/AUX avaliados/VERB 5.281/NUM munic´ıpios/NOUN ,/PUNCT ou/CCONJ<br>95/NUM %/SYM de/ADP o/DET total/NOUN de/ADP 5.569/NUM existentes/ADJ<br>em/ADP o/DET Brasil/NOUN ./PUNCT|
|DANTEStocks|BBAS3/PROPN comprar/VERB por/ADP R$/SYM 20,05/NUM indicado/VERB<br>em/ADP 27/02/2014/NUM 10:41/NUM http://t.co/zJRs3Eeyz9/SYM|
|PetroGold|Segundo/ADP<br>Luiz/PROPN<br>&/PROPN<br>Silva/PROPN<br>(/PUNCT<br>1995/NUM<br>)/PUNCT estas/DET feic¸˜oes/NOUN definem/VERB a/DET maioria/NOUN de/ADP|
||os/DET lineamentos/NOUN em/ADP mapas/NOUN magn´eticos/ADJ ./PUNCT|



para o tratamento de nomes pr´oprios, regras manuais e a sa´ıda de outros dois etiquetadores dispon´ıveis na literatura. Al´em do Mac-Morpho, o trabalho tamb´em utilizou o Bosque (que integra a Floresta Sint´a(c)tica) para o gˆenero jornal´ıstico. Para o gˆenero acadˆemico, utilizou a Selva Cient´ıfica (tamb´em parte da Floresta Sint´a(c)tica). A avaliac¸˜ao apresentou acur´acias de 98 _,_ 06%, 98 _,_ 30% e 98 _,_ 07%, respectivamente. Outros trabalhos baseados em RNRs e com uso de diferentes representac¸˜oes vetoriais alcanc¸aram alto desempenho no corpus Bosque. Destacam-se o UDPipe 2 [Straka 2018], com 96 _,_ 37% de acur´acia, o CNCSR [Heinzerling e Strube 2019], com 98 _,_ 1%, e o Stanza [Qi et al. 2020], com 97 _,_ 04%. Por fim, destaca-se o trabalho de [Bohnet et al. 2018], que utiliza a t´ecnica de Meta-BILSTM, com a premissa de que o uso de diferentes representac¸˜oes vetoriais pode contribuir para o desempenho na tarefa. O modelo alcanc¸ou 98 _,_ 11% de acur´acia no corpus Bosque. 

Os conjuntos de etiquetas morfossint´aticas ( _tagsets_ ) variam nos diferentes trabalhos. Os trabalhos mais recentes fazem uso do _tagset_ do modelo _Universal Dependencies_ (UD) [de Marneffe et al. 2021], composto por 17 etiquetas. As classes abertas s˜ao representadas pelas etiquetas ADJ, ADV, INTJ, NOUN, PROPN e VERB; as classes fechadas s˜ao ADP, AUX, CCONJ, DET, NUM, PART, PRON e SCONJ; h´a tamb´em as etiquetas para outros casos, como PUNCT, SYM e X. O modelo UD j´a ´e adotado por mais de 100 l´ınguas, contando com aproximadamente 200 _treebanks_ catalogados. Esse modelo tem tido grande aceitac¸˜ao em func¸˜ao de sua proposta de “universalidade”, com aplicac¸˜ao para l´ınguas tipologicamente diferentes, j´a tendo passado por algumas vers˜oes. Como comentado anteriormente, este trabalho tamb´em se filia ao modelo UD. 

## **3. Corpora** 

Neste trabalho, foram utilizados trˆes corpora de gˆeneros diferentes, anotados manualmente segundo o modelo UD. Para o gˆenero jornal´ıstico, foi utilizada a porc¸˜ao “base” do _treebank_ Porttinari [Pardo et al. 2021], com not´ıcias do jornal Folha de S˜ao Paulo. A porc¸˜ao “base” ´e a semente com base na qual o restante do _treebank_ foi anotado. Para o gˆenero de UGC, adotou-se o corpus DANTEStocks [Di Felippo et al. 2021], que cont´em _tweets_ do mercado financeiro. Contemplando o gˆenero acadˆemico, o corpus PetroGold [Souza et al. 2021] apresenta uma coletˆanea de textos da ´area de ´oleo e g´as, provenientes de teses, dissertac¸˜oes e monografias. Na Tabela 1, para evidenciar os desafios da tarefa, ´e poss´ıvel visualizar um exemplo manualmente anotado de sentenc¸a ou _tweet_ de cada corpus (a etiqueta morfossint´atica ´e separada dos _tokens_ pela barra). 

A Tabela 2 mostra o total de sentenc¸as e _tokens_ de cada corpus. E poss´ıvel obser-<sup>´</sup> var que o corpus DANTEStocks tem uma quantidade menor de _tokens_ quando comparado aos corpora Porttinari-base e PetroGold. Ressalta-se que os corpora DANTEStocks e Porttinari-base originalmente n˜ao possuem a divis˜ao em conjuntos de treino, validac¸˜ao e teste. Dessa forma, para fins de avaliac¸˜ao e comparac¸˜ao justa entre m´etodos, foi realizada essa divis˜ao com a amostragem aleat´oria, utilizando a proporc¸˜ao de 10% para validac¸˜ao e 20% para o conjunto de teste, resultando nos n´umeros mostrados na tabela. 

**Tabela 2. Estat´ısticas dos corpora utilizados** 

|Corpus|Gˆenero|Treino|Validac¸˜ao|Teste|Sentenc¸as|_tokens_|
|---|---|---|---|---|---|---|
|Porttinari-base|Jornal´ıstico|5.894|585|1.668|8.420|168.400|
|DANTEStocks|UGC|2.833|413|802|4.048|81.048|
|PetroGold|Acadˆemico|8.054|447|445|8.946|250.905|



´E interessante notar dois pontos adicionais sobre os corpora selecionados. Em primeiro lugar, eles contˆem textos bastante diferentes entre si, tanto em gˆenero quanto dom´ınio. Isso ´e importante para o teste que este artigo se prop˜oe a fazer, de avaliar a capacidade multigˆenero dos m´etodos. Em segundo lugar, h´a outros corpora que s˜ao anotados com UD e disponibilizados publicamente, como o Bosque [Rademaker et al. 2017], o CINTIL [Branco et al. 2022] e o PUD ( _Parallel Universal Dependencies_ ) [Zeman et al. 2017], mas que foram preteridos por n˜ao seguirem diretrizes de anotac¸˜ao similares e n˜ao conterem apenas textos em portuguˆes brasileiro. Os trˆes corpora selecionados, al´em de serem para o portuguˆes brasileiro, fazem parte de um esforc¸o nacional de estudo e uniformizac¸˜ao de UD para o portuguˆes<sup>1</sup> . Dessa forma, h´a menos vari´aveis envolvidas nos experimentos realizados. 

## **4. Experimentos** 

A experimentac¸˜ao foi dividida em duas etapas. A primeira consistiu em avaliar diferentes t´ecnicas de etiquetagem no corpus jornal´ıstico, o Porttinari-base. Em seguida, aplicou-se no contexto multigˆenero a t´ecnica de melhor desempenho, considerando ent˜ao os demais corpora. Essa estrat´egia visou a otimizar a sequˆencia de testes necess´arios. 

### **4.1. T´ecnicas de etiquetagem morfossint´atica** 

Foram selecionadas sete t´ecnicas/modelos de etiquetagem morfossint´atica para a avaliac¸˜ao no corpus Porttinari-base, sendo esta selec¸˜ao feita com base na representatividade e no desempenho dessas t´ecnicas na literatura. 

O primeiro modelo, UDPipe 2 [Straka 2018], foi avaliado com o tamanho de lotes ( _batch size_ ) de 128 amostras, com um treinamento de 16 ´epocas, onde, nas primeiras 8 ´epocas, ´e utilizada a taxa de aprendizagem de 10<sup>_−_3</sup> , e de 10<sup>_−_4</sup> nas demais. Como modelo de l´ıngua, foi utilizado o BERTimbau [Souza et al. 2020]. 

O Stanza [Qi et al. 2020] possui um m´odulo de etiquetagem morfossint´atica que utiliza redes Bi-LSTM para a classificac¸˜ao. Para este modelo, foi utilizado o tamanho em lotes padr˜ao de 5 _._ 000, taxa de aprendizagem de 10<sup>_−_3</sup> e n´umero m´aximo de atualizac¸˜oes de etapas de gradiente de 1 _._ 000. 

1https://sites.google.com/icmc.usp.br/poetisa 

O terceiro modelo, Meta-BiLSTM [Bohnet et al. 2018], foi treinado com o tamanho de lotes de 40 _._ 000 para o modelo em n´ıvel de palavras e 80 _._ 000 para o modelo em n´ıvel de caracteres. A taxa de aprendizagem ´e de 2 _×_ 10<sup>_−_3</sup> , com 3 camadas ocultas com 400 neurˆonios cada. O modelo utiliza representac¸˜oes est´aticas em n´ıvel de palavra, obtidas do Skip-gram do Word2Vec com dimens˜ao 300 [Hartmann et al. 2017]. 

Outra t´ecnica foi a CNCSR [Heinzerling e Strube 2019], que se baseia no uso de representac¸˜oes vetoriais em n´ıvel de palavra e caractere com rede Bi-LSTM. Foram utilizadas as representac¸˜oes em n´ıvel de caractere e subpalavra, sendo elas combinadas por meio de uma rede RNR meta. O modelo foi treinado com tamanho de lotes de 64, n´umero de ´epocas m´ınimo de 50 e m´aximo de 1.000, taxa de aprendizagem de 10<sup>_−_4</sup> , tamanho de vocabul´ario de 100 _._ 000 e taxa de _dropout_ de 0 _,_ 2. O modelo em n´ıvel de caractere possui representac¸˜ao vetorial de tamanho 50 e camada oculta com 256 neurˆonios; os modelos de subpalavra e meta possuem o mesmo n´umero de neurˆonios na camada oculta. 

Al´em destes modelos, foram realizados experimentos com trˆes diferentes modelos de l´ıngua em conjunto com etapas de ajuste fino. Dessa forma, s˜ao utilizadas as representac¸˜oes da primeira subpalavra de cada _token_ da sentenc¸a de entrada para detectar a classe gramatical. Foram utilizados os modelos de l´ıngua BERTimbau [Souza et al. 2020], DeBERTa-v3 [He et al. 2021] e XLM-R [Conneau et al. 2020]. Para os trˆes modelos, foram utilizados os seguintes hiper-parˆametros: m´aximo de 30 ´epocas, taxa de aprendizagem de 2 _×_ 10<sup>_−_5</sup> e _weight decay rate_ de 0 _,_ 01, que ´e um parˆametro do otimizador AdamW [Loshchilov e Hutter 2019]. Os modelos BERTimbau e XLM-R utilizaram tamanho de lotes de 32 e, para o DeBERTa-v3, foi utilizado tamanho 16. 

O procedimento experimental conta com a realizac¸˜ao de 10 execuc¸˜oes<sup>2</sup> de treinamento no conjunto de treino do corpus Porttinari-base, para, ent˜ao, realizar a comparac¸˜ao entre os modelos e realizac¸˜ao de testes de hip´otese para identificar diferenc¸as estatisticamente significativas na acur´acia. O teste Anova [Fisher 1992] com _post hoc_ de Tukey [Tukey 1949] foi selecionado para realizar esta avaliac¸˜ao. O teste Anova avalia se existem diferenc¸as significativas entre as m´edias de dois ou mais grupos. Se identificada tal diferenc¸a, o teste de Tukey ´e aplicado para determinar quais os grupos que possuem m´edias significativamente distintas entre si, com correc¸˜ao para m´ultiplas testagens. 

### **4.2. Resultados** 

A Tabela 3 apresenta os resultados da avaliac¸˜ao da etiquetagem morfossint´atica no corpus jornal´ıstico. S˜ao apresentadas a acur´acia m´edia e a Medida-F Macro m´edia das 10 execuc¸˜oes de experimentos para cada abordagem avaliada, al´em dos respectivos desvios padr˜oes. E poss´ıvel observar que os m´etodos baseados em RNRs possuem desempenho<sup>´</sup> inferior aos m´etodos baseados em modelos de l´ıngua com ajuste fino, tanto em termos de acur´acia quanto em Medida-F macro. Al´em disso, a abordagem com o BERTimbau possui o maior valor absoluto m´edio para acur´acia e Medida-F Macro. Os modelos DeBERTa-v3 e XLM-R possuem valores pr´oximos. As diferenc¸as observadas com relac¸˜ao `a acur´acia foram significativas (Anova _Z_ (70 _,_ 69) _≈_ 890 _, p_ = 6 _e −_ 59), com n´ıvel de confianc¸a de 95%). Em an´alise par-a-par, as diferenc¸as observadas foram significativas para todos os pares, exceto para BERTimbau _×_ DeBERTa-v3 e XLM-R _×_ DeBERTa-v3. 

> 2Cada experimento utilizou o mesmo conjunto de treinamento, com variac¸˜ao na semente aleat´oria que ´e utilizada na inicializac¸˜ao dos pesos do modelo. 

**Tabela 3. Acur´acia no corpus jornal´ıstico Porttinari-base** 

|Modelo|Abordagem|Acur´acia m´edia (%)|Medida-F macro m´edia (%)|
|---|---|---|---|
|BERTimbau|Modelo de l´ıngua|**99,07**_±_**0,03**|**96,39**_±_**0,32**|
|DeBERTa-v3|Modelo de l´ıngua|99_,_02_±_0_,_05|95_,_81_±_0_,_39|
|XLM-R|Modelo de l´ıngua|99_,_00_±_0_,_04|96_,_36_±_0_,_42|
|Meta-BiLSTM|RNR|98_,_47_±_0_,_06|94_,_89_±_0_,_28|
|Udpipe 2|RNR|98_,_01_±_0_,_03|93_,_13_±_0_,_54|
|Stanza|RNR|98_,_22_±_0_,_05|94_,_60_±_0_,_27|
|CNCSR|RNR|98_,_10_±_0_,_07|94_,_04_±_0_,_30|



Dado que n˜ao foi observada diferenc¸a significativa entre os m´etodos baseados nos modelos BERTimbau e DeBERTa-v3, o m´etodo baseado no BERTimbau foi selecionado para a pr´oxima etapa de experimentac¸˜ao, devido a seu menor n´umero de parˆametros. O m´etodo foi avaliado nos trˆes corpora de gˆeneros diferentes (jornal´ıstico, acadˆemico e UGC), em que o experimento ´e constitu´ıdo pelo treinamento do modelo em cada cen´ario de combinac¸˜ao dos corpora, seguido de sua avaliac¸˜ao separada em cada corpus individual. A Tabela 4 exibe a acur´acia m´edia dos experimentos nos conjuntos de teste. 

**Tabela 4. Acur´acia no contexto multigˆenero** 

||A|cur´acia m´edia(%)||
|---|---|---|---|
|Corpora de treinamento|Porttinari-base|DANTEStocks|PetroGold|
|Porttinari-base|**99,07**_±_**0,03**|87,14_±_0,60|96,46_±_0,17|
|DANTEStocks|96,55_±_0,23|**97,98**_±_**0,08**|94,95_±_0,20|
|PetroGold|96,99_±_0,10|84,96_±_0,46|**98,93**_±_**0,06**|
|Porttinari-base + DANTEStocks|99,05_±_0,04|97,91_±_0,10|96,58_±_0,16|
|Porttinari-base + PetroGold|98,95_±_0,06|85,29_±_0,34|98,85_±_0,07|
|DANTEStocks + PetroGold|97,86_±_0,06|97,99_±_0,07|98,92_±_0,05|
|Port.-base + DANTEStocks + PetroGold|**99,00**_±_**0,05**|**97,92**_±_**0,13**|**98,89**_±_**0,06**|



´E poss´ıvel observar que o cen´ario que obteve a maior acur´acia m´edia foi o cen´ario onde o modelo foi treinado apenas com dados do gˆenero alvo. Por exemplo, o melhor cen´ario para o corpus de gˆenero acadˆemico foi o cen´ario em que o treinamento foi exclusivamente neste gˆenero. Contudo, estes modelos possuem acur´acias mais baixas nos outros gˆeneros, por exemplo, o modelo treinado no corpus PetroGold com acur´acia de 98 _,_ 93% no gˆenero acadˆemico possui acur´acia de 84 _,_ 96% no gˆenero UGC. 

Tamb´em se pode notar maior discrepˆancia entre os gˆeneros que seguem a norma culta da l´ıngua e o gˆenero UGC, que possui caracter´ısticas lingu´ısticas diferentes. Quando o cen´ario com o PetroGold ´e avaliado no gˆenero jornal´ıstico, por exemplo, ´e poss´ıvel observar uma acur´acia de 96 _,_ 99% (ou seja, h´a uma diferenc¸a relativamente pequena em relac¸˜ao ao melhor resultado para esse gˆenero). J´a no gˆenero UGC, observa-se uma diferenc¸a maior em relac¸˜ao ao melhor modelo treinado no corpus DANTEStocks. 

Em relac¸˜ao ao treinamento multigˆenero, ´e poss´ıvel observar que o modelo treinado em todos os gˆeneros (´ultima linha da tabela) alcanc¸ou desempenho similar aos modelos treinados isoladamente, sendo que a diferenc¸a entre as m´edias possui valor m´aximo de 0 _,_ 067. Como esperado, essa diferenc¸a n˜ao foi estatisticamente significativa<sup>3</sup> . 

> 3Anova _Z_ (70 _,_ 69) _≈_ 1107 _, p_ = 7 _e −_ 62). Tukey: Multigˆenero vs Porttinari-base _Z ≈_ 0 _,_ 7 _e −_ 4 _, p ≈_ 

Al´em da acur´acia em n´ıvel de _tokens_ , tamb´em foi calculada e acur´acia em n´ıvel de sentenc¸a nos corpora, computando-se a porcentagem de sentenc¸as que foram anotadas de forma completamente correta, obtendo-se os seguintes resultados m´edios nos corpora: Porttinari-base – 64 _,_ 59%; DANTEStocks – 54 _,_ 25%; PetroGold – 47 _,_ 36%; Porttinaribase + DANTEStocks – 68 _,_ 31%; Porttinari-base + PetroGold – 55 _,_ 01%; DANTEStocks + PetroGold – 72 _,_ 79%; Porttinari-base + DANTEStocks + PetroGold – 77 _,_ 70%. Novamente, o cen´ario multigˆenero destaca-se. Aprofundando o estudo, na an´alise das sentenc¸as com erros no cen´ario multigˆenero, ´e poss´ıvel observar que: em 77% das sentenc¸as, houve apenas 1 erro; em 18%, dois erros; em 4%, 3 ou 4 erros; o restante ( _<_ 1%) tem 5 ou mais erros (que incluem casos de sentenc¸as de estrutura incomum). Os resultados indicam um novo estado da arte para a l´ıngua portuguesa, al´em de demonstrarem que ´e poss´ıvel ter um sistema multigˆenero robusto que possibilite o desenvolvimento de aplicac¸˜oes de PLN mais generalistas e que possam ser aplicados para textos variados. 

Ap´os a avaliac¸˜ao quantitativa, partiu-se para a avaliac¸˜ao qualitativa, essencial para entender a potencialidade real desse tipo de sistema e suas limitac¸˜oes. Partindo do modelo treinado no contexto multigˆenero, foi realizada a an´alise manual de erros (com o apoio de um linguista experiente), buscando-se encontrar erros ocorridos para cada etiqueta morfossint´atica. Aqui s˜ao reportados apenas os erros sistem´aticas observados. 

Com relac¸˜ao `a etiqueta ADJ, no corpus Porttinari-base, foram encontrados 23 casos onde os _tokens_ estavam na forma de partic´ıpio. Partic´ıpio ´e uma forma nominal do verbo e pode assumir as etiquetas ADJ, NOUN ou VERB, sendo um caso particularmente desafiador para a Lingu´ıstica [Duran 2021]. Naturalmente, o mesmo tipo de erro ´e encontrado ao analisar os erros das etiquetas NOUN e VERB. Nos corpora DANTEStocks e PetroGold, foram encontradas 4 ocorrˆencias em ambas as an´alises. 

Para a etiqueta PROPN, ´e poss´ıvel identificar casos em que o modelo classificou como NOUN, consistindo em outra dificuldade conhecida da ´area. No corpus Porttinaribase, foram 10 ocorrˆencias; no DANTEStocks, 21; e 8 ocorrˆencias no PetroGold. Em especial, no DANTEStocks, foi observado que alguns _tweets_ continham ´ındices da bolsa de valores sendo classificados com a etiqueta X. No total, foram encontradas 30 ocorrˆencias desse tipo. Esse corpus adotou a etiqueta X para ´ındices da bolsa que n˜ao possu´ıam func¸˜ao lingu´ıstica no _tweet_ e, quando possu´ıam func¸˜ao, a etiqueta PROPN deveria ser utilizada. 

Finaliza-se com a etiqueta X, utilizada para casos a que outras etiquetas n˜ao podem ser associadas. No corpus Porttinari-base, todos os erros encontrados foram casos de estrangeirismos a que o modelo tentou associar uma classe gramatical diferente da etiqueta X. Este tipo de erro foi encontrado em 11 casos no corpus DANTEStocks e n˜ao ocorreu no corpus PetroGold. Esse ´e um erro considerado plaus´ıvel, j´a que estrangeirismos poderiam ter outras etiquetas associados a eles. 

´E interessante observar que, caso esses erros relatados fossem computados como an´alises plaus´ıveis no c´alculo da acur´acia, a acur´acia geral do melhor modelo de etiquetagem se aproximaria dos 100%. Esses casos tamb´em podem servir de base para futuras discuss˜oes e eventuais aprimoramentos nos corpora anotados. 

> 0 _,_ 77, Multigˆenero vs DANTEStocks _Z ≈_ 0 _,_ 7 _e−_ 4 _, p ≈_ 0 _,_ 99, Multigˆenero vs PetroGold _Z ≈_ 0 _,_ 4 _e−_ 4 _, p ≈_ 

> 0 _,_ 99 ao n´ıvel de confianc¸a de 95%. 

## **5. Experimentos adicionais: o corpus Mac-Morpho** 

Dada a relevˆancia hist´orica do corpus Mac-Morpho [Alu´ısio et al. 2003] para a tarefa de etiquetagem morfossint´atica para o portuguˆes, testamos nesse corpus a melhor t´ecnica de etiquetagem observada no experimento anterior. O Mac-Morpho cont´em cerca de 1 milh˜ao de palavras em portuguˆes brasileiro, criado a partir de textos de jornais e revistas. A vers˜ao atual, Mac-Morpho v2 [Fonseca e Rosa 2013], conta com 23 etiquetas morfossint´aticas de base e 7 complementares. Sendo assim, o conjunto de etiquetas ´e distinto do conjunto da UD. A contribuic¸˜ao desses experimentos adicionais reside, portanto, na avaliac¸˜ao da robustez da melhor t´ecnica identificada em dados com um _tagset_ diferente. 

A Tabela 5 exibe as acur´acias obtidas por trabalhos pr´evios da literatura e pelo etiquetador deste artigo baseado no modelo BERTimbau. E poss´ıvel observar que o eti-<sup>´</sup> quetador deste trabalho obteve a maior acur´acia, demonstrando sua robustez e avanc¸ando o estado da arte de etiquetagem para o corpus Mac-Morpho tamb´em. 

**Tabela 5. Acur´acia para o corpus Mac-Morpho** 

|M´etodo|[Fonseca e Rosa 2013]|[de Sousa e Lopes 2019]|[Fonseca et al. 2015]|[Santos e Zadrozny2014]|BERTimbau|
|---|---|---|---|---|---|
|Acur´acia|96,48%|97,62%|97,31%|97,47%|**98,36%**|



## **6. Considerac¸˜oes finais** 

Este trabalho avanc¸ou a fronteira do conhecimento e o estado da arte ao demonstrar a potencialidade multigˆenero de um m´etodo de etiquetagem morfossint´atica baseado em modelagem de l´ıngua e ao produzir resultados superiores ao estado da arte. 

O melhor m´etodo observado, baseado no modelo BERTimbau, demonstrou uma boa capacidade de generalizac¸˜ao nos gˆeneros abordados, mas pode ser interessante no futuro avali´a-lo ainda em outros gˆeneros e dom´ınios a fim de confirmar tal robustez. Outro fator importante a ser considerado ´e o custo computacional desse etiquetador. Possuindo cerca de 110 milh˜oes de parˆametros e complexidade quadr´atica no mecanismo de autoatenc¸˜ao, o tempo de inferˆencia ´e consider´avel. Pode ser interessante explorar t´ecnicas de compress˜ao de modelos para reduzir o tamanho e tempo de inferˆencia. 

Para reproduc¸˜ao dos resultados apresentados, o reposit´orio<sup>4</sup> de c´odigo ´e disponibilizado. Al´em disso, uma aplicac¸˜ao<sup>5</sup> foi criada para que interessados possam utilizar o melhor etiquetador desenvolvido (no cen´ario multigˆenero ou n˜ao). Outras informac¸˜oes sobre este trabalho e sobre iniciativas relacionadas podem ser encontradas no portal web do projeto POeTiSA<sup>6</sup> . 

## **Agradecimentos** 

Este trabalho foi realizado no ˆambito do Centro de Inteligˆencia Artificial da Universidade de S˜ao Paulo (C4AI - http://c4ai.inova.usp.br/), com o apoio da Fundac¸˜ao de Amparo `a Pesquisa do Estado de S˜ao Paulo (processo FAPESP #2019/07665-4) e da IBM. Este projeto tamb´em foi apoiado pelo Minist´erio da Ciˆencia, Tecnologia e Inovac¸˜oes, com recursos da Lei N. 8.248, de 23 de outubro de 1991, no ˆambito do PPI-Softex, coordenado pela Softex e publicado como Residˆencia em TIC 13, DOU 01245.010222/2022-44. 

> 4https://github.com/huberemanuel/porttagger 

> 5https://huggingface.co/spaces/Emanuel/porttagger 

> 6https://sites.google.com/icmc.usp.br/poetisa/ 

## **Referˆencias** 

- Afonso, S., Bick, E., Haber, R., e Santos, D. (2002). Floresta sint´a(c)tica: A treebank for Portuguese. In _Proceedings of the Third International Conference on Language Resources and Evaluation_ , pages 1698–1703, Las Palmas, Spain. 

- Alu´ısio, S., Pelizzoni, J., Marchi, A. R., de Oliveira, L., Manenti, R., e Marquiaf´avel, V. (2003). An account of the challenge of tagging a reference corpus for brazilian portuguese. In _6th international conference on Computational processing of the Portuguese language_ , page 110–117, Faro, Portugal. 

- Bick, E. (2000). _The Parsing System “Palavras”. Automatic Grammatical Analysis of Portuguese in a Constraint Grammar Framework_ . University of Arhus. 

- Bohnet, B., McDonald, R., Sim˜oes, G., Andor, D., Pitler, E., e Maynez, J. (2018). Morphosyntactic tagging with a meta-BiLSTM model over context sensitive token encodings. In _Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics_ , pages 2642–2652, Melbourne, Australia. 

- Branco, A. e Silva, J. (2004). Evaluating solutions for the rapid development of stateof-the-art POS taggers for Portuguese. In _Proceedings of the Fourth International Conference on Language Resources and Evaluation_ , pages 507–510, Lisbon, Portugal. 

- Branco, A., Silva, J. R., Gomes, L., e Ant´onio Rodrigues, J. (2022). Universal grammatical dependencies for Portuguese with CINTIL data, LX processing and CLARIN support. In _Proceedings of the Thirteenth Language Resources and Evaluation Conference_ , pages 5617–5626, Marseille, France. 

- Cabral, B., Souza, M., e Claro, D. B. (2022). Portnoie: A neural framework for open information extraction for the portuguese language. In _Computational Processing of the Portuguese Language: 15th International Conference_ , page 243–255, Berlin, Heidelberg. 

- Conneau, A., Khandelwal, K., Goyal, N., Chaudhary, V., Wenzek, G., Guzm´an, F., Grave, E., Ott, M., Zettlemoyer, L., e Stoyanov, V. (2020). Unsupervised cross-lingual representation learning at scale. In _Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics_ , pages 8440–8451, Online. 

- de Marneffe, M.-C., Manning, C. D., Nivre, J., e Zeman, D. (2021). Universal Dependencies. _Computational Linguistics_ , 47:255–308. 

- de Sousa, R. C. C. e Lopes, H. (2019). Portuguese pos tagging using blstm without handcrafted features. In Nystr¨om, I., Hern´andez Heredia, Y., e Mili´an N´u˜nez, V., editors, _Progress in Pattern Recognition, Image Analysis, Computer Vision, and Applications_ , pages 120–130, Havana, Cuba. 

- Di Felippo, A., Postali, C., Ceregatto, G., Gazana, L., Silva, E., Roman, N., e Pardo, T. (2021). Descric¸˜ao preliminar do corpus dantestocks: Diretrizes de segmentac¸˜ao para anotac¸˜ao segundo universal dependencies. In _Anais do XIII Simp´osio Brasileiro de Tecnologia da Informac¸˜ao e da Linguagem Humana_ , pages 335–343, Porto Alegre, RS, Brasil. 

- Domingues, M. L. C. S. (2011). _Abordagem para o desenvolvimento de um etiquetador de alta acur´acia para o Portuguˆes do Brasil_ . PhD thesis, Universidade Federal do Par´a, Bel´em, PA, Brasil. 

- Duran, M. S. (2021). Manual de anotac¸˜ao de PoS tags: Orientac¸˜oes para anotac¸˜ao de etiquetas morfossint´aticas em l´ıngua portuguesa, seguindo as diretrizes da abordagem universal dependencies (UD). Technical report, Instituto de Ciˆencias Matem´aticas e de Computac¸˜ao da Universidade de S˜ao Paulo, S˜ao Carlos, Brasil. 

- Fisher, R. A. (1992). _Statistical Methods for Research Workers_ . Springer New York. 

- Fonseca, E. R., G Rosa, J. L., e Alu´ısio, S. M. (2015). Evaluating word embeddings and a revised corpus for part-of-speech tagging in portuguese. _Journal of the Brazilian Computer Society_ , 21:1–7. 

- Fonseca, E. R. e Rosa, J. L. G. (2013). Mac-morpho revisited: Towards robust part-ofspeech tagging. In _Proceedings of the 9th Brazilian Symposium in Information and Human Language Technology_ , pages 1–10, Fortaleza, Brasil. 

- Garimella, A., Banea, C., Hovy, D., e Mihalcea, R. (2019). Women’s syntactic resilience and men’s grammatical luck: Gender-bias in part-of-speech tagging and dependency parsing. In _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ , pages 3493–3498, Florence, Italy. 

- Hartmann, N. S., Fonseca, E. R., Shulby, C. D., Treviso, M. V., Rodrigues, J. S., e Alu´ısio, S. M. (2017). Portuguese word embeddings: Evaluating on word analogies and natural language tasks. In _Anais do XI Simp´osio Brasileiro de Tecnologia da Informac¸˜ao e da Linguagem Humana_ , pages 122–131, Porto Alegre, Brasil. 

- He, P., Gao, J., e Chen, W. (2021). Debertav3: Improving deberta using electra-style pretraining with gradient-disentangled embedding sharing. _CoRR_ , abs/2111.09543:1–19. 

- Heinzerling, B. e Strube, M. (2019). Sequence tagging with contextual and noncontextual subword representations: A multilingual evaluation. In _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ , pages 273–291, Florence, Italy. 

- Jurafsky, D. e Martin, J. H. (2009). _Speech and language processing : an introduction to natural language processing, computational linguistics, and speech recognition_ . Pearson Prentice Hall. 

- Lin, Y., Wang, C., Song, H., e Li, Y. (2021). Multi-head self-attention transformation networks for aspect-based sentiment analysis. _IEEE Access_ , 9:8762–8770. 

- Lopes, L., Duran, M., Fernandes, P., e Pardo, T. (2022). PortiLexicon-UD: a Portuguese lexical resource according to Universal Dependencies model. In _Proceedings of the Thirteenth Language Resources and Evaluation Conference_ , pages 6635–6643, Marseille, France. 

- Loshchilov, I. e Hutter, F. (2019). Decoupled weight decay regularization. In _7th International Conference on Learning Representations_ , pages 1–19, Toulon, France. 

- Pardo, T., Duran, M., Lopes, L., Felippo, A. D., Roman, N., e Nunes, M. (2021). Porttinari - a large multi-genre treebank for brazilian portuguese. In _Anais do XIII Simp´osio Brasileiro de Tecnologia da Informac¸˜ao e da Linguagem Humana_ , pages 1–10, Porto Alegre, Brasil. 

- Qi, P., Zhang, Y., Zhang, Y., Bolton, J., e Manning, C. D. (2020). Stanza: A Python natural language processing toolkit for many human languages. In _Proceedings of_ 

_the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations_ , pages 101–108, Online. 

- Rademaker, A., Chalub, F., Real, L., Freitas, C., Bick, E., e de Paiva, V. (2017). Universal Dependencies for Portuguese. In _Proceedings of the Fourth International Conference on Dependency Linguistics_ , pages 197–206, Pisa,Italy. 

- Santos, C. D. e Zadrozny, B. (2014). Learning character-level representations for partof-speech tagging. In _Proceedings of the 31st International Conference on Machine Learning_ , pages 1818–1826, Bejing, China. 

- Souza, E., Silveira, A., Cavalcanti, T., Castro, M., e Freitas, C. (2021). Petrogold – corpus padr˜ao ouro para o dom´ınio do petr´oleo. In _Anais do XIII Simp´osio Brasileiro de Tecnologia da Informac¸˜ao e da Linguagem Humana_ , pages 29–38, Porto Alegre, Brasil. 

- Souza, F., Nogueira, R., e Lotufo, R. (2020). Bertimbau: Pretrained bert models for brazilian portuguese. In _Intelligent Systems_ , pages 403–417, Cham. 

- Straka, M. (2018). UDPipe 2.0 prototype at CoNLL 2018 UD shared task. In _Proceedings of the CoNLL 2018 Shared Task: Multilingual Parsing from Raw Text to Universal Dependencies_ , pages 197–207, Brussels, Belgium. 

- Tukey, J. W. (1949). Comparing individual means in the analysis of variance. _Biometrics_ , 5:99–114. 

- Zeman, D., Popel, M., Straka, M., Hajic, J., Nivre, J., Ginter, F., Luotolahti, J., Pyysalo, S., Petrov, S., Potthast, M., Tyers, F., Badmaeva, E., Gokirmak, M., Nedoluzhko, A., Cinkova, S., Hajic jr., J., Hlavacova, J., Kettnerov´a, V., Uresova, Z., Kanerva, J., Ojala, S., Missil¨a, A., Manning, C. D., Schuster, S., Reddy, S., Taji, D., Habash, N., Leung, H., de Marneffe, M.-C., Sanguinetti, M., Simi, M., Kanayama, H., dePaiva, V., Droganova, K., Mart´ınez Alonso, H., C¸ ¨oltekin, c., Sulubacak, U., Uszkoreit, H., Macketanz, V., Burchardt, A., Harris, K., Marheinecke, K., Rehm, G., Kayadelen, T., Attia, M., Elkahky, A., Yu, Z., Pitler, E., Lertpradit, S., Mandl, M., Kirchner, J., Alcalde, H. F., Strnadov´a, J., Banerjee, E., Manurung, R., Stella, A., Shimada, A., Kwak, S., Mendonca, G., Lando, T., Nitisaroj, R., e Li, J. (2017). Conll 2017 shared task: Multilingual parsing from raw text to universal dependencies. In _Proceedings of the CoNLL 2017 Shared Task: Multilingual Parsing from Raw Text to Universal Dependencies_ , pages 1–19, Vancouver, Canada. 

- Zhao, F., Quan, B., Yang, J., Chen, J., Zhang, Y., e Wang, X. (2019). Document summarization using word and part-of-speech based on attention mechanism. _Journal of Physics: Conference Series_ , 1168:32008. 



---
title: Reconhecimento de entidades nomeadas para o português usando o OpenNLP
citekey: Chiele2015
authors:
- Gabriel Chiele
- Evandro Brasil Fonseca
- Aline Vanim
- Renata Vieira
year: 2015
date: '2015'
item_type: journalArticle
doi: ''
url: https://repositorio.pucrs.br/dspace/handle/10923/14040
zotero_key: 5SDM28AZ
collections:
- SA9KZ2CI
tags:
- ⛔ No DOI found
- /unread
- 'MetadataHunter: No DOI'
abstract: ''
source: zotero
tipo: academic_paper
parsed_with: pymupdf4llm
original_file: reconhecimento de entidades nomeadas para o português usando o opennlp.pdf
synced_at: '2026-09-29T18:30:02.314806'
---

# Reconhecimento de entidades nomeadas para o português usando o OpenNLP

**Autores:** Gabriel Chiele, Evandro Brasil Fonseca, Aline Vanim, Renata Vieira
**URL:** https://repositorio.pucrs.br/dspace/handle/10923/14040

## 📄 Conteúdo Completo do Documento

# **Reconhecimento de Entidades Nomeadas para o Portuguˆes Usando o OpenNLP** 

Evandro B. Fonseca, Gabriel C. Chiele, Renata Vieira _Faculdade de Inform´atica PUCRS Porto Alegre, Brazil Email: evandro.fonseca, gabriel.chiele{@acad.pucrs.br}, renata.vieira@pucrs.br_ 

Aline A. Vanin _Dep. de Educac¸˜ao e Humanidades UFCSPA Porto Alegre, Brazil Email: aline.vanin@ymail.com_ 

**_Abstract_ —** **_In this paper, we present the construction process for a named entity recognition model using NameFinder, an OpenNLP class. The aim is to recognize and classify named entities for Portuguese, since there is a lack of a model for Portuguese in OpenNLP. To train and evaluate the model, the Amazˆonia and HAREM corpora were used. We show that the resulting OpenNLP model is compatible when compared with the current state of the art._** 

**Resumo––Neste artigo apresentamos a construc¸˜ao de um modelo para o reconhecimento de entidades nomeadas utilizando o NameFinder, classe contida no OpenNLP. Nosso objetivo ´e reconhecer e classificar entidades nomeadas para o Portuguˆes, dada a inexistˆencia de um modelo para l´ıngua portuguesa no OpenNLP. Para treinar e avaliar o modelo, foram utilizados, respectivamente, os corpora Amazonas e Harem. Mostramos que nossos resultados s˜ao compat´ıveis com o atual estado da arte.** 

**_Keywords_ -** **_Named Entities Recognition; Portuguese Language; Natural Language Processing; Machine Learning_ .** 

## I. INTRODUC¸ ˜AO 

O reconhecimento de entidades nomeadas _(NER)_ – _Named Entity Recognition_ – ´e uma sub´area de estudo no campo de extrac¸˜ao de informac¸˜ao, cujo objetivo ´e identificar entidades nomeadas, bem como classific´a-las dentro de um conjunto de categorias pr´e-definidas, tais como Pessoa, Organizac¸˜ao, Local, as quais remetem a um referente espec´ıfico. Dentro desse contexto, esta tarefa tem sido amplamente estudada [1]. 

O reconhecimento de entidades nomeadas ´e uma t´ecnica amplamente utilizada em Processamento da Linguagem Natural e consiste na identificac¸˜ao de nomes de entidadeschave, presentes na forma livre de dados textuais. Nesse sentido, a entrada para um sistema de extrac¸˜ao de entidades nomeadas ´e um texto em sua forma livre, e sua sa´ıda ´e um conjunto de textos anotados, ou seja, uma representac¸˜ao estruturada a partir da entrada de um texto n˜ao estruturado, como podemos ver em **(a)** : 

**a)** “Jos´e da Silva reside em Florian´opolis e estuda na 

UFSC (Universidade Federal de Santa Catarina)”. 

Efetuando a extrac¸˜ao das entidades nomeadas do exemplo **(a)** , temos: [Jos´e da Silva], [Florian´opolis], [UFSC] e [Universidade Federal de Santa Catarina], respectivamente, entidades cujas categorias s˜ao: Pessoa, Local, Organizac¸˜ao e Organizac¸˜ao. 

Reconhecer e aferir categorias a entidades nomeadas presentes em um texto n˜ao ´e uma tarefa f´acil. Isso porque, quando o assunto s˜ao nomes pr´oprios e entidades, estes podem remeter a mais de uma categoria **(b)** , ou simplesmente n˜ao possuir um contexto mais determin´ıstico, que auxilie na desambiguac¸˜ao **(c)** : 

**b)** “A Mercedes esteve em crise nos ´ultimos meses. A empresa afirma que...”. 

**c)** “Hoje foi um ´otimo dia para Mercedes.” 

Para o exemplo **(b)** , o contexto poderia auxiliar na desambiguac¸˜ao. Isto ´e, havendo uma relac¸˜ao entre os sintagmas [A Mercedes] e [A empresa], podemos aferir a categoria “Organizac¸˜ao” `a entidade “Mercedes”, pois o sintagma nominal [a empresa] identifica uma organizac¸˜ao. 

Da mesma forma que o contexto pode auxiliar no reconhecimento de entidades nomeadas, a tarefa de NER pode acrescentar melhorias `a interpretao textual, por exemplo. Coreixas [2] mostrou que o uso de categorias de entidades pode proporcionar uma melhora significativa na tarefa na resoluc¸˜ao de correferˆencias. Em **(c)** , temos uma situac¸˜ao mais complexa. Note que apenas a informac¸˜ao contida na orac¸˜ao n˜ao ´e suficiente para aferir uma categoria `a entidade nomeada. N˜ao sabemos se “Mercedes” ´e uma empresa que obteve ˆexito em seus neg´ocios, ou se ´e uma pessoa que teve um ´otimo dia. 

Neste trabalho, apresentamos um novo classificador de entidades nomeadas para o Portuguˆes, utilizando como base o NameFinder, uma classe contida no OpenNLP [3], cujo 

objetivo ´e identificar e classificar entidades nomeadas. At´e o momento, o OpenNLP possu´ıa modelos de NER para diversas l´ınguas, como a espanhola, a inglesa, entre outras, mas nenhum havia sido desenvolvido para o portuguˆes. A vantagem de utilizarmos o OpenNLP para essa tarefa ´e que, com isso, podemos obter um recurso mais completo, que fornec¸a diversos tipos de anotac¸˜ao em uma ´unica ferramenta. De forma a avaliar o modelo gerado, utilizamos o corpus do HAREM [4], juntamente com alguns sistemas de _NER_ j´a existentes, dispon´ıveis para o Portuguˆes. 

A estrutura do texto est´a disposta da seguinte forma: na presente sec¸˜ao, foi dada uma breve introduc¸˜ao sobre o t´opico em estudo; na sec¸˜ao II, s˜ao relatados os principais recursos de _NER_ , dispon´ıveis para o Portuguˆes, juntamente com o OpenNLP, um recurso de PLN escrito em JAVA, utilizado neste trabalho; na sec¸˜ao III, apresentamos os dois principais corpora, utilizados para treino e teste de nosso modelo; na sec¸˜ao IV, descrevemos a metodologia empregada na construc¸˜ao de nosso modelo; na sec¸˜ao V, s˜ao exibidos os resultados provenientes da avaliac¸˜ao, juntamente com resultados comparativos, remetentes ao atual estado da arte; e, por fim, na sec¸˜ao VI, s˜ao apresentadas as conclus˜oes e os pr´oximos trabalhos que dar˜ao continuidade a este estudo. 

## II. SISTEMAS DE NER 

Atualmente, existe uma quantidade razo´avel de recursos de _NER_ , dispon´ıveis para a l´ıngua portuguesa . Nesta Sec¸˜ao, descrevemos os principais deles, juntamente com o OpenNLP, recurso utilizado para gerar nosso classificador. 

**NERP-CRF:** Desenvolvido em Python, sob licenc¸a opensource e utilizando aprendizagem de m´aquina, o NERP-CRF [1] ´e um recurso de _NER_ para a l´ıngua portuguesa, que reconhece e classifica 10 categorias de entidades nomeadas (Pessoa, Local, Organizac¸˜ao, Obra, Abstrac¸˜ao, Tempo, Coisa, Outro, Valor, Acontecimento). Como seu pr´oprio nome sugere, a ferramenta utiliza o algoritmo CRF e foi treinada por meio do corpus do HAREM [4]. 

**LanguageTasks:** LanguageTasks, tamb´em conhecido como Ltasks<sup>1</sup> , ´e um recurso de _NER_ , livre para fins acadˆemicos e pago para fins comerciais. Sua proposta principal ´e o reconhecimento e classificac¸˜ao de entidades nomeadas por meio de um ambiente web. O Ltasks conta tamb´em com uma _API_ , desenvolvida em Java, objetivando dinamizar o processo, dessa forma o usu´ario acaba tendo maior flexibilidade para automatizar o processo. No entanto, como se trata de um recurso propriet´ario, livre apenas para uso acadˆemico, em sua forma gratuita o n´umero de acessos di´arios restringe-se a 1000, havendo a necessidade de que o usu´ario cadastre-se no website da ferramenta. 

**FreeLing:** O FreeLing [5] ´e uma ferramenta de _NER_ , contida na FreeLing _package_ , cujo objetivo ´e prover recursos de PLN para o Portuguˆes. No entanto, este _toolkit_ possui recursos e funcionalidades para outros idiomas tamb´em, como o Espanhol e Inglˆes. O FreeLing ´e uma ferramenta _open-source_ , escrita na linguagem C++. Outro aspecto interessante desse recurso ´e a existˆencia de dois m´etodos para o reconhecimento de entidades nomeadas: o primeiro utiliza um modo mais simples, baseado em padr˜oes morfo-sint´aticos; j´a seu segundo m´etodo utiliza um meio mais sofisticado, envolvendo t´ecnicas de aprendizado de m´aquina. 

**Palavras:** Desenvolvido por Bick [6], o PALAVRAS ´e um parser para a l´ıngua portuguesa que possui uma s´erie de recursos, tais como _POS-tagging_ , anotac¸˜ao semˆantica, sint´atica, entre outras. Embora seu c´odigo seja fechado, sabe-se que este foi escrito utilizando as l´ınguagens Python e Pearl. O software ´e baseado em um l´exico contendo 50.000 lemmas e diversas regras gramaticais da l´ıngua portuguesa. Apesar de ser um recurso propriet´ario, o PALAVRAS ´e um _toolkit_ bastante utilizado e reconhecido pelo meio acadˆemico. 

**OpenNLP:** O Apache OpenNLP ´e uma biblioteca Java baseada em aprendizado de m´aquina para o processamento de linguagem natural em texto. Suporta tarefas como tokenizac¸˜ao, segmentac¸˜ao de sentenc¸a, etiquetagem morfosint´atica, extrac¸˜ao de sintagmas, an´alise sint´atica, resoluc¸˜ao de correferˆencias e reconhecimento de entidades nomeadas. Embora o OpenNLP seja um recurso muito vers´atil, com modelos<sup>2</sup> dispon´ıveis para diversos idiomas, at´e o momento n˜ao existia um reconhecedor de entidades nomeadas para o portuguˆes. 

Felizmente, o OpenNLP possui o NameFinder, uma biblioteca capaz de efetuar o treinamento de modelos, reconhecedores de entidades nomeadas, para qualquer idioma, por meio de um corpus de treinamento. Como bem sabemos, todo sistema baseado em aprendizado de m´aquina conta com features, que viabilizam a identificac¸˜ao de padr˜oes, que auxiliam na classificac¸˜ao de suas amostras. Semelhante ao Stanford [7], o NameFinder utiliza um gerador de _features_ padr˜ao no qual, por meio de um arquivo de configurac¸˜ao em xml, o usu´ario pode escolher quais _features_ ser˜ao utilizadas para conceber seu modelo. Na sec¸˜ao IV s˜ao mostrados como foi realizado o treinamento de nosso classificador de entidades usando esta _API_ . 

## III. CORPORA 

Nessa sec¸˜ao descrevemos os dois corpora, que tiveram papel fundamental na concepc¸˜ao deste trabalho, o Amazˆonia[8] e o HAREM [4]. 

> 2http://opennlp.sourceforge.net/models-1.5/ 

1http://ltasks.com/ 

**Amazˆonia:** O corpus Amazˆonia<sup>3</sup> cont´em 4.6 milh˜oes de palavras (cerca de 275 mil frases) retiradas do site colaborativo Overmundo<sup>4</sup> , um coletivo virtual que tem como objetivo apresentar a produc¸˜ao cultural brasileira. Por ser colaborativo, este website conta com um grande n´umero de autores de diversos pontos do Brasil, o que se reflete tamb´em em dife- 

rentes estilos de escrita. Para o Amazˆonia, foram coletados todos os textos da sec¸˜ao “Overblog” e todos os textos de n˜ao-ficc¸˜ao da sec¸˜ao “Banco de Cultura”, totalizando 4070 textos (1303 autores distintos). Diferentemente dos outros corpora da base do projeto Floresta Sint´atica, o Amazˆonia n˜ao ´e um corpus balanceado entre o portuguˆes do Brasil e de Portugal: todos os textos s˜ao brasileiros (PT-BR). 

O corpus Amazˆonia ´e proveniente do Projeto Floresta Sint´atica [8] e possui o formato espec´ıfico do projeto, chamado ´Arvores Deitadas (.ad), conforme podemos visualizar na Figura 1, que remete ao fragmento de texto **(d)** : 

**d)** “Jos´e In´acio de Abreu e Lima foi, nos anos finais...” 

Figura 1. Formato “.ad” do corpus Amazˆonia. 



No formato AD, a informac¸˜ao lingu´ıstica ´e codificada por meio dos pares **func¸˜ao** e **forma** . Assim, na terceira linha da Figura 1, h´a a indicac¸˜ao de que `a func¸˜ao sujeito (SUBJ) corresponde a forma sintagma nominal (np). A informac¸˜ao relativa `a hierarquia ´e marcada com o sinal de =. Na figura, vemos tamb´em que o sujeito “Jos´e <u>In´acio”</u> pertence `a categoria semˆantica “Pessoa” (“ _<_ hum _>_ ”). 

**Harem:** O corpus do HAREM [4] ´e uma iniciativa da Linguateca<sup>5</sup> , um centro de recursos distribu´ıdo para o processamento computacional da l´ıngua portuguesa, cujo objetivo ´e servir a comunidade que se dedica, em particular, ao processamento do Portuguˆes. O primeiro HAREM [9], foi publicado em 2006, contendo anotac¸˜oes _gold_ (anotac¸˜oes revisadas manualmente por profissionais das ´areas lingu´ıstica 

> 3Dispon´ıvel em: http://www.linguateca.pt/floresta/ficheiros/gz/amazonia.ad.gz 4http://www.overmundo.com.br/ 

> 5http://www.linguateca.pt/ 

e da computac¸˜ao) de entidades nomeadas e suas categorias. O segundo corpus do HAREM [10] foi disponibilizado em 2008, com o mesmo objetivo: prover uma base anotada, que pudesse servir como referˆencia no desenvolvimento e avaliac¸˜ao de sistemas voltados `a tarefa de _NER_ . Contudo, em sua vers˜ao mais recente, este foi ligeiramente melhorado. Atualmente, o HAREM possui 129 textos (89.241 palavras) anotados, distribu´ıdo em 10 categorias de entidades nomeadas, conforme podemos visualizar na Tabela I: 

Tabela I 

DISTRIBUIC¸ ˜AO DAS CATEGORIAS NO SEGUNDO HAREM [4] 

|Categoria|Entidades Nomeadas|Proporc¸˜ao|
|---|---|---|
|Pessoa|2035|27.11%|
|Local|1250|18.15%|
|Organizac¸˜ao|960|14.02%|
|Acontecimento|302|4.21%|
|Obra|437|6.31%|
|Abstrac¸˜ao|278|4.50%|
|Coisa|304|4.38%|
|Tempo|1189|15.21%|
|Valor|352|4.53%|
|Outro|79|1.2%|



## IV. GERAC¸ ˜AO DO MODELO 

Conforme dito anteriormente, para a concepc¸˜ao do novo modelo, utilizamos o OpenNLP, juntamente com suas bibliotecas e classes que viabilizam o treino, por meio de aprendizado de m´aquina. 

Diferente da maioria dos trabalhos que prop˜oem o aprendizado de m´aquina para a tarefa de _NER_ , utilizamos o corpus Amazˆonia para treinar o modelo e o corpus do segundo HAREM para avali´a-lo. O in´ıcio do processo de treino do modelo ´e dado com a marcac¸˜ao do corpus que ser´a usado. Sendo assim, realizamos um pr´e-processamento sobre o corpus de treino (Amazˆonia), com a finalidade de gerar as anotac¸˜oes das categorias, que ser˜ao usadas pelo m´etodo. Posteriormente, o corpus est´a pronto para ser usado como entrada do OpenNLP. 

Conforme vimos na Figura 1, o corpus Amazˆonia possui um formato espec´ıfico, chamado Arvores<sup>´</sup> Deitadas (.ad). Para realizarmos o treino, foi necess´aria a convers˜ao do corpus para um formato que seja aceito pelo m´etodo de treino da classe NameFinder. Este processo consiste em retirar marcac¸˜oes de _POS (Part-of-Speech)_ distribu´ıdas nos n´os do corpus (Figura 1) e adicionar as marcac¸˜oes de categorias. Assim, ao final do procedimento, o corpus conter´a apenas o texto com as anotac¸˜oes de categorias, conforme o fragmento de texto abaixo: 

_“A resposta do < START:person > Cineasta < END > italiano < START:person > Bertolucci < END > para ’ta lend´aria indagac¸˜ao ´e um N˜ao, ” caio efemente ” falando, assim mesmo , mai´usculo e negrito. < START:person > Bertolucci < END > foi t˜ao longe em ’ta sua posic¸˜ao em_ 

_relac¸˜ao ao tema que no seu filme ” < START:artprod > Os Sonhadores (sobre as manifestac¸˜oes juvenis ocorridas na Franc¸a de 1968) < END ...”_ 

Cada marcac¸˜ao de entidade nomeada inicia-se pela tag“ _<_ START: categoria _>_ ” e ´e delimitada por “ _<_ END _>_ ”. 

Realizada a etapa de pr´e-processamento, passamos `a etapa de treino, usando o pr´oprio NameFinder, contido no OpenNLP. Na Figura 2, podemos visualizar de forma mais detalhada a metodologia empregada para a concepc¸˜ao de nosso modelo. Basicamente, esta divide-se em duas etapas: Fase de Treino e Fase de Reconhecimento. A fase de treino, como o pr´oprio nome sugere, consiste em treinar o modelo usando o corpus pr´e-processado como entrada; a fase de reconhecimento consiste na identificac¸˜ao e classificac¸˜ao das entidades nomeadas, tendo como entrada textos simples, livres de anotac¸˜ao. 



<!-- Start of picture text -->
Figura 2. Arquitetura do Modelo<br><!-- End of picture text -->

## V. AVALIAC¸ ˜AO 

A avaliac¸˜ao do modelo foi realizada de duas formas: a primeira em relac¸˜ao `a colec¸˜ao dourada do segundo HAREM; e a segunda em relac¸˜ao aos outros recursos de _NER_ para a l´ıngua portuguesa (mencionados na sec¸˜ao III). 

Inicialmente, executamos o modelo, tendo como entrada os textos do segundo HAREM (livres de anotac¸˜ao). Em seguida, utilizamos um c´odigo escrito em JAVA, cujo objetivo ´e, basicamente receber como entrada a colec¸˜ao dourada do segundo HAREM, juntamente com a sa´ıda de cada sistema a ser avaliado. Na Tabela II podemos visualizar que existem 3 colunas: a primeira, “HAREM”, representa a quantidade de entidades nomeadas existentes na colec¸˜ao dourada segundo HAREM, que foram identificadas por nosso recurso de avaliac¸˜ao; a segunda, “Encontradas”, 

refere-se `a quantidade de entidades nomeadas encontradas pelo sistema de _NER_ ; a terceira, “Acertos”, remete `a quantidade de entidades nomeadas que o modelo encontrou, que possuem grafia e classe semˆantica idˆenticas `a colec¸˜ao dourada. 

Na Tabela III, temos a _precis˜ao_ , _recall_ e _f-measure_ de cada classe para o modelo. Note que as classes semˆanticas que obtiveram melhores resultados foram: “Pessoa”, “Local” e “Organizac¸˜ao”, atingindo respectivamente um _f-measure_ de 57.61%, 54.10% e 40.50%. Dessas trˆes classes, podemos notar, tamb´em, que “Organizac¸˜ao” obteve uma precis˜ao bastante baixa, se comparada `as duas anteriores. Isso remete `a dificuldade de muitos outros recursos de _NER_ , como podemos notar na Tabela VI. Nas tabelas IV, V e VI, mostramos resultados comparativos entre o modelo gerado e os atuais modelos, mencionados na sec¸˜ao III. Nas Tabelas VII, VIII e IX, mostramos a quantidade de entidades enconcontradas por cada sistema, bem como a quantidade de acertos. Realizamos testes levando em considerac¸˜ao as trˆes categorias de entidades nomeadas mais relevantes: Pessoa, Local e Organizac¸˜ao. Como podemos notar, o modelo apresenta resultados bastante compat´ıveis em relac¸˜ao aos demais modelos. Podemos notar tamb´em a dificuldade da maioria dos modelos em obter bons resultados para a categoria “Organizac¸˜ao”. 

Tabela II 

QUANTIDADE DE ENTIDADES CORRETAMENTE CLASSIFICADAS 

||HAREM|Encontrados|Acertos|
|---|---|---|---|
|Pessoa|2035|1964|1152|
|Local|1250|1164|653|
|Organizac¸˜ao|960|1919|583|
|Acontecimento|302|725|82|
|Obra|437|174|41|
|Abstrac¸˜ao|278|182|33|
|Coisa|304|78|11|
|Tempo|1189|666|45|
|Valor|352|335|138|
|Outro|79|0|0|
|Total|7186|7217|2741|



### Tabela III 

RESULTADOS DA AVALIAC¸ ˜AO DO MODELO 

||Precis˜ao|Recall|F-measure|
|---|---|---|---|
|Pessoa|58,65%|56,60%|57,61%|
|Local|56,09%|52,23%|54,10%|
|Organizac¸˜ao|30,38%|60,72%|40,50%|
|Acontecimento|11,72%|28,14%|16,53%|
|Obra|23,56%|9,38%|13,42%|
|Abstrac¸˜ao|17,18%|11,87%|14,04%|
|Coisa|14,10%|3,61%|5,75%|
|Tempo|6,75%|3,78%|4,85%|
|Valor|41,19%|39,20%|40,17%|
|Outro|0%|0%|0%|
|Total|37,97%|38,14%|38,06%|



Tabela IV 

AVALIAC¸ ˜AO DOS RECURSOS PARA A CATEGORIA PESSOA. 

|Sistema|Precis˜ao|Recall|F-measure|
|---|---|---|---|
|OpenNLP|58.65%|56.60%|57.61%|
|NERP-CRF|56.13%|49.73%|52.74%|
|LTASK|61.92%|61.38%|61.65%|
|Freeling|53.97%|60.44%|57.02%|
|PALAVRAS|59.66%|63.73%|61.63%|



### Tabela V 

AVALIAC¸ ˜AO DOS RECURSOS PARA A CATEGORIA LOCAL. 

|Sistema|Precis˜ao|Recall|F-measure|
|---|---|---|---|
|OpenNLP|56.09%|52.23%|54.10%|
|NERP-CRF|48.26%|53.36%|50.68%|
|LTASK|56.24%|52.64%|54.38%|
|Freeling|52.48%|60.08%|56.02%|
|PALAVRAS|54.19%|54.80%|54.49%|



tuguˆes. Utilizando a colec¸˜ao dourada do segundo HAREM, foi poss´ıvel avaliar o modelo para cada uma das 10 categorias. Al´em disso, efetuamos uma avaliac¸˜ao de desempenho entre nosso classificador e os principais recursos de _NER_ para o Portuguˆes, mostrando que nosso modelo ´e compat´ıvel com os demais, podendo ser ligeiramente superior em alguns aspectos. Al´em disso, uma grande vantagem na utilizac¸˜ao desse modelo, se da pela sua f´acil integrac¸˜ao ao OpenNLP. Dessa forma, conseguimos reunir diversas funcionalidades, tais como: _POS tagging_ , lematizac¸˜ao, an´alise morfol´ogica e reconhecimento de entidades nomeadas, utilizando um ´unico recurso. Futuramente, pretendemos integrar nosso modelo<sup>6</sup> de _NER_ desenvolvido a um sistema de resoluc¸˜ao de correferˆencias, o qual j´a est´a em fase de desenvolvimento. 

## VII. AGRADECIMENTOS 

### Tabela VI 

AVALIAC¸ ˜AO DOS RECURSOS PARA A CATEGORIA ORGANIZAC¸ ˜AO 

|Sistema|Precis˜ao|Recall|F-measure|
|---|---|---|---|
|OpenNLP|30.38%|60.72%|40.50%|
|NERP-CRF|43.64%|47.92%|45.68%|
|LTASK|28.19%|60.00%|38.36%|
|Freeling|27.54%|59.90%|37.73%|
|PALAVRAS|30.12%|51.15%|37.92%|



### Tabela VII 

ENTIDADES ENCONTRADAS E ACERTOS PARA A CATEGORIA PESSOA [HAREM: 2035]. 

|Sistema|Entidades Encontradas|Acertos|
|---|---|---|
|OpenNLP|1964|1152|
|NERP-CRF|1803|1028|
|LTASK|2017|1262|
|Freeling|2279|1243|
|PALAVRAS|2158|1318|



### Tabela VIII 

ENTIDADES ENCONTRADAS E ACERTOS PARA A CATEGORIA LOCAL [HAREM: 1250]. 

|Sistema|Entidades Encontradas|Acertos|
|---|---|---|
|OpenNLP|1164|653|
|NERP-CRF|1382|718|
|LTASK|1170|714|
|Freeling|1431|823|
|PALAVRAS|1193|741|



Os autores agradecem o suporte financeiro do CNPq, CAPES e Fapergs. 

## REFERENCIASˆ 

- [1] D. O. F. do Amaral, “O reconhecimento de entidades nomeadas por meio de conditional random fields para a l´ıngua portuguesa,” 2013. 

- [2] T. Coreixas, “Resoluc¸˜ao de correferˆencia e categorias de entidades nomeadas,” 2010. 

- [3] J. Baldridge, “The opennlp project,” _URL: http://opennlp. apache. org/index. html,(accessed 2 February 2012)_ , 2005. 

- [4] C. Freitas, C. Mota, D. Santos, H. G. Oliveira, and P. Carvalho, “Second harem: Advancing the state of the art of named entity recognition in portuguese.” in _LREC_ , 2010. 

- [5] L. Padr´o, M. Collado, S. Reese, M. Lloberes, I. Castell´on _et al._ , “Freeling 2.1: Five years of open-source language processing tools,” 2010. 

- [6] E. Bick, _The parsing system” Palavras”: Automatic grammatical analysis of Portuguese in a constraint grammar framework_ . Aarhus Universitetsforlag, 2000. 

- [7] J. R. Finkel, T. Grenager, and C. Manning, “Incorporating non-local information into information extraction systems by gibbs sampling,” in _Proceedings of the 43rd Annual Meeting on Association for Computational Linguistics_ . Association for Computational Linguistics, 2005, pp. 363–370. 

Tabela IX 

ENTIDADES ENCONTRADAS E ACERTOS PARA A CATEGORIA ORGANIZAC¸ ˜AO [HAREM: 960] 

|Sistema|Entidades Encontradas|Acertos|
|---|---|---|
|OpenNLP|1919|583|
|NERP-CRF|1054|511|
|LTASK|2043|639|
|Freeling|2088|631|
|PALAVRAS|1615|544|



## VI. CONCLUS ˜AO 

Neste artigo, apresentamos a construc¸˜ao de um modelo para o reconhecimento de entidades nomeadas para o Por- 

- [8] C. Freitas, P. Rocha, and E. Bick, “Um mundo novo na floresta sint´a (c) tica–o treebank do portuguˆes,” _Calidosc´opio_ , vol. 6, no. 3, pp. 142–148, 2008. 

- [9] D. Santos, N. Seco, N. Cardoso, and R. Vilela, “Harem: An advanced ner evaluation contest for portuguese,” in _Proceedings of LREC_ , 2006, pp. 1986–1991. 

- [10] D. Santos, C. Freitas, H. G. Oliveira, and P. Carvalho, “Second harem: new challenges and old wisdom,” in _Computational Processing of the Portuguese Language_ . Springer, 2008, pp. 212–215. 

> 6O modelo encontra-se dispon´ıvel em: http://www.inf.pucrs.br/linatural/Recursos 



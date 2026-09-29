%% abntex2.cls, v<VERSION> laurocesar
%% Copyright 2012-<COPYRIGHT_YEAR> by abnTeX2 group at https://www.abntex.net.br/ 
%%
%% This work may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version 1.3
%% of this license or (at your option) any later version.
%% The latest version of this license is in
%%   http://www.latex-project.org/lppl.txt
%% and version 1.3 or later is part of all distributions of LaTeX
%% version 2005/12/01 or later.
%%
%% This work has the LPPL maintenance status `maintained'.
%% 
%% The Current Maintainer of this work is the abnTeX2 team, led
%% by Lauro César Araujo. Further information are available on 
%% https://www.abntex.net.br/
%%
%% This work consists of the file abntex2.cls.
\LoadClass[
	% -- opções da classe memoir --
	12pt,				% tamanho da fonte
	openright,			% capítulos começam em pág ímpar (insere página vazia caso preciso)
	oneside,			% para impressão em recto e verso. Oposto a oneside
	sumario = tradicional,
	a4paper,			% tamanho do papel. 
	% -- opções da classe abntex2 --
	chapter=TITLE,		% títulos de capítulos convertidos em letras maiúsculas
% 	section=TITLE,		% títulos de seções convertidos em letras maiúsculas
% 	subsection=TITLE,	% títulos de subseções convertidos em letras maiúsculas
% 	subsubsection=TITLE,% títulos de subsubseções convertidos em letras maiúsculas
	% -- opções do pacote babel --
	english,			% idioma adicional para hifenização
	brazil,				% o último idioma é o principal do documento
	]{abntex2}

% ------------------------------------
% PACOTES
% ------------------------------------

% Pacotes fundamentais 
\RequirePackage{lmodern}			% Usa a fonte Latin Modern pslatex
\RequirePackage[T1]{fontenc}		% Selecao de codigos de fonte.
\RequirePackage[utf8]{inputenc}		% Codificacao do documento (conversão automática dos acentos)
\RequirePackage{indentfirst}		% Indenta o primeiro parágrafo de cada seção.
\RequirePackage{color}				% Controle das cores
\RequirePackage{graphicx}			% Inclusão de gráficos
\RequirePackage{microtype} 			% para melhorias de justificação
% Pacotes adicionais, usados no anexo do modelo de folha de identificação
\RequirePackage{multicol}
\RequirePackage{multirow}

% Pacotes de citações
\RequirePackage[brazilian, hyperpageref]{backref}	 % Paginas com as citações na bibl
\RequirePackage[alf]{abntex2cite}	% Citações padrão ABNT

\RequirePackage{titlesec}
\RequirePackage[labelfont=bf,textfont=normalfont]{caption}
\RequirePackage[labelfont=bf,textfont=normalfont]{subcaption}
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage{amsthm}
\RequirePackage{array}
\RequirePackage[a4paper, left = 3cm, right = 2cm, top = 3cm, bottom = 2cm]{geometry}

% ------------------------------------
% CONFIGURAÇÕES DE PACOTES
% ------------------------------------

% Configurações do pacote backref
% Usado sem a opção hyperpageref de backref
\renewcommand{\backrefpagesname}{Citado na(s) página(s):~}
% Texto padrão antes do número das páginas
\renewcommand{\backref}{}
% Define os textos da citação
\renewcommand*{\backrefalt}[4]{
	\ifcase #1 %
		Nenhuma citação no texto.%
	\or
		Citado na página #2.%
	\else
		Citado #1 vezes nas páginas #2.%
	\fi}%


% Configurações de aparência do PDF final

% alterando o aspecto da cor azul
\definecolor{blue}{RGB}{41,5,195}

% informações do PDF
\makeatletter
\hypersetup{
     	%pagebackref=true,
		pdftitle={\@title}, 
		pdfauthor={\@author},
    	%pdfsubject={\imprimirpreambulo},
	    pdfcreator={LaTeX with abnTeX2},
		pdfkeywords={abnt}{latex}{abntex}{abntex2}{tcc}, 
		colorlinks=false,       		% false: boxed links; true: colored links
    	linkcolor=black,          	% color of internal links
    	citecolor=black,            % color of links to bibliography
    	filecolor=black,      		% color of file links
		urlcolor=black,
		bookmarksdepth=4
}
\makeatother

% Espaçamentos entre linhas e parágrafos 

% O tamanho do parágrafo é dado por:
\setlength{\parindent}{1.3cm}

% Controle do espaçamento entre um parágrafo e outro:
\setlength{\parskip}{0.2cm}  % tente também \onelineskip

\newcommand{\Month}{%
  \ifcase\the\month
  \or Janeiro % 1
  \or Fevereiro % 2
  \or Mar\c{c}o % 3
  \or Abril % 4
  \or Maio % 5
  \or Junho % 6
  \or Julho % 7
  \or Agosto % 8
  \or Setembro % 9
  \or Outubro % 10
  \or Novembro % 11
  \or Dezembro % 12
  \fi}

%Configuracao de capitulo, seções, subseções e variantes
\titleformat{\section}{\Large\filcenter\bfseries}{\thesection}{1em}{\uppercase}

\newcommand{\key}[1]{$<$#1$>$}

%%criar um novo estilo de cabeçalhos e rodapés
\makepagestyle{ifma}
  %%cabeçalhos
  \makeevenhead{ifma} %%pagina par
     {} % cabeçalho lado esquerdo - pagina par
     {} % cabeçalho centro - pagina par
     {} % cabealho lado direito - pagina par
  \makeoddhead{ifma} %%pagina ímpar ou com oneside
     {} % cabeçalho lado esquerdo - pagina impar
     {} % cabeçalho centro - pagina impar
     {} % cabealho lado direito - pagina impar
  %% rodapé
  \makeevenfoot{ifma}
     {} % rodape lado esquerdo - pagina par
     {} % rodape centro - pagina par
     {} % rodape lado direito - pagina par
  \makeoddfoot{ifma} %%pagina ímpar ou com oneside
     {} % rodape lado esquerdo - pagina impar
     {\thepage} % rodape centro - pagina impar
     {} % rodape lado direito - pagina impar

%%criar um novo estilo de cabeçalhos e rodapés
\makepagestyle{ifma}
  %%cabeçalhos
  \makeevenhead{ifma} %%pagina par
     {} % cabeçalho lado esquerdo - pagina par
     {} % cabeçalho centro - pagina par
     {} % cabealho lado direito - pagina par
  \makeoddhead{ifma} %%pagina ímpar ou com oneside
     {} % cabeçalho lado esquerdo - pagina impar
     {} % cabeçalho centro - pagina impar
     {} % cabealho lado direito - pagina impar
  %% rodapé
  \makeevenfoot{ifma}
     {} % rodape lado esquerdo - pagina par
     {} % rodape centro - pagina par
     {} % rodape lado direito - pagina par
  \makeoddfoot{ifma} %%pagina ímpar ou com oneside
     {} % rodape lado esquerdo - pagina impar
     {\thepage} % rodape centro - pagina impar
     {} % rodape lado direito - pagina impar     
                       
\renewcommand{\theequation}{\arabic{equation}}
\numberwithin{equation}{chapter}

\renewcommand{\thefigure}{\arabic{figure}}
\numberwithin{figure}{chapter}

\renewcommand{\thetable}{\arabic{table}}
\numberwithin{table}{chapter}

\renewcommand{\ABNTEXchapterfont}{\bfseries}
\renewcommand{\ABNTEXchapterfontsize}{\Large}

\renewcommand{\ABNTEXsectionfont}{\bfseries}
\renewcommand{\ABNTEXsectionfontsize}{\nomalsize}


\newcommand{\dint}{\displaystyle\int}


\newtheorem{defi}{Definição}[chapter]
\newtheorem{thm}{Teorema}[chapter]
\newtheorem{cor}{Corolário}[chapter]
\newtheorem{lem}{Lema}[chapter]
\newtheorem{axm}{Axioma}[chapter]
\newtheorem{prop}{Proposição}[chapter]

\renewcommand{\qedsymbol}{}
\newcommand*{\cqd}{\hspace{\stretch9}\ensuremath{\blacksquare}}%

% Alterar layout de paginas em inicio de capitulo
% \makepagestyle{abntbookchapfirst}
% \makeoddhead{abntbookchapfirst}{}{}{}

% Configura layout para elementos textuais
\renewcommand{\textual}{%
  \pagestyle{ifma}%
  % \aliaspagestyle{chapter}{abntbookchapfirst}% customizing chapter pagestyle
  \aliaspagestyle{chapter}{ifma}% customizing chapter pagestyle
  \nouppercaseheads%
  \bookmarksetup{startatroot}% 
}

\renewcommand{\fonte}[1]{\flushright{\tiny{\textbf{Fonte:} #1}}}

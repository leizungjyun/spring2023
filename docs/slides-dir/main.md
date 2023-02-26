## Music & Culture

Jazz, Blues and Popular Music in the American Culture



LI Shaun, 2023-02-27
<!-- .element: style="font-size:20pt" -->

=== 

![shaun-lecture](docs/slides-dir/images/shaun-lecturer.jpeg) <!-- .element: width="400"  --> 

Teacher: 李颂元, LI Shaun

Website: leizungjyun.github.io/spring2023/

leizungjyun#(ZJUers would know)


==

![shaun-piano](docs/slides-dir/images/shaun-piano.jpeg) <!-- .element: width="600"  --> 

Keyboard playing since 1994


== 

![shaun-guitar](docs/slides-dir/images/shaun-guitar.jpeg) <!-- .element: height="500"  --> 

Guitar playing since 2003

==
![shaun-cello](docs/slides-dir/images/shaun-cello.jpeg) <!-- .element: width="600"  --> 

Cello playing since 2018


==

Classical background but popular teachers?

Chen Xi, Wendy, Michael Campbell
<!-- .element: style="font-size:20pt" -->

===

Jazz, Blues and Popular Music in the American Culture

Spring 2023
<!-- .element: style="font-size:20pt" -->


$\LaTeX$ Macros
<!-- .element: style="font-size:40pt" -->

  <pre><code data-trim data-noescape class="language-latex">
  % preamble
  \newcommand{\R}{\mathbb{R}}
  % preamble
  </code></pre>

  <pre><code data-trim data-noescape class="language-latex">
  % document
  $\R$
  % document
  </code></pre>

$\mathbb{R}$

===

## DRY
Don't Repeat Yourself

  <pre><code data-trim data-noescape class="language-latex">
  % preamble
  \newcommand{cmd}[args]{def}
  \renewcommand{cmd}[args]{def}
  \providecommand{cmd}[args]{def}
  % preamble
  </code></pre>

==
## example 1

  <pre><code data-trim data-noescape class="language-latex">
  % preamble
  \newcommand{\avector}[2]{(#1_1,#1_2,\ldots,#1_{#2})}
  % preamble
  </code></pre>

  <pre><code data-trim data-noescape class="language-latex">
  % document
  $\mathbf{x} = \avector{x}{42}$
  % document
  </code></pre>

  $\mathbf{x}=(x_1, x_2, \ldots, x_{42})$

==
## example 2
  <pre><code data-trim data-noescape class="language-latex">
  % preamble
  \newcommand{\ours}[1]{
      \renewcommand{\ours}{#1}
    }   
  \ours{SBGCS-Net}
  % preamble
  </code></pre>

  <pre><code data-trim data-noescape class="language-latex">
  % document
  In this paper, we present a novel method called \ours, % ...
  % document
  </code></pre>

  In this paper, we present a novel method called SBGCS-Net, ...
<!-- .element: style="font-size:20pt" -->
===

```metawriting```
<!-- .element: style="font-size:50pt" -->

$\LaTeX$ packages for scientific writing
==

![gitlab](docs/slides-dir/images/metawriting-gitlab.png) <!-- .element: width="800"  --> 

Gitlab repo

==
![gitlab](slides-dir/images/paper-metawriting.png) <!-- .element: width="800"  --> 

```metawriting``` as a submodule

==
  <pre><code data-trim data-noescape class="language-latex">
  % preamble
  \usepackage{metawriting/metawriting}
  \ours{SBGCS-Net}
  \usepackage{metawriting/sciabbr}
  </code></pre>
  Use the ```metawriting``` packages in your $\LaTeX$ preamble
<!-- .element: style="font-size:20pt" -->
===

The `sciabbr` Package
  <pre><code data-trim data-noescape class="language-latex">
  % preamble
  \usepackage{metawriting/metawriting}
  \ours{SBGCS-Net}
  \usepackage{metawriting/sciabbr}
  </code></pre>
==
  <pre><code data-trim data-noescape class="language-latex">
  % preamble
  %% normal text
  \usepackage{metawriting/sciabbr} 
  </code></pre>

  <pre><code data-trim data-noescape class="language-latex">
  % document
  \Eg, \ie, \wrt, \etc.
  </code></pre>
  E.g., i.e., w.r.t., etc.

  <pre><code data-trim data-noescape class="language-latex">
  % preamble
  %% \emph effect
  \usepackage[emph]{metawriting/sciabbr}
  </code></pre>

  <pre><code data-trim data-noescape class="language-latex">
  % document
  \Eg, \ie, \wrt, \etc.
  </code></pre>
  *E.g., i.e.,* w.r.t., *etc.*

===

  ## Summary
<!-- .slide: style="font-size:20pt" -->
  - Set `metawriting` as a submodule (`git` repo)
  - Add `metawriting` packages (preamble)
  - Use `metawriting` commands (document)
  - Create your own commands 
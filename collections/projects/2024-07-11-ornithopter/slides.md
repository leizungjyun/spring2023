[//]: # (
 
    
    )





### Ornithopter
Design and Implementation



![Dune](https://media.licdn.com/dms/image/C4D12AQGrje00HVipdQ/article-cover_image-shrink_720_1280/0/1636786281404?e=2147483647&v=beta&t=MOy4iArWui7yEty0yh9qUTxSDNzav5SXufuh1IGlJg4) <!-- .element: width="500" -->

LI Shaun, WANG Phil
<!-- .element: style="font-size:20pt" -->
2024-07-11
<!-- .element: style="font-size:20pt" -->
===


### Intro to Ornithoptor


The Flapping Wing Air Vehicles

![alt text](images/ornith_concept.jpg) <!-- .element: width="750" -->

==

#### The wing shape

![alt text](images/wingshape.jpg) <!-- .element: width="550" -->


==

#### Tech potentials

* Advantages
    * much more efficient than other types of UAVs
    * typically very safe
    * capable of hovering in place during flight
    * simple mechanical complexity
    * expanding the capabilities and applications



==

#### tech potential - example

* Pterosaurs
    * wing span > 10m
    * glide ratio > 10

![alt text](images/pteronsaurs.jpg) <!-- .element: width="750" -->






===
### State of the Art

* Dimensions
    * Macro vs Micro
    * Mechanical design 



== 

#### current research

![alt text](images/current_ornith.png) <!-- .element: width="750" -->



==
#### wing design techmap


![alt text](images/wingtechmap.jpg) <!-- .element: width="1050" style="filter:invert(93%)" -->




==
####  wing flapping structure

* single axis

![alt text](images/singleaxis.jpg) <!-- .element: width="750" style="filter:invert(93%)"-->


==
#### wing flapping structure

* multi-axis

![alt text](images/multiaxis.jpg) <!-- .element: width="750" style="filter:invert(93%)"-->





==
#### Perspective

* Recent
    * simplized wing design
    * few Aerodynamic consideration
    * traditional control theory
    * difficulty in take-off and landing


![alt text](images/current_design.svg)<!-- .element: width="750" style="filter:invert(93%)"-->


*证明哥德巴赫猜想，需要新的数学方法* 





===
### Research Targets

* Methodology
    * Flying oriented mechanics desgin
    * Constructure oriented controlling design

![alt text](images/our_design.png) <!-- .element: width="750" -->





===
### in Engineering

* implementation 
    * Evolutionary Design Procedure
    * Embodied Foundation model for Flapping control



== 
#### Evolutionary Design Procedure

State Description

![alt text](images/evolutionstate.jpg) <!-- .element: width="750" -->


==
#### Evolutionary Design Procedure

State Transition

![alt text](images/statetransition.jpg) <!-- .element: width="750" -->











===
### Training
===

![alt text](images/training.svg)
<!-- .element: style="filter:invert(93%)" -->
The training process




==
![google translate](https://f.hubspotusercontent20.net/hubfs/6374374/Imported_Blog_Media/google_translate_logo.jpg) <!-- .element: height="200" --> 
![vs](https://media.istockphoto.com/id/1459545409/vector/vs-versus-icon-logo-black-white-vector-symbol-fight-competition-battle-sport-game-grunge.jpg?s=612x612&w=0&k=20&c=dJPtK0BAzoTM9hI5mNBKg-b1-063mYO3WIBOtgScB3w=) <!-- .element: height="200" style="filter:invert(93%)"-->
![chatgpt](https://media.licdn.com/dms/image/D5612AQG8OZj2KQEQtg/article-cover_image-shrink_720_1280/0/1694623029215?e=2147483647&v=beta&t=DwGrBLpQS7BA7eYSvw3T2NTNCXjAzw8l86KSTQTb77A) <!-- .element: height="200" -->


Task-specific model or general-purpose model?
==

![open-x](https://robotics-transformer-x.github.io/img/overview.png)

*Increasingly,*

*the most effective way to tackle a given narrow task*

*is to adapt a general-purpose model.*

-- *[Open X-Embodiment](https://robotics-transformer-x.github.io/)*

==
![alt text](images/pretraining.svg)
<!-- .element: style="filter:invert(93%)" -->

===
### Autoregressive
==

![autoregressive](https://joaquinamatrodrigo.github.io/skforecast/0.4.3/img/forecasting_multi-step_en.gif)
<!-- .element: style="filter:invert(93%)" -->

Auto-regressive
==
![lm](https://miro.medium.com/max/447/1*bknGoZUriWYabncNGhUU5Q.gif)
<!-- .element: style="filter:invert(93%)" -->

Auto-regression in language models

==
![probabilty](https://api.wandb.ai/files/darek/images/projects/37727390/9ec381c5.gif)
<!-- .element: style="filter:invert(93%)" -->
==

![token-wise](https://www.megaputer.com/wp-content/uploads/autoregressive_generation.gif)
<!-- .element: style="filter:invert(93%)" -->

Token-wise in practice

==

![self-supervised](https://miro.medium.com/v2/resize:fit:1400/1*el-beq8gIjuIoLl1qFmJAA.gif)
<!-- .element: style="filter:invert(93%)" -->

Self-supervised Pretraining

===
### Mask autoencoding
==
![bert-like](https://developers.reinfer.io/blog/prompting/mlm-light.gif)
<!-- .element: style="filter:invert(93%)" -->
Maksed language modeling

==

![mlm](https://raw.githubusercontent.com/UKPLab/sentence-transformers/master/docs/img/MLM.png)
<!-- .element: style="filter:invert(93%)" -->

Maksed language modeling

==


![mask-autoencoder](https://miro.medium.com/v2/resize:fit:1400/1*MbmkubC541LdgIfnseaCQw.png)
Masked autoencoder (MAE)

==
![autoencoder](https://miro.medium.com/v2/resize:fit:1400/1*oUbsOnYKX5DEpMOK3pH_lg.png) <!-- .element: style="filter:invert(93%)" height="400"-->

Autoencoder (2006)
===

#### Pretraining for embodied agents

==


<video loop="" autoplay="" muted="" playsinline="" preload="metadata">
                <source src="https://robotic-pretrained-transformer.github.io/assets/method_animation_v4.m4v" type="video/mp4">
            </video>
            Pretraining: Mask autoencoding

==

<video loop="" autoplay="" muted="" playsinline="" preload="metadata">
                <source src=" https://robotic-pretrained-transformer.github.io/assets/inference_animation.mp4" type="video/mp4">
            </video>

Inference: Autoregressive
===

![flying bird](https://i.makeagif.com/media/1-28-2016/8zooMT.gif)

 ### LET'S FLY!

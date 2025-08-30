# VCSearch: Bridging the Gap Between Well-Defined and Ill-Defined Problems in Mathematical Reasoning

[![Paper](https://img.shields.io/badge/Paper-EMNLP_2025-blue)](./EMNLP_2025_vcsearch.pdf)

This repository contains the official implementation of the paper:

> **VCSearch: Bridging the Gap Between Well-Defined and Ill-Defined Problems in Mathematical Reasoning**  (EMNLP 25)
> Shi-Yu Tian\*, Zhi Zhou\*, Kun-Yang Yu, Ming Yang, Lin-Han Jia, Lan-Zhe Guo†, Yu-Feng Li†  
>
> LAMDA GROUP 
>
> Nanjing University 
> *Equal contribution, †Corresponding authors  

---

## 🔍 Overview

Large language models (LLMs) have demonstrated impressive performance on reasoning tasks, including mathematical reasoning. However, the current evaluation mostly focuses on carefully constructed benchmarks and neglects the consideration of real-world reasoning problems that present missing or contradictory conditions, known as ill-defined problems. To further study this problem, we develop a large-scale benchmark called ***P**roblems with **M**issing and **C**ontradictory conditions* **(PMC)** containing over 5,000 validated ill-defined mathematical problems. Our preliminary experiments through \benchmark reveal two challenges about existing methods: (1) traditional methods exhibit a trade-off between solving accuracy and rejection capabilities, and (2) formal methods struggle with modeling complex problems. To address these challenges, We develop ***V**ariable-**C**onstraint **Search*** (**VCSearch**), a training-free framework that leverages formal language to detect ill-defined problems, where a variable-constraint pair search strategy is incorporated to improve the modeling capability of formal language. Extensive experiments demonstrate that VCSearch improves the accuracy of identifying unsolvable problems by at least 12% across different LLMs, thus achieving stronger robust mathematical reasoning ability.

<img src="C:\Users\Administrator\Desktop\科研投稿\vcsearch\cemera-ready 版本\VCSearch\img\intro.png" alt="intro" style="zoom: 33%;" />

**PMC benchmark is available at [[Hugging Face]](https://huggingface.co/datasets/kevin715/PMC)**

**Paper is available at [[Arxiv]](https://arxiv.org/abs/2303.10365)**

## 🚀 Usage

<img src="C:\Users\Administrator\Desktop\科研投稿\vcsearch\cemera-ready 版本\VCSearch\img\frame.png" alt="frame" style="zoom: 30%;" />

run vcsearch with qwen model

~~~

~~~

## 📜 Citation

If you find this work useful, please cite our paper:

~~~python
@article{tian2024vc,
  title={VC Search: Bridging the Gap Between Well-Defined and Ill-Defined Problems in Mathematical Reasoning},
  author={Tian, Shi-Yu and Zhou, Zhi and Yu, Kun-Yang and Yang, Ming and Jia, Lin-Han and Guo, Lan-Zhe and Li, Yu-Feng},
  journal={arXiv preprint arXiv:2406.05055},
  year={2024}
}
~~~


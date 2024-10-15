# BEAF: Observing Before-AFter Changes to Evaluate Hallucination in Vision-language Models (ECCV 2024)
Authors: [Moon Ye-Bin*](https://sites.google.com/g.postech.edu/moon-ye-bin), [Nam Hyeon-Woo*](https://sites.google.com/view/namhyeonwoo/), Wonseok Choi, [Tae-Hyun Oh](https://ami.postech.ac.kr/members/tae-hyun-oh)

### [Project Page](https://beafbench.github.io/) | [Dataset](https://drive.google.com/file/d/1Xx7j8Hz8QX3Fl_hpSBet6r15njhwCgeR/view) | [Paper](https://arxiv.org/abs/2407.13442)

<p align="center">
  <img style="width: 80%" src="/teaser_out.gif" autoplay loop muted playsinline>
</p>

This repository is official implementation for the ECCV 2024 paper, ["BEAF: Observing BEfore-AFter Changes to
Evaluate Hallucination in Vision-language Models"](https://arxiv.org/abs/2407.13442). 
The key idea of our BEAF benchmark is manipulating visual scene information and designing the metrics based on the model's answer changes along the scene changes.

<br>

> **Abstract:** *Large vision language models (LVLMs) perceive the world through a combination of a visual encoder and large language models (LLMs). The visual encoder, pre-trained on large-scale vision-text datasets, provides zero-shot generalization to visual data, and LLMs endow the high reasoning ability to LVLMs. It leads LVLMs to achieve high performance on wide benchmarks without fine-tuning, known as zero or few-shot capability of LLMs. However, recent studies show that LVLMs are vulnerable to hallucination. This undesirable behavior degrades reliability and credibility, thereby making users unable to fully trust the output from LVLMs. To enhance trustworthiness and better tackle the hallucination of LVLMs, we curate a new evaluation dataset, called the BEfore-AFter hallucination dataset (BEAF), and introduce new metrics: True Understanding (TU), IGnorance (IG), StuBbornness (SB), and InDecision (ID). Unlike prior works that focus only on constructing questions and answers, the key idea of our benchmark is that we manipulate visual scene information by image editing models and design the metrics based on scene changes. This allows us to clearly assess whether LVLMs correctly understand a given scene by observing the ability to perceive changes. We also visualize the correctness heatmap by virtue of our two-axis view: vision and text. Upon evaluating LVLMs with our dataset, we observed that our metrics can reveal different aspects of LVLM hallucination.*


## Evaluation 
### 1. BEAF dataset download
\* [07/18] We released the BEAF dataset ver0, but it will be re-filtered and refined as ver1 soon!! \
\* [10/15] We updated the BEAF dataset ver1. The QnA JSON file is also updated. 

- Original + Manipulated images: download from [here](https://drive.google.com/file/d/1Xx7j8Hz8QX3Fl_hpSBet6r15njhwCgeR/view)
- The original images are sourced from the [COCO dataset](https://cocodataset.org/#home)

### 2. Get your model's answer
- Image name, question, GT answers, and additional metadata are in `./beaf_qna.json` file
- The format and question of our BEAF is inspired by the [POPE dataset](https://github.com/RUCAIBox/POPE?tab=readme-ov-file)
- The model output should be organized in a json file in the following format:
  ```bash
  [
    {"id": 0, "answer": "No."}, 
    {"id": 1, "answer": "Yes."}, 
    ... 
    {"id": 26063, "answer": "No."}
  ]
  ```
- Please refer to `answer_gpt4o.json` as an example of a model answer.

### 3. Evaluation
- Compute both our metrics (TU, IG, SBp, SBn, ID) and traditional metrics (Accuracy, Precision, Recall, F1)
- Run `beaf_metric.py` with:
  ```bash
  python beaf_metric.py --model-answers {your_model_answer.json}
  ```
<!-- ## Setup

Clone the repo with:

```bash
git clone https://github.com/postech-ami/TextManiA.git
cd TextManiA
```


The environment can be installed and activated with:

```bash
conda create --name textmania python=3.8
conda activate textmania
pip install -r requirements.txt
```

## Running TextManiA
Preprocessing the difference vectors with:
```bash
cd preprocessing
sh gen_diff_vec.sh
```
The training code is based on [Manifold Mixup](https://github.com/vikasverma1077/manifold_mixup#manifold_mixup-icml-2019).   
Running TextManiA on the CIFAR100-LT dataset with:
```bash
python src/main.py --dataset cifar100-lt --data_dir data/cifar100/ --root_dir experiments/ --arch resnet18  --ibf 100 --learning_rate 0.2 --epochs 200 --schedule 50 100 150 --gammas 0.1 0.1 0.1 --train textmania 
``` -->



## Citation
If you use BEAF in a research paper, please cite our work and related works as follows:
````BibTeX
@inproceedings{yebin2024beaf,
  title     = {BEAF: Observing BEfore-AFter Changes to Evaluate Hallucination in Vision-language Models},
  author    = {Ye-Bin, Moon and Hyeon-Woo, Nam and Choi, Wonseok and Oh, Tae-Hyun},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2024},
}

@inproceedings{lin2014microsoft,
  title     = {Microsoft coco: Common objects in context},
  author    = {Lin, Tsung-Yi and Maire, Michael and Belongie, Serge and Hays, James and Perona, Pietro and Ramanan, Deva and Doll{'a}r, Piotr and Zitnick, C Lawrence},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2014},
}

@inproceedings{Li-hallucination-2023,
  title     = {Evaluating Object Hallucination in Large Vision-Language Models},
  author    = {Yifan Li, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin Zhao and Ji-Rong Wen},
  booktitle = {The 2023 Conference on Empirical Methods in Natural Language Processing},
  year      = {2023},
}
````

## Acknowledgment
This work was partly supported by Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government(MSIT) (No.2021-0-02068, Artificial Intelligence Innovation Hub; No.2022-0-00124, Development of Artificial Intelligence Technology for Self-Improving Competency-Aware Learning Capabilities; No.RS-2019-II191906, Artificial Intelligence Graduate School Program(POSTECH))

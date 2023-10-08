# Large Language Models are Not Yet Human-Level Evaluators for Abstractive Summarization
**Authors**: Chenhui Shen, Liying Cheng, Xuan-Phi Nguyen, Yang You and Lidong Bing

This repository contains code and related resources of our paper ["Large Language Models are Not Yet Human-Level Evaluators for Abstractive Summarization"](https://arxiv.org/abs/2305.13091).

<!-- :star2: Check out this awesome [[demo]](https://huggingface.co/spaces/joaogante/contrastive_search_generation) generously supported by Huggingface ([@huggingface](https://github.com/huggingface) :hugs:) which compares contrastive search with other popular decoding methods. Many thanks to Huggingface :hugs:!  -->


****
If you find our paper and resources useful, please kindly leave a star and cite our papers. Thanks!

```bibtex
@inproceedings{shen2023llmeval,
  title={Large Language Models are Not Yet Human-Level Evaluators for Abstractive Summarization},
  author={Shen, Chenhui and Cheng, Liying and Nguyen, Xuan-Phi and Bing, Lidong and You, Yang},
  booktitle={Findings of EMNLP},
  url={"https://arxiv.org/abs/2305.13091"},
  year={2023}
}
```

<!-- ****

### News:
* [2022/10/26] Some content

**** -->

<span id='all_catelogue'/>

### Catalogue:
* <a href='#introduction'>1. Introduction</a>
* <a href='#file'>2. File Contents </a>
* <a href='#reproduce_examples'>3. Running our code</a>

    
****

<span id='introduction'/>

# 1. Introduction: <a href='#all_catelogue'>[Back to Top]</a>

Pre-trained language models (PLMs) have accomplished impressive achievements in abstractive single-document summarization (SDS). However, such benefits may not be readily extended to muti-document summarization (MDS), where the interactions among documents are more complex. Previous works either design new architectures or new pre-training objectives for MDS, or apply PLMs to MDS without considering the complex document interactions. While the former does not make full use of previous pre-training efforts and may not generalize well across multiple domains, the latter cannot fully attend to the intricate relationships unique to MDS tasks. In this paper, we enforce hierarchy on both the encoder and decoder and seek to make better use of a PLM to facilitate multi-document interactions for the MDS task. We test our design on 10 MDS datasets across a wide range of domains. Extensive experiments show that our proposed method can achieve consistent improvements on all these datasets, outperforming the previous best models, and even achieving better or competitive results as compared to some models with additional MDS pre-training or larger model parameters.

****


<span id='file'/>

# 2. File Contents

Under Root Dir,

* ``model_output_annotations/``: our processed <a href="https://github.com/Yale-LILY/SummEval"> SummEval </a> annotations for the abstractive summarization systems.

* ``eval_model_generations/``:  the outputs of LLM evaluations using RTS, MCQ or StarEval prompts, under respective directories of the evaluation model name (our results are stored under the captalized model names)

* ``comp_data/``: our processed head-to-head comparison inputs from models in the <a href="https://github.com/Yale-LILY/SummEval"> SummEval </a> dataset.

* ``comp_res/``: the output of LLM evaluations using H2H prompts.

* ``summeval.json``: the same file taken from <a href="https://github.com/krystalan/chatgpt_as_nlg_evaluator"> this </a> repo.

* ``eval_with_rts_or_mcq.py``: call ChatGPT or GPT-4 to evaluate with RTS or MCQ prompts; in order to run, add your own openai api key in ``secret.py``

* ``extract_model_scores.py``: extract all the llm-evaluated scores for a specific model stored under ``model_output_annotations`` 

* ``calc_data_corr.py``: to calculate correlation using the full 1200 summaries (results in Tab 5) for a given evaluator model.

* ``per_model_corr.py``: to calculate correlation for each candidate model.

* ``calc_meta_corr.py``: to calculate meta-correlation for a given evaluator model.




<span id='reproduce_examples'/>


# 3. Running our Code

To set up,
```yaml
pip install openai, tqdm, scipy
```

### 3.1 For RTS or MCQ

#### - Step 1
To get RTS or MCQ response from openai APIs, set your key in ``secret.py``, then
```yaml
# If you wish to see prompt first without calling the actual api, use flag --print_full_prompt_without_calling_api 

# For dim, 0 is relevance, 1 is consistency, 2 is fluency, and 3 is coherence;

# For eval_type, 0 is RTS, 1 is MCQ, 2 is StarEval.

python eval_with_rts_or_mcq.py --eval_model <openai model> --dim <int from 0 to 4> --eval_type <int from 0 to 3> 
```
#### - Step 2
To compile a new data file with all metric results 
```yaml
python extract_model_scores.py --eval_model <openai model>
```

#### - Step 3
* To calculate correlation for all 1200 summaries,
    ```yaml
    python calc_data_corr.py --eval_model <openai model> --eval_type <int from 0 to 3>
    ```

* To calculate correlation for each candidate model,
    ```yaml
    python per_model_corr.py --eval_model <openai model> --eval_type <int from 0 to 3>
    ```

* To calculate meta-correlation,
    ```yaml
    python calc_meta_corr.py --eval_model <openai model>
    ```

### 3.2 For H2H

#### - Step 1
To get H2H response from openai APIs, set your key in ``secret.py``, then
```yaml
# If you wish to see prompt first without calling the actual api, use flag --print_full_prompt_without_calling_api 

# For dim, 0 is relevance, 1 is consistency, 2 is fluency, and 3 is coherence;
python eval_with_h2h.py --eval_model <openai model> --dim <int from 0 to 4>
```
#### - Step 2
To calculate H2H pairs for the H2H method
```yaml
python calc_h2h_pairs.py --eval_model <openai model> 
```

#### - Step 3
To calculate H2H pairs for all __other__ methods 
```yaml
# For model type, 0 for calculating all pairs, 1 for the challenge set only
python calc_pairs.py --eval_model <openai model> --model_pair_type <0 or 1> --add_rts_res --add_mcq_res
```
You may include the flag ``--add_rts_res`` and ``--add_mcq_res`` to calculate for RTS and MCQ if you have already compiled the results by running ``extract_model_scores.py``.

### 3.3 Run on Llama 2

setup: we use vllm to run efficiently on multiple gpus.
```yaml
conda create --prefix ./vllm_torch_2+cuda118 python=3.8
source activate vllm_torch_2+cuda118
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install vllm 
pip install pandas # this is not auto installed by vllm and will cause trouble in ray 
```

to run llama inference on multiple gpus for RTS:
```yaml
python llama_eval_multi_gpu.py --model_name <llama model> --tensor_parallel_size <num_gpus>
```

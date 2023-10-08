from transformers import AutoTokenizer
import transformers
import torch
import json
import os
from tqdm import tqdm
import time
from prompt_templates import prepare_rts_prompt
import logging
import argparse


############ helper functions ####################
def parse_arguments(parser):
    ###Eval Hyperparameters
    parser.add_argument('--model_name', type=str, default="/mnt/workspace/utils/huggingface_models/llama-2-7b-chat-hf", help="the llama model to use")
    parser.add_argument('--tensor_parallel_size', type=int, default=1, help="number of gpus to use")

    args = parser.parse_args()
    for k in args.__dict__:
        print(k + ": " + str(args.__dict__[k]))
    return args
####################################################

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)

parser = argparse.ArgumentParser()
args = parse_arguments(parser)


# specify your local model path below
model_name = args.model_name

# dtype = "bfloat16"
dtype = "float16"
tensor_parallel_size = args.tensor_parallel_size

# the summeval data folder below
annotation_dir = f"./model_output_annotations" 
# the dir where we will write llama's responses below
eval_dir = os.path.join("./eval_model_generations", model_name.split("/")[-1])
logger.info(f'save to {eval_dir}')
import shutil

os.makedirs(eval_dir, exist_ok=True)

# get model
logger.info(f"loading model... {model_name}")

from vllm import LLM, SamplingParams
llm = LLM(
    model=model_name, 
    dtype=dtype, 
    tensor_parallel_size=tensor_parallel_size) # the number of gpu to use

max_new_tokens = 256
sampling_params = SamplingParams(
    temperature=0.0, 
    max_tokens=max_new_tokens,
    # stop=["</s>"],
)

logger.info(f"model ready... {sampling_params}")
logger.info(sampling_params)

def llm_gen(texts):
    global llm
    logger.info(f'Generate for {len(texts)} documents')
    gen = llm.generate(texts, sampling_params)
    gen_texts = [x.outputs[0].text for x in gen]
    logger.info(f'1st gen:\n{texts[0]}<<<{gen_texts[0]}>>>')
    return gen_texts


B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

## not used
# DEFAULT_SYSTEM_PROMPT = """You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your \
# answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure\
#  that your responses are socially unbiased and positive in nature.

# If a question does not make any sense, or is not factually coherent, explain why instead of answering something not \
# correct. If you don't know the answer to a question, please don't share false information."""

# B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS + conversation.new_user_input
text = "Score the following Summary given the corresponding Article with respect"

def wrap_prompt_as_chat(text):
    # init_input = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS + text
    init_input = B_SYS + E_SYS + text # we use empty system message
    output = f"{B_INST} {init_input} {E_INST}"
    return output


M_ID_LIST = ["M8","M9","M10","M11","M12","M13","M14","M15","M17","M20", "M22","M23"]
# M_ID_LIST = ["abstractive","pointer_c","pointer_n","pointer_s"] # chenhui: for newsroom

# each model has 100 examples, can specify the start_idx or end_idx to generate for specific samples
start_idx = 0 
end_idx = 100
# end_idx = 60 # chenhui: for newsroom

# use the correspoding number in id2asp to evaluate the dimensions
ASPECT_ID_LIST = [0,1,2,3] # use this to run on all dimensions 

id2asp = {
    0:"relevance",
    1:"consistency",
    2:"fluency",
    3:"coherence"
}

def eval_aspects(aspect_id, summary, article, results_dir, summary2 = None):
    # prep request
    eval_prompt = prepare_rts_prompt(aspect_id, summary, article)
    eval_prompt = wrap_prompt_as_chat(eval_prompt) # SCH: important to wrap in chat format!!!

    ### uncomment to see what the prompt is like
    # logger.info(eval_prompt)
    # exit()
    return eval_prompt

logger.info(f'{ASPECT_ID_LIST=}')
logger.info(f'{M_ID_LIST=}')
for ASPECT_ID in ASPECT_ID_LIST: # use this to run on all dimensions 
    for M_ID in M_ID_LIST:
        with open(os.path.join(annotation_dir, M_ID+"_outputs_annotations.jsonl")) as f:
            logger.info(M_ID)
            dataset = [json.loads(line) for line in f]
            # open files for score
            eval_results_dir = os.path.join(eval_dir,"eval_"+M_ID+"_generations")
            if not os.path.exists(eval_results_dir):
                os.mkdir(eval_results_dir)

            # if ASPECT_ID == 0:
                # f0 = open(os.path.join(eval_results_dir, id2asp[0]+".txt"),"a", encoding="utf-8")
            out_path = os.path.join(eval_results_dir, id2asp[ASPECT_ID]+"_rts.txt") 
            f0 = open(out_path, "w", encoding="utf-8")
            logger.info(f"eval {ASPECT_ID}")

            prompts = []
            ids = []
            for i in tqdm(range(start_idx, end_idx)): 
                example = dataset[i]
                model = example['model_id']
                assert model == M_ID
                id = example['id']
                summary = example['decoded']
                article = example['text']
                # get scores
                prompt = eval_aspects(ASPECT_ID, summary, article, eval_results_dir)
                prompts.append(prompt)
                ids.append(id)

            responses = llm_gen(prompts)
            for _id, prompt, resp in zip(ids, prompts, responses):
                obj = {"id": _id, "resp": resp}
                f0.write(json.dumps(obj, ensure_ascii=False) + "\n")


logger.info(f'out: {eval_dir}')

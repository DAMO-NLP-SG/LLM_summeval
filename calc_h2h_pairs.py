import json
import os
from tqdm import tqdm
from tabulate import tabulate
from utils import extract_choice
import argparse

###### const #########
model_pairs = [("M22","M23"), ("M23","M17"),("M17","M12"),("M12","M13"), ("M13","M15"), ("M15","M14"), ("M14","M8"),("M8","M9"), ("M9","M10"), ("M10","M20"),("M20","M11")]
source_data_dir = "comp_data"
res_root_dir = "comp_res"

id2dim = {
    0:"relevance",
    1:"consistency",
    2:"fluency",
    3:"coherence"
}

########### helper functions ############
def add_score(ans, score1, score2):
    if ans == 0:
        score1 += 0.5
        score2 += 0.5
    elif ans == 1:
        score1 += 1
    elif ans == 2:
        score2 += 1
    return score1, score2

def prep_result(file_path, toggle=False):
    res_dict = {}
    human_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        dataset = [json.loads(line) for line in f]
        for data in dataset:
            score1 = data["human_score_1"]
            score2 = data["human_score_2"]
            choice = extract_choice(data["resp"], toggle)
            id = data["id"]
            res_dict[id] = choice 

            # get human scores
            if score1 == score2:
                human_res = 0 # equal
            elif score1 > score2:
                human_res = 1 # larger
            else:
                human_res = 2 # smaller
            human_dict[id] = human_res
    assert set(res_dict.keys()) == set(human_dict.keys())

    return res_dict, human_dict

def parse_arguments(parser):
    ###Eval Hyperparameters
    # NOTE: "gpt-3.5-turbo-0301" may be deprecated, change to latest api model
    # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
    parser.add_argument('--eval_model', type=str, default="GPT-3.5-Turbo-0301", help="the ChatGPT model to use")
    
    args = parser.parse_args()
    for k in args.__dict__:
        print(k + ": " + str(args.__dict__[k]))
    return args


########################


def main():
    parser = argparse.ArgumentParser()
    config = parse_arguments(parser)
    eval_model = config.eval_model
    res_dir = os.path.join(res_root_dir, eval_model)

    all_stats = [["model pairs", 'coherence','consistency', 'fluency', 'relevance']]
    for model_1, model_2 in model_pairs:
        all_stats.append([model_1+"-"+model_2])
    all_stats.append(["total"])

    for dim in ['coherence','consistency', 'fluency', 'relevance']:
        correct_pairs = 0 
        total_pairs = 0
        for idx, (model_1, model_2) in enumerate(model_pairs):
            row_idx = idx + 1
            # print(f"eval {model_1}-{model_2}, {dim}")

            file_path = os.path.join(res_dir, model_1+"-"+model_2+"_" + dim +".result") 
            res_dict, true_dict = prep_result(file_path, toggle=False)
            toggle_file_path = os.path.join(res_dir, model_1+"-"+model_2+"_" + dim +"_toggle.result")
            toggle_res_dict, _ = prep_result(toggle_file_path, toggle=True)
            assert set(res_dict.keys()) == set(toggle_res_dict.keys())
            
            # convert to h2h scores
            human_score_1 = 0
            human_score_2 = 0
            llm_score_1 = 0
            llm_score_2 = 0

            
            for key in true_dict.keys():
                truth = true_dict[key]
                human_score_1, human_score_2 = add_score(truth, human_score_1, human_score_2)

                res = res_dict[key]
                llm_score_1, llm_score_2 = add_score(res, llm_score_1, llm_score_2)

                toggle_res = toggle_res_dict[key]
                llm_score_1, llm_score_2 = add_score(toggle_res, llm_score_1, llm_score_2)
            
            # get the average of the two
            llm_score_1 /= 2
            llm_score_2 /= 2

            total_pairs += 1
            if llm_score_1 > 50 and human_score_1 > 50:
                correct_pairs += 1
            elif llm_score_1 == 50 and human_score_1 == 50:
                correct_pairs += 1
            elif llm_score_1 < 50 and human_score_1 < 50:
                correct_pairs += 1
            all_stats[row_idx].append(f"{llm_score_1}/{human_score_1}")
        all_stats[-1].append(f"{correct_pairs}/{total_pairs}")

    print(tabulate(all_stats))


if __name__ == "__main__":
    main()
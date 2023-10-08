import json
import os
from tqdm import tqdm
from tabulate import tabulate
import argparse

###### const #########
M_ID_list = ["M8","M9","M10","M11","M12","M13","M14","M15","M17","M20","M22","M23"]
model_pairs = [("M22","M23"), ("M23","M17"),("M17","M12"),("M12","M13"), ("M13","M15"), ("M15","M14"), ("M14","M8"),("M8","M9"), ("M9","M10"), ("M10","M20"),("M20","M11")]
auto_metrics = ['rouge1_f', 'rouge2_f', 'rougel_f', 'bert_score_f', 'bart_score_src_hypo', 'bart_score_cnn_src_hypo', 'bart_score_para_src_hypo']

id2dim = {
    0:"relevance",
    1:"consistency",
    2:"fluency",
    3:"coherence"
}

########### helper functions ############
def add_to_score(score1, score2, total_score1, total_score2, larger_is_better=True):
    if score1 == score2:
        total_score1 += 0.5
        total_score2 += 0.5
    elif score1 > score2:
        if larger_is_better:
            total_score1 += 1
        else:
            total_score2 += 1
    elif score1 < score2:
        if larger_is_better:
            total_score2 += 1
        else:
            total_score1 += 1

    return total_score1, total_score2

def if_correct_pair_count(model_1, model_2, dim, metric, data):
    correct = False
    document_ids = data.keys()
    llm_score_1 = 0
    llm_score_2 = 0
    human_score_1 = 0
    human_score_2 = 0

    if metric == "MCQ" or metric == "RTS":
        metric = dim+"_"+metric.lower()
    for id in document_ids:
        score1 = float(data[id]['sys_summs'][model_1]["scores"][metric])
        score2 = float(data[id]['sys_summs'][model_2]["scores"][metric])
        truth1 = float(data[id]['sys_summs'][model_1]["scores"][dim])
        truth2 = float(data[id]['sys_summs'][model_2]["scores"][dim])
        llm_score_1, llm_score_2 = add_to_score(score1, score2, llm_score_1, llm_score_2)
        human_score_1, human_score_2 = add_to_score(truth1, truth2, human_score_1, human_score_2)

    assert llm_score_1 + llm_score_2 == 100
    assert human_score_1 + human_score_2 == 100

    if llm_score_1 > 50 and human_score_1 > 50:
        return True 
    elif llm_score_1 < 50 and human_score_1 < 50:
        return True
    elif llm_score_1 == 50 and human_score_1 == 50:
        return True
                
    return False

def parse_arguments(parser):
    ###Eval Hyperparameters
    # NOTE: "gpt-3.5-turbo-0301" may be deprecated, change to latest api model
    # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
    parser.add_argument('--eval_model', type=str, default="GPT-3.5-Turbo-0301", help="the ChatGPT model to use")
    parser.add_argument('--model_pair_type', type=int, default=0, choices=[0,1], help="0: full set; 1: challenge set")
    parser.add_argument('--add_rts_res', action="store_true", default=False, help="whether to calculate for RTS method of the model")
    parser.add_argument('--add_mcq_res', action="store_true", default=False, help="whether to calculate for MCQ method of the model")

    args = parser.parse_args()
    for k in args.__dict__:
        print(k + ": " + str(args.__dict__[k]))
    return args

########################
def main():
    parser = argparse.ArgumentParser()
    config = parse_arguments(parser)
    eval_model = config.eval_model
    model_pair_type = config.model_pair_type
    data_path = "summeval_"+eval_model+".json"

    if config.add_rts_res:
        auto_metrics.append("RTS")
    if config.add_mcq_res:
        auto_metrics.append("MCQ")

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stats = [["metric"]]
    for metric in auto_metrics:
        stats.append([metric])

    for dim in ['coherence','consistency', 'fluency', 'relevance']:
        stats[0].append(dim)
        for metric in auto_metrics:
            tcp = 0
            total = 0
            row_idx = auto_metrics.index(metric) + 1

            total_correct_pairs = 0
            total_pairs = 0

            if model_pair_type == 0:
                for i in range(len(M_ID_list)):
                    for j in range(i+1, len(M_ID_list)):
                        model_1 = M_ID_list[i]
                        model_2 = M_ID_list[j]
                        tcp += if_correct_pair_count(model_1, model_2, dim, metric, data)
                        total += 1
            else:
                for model_1, model_2 in model_pairs:
                    tcp += if_correct_pair_count(model_1, model_2, dim, metric, data)
                    total += 1

            stats[row_idx].append(f"{tcp}/{total}")

    print(tabulate(stats))

if __name__ == "__main__":
    main()


            
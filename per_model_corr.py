from scipy.stats import pearsonr, spearmanr, kendalltau
import json
import argparse
import os
from tabulate import tabulate


###### const #########

M_ID_LIST = ["M8","M9","M10","M11","M12","M13","M14","M15","M17","M20","M22","M23"]


postfix_dict = {
    0: "_rts",
    1: "_mcq",
    2: "_stareval"
}

########### helper functions ############

def parse_arguments(parser):
    ###Eval Hyperparameters
    # NOTE: "gpt-3.5-turbo-0301" may be deprecated, change to latest api model
    # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301

    parser.add_argument('--eval_model', type=str, default="GPT-3.5-Turbo-0301", help="the ChatGPT model used")
    parser.add_argument('--eval_type', type=int, default=0, choices = [0,1,2], help="evaluation method, 0 for rts, 1 for mcq, 2 for stareval")

    args = parser.parse_args()
    for k in args.__dict__:
        print(k + ": " + str(args.__dict__[k]))
    return args

def main():
    parser = argparse.ArgumentParser()
    config = parse_arguments(parser)
    eval_model = config.eval_model
    eval_type_id = config.eval_type
    data_path = "summeval_"+ eval_model+".json"
    if not os.path.exists(data_path):
        print(f"please prepare file {data_path} first.")
        exit()

    postfix = postfix_dict[eval_type_id]

    corr_val_table = [["Candidate"]]
    corr_sig_table = [["Candidate"]]
    for M_ID in M_ID_LIST:
        corr_val_table.append([M_ID])
        corr_sig_table.append([M_ID])

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for dim in ['coherence','consistency', 'fluency', 'relevance']:
        corr_val_table[0]+= [dim+"_S", dim+"_P", dim+"_K"]
        corr_sig_table[0]+= [dim+"_S", dim+"_P", dim+"_K"]
        
        for M_ID in M_ID_LIST:
            row_idx = M_ID_LIST.index(M_ID)+1

            human_score = []
            pred_score = []

            for id in data.keys(): # this ensures the same article scores are paird
                human_score.append(data[id]['sys_summs'][M_ID]['scores'][dim])
                pred_score.append(data[id]['sys_summs'][M_ID]['scores'][dim + postfix])

            s_corr = spearmanr(human_score,pred_score)
            p_corr = pearsonr(human_score,pred_score)
            k_corr = kendalltau(human_score,pred_score)

            corr_val_table[row_idx] += [round(s_corr[0], 3), round(p_corr[0], 3), round(k_corr[0], 3)]
            corr_sig_table[row_idx].append("*" if s_corr[1] < 0.05 else "")
            corr_sig_table[row_idx].append("*" if p_corr[1] < 0.05 else "")
            corr_sig_table[row_idx].append("*" if k_corr[1] < 0.05 else "")

    print(f"per model corr values")
    print(tabulate(corr_val_table))

    print(f"per model corr significance: * for p < 0.05")
    print(tabulate(corr_sig_table))

            

if __name__ == "__main__":
    main()
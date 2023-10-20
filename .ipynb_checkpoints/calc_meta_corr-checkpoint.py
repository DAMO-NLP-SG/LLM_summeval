from scipy.stats import pearsonr, spearmanr, kendalltau
import json
import argparse
import os
from tabulate import tabulate
import math

###### const #########

M_ID_LIST = ["M8","M9","M10","M11","M12","M13","M14","M15","M17","M20","M22","M23"]
auto_metrics = ['rouge1_f', 'rouge2_f', 'rougel_f', 'bert_score_f', 'bart_score_src_hypo', 'bart_score_cnn_src_hypo', 'bart_score_para_src_hypo']


postfix_dict = {
    0: "_rts",
    1: "_mcq",
    2: "_stareval",
    3: "_altrts",
    4: "_altmcq"
}

########### helper functions ############

def parse_arguments(parser):
    ###Eval Hyperparameters
    # NOTE: "gpt-3.5-turbo-0301" may be deprecated, change to latest api model
    # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301

    parser.add_argument('--eval_model', type=str, default="GPT-3.5-Turbo-0301", help="the ChatGPT model used")
    parser.add_argument('--eval_type', type=int, default=0, choices = [0,1,2,3,4], help="evaluation method, 0 for rts, 1 for mcq, 2 for stareval")

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
    auto_metrics.append(eval_model)

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # add row and column headings
    meta_corr_val_table = [["Metric"]]
    meta_corr_sig_table = [["Metric"]]
    for metric in auto_metrics:
        meta_corr_val_table.append([metric])
        meta_corr_sig_table.append([metric])

    for dim in ['coherence','consistency', 'fluency', 'relevance']:
        meta_corr_val_table[0]+= [dim+"_S", dim+"_P", dim+"_K"]
        meta_corr_sig_table[0]+= [dim+"_S", dim+"_P", dim+"_K"]

        human_metric = dim



        for metric in auto_metrics:
            if metric == eval_model:
                metric = dim + postfix 
                row_idx = auto_metrics.index(eval_model)+1
            else:
                row_idx = auto_metrics.index(metric)+1

            s_correlations = []
            p_correlations = []
            k_correlations = []
            human_avgs = []
            target_scores = {}
            global_target_scores = {}
            prediction_scores = {}

            for doc_id in data:
                sys_summs = data[doc_id]['sys_summs']
                for sys_name in M_ID_LIST:
                    if sys_name in target_scores:
                        prediction_scores[sys_name].append(float(sys_summs[sys_name]['scores'][metric]))
                        global_target_scores[sys_name].append(float(sys_summs[sys_name]['scores'][human_metric]))
                        target_scores[sys_name].append(float(sys_summs[sys_name]['scores'][human_metric]))
                    else:
                        prediction_scores[sys_name] = [float(sys_summs[sys_name]['scores'][metric])]
                        global_target_scores[sys_name] = [float(sys_summs[sys_name]['scores'][human_metric])]
                        target_scores[sys_name] = [float(sys_summs[sys_name]['scores'][human_metric])]
                    
            for sys_name in M_ID_LIST: # if we look at abstractive systems only
                s_corr = spearmanr(target_scores[sys_name], prediction_scores[sys_name])[0]
                p_corr = pearsonr(target_scores[sys_name], prediction_scores[sys_name])[0]
                k_corr = kendalltau(target_scores[sys_name], prediction_scores[sys_name])[0]
                # only add for meta_corr array if is number
                if not math.isnan(s_corr) and not math.isnan(p_corr) and not math.isnan(k_corr):
                    s_correlations.append(s_corr)
                    p_correlations.append(p_corr)
                    k_correlations.append(k_corr)
       
                    avg = sum(global_target_scores[sys_name])/len(global_target_scores[sys_name])
                    human_avgs.append(avg)
            
            s_meta = spearmanr(s_correlations, human_avgs)
            p_meta = pearsonr(p_correlations, human_avgs)
            k_meta = kendalltau(k_correlations, human_avgs)
            meta_corr_val_table[row_idx] += [round(s_meta[0], 3), round(p_meta[0], 3), round(k_meta[0], 3)]
            meta_corr_sig_table[row_idx].append("*" if s_meta[1] < 0.05 else "")
            meta_corr_sig_table[row_idx].append("*" if p_meta[1] < 0.05 else "")
            meta_corr_sig_table[row_idx].append("*" if k_meta[1] < 0.05 else "")



    print(f"meta-corr values")
    print(tabulate(meta_corr_val_table))

    print(f"meta-corr significance: * for p < 0.05")
    print(tabulate(meta_corr_sig_table))

            

if __name__ == "__main__":
    main()


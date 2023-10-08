from scipy.stats import pearsonr, spearmanr, kendalltau
import json
import argparse
import os

 
###### const #########

M_ID_LIST = ["M8","M9","M10","M11","M12","M13","M14","M15","M17","M20","M22","M23"]

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

    print(f"Evaluated model: {eval_model}")
    for dim in ["coherence", "consistency", "fluency", "relevance"]:
        human_metric = dim
        auto_metric= dim + postfix
        print(f'Human metric: {human_metric}')
        print(f'Model metric: {auto_metric}')

        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        target_scores = []
        prediction_scores = []
        for doc_id in data:

            sys_summs = data[doc_id]['sys_summs']

            for sys_name in M_ID_LIST: # ONLY CONSIDER abstractive ones
                pred = float(sys_summs[sys_name]['scores'][auto_metric])
                targ = float(sys_summs[sys_name]['scores'][human_metric])
                prediction_scores.append(pred)
                target_scores.append(targ)

        s_corr = spearmanr(target_scores, prediction_scores)
        print(s_corr)
        p_corr = pearsonr(target_scores, prediction_scores)
        print(p_corr)
        k_corr = kendalltau(target_scores, prediction_scores)
        print(k_corr)

if __name__ == "__main__":
    main()
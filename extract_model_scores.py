import json
import os
from utils import extract_score_rts, extract_score_stareval, extract_score_mcq
import argparse

###### const #########
M_ID_LIST = ["M8","M9","M10","M11","M12","M13","M14","M15","M17","M20","M22","M23"]
annotation_dir = "model_output_annotations"
eval_root_dir = "eval_model_generations"
if not os.path.exists(eval_root_dir):
    os.mkdir(eval_root_dir)

def parse_arguments(parser):
    ###Eval Hyperparameters
    # NOTE: "gpt-3.5-turbo-0301" may be deprecated, change to latest api model
    # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
    parser.add_argument('--eval_model', type=str, default="gpt-3.5-turbo-0301", help="the evaluator model")

    args = parser.parse_args()
    for k in args.__dict__:
        print(k + ": " + str(args.__dict__[k]))
    return args

def main():
    parser = argparse.ArgumentParser()
    config = parse_arguments(parser)
    eval_model = config.eval_model
    eval_dir = os.path.join(eval_root_dir, eval_model)
    if not os.path.exists(eval_dir):
        print(f"cannot find {eval_dir}, cannot process")
        exit()
        
    data_file_name = "summeval_"+eval_model.strip()+".json"


    eval_results_paths = {
        0: "relevance",
        1: "consistency",
        2: "fluency",
        3: "coherence"
    }

    postfix_dict = {
        0: "_rts",
        1: "_mcq",
        2: "_stareval",
        3: "_altrts",
        4: "_altmcq",
    }

    utils_dict = {
        0: extract_score_rts,
        1: extract_score_mcq,
        2: extract_score_stareval,
        3: extract_score_rts,
        4: extract_score_mcq,
    }


    with open('summeval.json', 'r', encoding='utf-8') as f:
        full_data = json.load(f)

    for M_ID in M_ID_LIST:
        print(M_ID)
        eval_results_dir = os.path.join(eval_dir,"eval_"+M_ID+"_generations")
        
        for i in range(4):
            for eval_type_id in range(len(postfix_dict.keys())):
                postfix = postfix_dict[eval_type_id]
                extract_score = utils_dict[eval_type_id]
                file_path = os.path.join(eval_results_dir, eval_results_paths[i]+postfix+".txt")
                if os.path.exists(file_path):
                    print("extracting marks from: ", file_path)
                    key = eval_results_paths[i]+postfix
                    with open(file_path, "r") as fd:
                        objs = [json.loads(line) for line in fd]
                        for line in objs:
                            resp = line['resp']
                            score = extract_score(resp)
                            id = line['id']
                            assert id in full_data
                            assert M_ID in full_data[id]["sys_summs"]
                            full_data[id]["sys_summs"][M_ID]["scores"][key] = score

    with open(data_file_name,"w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()
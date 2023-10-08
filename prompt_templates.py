id2asp = {
    0:"relevance",
    1:"consistency",
    2:"fluency",
    3:"coherence"
}


def prepare_rts_prompt(aspect_id, summary, article=None): # my own prompts
    assert aspect_id in range(4)

    if aspect_id == 0:
        prompt = f'Score the following Summary given the corresponding Article with respect to relevance from one to five, where one indicates "irrelevance", and five indicates "perfect relevance". Note that relevance measures the Summary\'s selection of important content from the Article, whether the Summary grasps the main message of the Article without being overwhelmed by unnecessary or less significant details.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score:'
        return prompt
    
    if aspect_id == 1:
        prompt = f'Score the following Summary given the corresponding Article with respect to consistency from one to five, where one indicates "inconsistency" and five indicates "perfect consistency". Note that consistency measures the factual alignment between the Summary and the Article, whether the Summary is faithful to the Article without introducing contradictions or misleading representations.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score:'
        return prompt

    if aspect_id == 2: 
        prompt = f'Score the following Summary given the corresponding Article with respect to fluency from one to five, where one indicates "disfluency" and five indicates "perfect fluency". Note that fluency measures the quality of individual sentences in the Summary, whether the Summary is well-written, grammatically correct, and readable on the sentence level.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score:'
        return prompt

    if aspect_id == 3:
        prompt = f'Score the following Summary given the corresponding Article with respect to coherence from one to five, where one indicates "incoherence" and five indicates "perfect coherence". Note that coherence measures the collective quality of the Summary, whether the Summary presents information that flows smoothly and avoids abrupt transitions or disjoint statements.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score:'
        return prompt


def prepare_mcq_prompt(aspect_id, summary, article=None):
    if aspect_id == 0:
        prompt = f'Choose an option from A to E in order to score the following Summary given the corresponding Article with respect to relevance from one to five, where one indicates "irrelevance", and five indicates "perfect relevance". Note that relevance measures the Summary\'s selection of important content from the Article, whether the Summary grasps the main message of the Article without being overwhelmed by unnecessary or less significant details.\n\nArticle: {article}\n\nSummary: {summary}\n\nA: The Summary is totally irrelevant to the Article. Score: One.\nB: The majority of the Summary is irrelevant to the Article. Score: Two.\nC: Some information in the Summary is relevant to the Article whereas some are not. Score: Three.\nD: The majority of the Summary is relevant to the Article. Score: Four.\nE: All information included in the Summary is relevant to the Article. Score: Five.\n\nYour Answer (enter 1 letter from A to E):'
        return prompt

    if aspect_id == 1:
        prompt = f'Choose an option from A to E in order to score the following Summary given the corresponding Article with respect to consistency from one to five, where one indicates "inconsistency" and five indicates "perfect consistency". Note that consistency measures the factual alignment between the Summary and the Article, whether the Summary is faithful to the Article without introducing contradictions or misleading representations.\n\nArticle: {article}\n\nSummary: {summary}\n\nA: The Summary is totally inconsistent with the Article. Score: One.\nB: The majority of the Summary is inconsistent with the Article. Score: Two.\nC: Some information in the Summary is consistent with the Article whereas some are not. Score: Three.\nD: The majority of the Summary is consistent with the Article. Score: Four.\nE: All information included in the Summary is consistent with the Article. Score: Five.\n\nYour Answer (enter 1 letter from A to E):'
        return prompt


    if aspect_id == 2: 
        prompt = f'Choose an option from A to E in order to score the following Summary given the corresponding Article with respect to fluency from one to five, where one indicates "disfluency" and five indicates "perfect fluency". Note that fluency measures the quality of individual sentences in the Summary, whether the Summary is well-written, grammatically correct, and readable on the sentence level.\n\nArticle: {article}\n\nSummary: {summary}\n\nA: The Summary is totally disfluent. Score: One.\nB: The majority of the Summary is disfluent. Score: Two.\nC: Some sentences in the Summary are fluent whereas some are not. Score: Three.\nD: The majority of the Summary is fluent. Score: Four\nE: All sentences in the Summary are fluent. Score: Five.\n\nYour Answer (enter 1 letter from A to E):'
        return prompt
    
    if aspect_id == 3:
        prompt = f'Choose an option from A to E in order to score the following Summary given the corresponding Article with respect to coherence from one to five, where one indicates "incoherence" and five indicates "perfect coherence". Note that coherence measures the collective quality of the Summary, whether the Summary presents information that flows smoothly and avoids abrupt transitions or disjoint statements.\n\nArticle: {article}\n\nSummary: {summary}\n\nA: The Summary is completely incoherent. Score: One.\nB: The Summary is mostly incoherent. Score: Two.\nC: The Summary is somewhat coherent. Score: Three.\nD: The Summary is mostly coherent. Score: Four.\nE: The Summary is completely coherent. Score: Five.\n\nYour Answer (enter 1 letter from A to E):'
        return prompt


    
def prepare_comp_prompt_mcq(aspect_id, summ1, summ2, article=None):
    if aspect_id == 0:
        prompt = f'Choose a more relevant summary from Summary #1 and Summary #2 with respect to the corresponding Article by choosing an option from A, B, or C. Note that relevance measures the summary\'s selection of important content from the Article, whether the summary grasps the main message of the Article without being overwhelmed by unnecessary or less significant details.\n\nArticle: {article}\n\nSummary #1: {summ1}\n\nSummary #2: {summ2}\n\nA: Summary #1 is more relevant.\nB: Summary #2 is more relevant.\nC: Both Summary #1 and Summary #2 are equally relevant.\n\nYour choice (enter 1 letter from A to C):'
        return prompt
    
    if aspect_id == 1:
        prompt = f'Choose a more consistent summary from Summary #1 and Summary #2 with respect to the corresponding Article by choosing an option from A, B, or C. Note that consistency measures the factual alignment between the summary and the Article, whether the summary is faithful to the Article without introducing contradictions or misleading representations.\n\nArticle: {article}\n\nSummary #1: {summ1}\n\nSummary #2: {summ2}\n\nA: Summary #1 is more consistent.\nB: Summary #2 is more consistent.\nC: Both Summary #1 and Summary #2 are equally consistent.\n\nYour choice (enter 1 letter from A to C):'
        return prompt

    if aspect_id == 2:
        prompt = f'Choose a more fluent summary from Summary #1 and Summary #2 with respect to the corresponding Article by choosing an option from A, B, or C. Note that fluency measures the quality of individual sentences in the summary, whether the summary is well-written, grammatically correct, and readable on the sentence level.\n\nArticle: {article}\n\nSummary #1: {summ1}\n\nSummary #2: {summ2}\n\nA: Summary #1 is more fluent.\nB: Summary #2 is more fluent.\nC: Both Summary #1 and Summary #2 are equally fluent.\n\nYour choice(enter 1 letter from A to C):'
        return prompt

    
    if aspect_id == 3:
        prompt = f'Choose a more coherent summary from Summary #1 and Summary #2 with respect to the corresponding Article by choosing an option from A, B, or C. Note that coherence measures the collective quality of the summary, whether the summary presents information that flows smoothly and avoids abrupt transitions or disjoint statements.\n\nArticle: {article}\n\nSummary #1: {summ1}\n\nSummary #2: {summ2}\n\nA: Summary #1 is more coherent.\nB: Summary #2 is more coherent.\nC: Both Summary #1 and Summary #2 are equally coherent.\n\nYour choice(enter 1 letter from A to C):'
        return prompt
    

def prepare_alt_rts_prompt(aspect_id, summary, article=None):
    if aspect_id == 0:
        prompt = f'Score the following Summary given the corresponding Article with respect to relevance from 1 to 5. Note that relevance measures the Summary\'s selection of important content from the Article. 5 points indicate all information included in the Summary are important and non-trivial to the Article.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score:'
        return prompt
    
    if aspect_id == 1:
        prompt = f'Score the following Summary given the corresponding Article with respect to consistency from 1 to 5. Note that consistency measures the factual alignment between the Summary and the Article. 5 points indicate all statements in the Summary are well-supported by the given Article.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score:'
        return prompt

    if aspect_id == 2: 
        prompt = f'Score the following Summary given the corresponding Article with respect to fluency from 1 to 5. Note that fluency measures the quality of individual sentences. 5 points indicate all sentences in the Summary are well-written and grammatically correct.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason in one sentence, then give a final score:'
        return prompt
    
    if aspect_id == 3:
        prompt = f'Score the following Summary given the corresponding Article with respect to coherence from 1 to 5. Note that coherence measures the collective quality of the Summary. 5 points indicate the Summary build smoothly to a coherent body of information on a focused topic.\n\nArticle: {article}\n\nSummary: {summary}\n\nProvide your reason then give a final score: '
        return prompt


def prepare_alt_mcq_prompt(aspect_id, summary, article=None):
    if aspect_id == 0:
        prompt = f"Choose an option from A to E that gives a suitable score for the following Summary given the corresponding Article with respect to relevance. Note that relevance measures the Summary\'s selection of important content from the Article. \n\nArticle: {article}\n\nSummary: {summary}\n\nA: No information included in the Summary is relevant to the Article. The Summary is totally irrelevant to the Article. 1 point.\nB: Only a small portion of the Summary is relevant to the Article. The majority of the Summary is irrelevant to the Article. 2 points.\nC: Some information in the Summary is relevant to the Article whereas some are not. 3 points.\nD: The majority of the Summary is relevant to the Article. Only a small portion of the Summary is irrelevant to the Article. 4 points. \nE: All information included in the Summary are relevant to the Article. 5 points.\n\nYour Answer (enter 1 letter from A to E):"
        return prompt
      
    if aspect_id == 1:
        prompt = f"Choose an option from A to E that gives a suitable score for the following Summary given the corresponding Article with respect to consistency. Note that consistency measures the factual alignment between the Summary and the Article. \n\nArticle: {article}\n\nSummary: {summary}\n\nA: None of the statements in Summary is consistent with the Article. Summary is totally inconsisent with Article. 1 point.\nB: Only a small portion of the Summary is consistent with the Article. Summary still contains major inconsistenties with the Article. 2 points.\nC: Some portion of the Summary is consistent with the Article whereas some are not. 3 points.\nD: The majority of the Summary is consitent with the Article. The Summary only contains some minor inconsistenties with the Article. 4 points. \nE: All statements in the Summary are consistent with the Article. 5 points.\n\nYour Answer (enter 1 letter from A to E):"
        return prompt
    
    if aspect_id == 2:
        prompt = f"Choose an option from A to E that gives a suitable score for the following Summary given the corresponding Article with respect to fluency. Note that fluency measures the quality of individual sentences. \n\nArticle: {article}\n\nSummary: {summary}\n\nA: None of the sentences in the Summary are well-written and grammatically correct. All sentences are ungrammatical. 1 point. \nB: Only a few sentences in the Summary are well-written and grammatically correct. Most sentences are ungrammatical. 2 points.\nC: Some sentences are well-written and grammatically correct whereas some are not. 3 points.\nD: Most sentences are well-written and grammatically correct. Only a few sentences are ungrammatical. 4 points. \nE: All sentences in the Summary are well-written and grammatically correct. 5 points. \n\nYour Answer (enter 1 letter from A to E):"
        return prompt
    
    if aspect_id == 3:
        prompt = f"Choose an option from A to E that gives a suitable score for the following Summary given the corresponding Article with respect to coherence. Note that coherence measures the collective quality of the Summary.\n\nArticle: {article}\n\nSummary: {summary}\n\nA: The Summary is completely incoherent. It cannot build smoothly to a coherent body of information on a focused topic. 1 point.\nB: The Summary is mostly incoherent. To a large extent, it cannot build smoothly to a coherent body of information on a focused topic. 2 points.\nC: The Summary is somewhat coherent. To a certain extent, it builds smoothly to a coherent body of information on a focused topic. 3 points.\nD: The Summary is mostly coherent. To a large extent, it builds smoothly to a coherent body of information on a focused topic. 4 points. \nE: The Summary is completely coherent. It builds smoothly to a coherent body of information on a focused topic. 5 points. \n\nYour Answer (enter 1 letter from A to E):"
        return prompt

# prompt same in the paper: Is ChatGPT a Good NLG Evaluator? A Preliminary Study 
def prepare_stareval_prompt(aspect_id, generated_summ, article):

    if aspect_id == 0:
        prompt_summeval_relevance = """Score the following news summarization given the corresponding news with respect to relevance with one to five stars, where one star means "irrelevance" and five stars means "perfect relevance". Note that relevance measures how well the summary captures the key points of the article. Consider whether all and only the important aspects are contained in the summary.

News: %s
Summary: %s
Stars:
""" % (article, generated_summ)
        return prompt_summeval_relevance
    
    if aspect_id == 1:
        prompt_summeval_consistency = """Score the following news summarization given the corresponding news with respect to consistency with one to five stars, where one star means "inconsistency" and five stars means "perfect consistency". Note that consistency measures whether the facts in the summary are consistent with the facts in the original article. Consider whether the summary does reproduce all facts accurately and does not make up untrue information.

News: %s
Summary: %s
Stars:
""" % (article, generated_summ)
        return prompt_summeval_consistency
    
    if aspect_id == 2:
        prompt_summeval_fluency = """Score the following news summarization given the corresponding news with respect to fluency with one to five stars, where one star means "disfluency" and five stars means "perfect fluency". Note that fluency measures the quality of individual sentences, are they well-written and grammatically correct. Consider the quality of individual sentences.

News: %s
Summary: %s
Stars:
""" % (article, generated_summ)
        return prompt_summeval_fluency
    
    if aspect_id == 3:
        prompt_summeval_coherence = """Score the following news summarization given the corresponding news with respect to coherence with one to five stars, where one star means "incoherence" and five stars means "perfect coherence". Note that coherence measures the quality of all sentences collectively, to the fit together and sound naturally. Consider the quality of the summary as a whole.

News: %s
Summary: %s
Stars:
""" % (article, generated_summ)
        return prompt_summeval_coherence
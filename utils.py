import re

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
        
def extract_score_stareval(text):
    pattern = "([^\s]+)\sstar"
    match = re.search(pattern, text.lower())
    score = None
    text_list = ["one", "two", "three", "four","five"]
    if match:
        score_tmp = match.group(1)
        if isfloat(score_tmp):
            score = score_tmp
        elif score_tmp.strip() in text_list:
            score = text_list.index(score_tmp.strip())+1
    if not score:
        print(f"cannot extract score from resp: {text}")
    assert isfloat(score), f"{score} is not a number, from resp: {text}"
    return float(score)

def extract_score_rts(text):
    score_text_list = ["one", "two", "three", "four","five"]
    pattern = "score:\s*([1-5](?:\.\d)?)"
    match = re.search(pattern, text.lower())
    if match:
        score = match.group(1)
        return float(score)
    
    pattern = "score:\s*(one|two|three|four|five)"
    match = re.search(pattern, text.lower())
    if match:
        score_text = match.group(1)
        score = score_text_list.index(score_text) + 1
        return float(score)
    
    pattern = "(?:score|scoring)[^\.]+[1-5](?:\.\d)?" # find anywhere mention the score, before end of sentence
    match = re.search(pattern, text.lower()) # no case sensitivity
    if match:
        text = match.group(0) # could be "scoring a 2" or "scoring a 2 out of 5"
        score = re.search("[1-5](\.[1-5])?", text).group(0)
        return float(score)

    pattern = "(?:score|scoring)[^\.]+\s(one|two|three|four|five)[\s\.\,]"
    match = re.search(pattern, text.lower())
    if match:
        text = match.group(0)
        score_text = re.search("one|two|three|four|five", text).group(0)
        score = score_text_list.index(score_text)+1
        return float(score)
    
    pattern = "score of (one|two|three|four|five)[\s\.\,]"
    match = re.search(pattern, text.lower())
    if match:
        text = match.group(0)
        score_text = re.search("one|two|three|four|five", text).group(0)
        score = score_text_list.index(score_text)+1
        return float(score)
    
    # last resort, find last number
    pattern = "[1-5](?:\.\d\s)?(?:out of [1-5])?"
    match = re.findall(pattern, text.lower())
    if len(match) > 0:
        # print(text) # this may occur error, check these texts
        text = match[-1]
        score = re.search("[1-5](\.[1-5])?", text).group(0)
        return float(score)

    return -1 # cannot extract

def extract_score_mcq(text):
    text = text.strip()
    # print(text)
    letter2score = {
        "A":1,
        "B":2,
        "C":3,
        "D":4,
        "E":5
    }
    return letter2score[text]

def extract_choice(resp, toggle):
    # # type 0, 1, 2
    # choice = int(resp)
    # assert choice in [0, 1, 2], f"{resp} not in [0,1,2]"
    # return choice
    if len(resp.strip()) != 1:
        pattern = r"summary ([abc])"
        match = re.search(pattern, resp.lower())
        if match:
            resp = match.group(1)
            # print(f"found match in {pattern}: {resp}")
        else:
            pattern = r"^([abc])[\s.:]"
            match = re.search(pattern, resp.lower())
            if match:
                resp = match.group(1)
                # print(f"found match in {pattern}: {resp}")
            else:
                print(f"have trouble extracting: {resp}")

    if resp.upper() == "A":
        return 1 if not toggle else 2
    elif resp.upper() == "B":
        return 2 if not toggle else 1
    else:
        return 0

import pronouncing

def last_syllable(word):
    vowels = 'aeiouy'
    rev = word[::-1]
    idx = -1
    start = 0
    if rev.startswith('el') and len(rev) > 2 and rev[2] not in vowels:
        idx = 1
    elif rev.startswith('e'):
        start = 1
    if rev.startswith('sel') and len(rev) > 3 and rev[3] not in vowels:
        idx = 2
    elif rev.startswith('se'):
        start = 2
    if idx < 0:
        for i in range(start, len(rev)):
            if rev[i] in vowels:
                idx = i
                break
                
    if idx < 0:
        idx = len(rev)
        
    return rev[idx::-1]

def rhyme_score(line1, line2, alpha = 0.4):
    word1 = re.sub(r"\W+", '', line1.split(" ")[-1]).lower().strip(".:;?!")
    word2 = re.sub(r"\W+", '', line2.split(" ")[-1]).lower().strip(".:;?!")
    if word2 in pronouncing.rhymes(word1) or word1 in pronouncing.rhymes(word2):
        return 1
    elif last_syllable(word1) == last_syllable(word1):
        return alpha
'''
    some special case that help narrow the result_list
'''

def narrowResultList(result_list):
    letter1_list = [i[1] for i in result_list]
    letter_list = list(set(letter1_list))
    if 'E' in letter_list:
        return ['E']
    if ('8' in letter_list and 'S' not in letter_list) or 'B' in letter_list:
        return ['B']
    if 'R' in letter_list:
        return ['R']
    if 'S' in letter_list:
        return['S']
    if 'X' in letter_list and ('H' not in letter_list or 'I' not in letter_list):
        if 'K' in letter_list:
            return ['K', 'X']
        else:
            return['X']
    if 'D' in letter_list:
        return ['D']
    if 'J' in letter_list:
        return ['J']
    if 'F' in letter_list:
        if 'T' not in letter_list:
            return ['F']
        else:
            return ['F', 'T']
    if 'G' in letter_list:
        return ['G']
    if 'd' in letter_list or 'p' in letter_list or 'P' in letter_list:
        return ['P']
    if ('K' in letter_list or 'k' in letter_list) and ('H' not in letter_list or 'I' not in letter_list) and ('T' not in letter_list):
        if 'X' not in letter_list:
            return['K']
        else:
            return ['K', 'X']
    
    if 'Y' in letter_list: # unsure
        if 'T' not in letter_list:
            return['Y']
        else:
            return ['Y', 'T']

    if 'T' in letter_list:
        return ['T']
    if 'C' in letter_list:  #unsure
        if 'U' in letter_list:
            return ['U']
        elif 'S' in letter_list:
            return ['S']
        else:
            return ['C']
    if 'U' in letter_list:
        return ['U']
    if 'V' in letter_list or 'A' in letter_list:
        if ((letter1_list.count('N') / len(letter1_list)) <= 1/3): # if N is minority then it cannot be N
            if '4' in letter_list:
                return ['A']
            else:
                return ['A', 'V', 'L', '7']
    if 'H' in letter_list or 'I' in letter_list:
        return ['H']
    if 'M' in letter_list or 'W' in letter_list:
        return ['M', 'W']
    if 'N' in letter_list or 'Z' in letter_list:
        if ((letter1_list.count('V') / len(letter1_list)) <= 1/3): # if V is minority then it cannot be V
            return ['N', 'Z']
    if '0' in letter_list:   #unsure
        if 'Q' in letter_list:
            return ['Q']
        elif 'U' in letter_list:
            return ['U']
        else:
            return['O', '0', 'Q']
    
    # when all cases are failed
    return letter_list
    
        
    


    
    
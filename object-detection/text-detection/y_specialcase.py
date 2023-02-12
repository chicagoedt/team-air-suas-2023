'''
    Some special cases that easyocr has to deal with
    
'''


# the result is any of the following letters Z, N, z, 2 then it should be Z or N
caseZ_N_z = ['Z', 'N']

# the result is 0 then it could be Q, O, B, D
case0 = ['O', 'Q', 'B', 'D', 'C']

# the result is H or I, then it must be H
caseH_I = ['H'] 

# the result is 3, m then it must be E  
case3_m = ['E']

# the result is A or 4, then it must be A
caseA_4 = ['A']

# the result is V then it could be A or V 
caseV = ['A', 'V']

# the result is M, E, W, then it should be one of following M, E, or W
caseM_E_W = ['M', 'E', 'W']

# the result is p, d, P, then it must be P
caseP_p_d = ['P']

# the result is S, 9, 6, s then it must be S
caseS_9_6_s = ['S']

# the result is F, L, 7 then it could be F or L
caseF_L_7 = ['F', 'L']

# the result is 8, then it must be B
case8_B = ['B']


def specialCase(detectedLetter):
    if detectedLetter in ['Z', 'N', 'z', '2']:
        return caseZ_N_z
    elif detectedLetter in ['0']:
        return case0
    elif detectedLetter in ['H', 'I']:
        return caseH_I
    elif detectedLetter in ['3', 'm']:
        return case3_m
    elif detectedLetter in ['A', '4']:
        return caseA_4
    elif detectedLetter in ['V']:
        return caseV
    elif detectedLetter in ['M', 'E', 'W', 'm']:
        return caseM_E_W
    elif detectedLetter in ['P', 'd', 'p']:
        return caseP_p_d
    elif detectedLetter in ['S', '9', '6', 's']:
        return caseS_9_6_s
    elif detectedLetter in ['F', 'L', '7']:
        return caseF_L_7
    elif detectedLetter in ['8', 'B']:
        return case8_B
    else:
        return [detectedLetter]






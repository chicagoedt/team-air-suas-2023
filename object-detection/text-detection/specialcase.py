'''
    Some special cases that easyocr has to deal with
    
'''


# case with Z and N and z
caseZ_N = ['Z', 'N', 'z']

# case with 0 and O and Q
case0_O_Q = ['0', 'O', 'Q']

# case with H and I: if the model detects to 'H', then it could be H or I
caseH_I = ['H', 'I'] 

# case with A and 4
caseA_4 = ['A', '4']

# case with M and E and W and m
caseM_E_W = ['M', 'E', 'W', 'm']

# case with P and p and d: if the model detects p or d or P, the answer is P
caseP_p_d = ['P', 'p', 'd']

# case with S and 9 and 6: if the model detects s or 9 or 6
caseS_9_6 = ['S', '9', '6', 's']

# case with D as 0: if the result is D, it must be D. but if the result is 0, it could be D or 0
caseD_0 = ['D', '0']

# case with F as L 
caseF_L = ['F', 'L']

# case with never detecting an I

# case with cannot detecting an O but sometimes detect it as 0 ->>> ???


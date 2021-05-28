from fractions import Fraction as frac

def comb(N, k):
    C = 1
    if N < 0 or k < 0 or N < k:
        raise ValueError
    if k == 0 or N == 0:
        return C
    C *= comb(N, k-1)*(frac(N-k+1)/k) if k != 1 else N
    return int(C)

def normalize(B, A):
    f = A[0]
    num = [n / f for n in B]
    den = [d / f for d in A]
    k = num[0]
    num = [n / k for n in num]
    
    return num, den, k

def bilinear(B, A, fs = 1):
    N = len(B) - 1
    D = len(A) - 1
    M = max([N, D])
    Bp = [0 for i in range(M + 1)]
    Ap = [0 for i in range(M + 1)]

    # Calculate Coeffs for A
    for j in range(0, M + 1):
        val = 0.0
        for i in range(0, N + 1): # i to loop over original coefficients 
            # Loop and calculate coeff of z^-i from binomial expansions
            for k in range(0, i + 1):
                for l in range(0, M - i + 1):
                    if k + l == j:
                        val += B[i] * (2**i) * (fs**i) * comb(i, k) * ((-1)**k) * comb(M-i, l)
        Bp[j] = val
    
    # Calculate Coeffs for B
    for j in range(0, M + 1):
        val = 0.0
        for i in range(0, D + 1): # i to loop over original coefficients
            # Loop and calculate coeff of z^-i from binomial expansions
            for k in range(0, i + 1):
                for l in range(0, M - i + 1):
                    if k + l == j:
                        val += A[D - i] * (2**i) * (fs**i) * comb(i, k) * ((-1)**k) * comb(M-i, l)
        Ap[j] = val

    Bp, Ap, k = normalize(Bp, Ap)
    return Bp + Ap, k

def bilinear_sos(sos, fs):
    ret = []
    gain = 1
    for section in sos:
        B = list(section[0:3])
        A = list(section[3:])
        c, k = bilinear(B, A, fs)
        ret.append(c)
        gain *= k
    ret.reverse()
    ret[0] = [ret[0][i] * (gain if i < 3 else 1) for i in range(6)]
    return ret
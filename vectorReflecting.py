# 하... 반사벡터를 구해보자
# 반사벡터구하기 모듈

from sympy import Symbol, solve, Eq

def getVerticalVector(v1):
    v2=[-v1[1],v1[0]]
    return v2

def getReflectedVector(slope, inVector):
    # 연립방정식 계수
    s = Symbol('s')
    t = Symbol('t')

    # inVector는 입사벡터
    outVector=[] # 반사벡터
    uVector=getVerticalVector(slope)

    # -입사벡터=s*slope=t*uVector
    e1 = Eq((-1)*inVector[0], s*slope[0]+t*uVector[0])
    e2 = Eq((-1)*inVector[1], s*slope[1]+t*uVector[1])

    result=solve([e1, e2], s,t)
    tValue=float(result[t])
    # print(tValue)
    outVector.append(inVector[0]+2*tValue*uVector[0])
    outVector.append(inVector[1]+2*tValue*uVector[1])

    #반사벡터를 리턴
    return outVector

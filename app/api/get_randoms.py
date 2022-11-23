import os
import math
import random
from pathlib import Path
import pandas as pd
import dataframe_image as dfi
"""
계수(seed)값이나 점화식 연산 시 생성되는 난수들이 아닌 최종 난수만 리턴하는 모듈입니다. (실전용)
"""

BASE_DIR = Path(__file__).resolve().parent.parent
root = os.path.abspath(BASE_DIR.parent)
images = os.path.join(root, "static/images")

def get_1_or_0() -> int:
    return int(round(random.random(), 0))

def get_random_element(_list: list) -> int or str:
    # get_1_or_0()을 활용한 리스트 원소 랜덤 추출 함수
    
    if len(_list) == 1:
        return _list[0]
    
    elif len(_list) == 0:
        raise ValueError("List is empty.")
    
    else:
        _randoms: list = []
        while len(_randoms) != 1:
            for elm in _list:
                if get_1_or_0() == 1:
                    _randoms.append(elm)
                    
            if len(_randoms) > 1:
                _list = _randoms
                _randoms = []
        
        return _randoms[0]

def get_increment(m: int, max_iters: int = 10 ** 6) -> int:
    """
    c(increment)값 결정
        - c와 m은 서로소 (0<= c < m)
        
    * max_iters: 연산 횟수가 10 ** 6 초과 되는것을 방지
    """
    
    flag: bool = False
    coprime: int = 1
    coprimes: list = []
    for i in range(2, m):
        if math.gcd(m, i) == 1:
            # get random 1 or 0
            # 1일 때만 곱하기
            if get_1_or_0() == 1:
                coprimes.append(i)
                coprime *= i
        
                # 계수 크기 조정
                while coprime >= m:
                    _coprime = get_random_element(coprimes)
                    coprime //= _coprime
                    flag = True
        if flag:
            break
        if i > max_iters:
            # 최대 연산 횟수 초과시 m-1로 재연산
            coprime = get_increment(m-1)
            return coprime
        
    return coprime

def get_multiplier(m: int, max_iters: int = 10 ** 6) -> int:
    """
    a(multiplier)값 결정
        - m이 4의 배수이면 a-1도 4의 배수
        - a-1은 m의 모든 소인수*로 나누어 떨어짐
        * 연산 시간 문제와 계수 예측을 막기 위해 소인수 전체집합의 부분집합의 곱으로 설정함
        (get_1_or_0 함수를 통해 랜덤하게 구함)
        
    * max_iters: 연산 횟수가 10 ** 6 초과 되는것을 방지
    """
    m_org = m
    
    # b = a - 1
    # 4의 배수 조건 체크
    if m % 4 == 0:
        b = 4
        m //= 4
    else:
        b = 1

    factor: int = 2
    factors: list = []
    while factor**2 <= m:
        # b값 설정: 소인수 분해
        while m % factor == 0:
            m = m // factor
            # get random 1 or 0
            # 1일 때만 곱하기
            if get_1_or_0() == 1:
                factors.append(factor)
                b *= factor
                # 계수 크기 조정
                while b >= m_org or b > max_iters:
                    _factor = get_random_element(factors)
                    b //= _factor
            
        factor += 1
        if factor > max_iters:
            # 최대 연산 횟수 초과시 m-1로 재연산
            a = get_multiplier(m-1)
            return a
        
    if m > 1:
        # get random 1 or 0
        # 1일 때만 곱하기
        if get_1_or_0() == 1:
            factors.append(m)
            b *= m
            # 계수 크기 조정
            while b >= m_org or b > max_iters:
                _factor = get_random_element(factors)
                b //= _factor    
                
    a = b + 1
    
    return a

def get_random(n: int, interations: int = None) -> int:
    """
    Linear congruential generator
        Recurrence Relation: Xn+1 = (a * Xn + c) % m
        c: increment, a: multiplier, m: modulus
        
        ** 주기가 최대가 되기위한 계수 조건 ** 
            - c와 n은 서로소 (0<= c < n) 
            - m이 4의 배수이면 a-1도 4의 배수
            - a-1은 m의 모든 소인수*로 나누어 떨어짐
                * 연산 시간 문제와 계수 예측을 막기 위해 소인수 전체집합의 부분집합의 곱으로 설정함
                  (get_1_or_0 함수를 통해 랜덤하게 구함)
    """
    if n < 0 or type(n) != int:
        raise TypeError("0이상의 정수를 입력해주세요.")
    elif n <= 2:
        return get_random_element(range(0, n+1))
    else:
        # 폐구간 [0, n] 사이의 임의의 정수 1개 return
        m = n + 1
        seed = get_1_or_0() # seed
        a = get_multiplier(m)
        c = get_increment(m)

        x: int = seed
        i: int = 0
        if interations is None:
            while i < a:
                x = (a * x + c) % m
                i += 1  
        else:
            while i < interations:
                x = (a * x + c) % m
                i += 1    
            
        return x

class Random:
    
    def __init__(self):
        self.init_ints()
        
    def init_ints(self):
        self.integers: list = []
        
    def get_randoms(self, interations: int = None) -> list:
        """
        multi integers random generator
        """
        
        randoms = []
        for i in self.integers:
            j = 0
            while j < interations:
                rand = get_random(i)
                randoms.append([i, rand])
                j += 1
        
        return randoms
    
    def save_df_to_png(self, interations: int = None) -> None:
        
        randoms = self.get_randoms(interations)
        df = pd.DataFrame(randoms, columns=['input_number', 'random_number'])
        file_path = os.path.join(images, 'df_img.png')
        dfi.export(df, file_path)
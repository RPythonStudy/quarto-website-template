# example.py
# 교육용 예시 사용자정의 함수들

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from logger.logger import get_logger

# 로거 인스턴스 생성
logger = get_logger(__name__)

def say_hello(name="World"):
    """
    간단한 인사 함수
    
    Args:
        name (str): 이름
        
    Returns:
        str: 인사말 문자열
    """
    logger.info(f"say_hello 함수 호출됨, name: {name}")
    return f"안녕하세요, {name}님!"

def add_numbers(a, b):
    """
    두 수의 합을 계산하는 함수
    
    Args:
        a (float): 첫 번째 수
        b (float): 두 번째 수
        
    Returns:
        float: 두 수의 합
    """
    result = a + b
    logger.debug(f"add_numbers: {a} + {b} = {result}")
    return result

def summarize_data(df):
    """
    데이터프레임을 요약하는 함수 (pandas DataFrame 사용)
    
    Args:
        df: pandas DataFrame
        
    Returns:
        dict: 요약 정보
    """
    logger.info("데이터프레임 요약 시작")
    
    summary_info = {
        'rows': len(df),
        'cols': len(df.columns),
        'col_names': list(df.columns),
        'na_count': df.isnull().sum().sum()
    }
    
    logger.info(f"데이터 요약 완료 - 행: {summary_info['rows']}, 열: {summary_info['cols']}")
    return summary_info

# 함수 로딩 완료 로그
logger.info("example.py 함수들이 로딩되었습니다")

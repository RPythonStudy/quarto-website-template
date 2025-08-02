# 로깅 시스템 가이드

## 개요

> AI4REF 프로젝트는 R과 Python을 함께 사용하는 Quarto 기반 연구 프로젝트입니다.   
> 협업 개발과 코드 디버깅을 위해 통합된 로깅 시스템을 제공합니다. 
> 이 가이드는 개발자들이 로깅 시스템을 자신의 코드에 적용하는 방법을 설명합니다.

## 설계 원칙

### 1. 통합 로깅 아키텍처
- Python 위치: `src/common/logger.py`
- R 위치: `src/R/logger.R`
- 목적: 프로젝트 전체에서 일관된 로깅 인터페이스 제공
- ELK Stack 호환: JSON 형태로 로그를 저장하여 Elasticsearch 연동 최적화

### 2. 이중 출력 방식
- stdout (콘솔): 가독성이 좋도록 텍스트형태로 [timestamp, level, logger name, message] 
- 파일: JSON 형태로 구조화된 로그 저장 (`logs/dev.log`)

### 3. 설정 우선순위
1. 현재 작업 디렉토리 폴더명 (기본값)
2. 환경변수 PROJECT_NAME (`.env` 파일 포함)  
3. 하드코딩된 기본값 (`ai4ref`)

## 로그 레벨 (5단계)

| 레벨 | 설명 | 사용 예시 |
|------|------|-----------|
| `CRITICAL` | 시스템 중단 수준의 심각한 오류 | 데이터베이스 연결 실패, 암호화 키 손실 |
| `ERROR` | 오류 발생하지만 시스템 계속 동작 | 파일 처리 실패, API 호출 오류 |
| `WARNING` | 주의가 필요한 상황 | 권한 부족, 설정 누락 |
| `INFO` | 일반적인 정보 (기본값) | 작업 시작/완료, 처리 건수 |
| `DEBUG` | 디버깅용 상세 정보 | 변수 값, 함수 호출 흐름 |

## Python 로깅 사용법

### 1. 기본 로거 사용
```python
from common.logger import get_logger
logger = get_logger()  # 기본: 프로젝트 이름 사용
# 또는
logger = get_logger("custom_name")  # 커스텀 이름 사용
```

### 2. Wrapper 함수 사용 (권장)
```python
from common.logger import log_debug, log_info, log_warn, log_error, log_critical

log_debug("디버그 메시지")
log_info("정보 메시지")
log_warn("경고 메시지")
log_error("에러 메시지")
log_critical("심각한 오류")
```

## R 로깅 사용법

### 1. 로거 초기화
```r
# 사용자정의함수 로드 (logger.R 포함)
invisible(lapply(
  list.files(here::here("src", "R"), pattern = "\\.R$", full.names = TRUE),
  source,
  encoding = "UTF-8"
))

# 로거 초기화 (.env에서 LOG_LEVEL 읽어서 설정)
init_logger()
```

### 2. 로그 메시지 출력
```r
log_debug("디버그 메시지")
log_info("정보 메시지")
log_warn("경고 메시지")
log_error("오류 메시지")
```

출력 형식: `[2025-08-02 11:09:49] [DEBUG] 디버그 메시지`

## 감사 로그 (Audit Log)

### 감사 로그 함수 사용
```python
from common.logger import audit_log

audit_log(
    action="파일_처리_완료",
    detail={"파일명": "data.csv", "처리건수": 1000},
    compliance="개인정보보호법 제28조"
)
```

## 환경 설정

### .env 파일 설정
```bash
# Python 환경 변수 설정
PYTHONPATH=/home/ben/projects/ai4ref
LOG_LEVEL=DEBUG
PROJECT_NAME=ai4ref  # 선택사항
LOG_PATH=logs/dev.log  # 선택사항
```

### R 환경 설정
```bash
# R 로깅 레벨 설정
LOG_LEVEL=DEBUG
```

## 프로젝트별 적용 예시

### Python 스크립트 예시
```python
from common.logger import log_info, log_debug

def process_data():
    log_info("데이터 처리 시작")
    # ... 처리 로직 ...
    log_debug("중간 처리 결과 확인")
    log_info("데이터 처리 완료")
```

### Quarto 문서(QMD)에서 사용
````markdown
```{r}
#| label: setup
#| include: false

# 사용자정의함수 로드
invisible(lapply(
  list.files(here::here("src", "R"), pattern = "\\.R$", full.names = TRUE),
  source,
  encoding = "UTF-8"
))

# 로거 초기화
init_logger()
```

```{python}
from common.logger import log_info
log_info("Python 코드 블록 실행")
```
````

## 협업 개발자를 위한 체크리스트
- [x] Python: `from common.logger import log_debug, log_info, log_warn, log_error` 사용
- [x] R: `init_logger()` 초기화 후 `log_info()`, `log_debug()` 등 사용
- [x] 프로젝트 스크립트: 로깅 시스템 적용
- [x] 교육용 QMD 파일: 로깅 없이 간결하게 작성
- [x] 환경 설정: .env 파일로 LOG_LEVEL, PYTHONPATH 관리

---

## PYTHONPATH 설정 및 import 경로

### 현재 프로젝트 구조
```
ai4ref/
├── src/
│   ├── common/
│   │   └── logger.py      # Python 로거
│   └── R/
│       └── logger.R       # R 로거
├── scripts/
│   ├── python/
│   └── R/
└── .env                   # 환경 변수 설정
```

### PYTHONPATH 설정
본 프로젝트는 .env 파일을 통해 PYTHONPATH를 설정합니다:
```bash
PYTHONPATH=/home/ben/projects/ai4ref
```

이 설정으로 인해 `src` 디렉토리가 Python 모듈 검색 경로에 포함되어 다음과 같이 import할 수 있습니다:

### Python에서의 import
```python
# src 하위 모듈들을 직접 import
from common.logger import log_info, log_debug
from common.logger import get_logger, audit_log
```

### VS Code 설정
`.vscode/settings.json`에 다음 설정을 추가하여 VS Code에서 자동으로 .env 파일을 인식하도록 합니다:
```json
{
    "python.envFile": "${workspaceFolder}/.env"
}
```
# Quarto Website Template

R과 Python 사용하여 프로젝트를 개발하는 것을 실습하기 위해 Quarto 문서인 qmd 파일을 사용하는 프로젝트가 있으며, 이를 위한 Template입니다.

## 프로젝트 구조

### R 환경 관리
- renv: R 패키지 환경 격리
- .env: R 로깅 레벨 설정 (LOG_LEVEL: "DEBUG", "INFO", "WARN", "ERROR")

### R 로거 사용법
```r
# 1. 사용자정의함수 로드 (logger.R 포함)
invisible(lapply(
  list.files(here::here("src", "R"), pattern = "\\.R$", full.names = TRUE),
  source,
  encoding = "UTF-8"
))

# 2. 로거 초기화 (.env에서 LOG_LEVEL 읽어서 설정)
init_logger()

# 3. 로그 메시지 출력
log_debug("디버그 메시지")
log_info("정보 메시지")
log_warn("경고 메시지")
log_error("오류 메시지")
```

출력 형식: `[2025-08-02 11:09:49] [DEBUG] 디버그 메시지`

### Python 환경관리
- pyenv: pyenv local 3.13.5 등으로 Python 버전 관리
- .venv: Python 가상환경 사용
- direnv: .envrc 파일을 통한 PYTHONPATH 자동 설정
- .env: Python 환경 변수 설정 (LOG_LEVEL 등)

### Python 환경 설정
```bash
# 1. direnv 설치 (Ubuntu/Debian)
sudo apt install direnv

# 2. ~/.bashrc에 hook 추가
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc

# 3. 프로젝트 폴더에서 허용
direnv allow
```

### Python 로거 사용법
```python
# PYTHONPATH가 direnv로 자동 설정되므로 직접 import 가능
from common.logger import log_debug, log_info, log_warn, log_error

log_debug("디버그 메시지")
log_info("정보 메시지")
log_warn("경고 메시지")
log_error("에러 메시지")
```

중요: direnv가 PYTHONPATH를 자동으로 관리하므로 Python 스크립트에서 sys.path를 수동으로 조작하지 마세요.

### 각 파일의 목적

## 로깅 시스템

본 프로젝트는 R과 Python을 위한 통합 로깅 시스템을 제공합니다. 상세한 사용법은 [로깅 시스템 가이드](wiki/logging-guide.md)를 참조하세요.

- R 로거: `src/R/logger.R`
- Python 로거: `src/common/logger.py`
- 로그 파일: `logs/dev.log` (JSON 형식)
- 설정 파일: `.env` (로그 레벨 등)


## generative AI 숙지사항
> vs code 내의 generative AI (=copilot)는 .github/conpilot-instructions.md를 통해 사용자의 지시사항을 인지하고 프로젝트 구조나 스크립트를 제안할 때 아래의 사항을 준수한다.
> chatGPT는 프로젝트 지침에 이 파일이 포함되며 이 파일을 통해 사용자의 지시사항을 인지하고 프로젝트 구조나 스크립트를 제안할 때 아래의 사항을 준수한다.
- vs code에서 터미널 스크립트를 제안할 때, Python 가상환경을 사용하는 프로젝트이므로 반드시 이를 고려해서 제안해야 한다.
- 이모지나 이모티콘은 절대 사용하지 않으며, markdown 문구를 제안할 때에도 **굵은글씨**를 사용하지 않는다.
- 스크립트는 직관적으로 이해하기 쉽고 간결하게 제안하고, 디버깅이 용이한 구조로 제안하다. 
- 프로젝트 자체를 위한 스크립트에는 로깅을 적용한다. 하지만 교육적인 목적으로 qmd 파일을 작성할 때는 로깅을 적용하지 않는다.
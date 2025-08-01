# 로깅 시스템 가이드

## 개요

> AI4RM 프로젝트는 의료 데이터 처리의 특성상 상세한 로깅과 감사 추적이 필요합니다.   
> 또한 협업 개발을 가정해도 필요합니다. 
> 이 가이드는 협업 개발자들이 로깅 시스템을 자신의 코드에 적용하는 방법을 설명합니다.

## 설계 원칙

### 1. 통합 로깅 아키텍처
- 위치: `ai4rm/logger/logger.py`
- 목적: 프로젝트 전체에서 일관된 로깅 인터페이스 제공
- ELK Stack 호환: JSON 형태로 로그를 저장하여 Elasticsearch 연동 최적화

### 2. 이중 출력 방식
- stdout (콘솔): 가독성이 좋도록 텍스트형태로 [timestamp, level, logger name, message] 
- 파일: JSON 형태로 구조화된 로그 저장 (`logs/dev.log`)

### 3. 설정 우선순위
1. 명령행 인자 (최우선)
2. 환경변수 (`.env` 파일 포함)
3. 기본값 (`INFO`)

## 로그 레벨 (6단계)

| 레벨 | 설명 | 사용 예시 |
|------|------|-----------|
| `CRITICAL` | 시스템 중단 수준의 심각한 오류 | 데이터베이스 연결 실패, 암호화 키 손실 |
| `ERROR` | 오류 발생하지만 시스템 계속 동작 | 파일 처리 실패, API 호출 오류 |
| `WARNING` | 주의가 필요한 상황 | 권한 부족, 설정 누락 |
| `INFO` | 일반적인 정보 (기본값) | 작업 시작/완료, 처리 건수 |
| `DEBUG` | 디버깅용 상세 정보 | 변수 값, 함수 호출 흐름 |
| `TRACE` | 가장 상세한 추적 정보 | 데이터 변환 과정, 세밀한 실행 단계 |


## 운영/감사 로그 적용 실전 가이드

### 1. 표준 로거 사용
```python
from logger import get_logger
logger = get_logger("service_name")
```

### 2. 감사 로그(Audit Log) 패턴
```python
import logging
from datetime import datetime, timezone
import os, socket

def audit_log(action: str, detail: dict = None, compliance: str = "개인정보보호법 제28조"):
    audit_logger = logging.getLogger("audit")
    user = os.getenv("USER") or "unknown"
    log = {
        "action": action,
        "user": user,
        "process_id": os.getpid(),
        "server_id": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "compliance_check": compliance
    }
    if detail:
        log.update(detail)
    audit_logger.info(log)
```

### 3. 서비스별 적용 예시
#### 인증서 생성 유틸리티 (cert_utils.py)
```python
from logger import get_logger
def generate_self_signed_cert(...):
    logger = get_logger("cert_utils")
    ...
    logger.info(f"인증서 생성 완료: {crt_path}")
    audit_log(
        action="cert_created",
        detail={"crt_path": crt_path, "key_path": key_path},
    )
```

#### Vault 설치 CLI (vault_install_cli.py)
```python
logger.info("Vault 설치 시작")
audit_log(action="vault_install_started", detail={...})
```

### 4. 감사 로그 핸들러 분리 (logging.yaml 예시)
```yaml
handlers:
  audit_file:
    class: logging.FileHandler
    level: INFO
    formatter: json
    filename: logs/audit.log
loggers:
  audit:
    handlers: [audit_file]
    level: INFO
    propagate: False
```

## 협업 개발자를 위한 체크리스트
- [x] 모든 서비스/유틸리티에서 표준 로거(get_logger) 사용
- [x] 개인정보 처리/중요 이벤트는 운영+감사 로그 중복 기록
- [x] 감사 로그에 사용자/프로세스/서버/컴플라이언스 정보 포함
- [x] 로그레벨/핸들러는 logging.yaml 또는 .env로 설정
- [x] 테스트 코드에서도 동일한 로깅 패턴 적용

---

## Q&A 및 추가 안내

- 운영/감사 로그 중복 기록은 서비스/유틸리티 코드에서 직접 구현합니다. (로깅 인프라에서는 분리만 지원)
- 감사 로그 핸들러는 logging.yaml에서 별도 파일로 지정 가능
- 컴플라이언스 태그, 사용자/프로세스 정보는 감사 로그에 반드시 포함

- 문의: benkorea.ai@gmail.com

프로젝트의 모든 실행은 루트 디렉터리 기준으로 이루어집니다.

### 프로젝트 루트에서의 임포트
`logger/__init__.py`에서  
```python
from .logger import get_logger
```
로 설정되어 있으므로, 루트에서 다음과 같이 임포트하여 사용할 수 있습니다:
```python
from logger import get_logger
```

### import 경로 설정
본 프로젝트는 모노레포 구조를 채택하고 있으며, 저자는 편집자 개발모드를 이용해 경로를 설정하는 것이 이 프로젝트에 적합치 않다고 판단했습니다. 따라서 이 프로젝트에서는 `PYTHONPATH=home/ben/projects/ai4rm` 환경변수로 경로를 설정하는 방법을 적용키로 하였습니다.   
구체적으로는 .env 파일을 사용하여 환경변수를 설정하였고   
프로젝트에서 자동으로 경로를 인식케 하려고 .vscode/settings.json 파일에 아래의 설정을 적용했습니다.
```json
{
    "python.envFile": "${workspaceFolder}/.env"
}
```  

### src/ 하위 디렉터리에서의 임포트
위의 설정 때문에 `src/` 내부 모듈에서 로거를 임포트할 때도 프로젝트의 루트에서 임포트와 같은 방식으로 가능하게 됩니다.
```python
from logger import get_logger
```

### tests/ 하위 디렉터리에서의 임포트
테스트 코드에서 로거를 사용하려면 역시 루트에서 임포트 하듯이 가능합니다.

- 끝 -
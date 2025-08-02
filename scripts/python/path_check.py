# scripts/python/path_check.py

import sys
from pathlib import Path
from common.logger import log_info, log_debug

log_info("=== Python 모듈 검색 경로 (sys.path) ===")
for i, path in enumerate(sys.path):
    log_info(f"{i}: {path}")

log_info("=== 현재 작업 디렉토리 ===")
log_info(str(Path.cwd()))

log_info("=== common.logger import 테스트 ===")
try:
    log_info("✓ common.logger import 성공!")
    log_debug("path_check.py에서 로거 테스트")
except Exception as e:
    log_info(f"✗ common.logger import 실패: {e}")

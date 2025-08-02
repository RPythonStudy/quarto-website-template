import os
import sys
import logging
import json
import socket
from pathlib import Path
from logging import Formatter, StreamHandler, FileHandler
from dotenv import load_dotenv
from datetime import datetime, timezone

def _get_project_name() -> str:
    try:
        return Path.cwd().name
    except:
        project_name = os.getenv("PROJECT_NAME")
        if project_name:
            return project_name
        return "Template"  # 최종 기본값

PROJECT_NAME = _get_project_name()

def _load_dotenv():
    if Path(".env").exists():
        load_dotenv(override=True)

def _get_log_level():
    _load_dotenv()
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    valid_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    return level if level in valid_levels else "INFO"

def setup_logging():
    level = _get_log_level()
    log_file_path = Path(os.getenv("LOG_PATH", "logs/dev.log"))
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    class JsonLogFormatter(Formatter):
        def format(self, record):
            record_dict = {
                "timestamp": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "pathname": record.pathname,
                "lineno": record.lineno,
                "funcName": record.funcName,
            }
            if record.exc_info:
                record_dict["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(record_dict, ensure_ascii=False)

    stream_formatter = Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s")
    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(stream_formatter)

    file_formatter = JsonLogFormatter()
    file_handler = FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)

    logging.basicConfig(
        level=level,
        handlers=[stream_handler, file_handler]
    )

def get_logger(name: str = PROJECT_NAME) -> logging.Logger:
    root_logger = logging.getLogger()
    if not root_logger.hasHandlers():
        setup_logging()
    return logging.getLogger(name)


def audit_log(action: str, detail: dict = None, compliance: str = "개인정보보호법 제28조"):
    """
    AI4RM 표준 감사 로그 기록 함수
    - action: 이벤트명 (필수)
    - detail: dict (추가 상세정보, 선택)
    - compliance: 컴플라이언스 조항명 (기본값: 개인정보보호법 제28조)
    """
    audit_logger = get_logger("audit")
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


def log_debug(message: str) -> None:
    get_logger().debug(message)

def log_info(message: str) -> None:
    get_logger().info(message)

def log_warn(message: str) -> None:
    get_logger().warning(message)

def log_error(message: str) -> None:
    get_logger().error(message)

def log_critical(message: str) -> None:
    get_logger().critical(message)

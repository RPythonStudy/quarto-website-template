library(logger)

init_logger <- function() {
  readRenviron(".env")
  log_level <- Sys.getenv("LOG_LEVEL", "INFO")
  
  logger::log_threshold(log_level)
  
  logger::log_layout(logger::layout_glue_generator(
    format = '[{format(time, "%Y-%m-%d %H:%M:%S")}] [{toupper(level)}] {msg}'
  ))
  
  logger::log_info("R 로거 초기화 완료")
}

# 로그 함수들 (logger 패키지 함수 그대로 사용)
log_debug <- logger::log_debug
log_info <- logger::log_info  
log_warn <- logger::log_warn
log_error <- logger::log_error

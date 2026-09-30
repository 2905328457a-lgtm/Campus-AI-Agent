from datetime import datetime
import logging
import os
from utils.path_tool import get_abs_path

# 日志保存的根目录
LOG_ROOT = get_abs_path("logs")
os.makedirs(LOG_ROOT, exist_ok=True)

# 统一日志格式：[时间] - [记录器名] - [级别] - [文件名:行号] - 信息
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] -"
    " %(message)s"
)


def get_logger(
    name: str = "agent",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_file=None,
) -> logging.Logger:
  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)

  # 避免重复添加 Handler
  if logger.handlers:
    return logger

  # 1. 控制台 Handler（负责打印到屏幕，只打印 INFO 及以上的重要内容）
  console_handler = logging.StreamHandler()
  console_handler.setLevel(console_level)
  console_handler.setFormatter(DEFAULT_LOG_FORMAT)
  logger.addHandler(console_handler)

  # 2. 文件 Handler（负责写入本地硬盘日志文件，保留所有 DEBUG 细节）
  if not log_file:
    log_file = os.path.join(
        LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    )

  file_handler = logging.FileHandler(log_file, encoding="utf-8")
  file_handler.setLevel(file_level)
  file_handler.setFormatter(DEFAULT_LOG_FORMAT)
  logger.addHandler(file_handler)

  return logger


# 快捷获取全局默认 logger
logger = get_logger()

if __name__ == "__main__":
  logger.info("这是一条普通信息日志（屏幕和文件都有）")
  logger.error("这是一条错误日志（屏幕和文件都有）")
  logger.debug(
      "这是一条底层调试日志（只有文件里有，屏幕上不会显示，防止刷屏）"
  )
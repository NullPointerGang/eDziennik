from lynx_logger import LynxLogger, LogConfig, Level, Format

from core.config import config


logger = LynxLogger(
    LogConfig(
        name="auth_service",
        level=Level(config.logging.level),
        dev_mode=config.logging.dev_mode,
        log_to_console=config.logging.log_to_console,
        logs_dir=config.logging.logs_dir
    )
)


__all__ = ['logger']
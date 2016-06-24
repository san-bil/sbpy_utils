function logger = logger_pop(logger)

logger.stack = logger.stack(1:end-1);

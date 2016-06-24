function logger = logger_push(logger)

my_stack = dbstack;
caller_function = my_stack(2).name;
logger.stack{end+1} = caller_function;

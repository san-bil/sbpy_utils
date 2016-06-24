function logger = logger_create(root_path)

logger = [];
logger.root_node = root_path;
logger.counter = 0;

my_mkdir(root_path);

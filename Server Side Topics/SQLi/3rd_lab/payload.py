"""
log = logging.getLogger(__name__) #Ч : Создаёт логгер с именем текущего модуля (файла).
logging.basicConfig(
    stream=sys.stdout, #Логи выводятся в стандартный вывод (терминал).
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}][{name}] {message}",
    style="{",
    datefmt="%H:%M:%S",
)
"""
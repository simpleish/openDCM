import logging
import sys

formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
handler_print = logging.StreamHandler(sys.stdout)
handler_print.setLevel(logging.INFO)
handler_print.setFormatter(formatter)

log = logging.getLogger("migration_run_log")
log.addHandler(handler_print)
log.setLevel(logging.INFO)
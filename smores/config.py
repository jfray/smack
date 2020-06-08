import logging as log
import os
import sys

COMMAND_IDENTIFIER = "#"
log_path = os.path.expanduser("~/logs")
os.mkdir(log_path) and sys.stderr.write(f"Created {log_path}.\n") if not os.path.exists(log_path) else None

log.basicConfig(
  filename=f"{log_path}/smores.log",
  level=log.DEBUG,
  filemode="a",
  format='%(name)s - %(levelname)s - %(message)s'
)


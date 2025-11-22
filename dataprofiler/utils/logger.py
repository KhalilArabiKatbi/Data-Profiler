import sys
from datetime import datetime


class Logger:
    def __init__(self, name: str = "dataprofiler", level: str = "INFO"):
        self.name = name
        self.level = level.upper()

    def _log(self, level: str, msg: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {self.name} {level}: {msg}"
        print(line, file=sys.stdout)

    def info(self, msg: str):
        self._log("INFO", msg)

    def warn(self, msg: str):
        self._log("WARN", msg)

    def error(self, msg: str):
        self._log("ERROR", msg)
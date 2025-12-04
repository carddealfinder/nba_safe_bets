import logging

# Create single global logger
log = logging.getLogger("nba_safe_bets")
log.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)

# Attach handler
if not log.handlers:
    log.addHandler(ch)

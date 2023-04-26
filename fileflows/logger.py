def write_log(text: str, log_name: str = "/scripts/fileflows/log.txt") -> None:
    with open(log_name, "a") as f:
        f.write(f"{text}")

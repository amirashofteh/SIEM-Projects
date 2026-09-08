import re
import json


LOG_FILE = "sample_auth.log"


pattern = re.compile(
    r"^(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+"
    r"(?P<hostname>\S+)\s+"
    r"sshd-session\[\d+\]:\s+"
    r"Failed password for "
    r"(?:(?P<invalid>invalid user)\s+)?"
    r"(?P<username>\S+)\s+"
    r"from\s+(?P<source_ip>\S+)\s+"
    r"port\s+(?P<source_port>\d+)\s+ssh2"
)


def parse_log_line(line):
    match = pattern.match(line)

    if not match:
        return None

    data = match.groupdict()

    return {
        "timestamp": data["timestamp"],
        "hostname": data["hostname"],
        "event_type": "failed_login",
        "username": data["username"],
        "source_ip": data["source_ip"],
        "source_port": int(data["source_port"]),
        "protocol": "ssh",
        "invalid_user": bool(data["invalid"])
    }


if __name__ == "__main__":
    with open(LOG_FILE, "r") as file:
        for line in file:
            event = parse_log_line(line.strip())

            if event:
                print(json.dumps(event))

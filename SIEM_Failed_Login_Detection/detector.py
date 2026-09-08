from datetime import datetime, timedelta
from collections import defaultdict
import json

from parser import parse_log_line
import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict

from parser import parse_log_line

import sys

RULE_FILE = "rules/failed_login_rules.json"
LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else "sample_auth.log"
ALERT_FILE = "alerts/alerts.json"

def save_alerts(alerts):
    with open(ALERT_FILE, "w") as file:
        json.dump(alerts, file, indent=2)

def load_rule():
    with open(RULE_FILE, "r") as file:
        rules = json.load(file)

    return rules["ssh_brute_force"]

LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else "sample_auth.log"


def load_events():
    events = []

    with open(LOG_FILE, "r") as file:
        for line in file:
            event = parse_log_line(line.strip())

            if event:
                event["timestamp"] = datetime.strptime(
 		   f"2026 {event['timestamp']}",
   			 "%Y %b %d %H:%M:%S"
)
                events.append(event)

    return events


def detect_brute_force(events, rule):
    threshold = rule["threshold"]
    time_window = timedelta(minutes=rule["time_window_minutes"])

    grouped = defaultdict(list)

    for event in events:
        grouped[event["source_ip"]].append(event)

    alerts = []

    for source_ip, ip_events in grouped.items():
        ip_events.sort(key=lambda event: event["timestamp"])

        for i in range(len(ip_events)):
            window_start = ip_events[i]["timestamp"]
            window_end = window_start + time_window

            window_events = [
                event
                for event in ip_events[i:]
                if event["timestamp"] <= window_end
            ]

            if len(window_events) >= threshold:
                usernames = sorted(
                    set(event["username"] for event in window_events)
                )

                alerts.append({
                    "rule": "SSH Brute Force",
                    "severity": rule["severity"],
                    "source_ip": source_ip,
                    "failed_attempts": len(window_events),
                    "time_window": f'{rule["time_window_minutes"]} minutes',
		    "first_seen": window_events[0]["timestamp"].strftime("%b %d %H:%M:%S"),	
		    "last_seen": window_events[-1]["timestamp"].strftime("%b %d %H:%M:%S"),
                    "targeted_users": usernames
                })

                break

    return alerts

rule = load_rule()

if not rule["enabled"]:
    sys.exit(0)

events = load_events()
alerts = detect_brute_force(events, rule)

save_alerts(alerts)

for alert in alerts:
    print(json.dumps(alert, indent=2))

# 🔐 Failed Login Detection

A small **SIEM-style SSH failed-login detection project** built with Python, Linux `systemd-journald`, JSON-based detection rules, and SOC investigation practices.

The project demonstrates the basic workflow of a security monitoring system:

```text
Log Collection → Parsing → Normalization → Detection → Alert → Investigation
```

---

## 🎯 Project Objective

Detect suspicious SSH authentication activity by identifying multiple failed login attempts from the same source IP within a defined time window.

The detection rule used in this project is:

> **5 or more failed SSH login attempts from the same source IP within 5 minutes → HIGH severity alert**

The project also produces a persistent JSON alert and an analyst-style investigation report.

---

## 🏗️ Architecture

```text
                    Kali Linux
                        │
                        ▼
                systemd-journald
                        │
                        ▼
                 sample_auth.log
                        │
                        ▼
                    parser.py
                        │
                        ▼
              Normalized SSH Events
                        │
                        ▼
                   detector.py
                        ▲
                        │
            failed_login_rules.json
                        │
                        ▼
                 Detection Alert
                   ┌────┴────┐
                   ▼         ▼
             Terminal    alerts.json
                             │
                             ▼
                  SOC Investigation
                             │
                             ▼
                   investigation.md
```

---

## 📁 Project Structure

```text
Failed-Login-Detection/
│
├── parser.py
├── detector.py
│
├── sample_auth.log
├── test_low_attempts.log
│
├── rules/
│   └── failed_login_rules.json
│
├── alerts/
│   └── alerts.json
│
└── reports/
    └── investigation.md
```

---

## 🛠️ Technologies

* Linux
* Kali Linux
* systemd-journald
* OpenSSH
* Python 3
* Regular Expressions
* JSON
* Bash
* SOC / SIEM concepts

---

## 🔍 1. Log Collection

The Kali system did not use the traditional:

```text
/var/log/auth.log
```

for the SSH authentication events used in this lab.

Instead, authentication events were available through:

```bash
journalctl
```

SSH events were identified under:

```text
sshd-session
```

A reproducible dataset was created from the journal:

```bash
sudo journalctl --since "10:45:00" --until "10:48:00" --no-pager | grep 'sshd-session' > sample_auth.log
```

This allows the detection system to work with a fixed dataset during development and testing.

---

## 🧩 2. Log Parsing

`parser.py` extracts useful fields from raw SSH authentication logs.

Example raw event:

```text
Sep 08 10:45:55 kali sshd-session[60968]: Failed password for invalid user wronguser from ::1 port 45138 ssh2
```

The parser converts it into a normalized event:

```json
{
  "timestamp": "Sep 08 10:45:55",
  "hostname": "kali",
  "event_type": "failed_login",
  "username": "wronguser",
  "source_ip": "::1",
  "source_port": 45138,
  "protocol": "ssh",
  "invalid_user": true
}
```

This demonstrates the SIEM concept of **log normalization**.

---

## 🚨 3. Detection

`detector.py` analyzes the normalized SSH events.

The detector:

1. Groups events by source IP.
2. Sorts events chronologically.
3. Creates a configurable time window.
4. Counts failed login attempts.
5. Compares the count against the configured threshold.
6. Generates an alert when the threshold is exceeded.

---

## ⚙️ Detection Rule

The detection rule is stored separately from the Python code:

```text
rules/failed_login_rules.json
```

Current configuration:

```json
{
  "ssh_brute_force": {
    "enabled": true,
    "threshold": 5,
    "time_window_minutes": 5,
    "severity": "HIGH"
  }
}
```

Keeping the detection policy separate from the detection engine makes the system easier to modify and extend.

---

## 🔔 4. Alert Generation

When the detection rule is triggered, the system generates an alert similar to:

```json
{
  "rule": "SSH Brute Force",
  "severity": "HIGH",
  "source_ip": "::1",
  "failed_attempts": 6,
  "time_window": "5 minutes",
  "first_seen": "Sep 08 10:45:55",
  "last_seen": "Sep 08 10:47:15",
  "targeted_users": [
    "helpdesk",
    "wronguser"
  ]
}
```

The alert is displayed in the terminal and stored persistently in:

```text
alerts/alerts.json
```

---

## 🧪 5. Testing

The detection engine was tested with different numbers of failed attempts.

### Above threshold

```text
6 failed attempts
Threshold: 5
```

Result:

```text
HIGH severity alert
```

### Below threshold

```text
3 failed attempts
Threshold: 5
```

Result:

```text
No alert
```

This verifies that the detection rule does not trigger below the configured threshold.

---

## 🔎 6. Investigation

After an alert is generated, the underlying raw logs are investigated rather than relying only on the alert summary.

The investigation examines:

* Source IP
* Targeted usernames
* Number of failed attempts
* Authentication timestamps
* Attempt pattern
* Detection threshold
* Time window
* Whether the activity appears local or external

The investigation report is stored in:

```text
reports/investigation.md
```

---

## 🕵️ Investigation Result

The test generated six failed SSH authentication attempts:

```text
Source IP:       ::1
Failed attempts: 6
Targeted users:  helpdesk, wronguser
First seen:      Sep 08 10:45:55
Last seen:       Sep 08 10:47:15
```

The activity matched the configured brute-force detection rule.

However, `::1` is the IPv6 loopback address, meaning the activity originated locally from the Kali machine.

Therefore, this was a **controlled security test**, not evidence of an external attack.

---

## ▶️ Usage

Run the parser:

```bash
python3 parser.py
```

Run the detector using the default dataset:

```bash
python3 detector.py
```

Run the detector against another log file:

```bash
python3 detector.py another_log.log
```

View generated alerts:

```bash
cat alerts/alerts.json
```

View the investigation:

```bash
cat reports/investigation.md
```

---

## 🧠 SIEM Concepts Practiced

This project covers several fundamental SOC/SIEM concepts:

* Log collection
* Linux authentication logs
* SSH monitoring
* Log parsing
* Regular expressions
* Event normalization
* Detection rules
* Threshold-based detection
* Time-window detection
* Alert severity
* Alert persistence
* False-positive testing
* Security investigation
* Evidence-based analysis
* Incident reporting

---

## 🚀 Possible Future Improvements

This project can be extended into a more realistic detection engine by adding:

* Live `journalctl` ingestion
* Structured `journalctl -o json` ingestion
* Multiple detection rules
* Configurable rule IDs
* Alert IDs
* Alert timestamps
* More severity levels
* Automatic investigation reports
* Email/Slack alerting
* IP reputation checks
* Multiple source IP detection
* User-specific brute-force detection
* Alert deduplication
* Unit tests
* A web dashboard
* Integration with Wazuh or Splunk

---

## 📌 Project Status

**Status: ✅ Complete**

The project successfully implements a complete mini-SIEM workflow:

```text
Raw Logs
   ↓
Parsing
   ↓
Normalization
   ↓
Detection
   ↓
Alert Generation
   ↓
Alert Storage
   ↓
Investigation
   ↓
SOC Report
```

---

## 🎓 What I Learned

This project demonstrates how a basic SIEM pipeline can be constructed from scratch using Linux logs and Python.

The most important lesson is that **detection and investigation are separate stages**:

> The detector identifies suspicious behavior; the analyst investigates the evidence behind the alert.

This project provides the foundation for more advanced SIEM detection and SOC investigation projects.

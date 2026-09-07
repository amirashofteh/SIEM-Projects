# SIEM Authentication Log Analysis

A Bash-based authentication log analyzer designed to simulate a basic SOC/SIEM workflow for detecting suspicious SSH authentication activity.

The project analyzes Linux SSH authentication logs, extracts useful security information, correlates failed and successful login attempts, detects possible brute-force attacks, and generates a security report.

This project was built as part of a practical SIEM/SOC learning roadmap with a focus on learning through hands-on security projects.

---

## 🎯 Objectives

* Analyze Linux SSH authentication logs
* Identify successful and failed authentication attempts
* Extract usernames and source IP addresses
* Count failed authentication attempts by IP
* Detect possible brute-force activity
* Detect successful logins following repeated failures
* Generate a basic authentication security report
* Practice Bash scripting and Linux log analysis
* Work with both synthetic and real SSH authentication data

---

## 🛠️ Technologies

* Linux
* Bash
* `grep`
* `sed`
* `journalctl`
* Regular expressions
* Associative arrays
* SSH authentication logs
* Git / GitHub

---

## 📁 Project Structure

```text
SIEM_Authentication_Log_Analysis/
├── logs/
│   ├── real_ssh.log
│   └── sample_auth.log
│
├── reports/
│   └── authentication_report.txt
│
├── scripts/
│   └── auth_analyzer.sh
│
└── README.md
```

### Directories

**`logs/`**

Contains the authentication datasets used by the analyzer.

* `sample_auth.log` — synthetic dataset containing normal and suspicious authentication activity
* `real_ssh.log` — authentication-related SSH events collected from a real Kali Linux system using `journalctl`

**`scripts/`**

Contains the Bash analyzer.

**`reports/`**

Contains the generated security analysis report.

---

## 🔍 Detection Logic

The analyzer looks for two primary SSH authentication events.

### Failed Authentication

Example:

```text
Failed password for invalid user admin from 192.168.100.50
```

The analyzer extracts:

```text
Username: admin
Source IP: 192.168.100.50
```

The failed attempt is then added to the failure counter for that IP.

### Successful Authentication

Example:

```text
Accepted password for admin from 192.168.100.50
```

The analyzer extracts:

```text
Username: admin
Source IP: 192.168.100.50
```

The successful authentication is also checked against previous failed attempts from the same source IP.

---

## 🚨 Brute-Force Detection

The analyzer uses a configurable threshold to identify possible brute-force activity.

The default threshold is:

```text
5 failed attempts
```

If an IP reaches or exceeds the threshold, the analyzer generates an alert:

```text
[ALERT] Possible brute-force attack from 192.168.100.50
```

The threshold can also be changed when running the script.

For example:

```bash
./scripts/auth_analyzer.sh logs/sample_auth.log 3
```

This changes the threshold from `5` to `3`.

---

## 🚨 Suspicious Successful Login Detection

The analyzer also correlates authentication events.

If an IP produces repeated failed authentication attempts and subsequently succeeds, the analyzer reports:

```text
[ALERT] Successful login after repeated failures from 192.168.100.50
```

This can represent a potentially successful brute-force attack or compromised credentials.

Example attack sequence:

```text
192.168.100.50
        │
        ├── Failed login
        ├── Failed login
        ├── Failed login
        ├── Failed login
        ├── Failed login
        │
        └── Successful login
                 │
                 ▼
          🚨 Suspicious Activity
```

---

## 📊 Authentication Statistics

The analyzer calculates:

* Total authentication attempts
* Successful authentication attempts
* Failed authentication attempts
* Failed attempts per source IP

Example:

```text
=== Authentication Summary ===
Total attempts:      11
Successful attempts: 3
Failed attempts:     8
```

---

## 📄 Security Report

The analyzer generates:

```text
reports/authentication_report.txt
```

Example:

```text
========================================
 Authentication Security Report
========================================

Total attempts:      11
Successful attempts: 3
Failed attempts:     8

Failed Attempts by IP
---------------------
10.10.10.15    3
192.168.100.50    5
[HIGH] Possible brute-force attack from 192.168.100.50
```

The report provides a concise summary that could be used as a starting point for SOC investigation.

---

## ▶️ Usage

Make sure the script is executable:

```bash
chmod +x scripts/auth_analyzer.sh
```

Run the analyzer against the sample dataset:

```bash
./scripts/auth_analyzer.sh logs/sample_auth.log
```

Run it against the real SSH dataset:

```bash
./scripts/auth_analyzer.sh logs/real_ssh.log
```

Specify a custom brute-force threshold:

```bash
./scripts/auth_analyzer.sh logs/sample_auth.log 3
```

---

## 🧪 Sample Dataset

The synthetic dataset contains multiple authentication scenarios.

### Scenario 1 — Possible Brute Force

```text
192.168.100.50
```

Five failed authentication attempts are followed by a successful login.

Expected detection:

```text
Possible brute-force attack
Successful login after repeated failures
```

### Scenario 2 — Repeated Failed Authentication

```text
10.10.10.15
```

Three failed authentication attempts occur without a successful login.

This becomes suspicious when the configured threshold is set to `3`.

### Scenario 3 — Normal Authentication

```text
192.168.100.73
```

A successful login occurs without preceding failed attempts.

### Scenario 4 — Normal Authentication

```text
192.168.100.20
```

A successful login occurs without suspicious preceding failures.

---

## 🖥️ Real Log Analysis

The project also uses authentication-related events collected from a real Kali Linux system.

The system did not provide `/var/log/auth.log`, so SSH authentication events were collected through `systemd-journald`:

```bash
sudo journalctl _COMM=sshd-session --no-pager > logs/real_ssh.log
```

The real dataset contained successful SSH authentication events and connection/session events.

The analyzer correctly ignores unrelated session-management messages and focuses on recognized authentication events such as:

```text
Accepted password
Failed password
```

This demonstrates why understanding the actual logging system of the target Linux distribution is important when building security automation.

---

## 🧠 Bash Concepts Practiced

This project was also designed to reinforce practical Bash skills.

The analyzer uses:

* Command-line arguments
* Input validation
* File existence checks
* `while read` loops
* `if / elif` conditions
* Pipes
* `grep`
* `sed`
* Regular expressions
* Command substitution
* Arithmetic operations
* Associative arrays
* Parameter expansion
* Input redirection
* Output redirection
* Functions/command grouping
* Exit codes

---

## 🔐 SOC/SIEM Concepts Practiced

This project introduces several concepts used in real SOC environments:

* Authentication monitoring
* Failed login detection
* Brute-force detection
* Source IP tracking
* Event correlation
* Threshold-based detection
* Suspicious successful authentication
* Security alert generation
* Log normalization
* Security reporting
* Incident investigation workflow

The basic workflow is:

```text
Raw Logs
   │
   ▼
Log Parsing
   │
   ▼
Event Extraction
   │
   ├── Username
   ├── Source IP
   └── Authentication Result
   │
   ▼
Correlation
   │
   ▼
Detection Rules
   │
   ├── Brute Force
   └── Suspicious Successful Login
   │
   ▼
Security Report
```

---

## 📈 Project Development

The analyzer was developed incrementally:

### V1 — Event Classification

Identified:

* Failed authentication
* Successful authentication

### V2 — Field Extraction

Extracted:

* Username
* Source IP

### V3 — Detection

Added:

* Failed attempts per IP
* Brute-force detection
* Successful login after repeated failures

### V4 — Statistics & Reporting

Added:

* Authentication statistics
* Security report generation

### V5 — Reliability

Added:

* Input validation
* File existence validation
* Configurable detection threshold
* Reliable report path handling

---

## 🚀 Future Improvements

Possible future versions could include:

* Timestamp extraction
* Time-window-based brute-force detection
* Username-based attack detection
* Multiple attack thresholds
* GeoIP enrichment
* Private/public IP classification
* JSON output
* CSV output
* Log severity levels
* Whitelisting trusted IP addresses
* Real-time log monitoring
* Integration with Wazuh
* Integration with Splunk
* Alert forwarding
* Dashboard visualization

---

## ⚠️ Limitations

This project is a lightweight Bash-based authentication analyzer and is **not a replacement for a full SIEM platform**.

The current detection logic is intentionally simple and primarily focuses on SSH authentication events.

It does not currently provide:

* Persistent event storage
* Advanced correlation
* Network-wide log collection
* Threat intelligence enrichment
* Distributed detection
* Real-time alert management
* Full incident-response capabilities

The purpose of the project is to demonstrate the fundamental concepts behind authentication monitoring and detection before moving to larger SIEM platforms.

---

## 🎓 Learning Outcome

This project demonstrates how raw Linux authentication logs can be transformed into security-relevant information using a relatively small Bash script.

The project follows a practical SOC workflow:

```text
Collect
   ↓
Parse
   ↓
Extract
   ↓
Correlate
   ↓
Detect
   ↓
Alert
   ↓
Report
```

It also provides a foundation for implementing similar detection logic in dedicated SIEM platforms such as Wazuh and Splunk.

---

## 👤 Author

**Amir Ashofteh**

Cybersecurity / Network & Systems Engineering

GitHub:

`https://github.com/amirashofteh`

---

## 📌 Project Status

**Completed — Portfolio Project**

The current version supports SSH authentication analysis, brute-force detection, suspicious successful-login correlation, configurable thresholds, authentication statistics, and security report generation.

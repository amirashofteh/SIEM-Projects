# SSH Brute Force Investigation

## 1. Alert Summary

* Rule: SSH Brute Force
* Severity: HIGH
* Source IP: ::1
* Failed Attempts: 6
* Time Window: 5 minutes
* First Seen: Sep 08 10:45:55
* Last Seen: Sep 08 10:47:15

## 2. Targeted Accounts

* helpdesk
* wronguser

## 3. Timeline

| Time     | Event                                                            |
| -------- | ---------------------------------------------------------------- |
| 10:45:55 | Failed SSH login attempt for invalid user `wronguser` from `::1` |
| 10:46:18 | Failed SSH login attempt for invalid user `wronguser` from `::1` |
| 10:46:19 | Failed SSH login attempt for invalid user `wronguser` from `::1` |
| 10:47:07 | Failed SSH login attempt for user `helpdesk` from `::1`          |
| 10:47:12 | Failed SSH login attempt for user `helpdesk` from `::1`          |
| 10:47:15 | Failed SSH login attempt for user `helpdesk` from `::1`          |

## 4. Analysis

### What happened?

Six failed SSH authentication attempts were detected from the same source IP address, `::1`.

Three attempts targeted the invalid username `wronguser`, while three attempts targeted the valid account `helpdesk`.

### Why was this detected?

The SSH Brute Force detection rule is configured to generate a HIGH severity alert when at least 5 failed SSH login attempts originate from the same source IP within a 5-minute window.

Six failed attempts were detected within approximately 1 minute and 20 seconds, which exceeded the configured threshold.

### Is this likely malicious?

The behavior matches a brute-force login pattern because multiple failed authentication attempts occurred within a short period.

However, the source IP `::1` is the IPv6 loopback address. This means the activity originated locally on the Kali system used for this lab.

Therefore, this event should not be considered evidence of an external attack. It is a controlled security event used to test the detection rule.

## 5. Investigation Findings

* Source: `::1` (IPv6 loopback address)
* Authentication method: SSH password authentication
* Targeted accounts: `helpdesk`, `wronguser`
* Failed attempts: 6
* Attempt pattern: Multiple failed SSH authentication attempts from the same source IP within a short period
* First observed: Sep 08 10:45:55
* Last observed: Sep 08 10:47:15
* Detection threshold: 5 failed attempts within 5 minutes
* Detection result: Threshold exceeded
* External attacker confirmed: No
* Event classification: Controlled brute-force detection test

## 6. Recommended Actions

* Review the SSH authentication logs for additional failed login attempts.
* Investigate the local process or user responsible for generating the failed SSH attempts.
* Monitor for repeated brute-force patterns from other source IP addresses.
* For real external attacks, consider blocking or rate-limiting the offending source IP.
* Consider SSH hardening measures such as key-based authentication and disabling password authentication where appropriate.

## 7. Conclusion

The SIEM detection rule successfully identified a brute-force-style SSH authentication pattern.

Six failed login attempts were observed from the same source IP within the configured 5-minute detection window, exceeding the threshold of five attempts and correctly generating a HIGH severity alert.

The investigation determined that the source IP was `::1`, the IPv6 loopback address. Therefore, the activity originated locally and represents a controlled test of the SIEM detection capability rather than a confirmed external attack.

The detection, alert generation, and investigation workflow operated as expected.

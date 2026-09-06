# SIEM Fundamentals & Architecture

## 1. SIEM Overview

A SIEM (Security Information and Event Management) system centrally collects,
processes, analyzes, and correlates security-related events from multiple
sources.

## 2. SIEM Architecture

```text
                    LOG SOURCES
        ┌──────────────┬──────────────┐
        │              │              │
     Linux          Windows        Firewall
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                LOG COLLECTION
                       ↓
              PARSING / NORMALIZATION
                       ↓
                  SIEM PLATFORM
                       ↓
              CORRELATION / ANALYSIS
                       ↓
                 DETECTION RULES
                       ↓
                    ALERTS
                       ↓
                SOC ANALYST
                       ↓
             INVESTIGATION / RESPONSE

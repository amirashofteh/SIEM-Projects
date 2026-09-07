#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <log_file>"
    exit 1
fi

LOG_FILE="$1"
THRESHOLD="${2:-5}"
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file not found: $LOG_FILE"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_FILE="$SCRIPT_DIR/../reports/authentication_report.txt"

declare -A failed_attempts
declare -A alerted_ips
total_attempts=0
successful_attempts=0
failed_attempts_count=0

while read -r line; do
    total_attempts=$((total_attempts + 1))

    if echo "$line" | grep -q "Failed password"; then

        username=$(echo "$line" | sed -E 's/.*Failed password for (invalid user )?([^ ]+) from.*/\2/')
        ip=$(echo "$line" | sed -E 's/.*from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) port.*/\1/')
        failed_attempts["$ip"]=$((failed_attempts["$ip"] + 1))
	failed_attempts_count=$((failed_attempts_count + 1))
        echo "[FAILED]  User: $username  IP: $ip"

    elif echo "$line" | grep -q "Accepted password"; then

        username=$(echo "$line" | sed -E 's/.*Accepted password for ([^ ]+) from.*/\1/')
        ip=$(echo "$line" | sed -E 's/.*from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) port.*/\1/')
	successful_attempts=$((successful_attempts + 1))
    if [ "${failed_attempts[$ip]:-0}" -ge "$THRESHOLD" ]; then
        echo "[ALERT] Successful login after repeated failures from $ip"
   fi
        echo "[SUCCESS] User: $username  IP: $ip"

    fi

done < "$LOG_FILE"

echo
echo "=== Failed Attempts by IP ==="

for ip in "${!failed_attempts[@]}"; do
    echo "IP: $ip  Failed attempts: ${failed_attempts[$ip]}"

    if [ "${failed_attempts[$ip]}" -ge "$THRESHOLD" ]; then
        echo "[ALERT] Possible brute-force attack from $ip"
    fi
done

echo
echo "=== Authentication Summary ==="
echo "Total attempts:      $total_attempts"
echo "Successful attempts: $successful_attempts"
echo "Failed attempts:     $failed_attempts_count"

{
    echo "========================================"
    echo " Authentication Security Report"
    echo "========================================"
    echo
    echo "Total attempts:      $total_attempts"
    echo "Successful attempts: $successful_attempts"
    echo "Failed attempts:     $failed_attempts_count"
    echo
    echo "Failed Attempts by IP"
    echo "---------------------"

    for ip in "${!failed_attempts[@]}"; do
        echo "$ip    ${failed_attempts[$ip]}"

        if [ "${failed_attempts[$ip]}" -ge "$THRESHOLD" ]; then
            echo "[HIGH] Possible brute-force attack from $ip"
        fi
    done
} > "$REPORT_FILE"

---
name: linux-host-ops
description: Defensive Linux host operations for local maintenance and troubleshooting. Use for Arch/Linux cases involving NetworkManager, iwd, Wi-Fi, systemd services, journalctl logs, permissions, disk/log cleanup, packages, kernel/module diagnosis, rollback-safe host tweaks, and non-offensive incident triage.
risk: medium
source: local
---

# Linux Host Ops

Use this skill for authorized local Linux host maintenance, stability, and defensive diagnosis.

## Scope
- Arch/Linux package, service, boot, kernel/module, permission, disk, log, and config issues.
- NetworkManager, iwd, Wi-Fi, DNS, firewall, VPN, and connectivity diagnosis.
- systemd units, timers, journalctl, audit logs, and rollback-safe host tweaks.
- Defensive incident triage on owned systems without exploit development.

## Operating Rules
- Inspect current state before proposing changes: distro, service manager, active network stack, relevant config, logs, and recent changes.
- Treat `/etc`, auth, firewall, network, package manager, bootloader, kernel, and user data operations as high-risk.
- Before destructive or disruptive actions, state exact impact and rollback path, then wait for explicit confirmation.
- Prefer read-only checks first; avoid blind restarts, broad permission changes, package removals, or config rewrites.
- Never print secrets from configs, env, keyrings, tokens, browser stores, or logs.

## Diagnosis Flow
1. Identify symptom, scope, and last-known-good state.
2. Inspect service status, logs, config precedence, package ownership, and relevant kernel/network state.
3. Form one or two testable hypotheses.
4. Apply the smallest reversible fix.
5. Verify behavior and document rollback.

## Verification
- Confirm service/config state after changes.
- Re-check logs for repeated errors.
- For network cases, test DNS, route, interface, and direct IP separately.
- For performance/storage cases, compare before/after metrics.

## Escalation
If the task becomes malware analysis, memory forensics, cloud IR, or exploit testing, route to the more specific defensive skill and confirm authorization/scope first.

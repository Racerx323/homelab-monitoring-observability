# Uptime Kuma active monitoring

## Objective and baseline

Review the monitors Aaron configured on `j2-svpi3bmf` and the coverage published on [The AMA Homelab](https://uptime.local.theama.co/status/one). Use the existing settings as the starting point for workload and alert acceptance. Select any changes after reviewing what failures the current checks can detect.

The [installation result](../2026-11-09-uptime-kuma/RESULT.md) records zero configured monitors and notifications at acceptance. The Pi’s capacity observations cover that empty workload. Host mail used the shared fleet transport. The subsequent delivery check is recorded in the work ledger. Two off-node backup hashes were verified at installation closeout. Aaron selected svmf (10.1.3.83) as the recurring backup target.

## Service and host coverage

Use the hostname and protocol clients use for each service. Publish the eight service checks, six host checks and external heartbeat on the status page as approved on November 24. Keep per-host reachability in a separate operator group so a failed standby can alert while the service stays up. Kuma on the Pi observes the network from one location. An independent observer must cover loss of the Pi or monitoring process.

| Existing service | Proposed check |
| --- | --- |
| DNS Cluster | Query the shared resolver for a stable local record. Verify the known answer where supported. Cover IPv6 resolver transport separately if clients depend on it. |
| Proxy Cluster | Require exactly HTTP 204 with trusted TLS at the proxy’s root health route. Keep the Munin HTTPS keyword probe as a check through to an application. |
| NTP and NTP1 | Retain protocol checks on both configured endpoints. Confirm which names clients use before labeling a check as shared-service coverage. |
| Apprise-API and SMTP Relay | Use the notification owner’s API status endpoint and the SMTP listener for component availability. Verify delivery through the selected production route separately. |

Start with one direct management-address probe per inventory host, using ICMP where it is allowed. Use a known management TCP listener where ICMP is filtered and label the result accordingly. A missed probe shows loss of reachability from its observer. For the Kuma host use an independent observer. Proposed paging default is a 60-second interval with two retries 30 seconds apart for fast LAN checks. Retain the existing five-minute NTP schedule initially. Confirm the expected failure-detection time before applying these settings.

Repeat the private DOWN/UP delivery test after changing the alert route. Confirm both transitions at the final destinations. Aaron deferred scheduled end-to-end delivery tests. Kuma sends a heartbeat using a private ping URL to Healthchecks.io every five minutes. Allow ten minutes of grace. Verify the external check detects a missed heartbeat, returns to UP when Kuma resumes, and emails Aaron directly on both transitions.

## Approach and acceptance

| ID | Outcome | Verification |
| --- | --- | --- |
| AC-001 | Service checks measure user-visible availability. Host checks independently measure reachability of each selected host. | Agree on the endpoint, expected response, interval, timeout and retry policy. After activation, compare the stored settings and observed checks with that definition. |
| AC-002 | The Pi supports the selected workload. | During a representative polling window, check dashboard availability, restarts, memory headroom and data growth against the [existing resource limits](../../uptime-kuma/manifests/deployment.yaml). Record the interval and limits of the observation. |
| AC-003 | An actionable failure and its recovery reach the selected destination. | Agree on the recipient and a safe test method with the notification owner. Correlate Kuma’s state changes with receipt at the destination. |
| AC-004 | Operators can maintain or withdraw the monitor. | Record its owner, alert route, backup coverage and how to pause it in the [operations guide](../../uptime-kuma/docs/OPERATIONS.md). |

## Recurring backup policy

Prepare one nightly off-node copy of the Pi’s complete Kuma data on svmf. Use a consistent SQLite snapshot and include the other application data. Provision a dedicated writer for `/var/backups/uptime-kuma/` on svmf’s local NVMe filesystem. Use mode 0700 for the directory and 0600 for archives. Verify a transfer under the writer identity before scheduling. Keep the latest seven successful daily copies. Rotate only after a new archive has been received and verified. Before accepting coverage, restore one copy in isolation and verify the populated monitor inventory, status-page groups and notification assignments with outbound notifications disabled.

## Execution and recovery

The [accepted result](RESULT.md) records completion of this plan. For subsequent changes, review the affected checks, observation window, resource thresholds, alert destinations and recovery before activation. Preserve the manually configured monitors and status-page groups. Before applying a change, verify current settings and the recovery copy. If checks target the wrong service, alerts misroute, or the workload breaches the agreed limits, pause the new monitor, detach its notification route and verify dashboard health and prior configuration. A test must preserve service availability.

# Anti-Entropy

Anti-Entropy in Consul is better described on this document [Anti-Entropy Enforcement](https://developer.hashicorp.com/consul/docs/architecture/anti-entropy).

## Summary

- **Purpose:** Anti-entropy keeps the Consul cluster's state consistent and ordered, counteracting disorder in distributed systems.

- **Components:**
  - **Agent:** Maintains local state, service, and health check registrations. Runs health checks and updates its own state.
  - **Catalog:** Maintained by server nodes, provides a global, consistent view of the cluster, and aggregates agent information for service discovery.

- **How It Works:**
  - Synchronizes agent local state with the global catalog.
  - When a service or check is registered or deleted on the agent, the change is reflected in the catalog.
  - The agent's state is authoritative; if there's a mismatch, the catalog is updated to match the agent.
  - Services/checks in the catalog but not on the agent are removed.

- **Periodic Synchronization:**
  - Anti-entropy runs on changes and periodically (interval depends on cluster size) to keep the catalog in sync with agents.
  - Sync intervals are staggered to avoid spikes.

- **Best-Effort Sync:**
  - If a sync fails (due to misconfiguration, I/O, or network issues), the agent logs the error and retries later.

- **Tag Override:**
  - The `enable_tag_override` parameter allows external sources to override service tags during anti-entropy syncs.


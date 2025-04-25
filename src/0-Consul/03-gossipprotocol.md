# 03. Gossip Protocol

Consul's gossip protocol is described in detail in the [official documentation](https://developer.hashicorp.com/consul/docs/architecture/gossip).

## Summary

- **Purpose:** The [gossip protocol](https://en.wikipedia.org/wiki/Gossip_protocol) in Consul manages cluster membership and message broadcasting, ensuring nodes are aware of each other and can communicate efficiently.

- **Implementation:**

  - Consul uses the [Serf library](https://github.com/hashicorp/serf/), which implements a modified version of the [SWIM (Scalable Weakly-consistent Infection-style Process Group Membership)](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf) protocol.
  - The protocol is enhanced with "Lifeguard" improvements for better reliability and situational awareness.

- **Gossip Pools:**

  - **LAN Gossip Pool:**
    - Exists within each datacenter and includes all clients and servers.
    - Enables automatic server discovery, distributed failure detection, and fast event broadcasting.
  - **WAN Gossip Pool:**
    - Globally unique and includes all servers across datacenters.
    - Supports cross-datacenter requests and robust failure detection for inter-datacenter connectivity.

- **Lifeguard Enhancements:**

  - Addresses issues where local node resource exhaustion could cause false failure detection.
  - Improves the reliability of the protocol by making failure detection more situationally aware, reducing false alarms and unnecessary resource usage.

- **Additional Resources:**
  - For more technical details, see the [Serf documentation](https://developer.hashicorp.com/consul/docs/architecture/gossip#serf-documentation) and the [Lifeguard research paper](https://www.hashicorp.com/blog/making-gossip-more-robust-with-lifeguard).

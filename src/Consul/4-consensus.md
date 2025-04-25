# 4. Consensus Protocol

Consul's consensus protocol is described in detail in the [official documentation](https://developer.hashicorp.com/consul/docs/architecture/consensus).

## Summary

- **Purpose:**

  - The consensus protocol in Consul ensures consistency (as defined by the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)) for cluster state and operations.
  - It is based on the Raft algorithm, which is designed to be understandable and robust.

- **Key Concepts:**

  - **Log:** An ordered sequence of entries that record all changes in the cluster. Consistency is achieved when all nodes agree on the log's contents and order.
  - **Peer Set:** All server nodes in a datacenter participate in log replication and consensus.
  - **Quorum:** A majority of the peer set (N/2 + 1) is required to commit entries and maintain availability.
  - **Leader:** One server is elected as leader, responsible for ingesting new log entries, replicating to followers, and managing commits.
  - **Committed Entry:** An entry is committed when stored on a quorum of nodes and can then be applied to the state machine.
  - **Finite State Machine (FSM):** Consul uses a deterministic FSM (MemDB) to maintain cluster state.

- **Raft Protocol Overview:**

  - Nodes can be in one of three states:
  - follower: Followers accept log entries and cast votes. If no leader is detected, a node becomes a candidate and requests votes.
  - candidate: A candidate with a quorum of votes becomes leader, accepts new log entries, and replicates them to followers.
  - leader: All writes go through the leader; reads can be served in different consistency modes.

- **Consistency Modes:**

  - **Default:** Fast reads, may be slightly stale due to leader leasing.
  - **Consistent:** Strongly consistent reads, requires a round-trip to a quorum, higher latency.
  - **Stale:** Any server can serve reads, may be arbitrarily stale but very fast and available.

- **Cluster Operations:**

  - Only server nodes participate in Raft; clients forward requests to servers.
  - Each datacenter has its own independent Raft cluster and leader.
  - Data is partitioned by datacenter for performance and availability.

- **Fault Tolerance and Deployment:**

  - A cluster can tolerate up to (N-1)/2 failures (e.g., 3 nodes tolerate 1 failure, 5 nodes tolerate 2).
  - Recommended to run 3 or 5 servers per datacenter for best balance of availability and performance.
  - If quorum is lost, the cluster becomes unavailable and manual intervention is required.

- **Additional Resources:**
  - For a visual explanation of Raft, see [The Secret Lives of Data](https://thesecretlivesofdata.com/raft/).
  - For the full Raft specification, see the [original paper](https://raft.github.io/raft.pdf).

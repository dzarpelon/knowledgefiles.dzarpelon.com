# Understanding Consul Agents

Consul Agents are lightweight process on each node.
Client runs on every node where there are services.

More information on agents can be found in [Agents overview](https://developer.hashicorp.com/consul/docs/agent#consul-agent)

## Agent Lifecycle

Here's the lifecycle of a Consul agent within a cluster:

1. **Start**: The agent starts and joins the cluster. This can be either manually or automatically.
2. **Join**: The agent joins the cluster and starts to communicate with other agents.
3. **Information gossip**: Information about the agent is send to other agents in the cluster. This makes the nodes aware of each other.
4. **Replication**: If the agent is a server, the other server agents will replicate the info to it.

## Failures and crashes.

- Unreachable nodes are marked as `failed`.
- There's no distinction between a network crash and an agent crash, so they are treated the same.
- The catalog can only updated if it still has a quorum.
- Once the node is reachable again, it will rejoin the cluster and update its state. It will them be unmarked as `failed`.

- The agent will rejoin the cluster and update its state.

## Exiting nodes

- Nodes exiting the cluster are marked as `left`.
- Once it is left, all of the services provided by the node are removed.
- Consul automatically removes "dead nodes" (left or failed nodes) out of the catalog.
- The above is done every 72 hours by default. This can be configured, it is not recommended as it have repercussions during outages.

## Limiting traffic rates

- Used to protect the cluster from being overwhelmed by too many requests.
- Helps avoid service interruptions.
- Can be done globally.
- Allow Consul to deny read or write requests that exceed the rate limit.
- More info on rate limiting can be found in [Traffic rate limiting overview](https://developer.hashicorp.com/consul/docs/agent/limits)

## Requirements

- One agent per server or node.
- At least one server agent per deployment. 3 to five is recommended.
- Because of the gossip protocol a latency requirement is in place.
  - Average RTT can not exceed 50ms.
  - RTT for 99% of the traffic cannot exceed 100ms.

## Agent startup output

- When running `  consul agent`, the command will output something like this:

```bash
consul agent -data-dir=/tmp/consul
==> Starting Consul agent...
==> Consul agent running!
       Node name: 'Armons-MacBook-Air'
      Datacenter: 'dc1'
          Server: false (bootstrap: false)
     Client Addr: 127.0.0.1 (HTTP: 8500, DNS: 8600)
    Cluster Addr: 192.168.1.43 (LAN: 8301, WAN: 8302)

==> Log data will now stream in as it occurs:

    [INFO] serf: EventMemberJoin: Armons-MacBook-Air.local 192.168.1.43
...
```

- The output will show the following:
  - Node name
  - Datacenter
  - Server
  - Client address
  - Cluster address
  - Log data

## Configuring agents:

- Consul agents can be configured using a json file. that can be done like this:

```bash
consul agent -config-file=agent.json
```

- Some common configurations can be found [here](https://developer.hashicorp.com/consul/docs/agent#common-configuration-settings)

## Stopping the agent

- When gracefully stopped, the agent will first notify the cluster it intends to leave, so the other agents can notify the cluster that the node has left.
- When gracefully exited, the server agent will **not** be marked as left. Instead it will be marked as failed to keep the quorum consensus.
- To remove the node from the cluster, we should use `-force-leave` command. Which will put the server in a `left` state.
- We can also force the agent stop by using `kill -KILL consul_pid` command. Which will instantly kill the agent.
- In that case the other agents will detect the failure and mark the node as `failed`.
- On cliet agents the distinction between `left` and `failed` does not matter much. The service will be removed from the catalog anyways.
  - The above can be configured using `skip_leave_on_interrupt` or `leave_on_terminate` flags.
    - skip_leave_on_interrupt: When Consul receives an interrupt signal (such as hitting Control-C in a terminal), Consul will gracefully leave the cluster. Setting this to true disables that behavior. For client agents this is set to false by default and for server agents it is set to true by default.
    - leave_on_terminate: it will send a Leave message to the rest of the cluster and gracefully leave. Client agents have this setting set to true by default. Server agents have this set to false by default.

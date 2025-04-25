# 1. Introduction to Consul

These notes are based on the Youtube video <a href="https://youtu.be/mxeMdl0KvBI" target="_blank" rel="noopener">Introduction to HashiCorp Consul with Armon Dadgar</a> at the official Hashicorp channel.

<div style="text-align: center;">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/mxeMdl0KvBI" frameborder="0" allowfullscreen></iframe>
</div>

## Summary

- The change from monolithic applications to microservices introduces a few challenges as now the services are distributed and communication occurs via network.
- One of these challenges is service discovery.
- Before, this issue was tackled by adding load balancers and hardcoding the LB IP address in the application, which adds latency and is not flexible.
- Consul solves this problem by using a service registry. When applications start, they register themselves in the registry, and discover each other by querying it.
- Health information (if a service is up or down) is also stored in the registry, mimicking the LB without needing one.
- Another big challenge brought by microservices is configuration management, as each service has a different view of the configuration. Consul provides a key-value store for configuration data.
- The network pattern is more complex in microservices, as the traditional three layers of the monolithic network (DMZ, Internal, DB) are no longer present, leading to a third challenge: segmentation.
- That challenge is dealt by Consul with a feature called Connect.
- Connect has two basic components:
  - The TLS certificates that are created for each service. These are used to ascertain service identity.
  - The Service Graph. This is a graph that shows the relationships between services and how they communicate with each other. Fundamentally working as an ACL between services.
  - The way this works is that when a service is deployed a sidecar proxy is added to it. This proxy is responsible for managing the communication between the service and the rest of the network. The proxy is configured to only allow communication with other services that are allowed to communicate with it. This is done by using the service graph to determine which services are allowed to communicate with each other. And the proxy is tied to the particular service identity via the TLS certificate.

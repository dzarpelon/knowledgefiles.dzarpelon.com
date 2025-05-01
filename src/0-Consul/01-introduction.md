# 01. Introduction to Consul

These notes are based on the Youtube video <a href="https://youtu.be/mxeMdl0KvBI" target="_blank" rel="noopener">Introduction to HashiCorp Consul with Armon Dadgar</a> at the oficial Hashicorp channel.

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/mxeMdl0KvBI" frameborder="0" allowfullscreen></iframe>
</div>
- The change from monolitic applications to microservices introduces a few challenges as now the services are distributed and communication occurs via network. ]
- One of these challenges is service discovery.
- Before we tackled this issue by adding load balancers and hardcoding the LB ip address in the application.
- That adds latency and is not flexible.
- The way Consul tries to solve this problem is by using a service registry.
- When applications start they register themselves in the registry.
- The applications discover each other by querying the registry.
- Information about the health of a service (if it's up or down) is also stored in the registry. These mimics the LB without the need for it.
- The other big challenge brought by microservices is configuration management.Because each service has a different "view" of the configuratiuon. So that needs to be managed.
- Consul provides a key-value store that can be used to store configuration data.
- Also, the network pattern is more complex as now we don't have anymore the three layers of the monolitic network ( DMZ, Internal, DB).
- This generates a third challenge: Segmentation.

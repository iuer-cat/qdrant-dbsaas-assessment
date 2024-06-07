Networking
==========

Currently, it seems that Qdrant Cloud only offers public access to
managed clusters. Recently, they launched a Hybrid Cloud product
which, in my opinion, adopts a mixed on-prem deployment model. In
this model, although the cluster remains within the client's
boundaries, it can be partially managed from Qdrant Cloud's Control
Plane.

This use case is relevant for those implementations where, due to
latency or regulation issues, the data cannot be hosted in the
cloud. This practice is common in many professional solutions.

However, there are more configuration options or network topologies
that could be interesting and that Qdrant seems to lack so far.

1 - VPC Level Peerings
    Major Cloud Providers have been offering VPC peerings for years.
    These are essentially cross-account network connections that
    allow communications to flow through private networks belonging
    to the same Cloud provider and not be exposed to the Internet.
    Some providers of solutions similar to Qdrant like Mongo or
    Elastic offer the creation of automated peerings, which
    increases the security of the data and reduces its latency.
    This solution is ideal for clients who have their workloads
    hosted in the cloud.

2 - Network Access Control
    In both the case of services exposed to the internet and the
    case of services connected via peering, it is interesting to
    have network-based access control systems. This essentially
    means application firewalls that filter or grant access based on
    the IP or CIDR of a client. Just like in the case of Peerings,
    some providers like Mongo Cloud provide this service, which
    helps to improve security and control access to information.

3 - Private Links
    This arrangement is a bit more complex and is served by major
    Cloud Providers. It consists of creating a private network
    channel between the Qdrant cluster and an external location
    outside the cloud where the client has their applications.
    Basically, it connects on-premise networks to the Qdrant cloud,
    unlike a VPN where traffic travels encrypted over the internet.
    In Private Links or Direct Connects, communication goes through
    dedicated channels of low latency and high bandwidth. These are
    complex solutions, where the client wants the cluster to remain
    managed but the flow of their data to be private and low latency.

Scope
=====


Analysis and Contextualization
------------------------------
The test describes the creation of a functional prototype capable of
fulfilling the following requirements.

- DBaaS or Database as a Service, able to start with the capacity to
  select the desired computational **resources** as well as the number of **nodes**
  served via **API**.

- Such a system must be capable of provisioning *Qdrant* on one of the major
  cloud providers, and although the implementation of one is specified,
  it is also required to be designed to function in a **multi-cloud** environment.

- The endpoint connection with the *Qdrant* cluster must be protected by
  **token-based** authentication.

- It is also requested to describe by analyzing the pros and cons of
  different network configurations associated with a *Qdrant* cluster.

Once the prototype is completed, it will have to be defended in a call
during an architecture discussion.

In addition to the technical requirements of the prototype, it is determined
that support 'material' such as diagrams or documentation is expected to
enrich the discussion.


Assumptions of the Challenge
----------------------------
The focus and wording of the tech-test challenge are clearly oriented
towards *Qdrant's* main product, its private cloud, similar to Hashicorp
Cloud, Mongo Cloud, or Elastic Cloud. The *Qdrant* cloud solutions is one of
the ways to obtain Enterprise support for *Qdrant* as well as other variants
related to the marketplaces of AWS, Azure, and Google Cloud.

The assumptions I took addressing the architecture and the implementation,
broadly, have been the following:

- The fundamental piece of this work is the **DOCUMENTATION** you are
  reading, with all the added graphic material. The implementation,
  although **FUNCTIONAL**, accompanies the documentation and serves as an
  exemplification of what is explained here.

- Qdrant currently recommends that production environments be
  based on Kubernetes and also offers, under a free license, a Helm
  Chart for installation and, optionally upon request, a K8s Operator.
  The Helm Chart has been used, as it was not possible to find the
  K8s Operator.

- Given that Kubernetes is a container orchestrator that offers a
  ubiquitous cross-cloud provider API and that operational differences
  between Cloud providers are small (especially affecting network and
  storage resources) we have assumed that such divergences can be
  addressed at the level of the Helm Chart, or the K8s Operator or
  similar without the implementation here requiring major changes or
  being highly coupled to the proprietary APIs of each Cloud-Provider.

- Application testing has been voluntarily omitted, due to scope
  and timing reasons, although it is an interesting field of exploration
  due to the high coupling with infrastructure that the product has.

- Issues of CI/CD for the services have also not been considered,
  due to scope and timing reasons.
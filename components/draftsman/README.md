# What is Draftsman?

Draftsman is a conceptual component, one of the most crucial, encompassing
all IaaC code, pipelines, and automation required to manage the lifecycle of
Kubernetes infrastructure across various cloud providers for this prototype.

Draftsman is intentionally outlined in a vague manner; it is neither functional
nor complete. This is deliberate because the underlying infrastructure depends
on business-level decisions such as budget or the Total Cost of Ownership (TCO)
that is acceptable for the given solution.

For example, Qdrant could opt to use Kubernetes plus Serverless to simplify
infrastructure management at the cost of slightly higher expenditures per
computed unit (CPU, Memory, RAM).

On another note, at a certain scale (once the service gains traction), it might
be beneficial to shift to an architecture based on large On-Demand or Reserved
hosts. Furthermore, the technical specifications of the underlying
infrastructure could influence decisions, such as the fact that different
instance types have varying clock speeds for both memory and CPU, which might
be advantageous.

Given the wide array of configurations and the non-uniformity of cloud providers
where Qdrant will be deployed, this prototype assumes the most pragmatic choice:
Managed Kubernetes + Serverless Workloads, delegating resource auto-scaling
management to the provider.
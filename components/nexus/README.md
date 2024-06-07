# What is Nexus?

Nexus is conceptually and architecturally a shared library, or as I prefer to
call it, a Shared Kernel (DDD).

Primarily, Nexus serves two purposes: it facilitates the reuse of critical
components common to several projects, and it acts as an external boundary
that defines the criticality of the elements it contains, such as contracts
(Ports) or models that are expected to be common.

Ideally, the Shared Kernel should be as small as possible, since its very
existence creates coupling. However, it also protects the domain and alerts
developers to the potential side effects that changes in this library could
trigger.

With the addition of Nexus as a Shared Kernel, we go beyond the typical 'utils'
modules or packages found in multiple projects, attempting to define and
strictly delineate its contents.

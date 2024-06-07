## Why I add these Models?

These models are not strictly necessary within the context of the statement, 
and even less so in the context of a prototype or proof of concept as described 
in the statement.

However, the nexus component and the concepts of service bus, command bus, and 
event bus have been with me for several years when creating distributed systems 
based on messaging.

Due to the heterogeneity of some systems I have worked on, solutions like Celery 
workers and others have shown certain difficulties when integrating with other 
systems. From there, the idea arose to transfer anemic DTOs that could be 
validated with a schema and expressed in Plain JSON.

The modeling you see has not been specifically created for this project. On the 
contrary, you should consider it as if I were leveraging a third-party library 
in order to maintain the schema-integrity of the messages from one system to 
another.

I found it interesting not to oversimplify this part since it can lead to debate 
about asynchronous communication between distributed systems.
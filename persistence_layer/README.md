# What is the 'Persistence Layer'?

The prototype has been designed to minimize complexity to facilitate
understanding and to focus sharply on the required architecture and features.

Thus, all persistence mechanisms, such as databases and queues, have been
emulated using plain text files. This approach not only avoids a large amount
of boilerplate code but also aids in understanding how components communicate
with each other and what the state of the entire prototype looks like.

The decision to use file-based persistence was deliberate and allows for
the storage of this data in a Git repository, making it easier to access,
explain, and discuss during the technical discussion accompanying this tech
challenge.
# Chord-DHT-Implementation
A simple implementation of Chord P2P Distributed Hash Table

Chord is a protocol and algorithm for a peer-to-peer distributed hash table. A distributed hash table stores key-value pairs by assigning keys to different computers (known as “nodes”); a node will store the values for all the keys for which it is responsible. Chord specifies how keys are assigned to nodes, and how a node can discover the value for a given key by first locating the node responsible for that key.
Chord is based on consistent hashing.

I have evaluated the performance of my network for different number of nodes in the network. There will be three configurations, with number of nodes as 100, 500 and 1000. For each configuration I have performed 100000 random search queries, after populating the network with 10,000 data points. I have performed following operations for each of the configurations:

* Average number of hops for search queries.
* A histogram showing the distribution of the hops required.
* Operation: Delete half of the nodes from the network, randomly.
* Average number of hops for search queries in this reduced set.
* A histogram showing the distribution of the hops required in this reduced set.

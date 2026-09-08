# System Design Interview Questions

## Easy

### Q1: What is the difference between Vertical Scaling and Horizontal Scaling?
**Answer:** Vertical scaling (scaling up) involves increasing the computing capacity of an existing single server by upgrading its hardware resources, such as adding more RAM, faster CPU cores, or larger SSD storage. Horizontal scaling (scaling out) involves adding more server instances to the resource pool and distributing incoming traffic across them using a load balancer. While vertical scaling is simple to implement and introduces no distributed systems complexity, it has strict hardware limits and creates a single point of failure. Horizontal scaling provides virtually limitless elasticity, fault tolerance, and high availability, but requires distributed architecture patterns, stateless application servers, and network-level coordination.
**Key Points:**
- Vertical (Scaling Up): Adding CPU, RAM, or storage to an existing single machine.
- Horizontal (Scaling Out): Adding more independent server instances to a cluster behind a load balancer.
- Cost/Limits: Vertical hits physical hardware limits and exponential costs; horizontal scales cost-effectively on commodity hardware.
- Fault Tolerance: Vertical has a single point of failure; horizontal provides high redundancy and zero-downtime rolling upgrades.
**Evaluation Criteria:** Candidate should clearly differentiate between adding hardware to a single machine vs adding machines to a network, discuss physical limits vs elasticity, and mention single-point-of-failure risks.

### Q2: What is a Load Balancer and what are common load balancing algorithms?
**Answer:** A load balancer is a reverse proxy device or software service that sits between client devices and backend server pools, evenly distributing incoming network traffic across multiple healthy servers to prevent any single server from becoming overwhelmed. It enhances system capacity, responsiveness, and overall availability by conducting health checks and automatically routing traffic away from failed nodes. Common load balancing algorithms include **Round Robin** (sequentially distributes requests), **Weighted Round Robin** (allocates traffic based on server capacity ratings), **Least Connections** (routes requests to the server with the fewest active sessions), **IP Hash** (hashes client IP to route repeat users to the same server for session affinity), and **Random**. Load balancing can occur at Layer 4 (Transport layer, TCP/UDP routing based on IP/Port) or Layer 7 (Application layer, HTTP routing based on URLs, headers, and cookies).
**Key Points:**
- Acts as reverse proxy distributing incoming traffic across server clusters.
- Performs continuous health checks to dynamically remove failing nodes from traffic pools.
- Common algorithms: Round Robin, Weighted Round Robin, Least Connections, IP Hash.
- Operates at Layer 4 (transport protocol routing) or Layer 7 (application-aware HTTP path/header routing).
**Evaluation Criteria:** Candidate should explain the functional role of a load balancer, describe at least three algorithms with appropriate use cases, and distinguish between L4 and L7 load balancing.

### Q3: What is Caching and where can caching layers be placed in a distributed system?
**Answer:** Caching is the technique of storing copies of frequently accessed or computationally expensive data in high-speed, temporary storage (typically in-memory RAM) so that future requests can be served significantly faster than querying the primary data store. By exploiting the principle of locality (temporal and spatial), caching dramatically cuts down read latency and protects backend databases from high request volumes. Caching layers can be placed at multiple architectural tiers: **Client-side** (browser or mobile cache), **Edge/Network tier** (Content Delivery Networks and reverse proxies), **Web/API tier** (in-memory local app cache or web server accelerators like Varnish), **Application/Distributed tier** (dedicated shared in-memory stores like Redis or Memcached), and **Database tier** (internal database buffer pools and query result caches).
**Key Points:**
- Stores high-frequency data in fast in-memory storage (RAM) to minimize read latency.
- Exploits temporal (recently used) and spatial (nearby data) locality.
- Caching tiers: Browser/Client -> CDN/Edge -> Web/Reverse Proxy -> Distributed App Cache (Redis/Memcached) -> Database Buffer Pool.
- Massive read throughput boost, but introduces cache coherence and invalidation challenges.
**Evaluation Criteria:** Candidate should define caching and locality, enumerate multiple tiers where caches reside from client to database, and identify trade-offs like data freshness.

### Q4: What is a Content Delivery Network (CDN) and how does it reduce latency?
**Answer:** A Content Delivery Network (CDN) is a geographically distributed network of proxy edge servers (Points of Presence - PoPs) deployed worldwide to deliver web content quickly to end users. When a user requests assets like images, videos, CSS, JavaScript, or static HTML, the request is geographically routed via Anycast DNS to the nearest edge PoP rather than traveling across global transit networks to the central origin server. If the edge server has the asset cached, it serves it immediately with minimal round-trip time (RTT); if it is a cache miss, the CDN fetches it from origin, caches it locally, and serves the user. CDNs drastically reduce network latency, absorb massive traffic spikes (such as DDoS attacks), and significantly offload bandwidth consumption from origin infrastructure.
**Key Points:**
- Geographically dispersed network of edge servers (PoPs) caching static and dynamic web content.
- Minimizes physical distance between user and server, cutting Round-Trip Time (RTT).
- Uses Anycast routing and GeoDNS to direct requests to the closest physical PoP.
- Offloads traffic and egress bandwidth from origin servers and absorbs volumetric DDoS attacks.
**Evaluation Criteria:** Candidate should explain physical proximity/RTT reduction, describe the edge-to-origin cache-fill workflow, and mention security/bandwidth offloading benefits.

### Q5: What is the CAP Theorem and what are its three fundamental properties?
**Answer:** The CAP Theorem (Brewer's Theorem) states that any distributed data store can simultaneously provide at most two out of three fundamental guarantees: **Consistency (C)**, **Availability (A)**, and **Partition Tolerance (P)**. Consistency means every read receives the most recent write or an error (linearizability). Availability means every non-failing node returns a non-error response for every received request, without guaranteeing it contains the absolute latest write. Partition Tolerance means the system continues to operate despite an arbitrary number of messages being dropped or delayed by the network between nodes. Because physical network partitions and cable cuts are an unavoidable reality of distributed hardware, a system must always choose Partition Tolerance; therefore, the practical trade-off in network failures is strictly between Consistency (CP systems, e.g., HBase, Spanner) and Availability (AP systems, e.g., Cassandra, DynamoDB).
**Key Points:**
- Consistency: Every read receives the most recent write or errors out (linearizable reads).
- Availability: Every request receives a valid, non-error response, regardless of recency.
- Partition Tolerance: System continues functioning despite arbitrary network message loss or delay.
- In distributed networks, P is non-negotiable; thus the trade-off is strictly between CP and AP during network partitions.
**Evaluation Criteria:** Candidate must accurately define C, A, and P, emphasize that network partitions are inevitable in real-world systems, and clearly explain the binary trade-off between CP and AP.

### Q6: What is an API Gateway and what core responsibilities does it handle?
**Answer:** An API Gateway is a centralized architectural entry point that sits between external client applications (web, mobile, third-party) and internal backend microservices. It acts as a reverse proxy, insulating client applications from internal service topologies, network protocols, and decomposition changes. Core responsibilities handled by an API Gateway include **Request Routing** (routing URLs to appropriate downstream microservices), **Authentication and Authorization** (validating API tokens, OAuth, and JWTs centrally), **Rate Limiting and Throttling** (protecting services from abuse), **SSL Termination** (offloading TLS handshakes), **Response Aggregation** (combining responses from multiple microservices into a single client payload), and **Logging, Metrics, and Tracing** for system observability.
**Key Points:**
- Centralized reverse proxy serving as the single entry point for all external client traffic.
- Decouples client applications from internal microservice architectures and topologies.
- Centralizes cross-cutting concerns: Auth/OAuth validation, SSL termination, rate limiting, CORS.
- Provides protocol translation (e.g., external REST/HTTP to internal gRPC) and response aggregation.
**Evaluation Criteria:** Candidate should define the gateway pattern, explain how it shields internal microservices, and list at least four distinct cross-cutting concerns handled at this layer.

### Q7: What is a Message Queue and why is asynchronous processing advantageous?
**Answer:** A message queue is an asynchronous point-to-point or pub/sub communication buffer (such as RabbitMQ, AWS SQS, or Apache ActiveMQ) that enables distributed services to communicate reliably without direct, synchronous coupling. A producer service publishes a message (a unit of work) to the queue, and one or more consumer services pull and process the message independently. The primary advantages of asynchronous processing include **Decoupling** (producers and consumers can evolve, deploy, and scale independently), **Buffering and Traffic Smoothing** (absorbing sudden traffic spikes by queuing requests rather than crashing downstream databases), **Improved Latency** (acknowledging user requests immediately while delegating heavy operations like image processing or email sending to background workers), and **Resilience** (if consumer services crash, messages remain safely queued until recovery).
**Key Points:**
- Asynchronous FIFO or pub/sub message buffer decoupling producers from consumers.
- Traffic smoothing / Load leveling: Queues incoming spikes to protect downstream backends from saturation.
- Lowers user perceived latency by delegating long-running jobs (emails, transcoding) to background workers.
- Enhances fault tolerance: Guarantees message persistence and retries if consumers temporarily fail.
**Evaluation Criteria:** Candidate should explain asynchronous decoupling, contrast synchronous HTTP calls with queued messages, and describe benefits regarding traffic spikes and fault resilience.

### Q8: What is Database Sharding (Horizontal Partitioning) and how does it differ from Vertical Partitioning?
**Answer:** Database sharding is a horizontal scaling technique that partitions a single large database dataset into smaller, faster, and more manageable subsets called shards, which are distributed across multiple independent physical database servers. In horizontal partitioning (sharding), rows of the same table are split across shards based on a defined **Shard Key** (e.g., routing User IDs 1-1M to Shard 1, and 1M-2M to Shard 2), with all shards sharing the identical schema. In contrast, vertical partitioning splits a database by columns or distinct functional domains—such as separating frequently accessed user profile columns into one table/server and large, rarely accessed text descriptions into another, or splitting Users and Orders into separate databases. Sharding enables near-infinite storage and write scaling, but introduces challenges like cross-shard joins, distributed transactions, and rebalancing hot shards.
**Key Points:**
- Horizontal Partitioning (Sharding): Splits table rows across multiple database servers using a Shard Key.
- Vertical Partitioning: Splits table columns or distinct domain tables onto separate machines.
- Overcomes single-node storage, memory, and write throughput limits.
- Challenges: Inability to run native cross-shard SQL joins, complex distributed transactions, and data rebalancing.
**Evaluation Criteria:** Candidate should contrast row-splitting (horizontal) with column/table-splitting (vertical), define the role of a Shard Key, and identify major operational challenges of sharding.

### Q9: What is Rate Limiting and why is it essential for production APIs?
**Answer:** Rate limiting is a traffic control strategy that caps the number of requests a client or IP address can submit to an API within a specified time window (e.g., 100 requests per minute). When a client exceeds this threshold, the API rejects subsequent requests with HTTP status code `429 Too Many Requests`. Rate limiting is essential in production to **prevent Denial of Service (DoS) attacks** (malicious or accidental request floods), **protect backend services from cascading failures** by keeping throughput within verified capacity limits, **eliminate the "Noisy Neighbor" problem** in multi-tenant SaaS environments, **prevent credential stuffing and brute-force attacks** on authentication endpoints, and **monetize API usage** by enforcing billing tiers.
**Key Points:**
- Restricts the frequency of client requests over a designated time window; returns HTTP 429 when breached.
- Security defense: Guards against volumetric DoS, credential stuffing, scraping, and brute-force attacks.
- System stability: Protects underlying databases and services from traffic saturation and cascading crashes.
- Multi-tenancy: Prevents individual abusive tenants from degrading performance for other users.
**Evaluation Criteria:** Candidate should state the HTTP 429 status code, identify security and stability motivations, and explain multi-tenant fair-sharing benefits.

### Q10: What is a Microservices Architecture and how does it differ from a Monolith?
**Answer:** A monolithic architecture packages all business logic, user interfaces, and data access layers into a single, unified codebase and single deployable artifact running against a centralized database. A microservices architecture decomposes the application into a collection of small, autonomous, loosely coupled services, where each service models a single business capability (domain-driven design) and maintains its own private database. While monoliths are simpler to develop, test, and deploy initially with zero network overhead, they become unwieldy bottlenecks as engineering teams scale, where small bugs can crash the entire application and deployments require coordinating entire teams. Microservices allow independent deployments, heterogeneous technology stacks, isolated failure domains, and targeted scaling of high-demand services, at the cost of substantial distributed systems complexity (network latency, distributed data consistency, and distributed tracing).
**Key Points:**
- Monolith: Single unified codebase, single deployable artifact, shared centralized database.
- Microservices: Suite of small, loosely coupled services organized around business capabilities with private databases.
- Monolith advantages: Simple local development, easy cross-table joins, atomic transactions, no network overhead.
- Microservices advantages: Independent deployment cycles, decoupled scaling, fault isolation, polyglot tech stacks.
- Microservices trade-offs: Network latency, eventual consistency, complex distributed tracing and observability.
**Evaluation Criteria:** Candidate should contrast code and database deployment models, weigh operational complexity against organizational scaling, and highlight trade-offs in data consistency.

---

## Medium

### Q1: Explain Cache Invalidation Strategies (Write-Through, Write-Back / Write-Behind, Cache-Aside, Write-Around) and their trade-offs.
**Answer:** Cache invalidation strategies dictate how data flows between application code, the cache, and the underlying database during read and write operations. In **Cache-Aside (Lazy Loading)**, the application first checks the cache; on a hit, it returns the data, and on a miss, it fetches from the database, writes to the cache, and returns; writes go directly to the database followed by cache invalidation. In **Write-Through**, data is written to the cache and the database synchronously within the same call; reads are fast and cache data is never stale, but write latency is high. In **Write-Back (Write-Behind)**, the application writes only to the cache, which immediately acknowledges the write; an asynchronous background worker batches writes to the primary database later, providing ultra-low write latency at the risk of permanent data loss if the cache crashes before flushing. In **Write-Around**, writes go directly to the database without touching the cache, preventing the cache from being flooded with data that may never be read again, but causing immediate cache misses on subsequent reads.
**Key Points:**
- Cache-Aside: App coordinates cache and DB; on miss loads from DB to cache; prone to stale reads if invalidation fails.
- Write-Through: Synchronous write to Cache + DB; high consistency, zero stale reads, high write latency.
- Write-Back / Write-Behind: Writes to Cache immediately; asynchronous delayed write to DB; ultra-fast writes, high data loss risk.
- Write-Around: Writes directly to DB bypassing cache; prevents cache pollution on write-heavy infrequent-read data.
**Evaluation Criteria:** Candidate must define all four strategies, diagram or explain the write/read data flows, and analyze the specific latency vs consistency trade-offs of each.

### Q2: What is Consistent Hashing and how does it solve rehashing overhead when adding or removing nodes in a distributed cache?
**Answer:** In naive distributed caching with N nodes, mapping a key to a server uses modulo arithmetic: `server = hash(key) % N`. When a node is added or removed, N changes to N+1 or N-1, causing almost 100% of all keys to rehash to completely different servers, triggering a catastrophic cache stampede that overwhelms the backend database. Consistent Hashing solves this by mapping both cache nodes and data keys onto a circular hash ring (e.g., from 0 to 2^32 - 1) using the same hash function. To find which server holds a key, the system hashes the key onto the ring and walks clockwise until it encounters the first server node. When a node is added or removed, only keys located in the immediate preceding sector of the ring must be remapped—on average only k/N keys, where k is total keys and N is total servers. Furthermore, by introducing **Virtual Nodes** (assigning multiple random points on the ring to each physical server), consistent hashing ensures uniform key distribution and eliminates hot spots.
**Key Points:**
- Naive modulo hashing `hash(k) % N` causes catastrophic ~100% key displacement when N changes.
- Consistent Hashing maps both keys and servers to a circular 0 to 2^32-1 hash ring.
- Routing: Walk clockwise from hash(key) to find the first encountered server.
- Node changes: Adding/removing a node displaces only k/N keys on average, preventing cache stampedes.
- Virtual Nodes: Maps each physical server to multiple positions on the ring to balance load uniformly.
**Evaluation Criteria:** Candidate should explain why modulo hashing fails, describe the circular ring and clockwise traversal, calculate key migration impact (k/N), and explain how virtual nodes prevent load skew.

### Q3: How do you design and implement a distributed Rate Limiter (Token Bucket, Leaky Bucket, Sliding Window Log, Sliding Window Counter)?
**Answer:** A distributed rate limiter controls request velocity across clustered API gateways using specialized rate-limiting algorithms backed by a fast in-memory store like Redis. **Token Bucket** maintains a bucket of capacity B that continuously refills with tokens at rate R per second; requests consume a token, allowing controlled bursts up to capacity B. **Leaky Bucket** processes requests at a strictly constant rate from a FIFO queue, smoothing out bursts completely into a steady output stream. **Sliding Window Log** logs the timestamp of every request in a Redis sorted set; it provides 100% precision by counting entries within `[now - window, now]`, but consumes excessive memory storing millions of timestamps. **Sliding Window Counter** approximates the log with minimal memory by taking a weighted sum of the previous window's count and current window's count: Count = Previous_Count * (1 - elapsed_fraction) + Current_Count. In distributed environments, race conditions between checking and decrementing counts are solved using atomic Redis Lua scripts or Redis cell modules.
**Key Points:**
- Token Bucket: Refills tokens at fixed rate R up to max B; permits controlled traffic bursts; standard API default.
- Leaky Bucket: Fixed-capacity queue leaking requests at constant rate; enforces rigid traffic smoothing.
- Sliding Window Log: Tracks timestamps in Redis Sorted Sets; perfectly accurate but high memory overhead.
- Sliding Window Counter: Weighted hybrid of current and previous window counts; highly memory efficient with <0.05% error.
- Distributed synchronization: Uses atomic Redis Lua scripts to prevent check-then-act race conditions.
**Evaluation Criteria:** Candidate should contrast all four algorithms, explain burst tolerance differences, formulate the sliding window counter approximation, and explain how Redis Lua scripts guarantee atomic concurrency.

### Q4: Compare Relational (SQL) and Non-Relational (NoSQL) databases, detailing when each is appropriate.
**Answer:** Relational (SQL) databases (such as PostgreSQL and MySQL) organize data into structured, fixed schemas with tables, rows, and foreign key relationships, enforcing ACID (Atomicity, Consistency, Isolation, Durability) transactions. They are optimal for systems requiring absolute data integrity, complex relational joins, and financial accuracy (e.g., banking, order processing, ERPs). Non-Relational (NoSQL) databases relax strict schemas and ACID guarantees (often embracing BASE: Basically Available, Soft state, Eventual consistency) to achieve horizontal scalability and high write throughput across distributed nodes. NoSQL encompasses four primary data models: **Document stores** (MongoDB, Couchbase) for flexible, semi-structured JSON hierarchies; **Key-Value stores** (Redis, DynamoDB) for high-speed lookups and caching; **Wide-Column stores** (Cassandra, ScyllaDB) for massive-scale time-series and write-heavy workloads; and **Graph databases** (Neo4j) for interconnected relationship traversal.
**Key Points:**
- SQL: Fixed schema, complex multi-table joins, vertical scaling, strict ACID compliance; standard for financial/transactional systems.
- NoSQL: Dynamic schema, denormalized structures, horizontal scaling, BASE/eventual consistency models.
- Document Stores: Hierarchical JSON/BSON entities (MongoDB).
- Key-Value Stores: O(1) latency lookups by primary key (Redis, DynamoDB).
- Wide-Column Stores: Distributed partition-key clustering for petabyte-scale writes (Cassandra).
- Graph Stores: Native index-free adjacency for complex relational networks (Neo4j).
**Evaluation Criteria:** Candidate should contrast ACID vs BASE, explain horizontal vs vertical scaling differences, and categorize NoSQL types with appropriate architectural use cases.

### Q5: What is the Saga Pattern and how does it manage distributed transactions across microservices compared to Two-Phase Commit (2PC)?
**Answer:** In a microservices architecture where each service has its own private database, traditional ACID transactions cannot span service boundaries. Two-Phase Commit (2PC) coordinates a distributed transaction using a central coordinator that executes a Prepare phase followed by a Commit phase; however, 2PC is blocking, suffers from poor performance over high-latency networks, and creates availability bottlenecks if the coordinator crashes while locks are held. The Saga Pattern solves this by decomposing a distributed transaction into a sequence of local ACID transactions across participating microservices. Each local transaction updates the service's database and publishes an event or message triggering the next step. If any local step fails (e.g., payment declined), the Saga executes a series of **Compensating Transactions** in reverse order to undo earlier changes (e.g., unreserving inventory and refunding vouchers). Sagas can be coordinated via **Choreography** (services listen to domain events and react autonomously) or **Orchestration** (a dedicated orchestrator service explicitly directs participants via command messages).
**Key Points:**
- Replaces blocking 2PC distributed transactions with a sequence of local database transactions.
- Compensating Transactions: Semantic undo operations executed in reverse order upon step failure.
- Choreography: Decentralized event-driven pub/sub; services react to neighbor events; simple for small flows.
- Orchestration: Centralized state machine directing participant services; easier to monitor and debug complex multi-step workflows.
- Trade-off: Guarantees Eventual Consistency rather than immediate isolation (susceptible to dirty reads during execution).
**Evaluation Criteria:** Candidate should explain why 2PC fails in microservices (blocking, coordinator failure, lock contention), describe compensating transactions, and contrast Choreography vs Orchestration.

### Q6: Explain Database Replication (Master-Slave / Primary-Replica vs Master-Master / Multi-Primary) and replication lag.
**Answer:** Database replication copies data across multiple database servers to improve read throughput, provide redundancy, and ensure high availability. In **Primary-Replica (Master-Slave)** architecture, all write operations (INSERT, UPDATE, DELETE) are directed to a single Primary node, which records changes in its write-ahead log (WAL) and replicates them to one or more read-only Replica nodes. This dramatically scales read capacity and allows replicas to be promoted if the primary fails, but can introduce **Replication Lag**—the time delay before writes propagate to replicas. In asynchronous replication, replication lag causes stale reads, where a user writes data and immediately refreshes to find their data missing (mitigated by read-your-own-writes routing). In **Multi-Primary (Master-Master)** architecture, multiple nodes accept both reads and writes, providing global low-latency writes and redundancy, but requiring complex conflict resolution mechanisms (such as Last-Write-Wins, CRDTs, or vector clocks) when concurrent conflicting writes hit different primary nodes.
**Key Points:**
- Primary-Replica: Single write master, multiple read replicas; isolates write traffic and scales read throughput.
- Synchronous replication guarantees zero data loss at the cost of high write latency; Asynchronous replication provides fast writes but risks replication lag.
- Replication Lag causes stale reads; mitigated by routing read-your-own-writes queries to the primary.
- Multi-Primary: Multiple nodes accept concurrent writes; requires conflict detection and resolution algorithms (LWW, CRDTs).
**Evaluation Criteria:** Candidate should contrast Primary-Replica and Multi-Primary architectures, analyze synchronous vs asynchronous replication trade-offs, explain replication lag, and propose mitigations for stale reads.

### Q7: How do you handle Idempotency in distributed APIs and payment processing systems?
**Answer:** An API operation is idempotent if executing it multiple times produces the exact same system state and outcome as executing it once: f(f(x)) = f(x). In distributed systems and payment workflows, network timeouts frequently occur after a server processes a charge but before the client receives the 200 OK response; naive client retries would result in duplicate billing. Idempotency is achieved by attaching a unique **Idempotency Key** (such as a UUIDv4 generated by the client) to every mutating request header: `Idempotency-Key: 123e4567-e89b...`. When the payment server receives the request, it checks an atomic in-memory lock/datastore (like Redis or PostgreSQL with unique constraints). If the key is new, the server records it with a status of `PROCESSING`, executes the transaction, stores the final API response payload, and returns the response. If a retry arrives with an existing key, the server detects the duplicate, skips payment execution, and immediately returns the cached original response.
**Key Points:**
- Idempotence: Executing identical requests repeatedly yields identical system state without duplicate side-effects.
- Solves network retry hazards where clients re-transmit after timeouts on completed operations.
- Client generates unique Idempotency Key (UUID) transmitted via request headers.
- Server uses atomic database locks to track state: `PROCESSING` -> `COMPLETED` with stored response payload.
- Subsequent requests with duplicate keys return the cached original response immediately without re-processing.
**Evaluation Criteria:** Candidate should define idempotency mathematically and practically, explain why network retries cause duplicate payments, and walk through the idempotency-key database lifecycle.

### Q8: What is Event Sourcing and CQRS (Command Query Responsibility Segregation)?
**Answer:** Traditional architectures store only the current mutable state of entities in a database, overwriting historical transitions. **Event Sourcing** replaces this by storing all state changes as an immutable, append-only log of domain events (e.g., `AccountCreated`, `MoneyDeposited`, `MoneyWithdrawn`). An entity's current state is reconstructed by replaying its historical stream of events from the beginning (or from a recent periodic snapshot). **CQRS (Command Query Responsibility Segregation)** separates the application's data architecture into two distinct models: the **Command Model** (handles business logic, validations, and writes events to the append-only event store) and the **Query Model** (reads from denormalized, optimized read-only projections updated asynchronously via event handlers). While CQRS and Event Sourcing provide perfect audit trails, temporal queries ("time travel"), and independent read/write scalability, they introduce eventual consistency and operational complexity in maintaining projection synchronization.
**Key Points:**
- Event Sourcing: State is persisted as an append-only sequence of immutable events rather than overwriting mutable records.
- Current state is computed by replaying events from genesis (accelerated via periodic snapshots).
- Provides 100% auditability, regulatory compliance, and time-travel debugging.
- CQRS: Separates write operations (Commands) from read operations (Queries) into specialized data stores.
- Projections asynchronously materialize read-optimized views (e.g., syncing relational writes to Elasticsearch queries).
**Evaluation Criteria:** Candidate should explain append-only event logs vs mutable state, describe how state is hydrated via event replay/snapshots, and explain how CQRS decouples write models from read projections.

### Q9: Explain Circuit Breaker and Retry with Exponential Backoff patterns in microservices fault tolerance.
**Answer:** In distributed systems, transient network glitches or downstream service slow-downs can trigger cascading failures across the entire ecosystem if callers retry aggressively without backoff, saturating struggling services. **Retry with Exponential Backoff and Jitter** addresses transient glitches by progressively doubling the wait time between successive retries (e.g., 100ms, 200ms, 400ms, 800ms) and adding a random variance (jitter: `sleep = rand(0, base * 2^attempt)`) to desynchronize retry waves and prevent the "thundering herd" problem. If a service suffers prolonged downtime, retries only exacerbate the outage; here, the **Circuit Breaker** pattern (popularized by Netflix Hystrix and Resilience4j) intervenes. The circuit breaker operates across three states: **Closed** (requests pass through normally; failures are counted), **Open** (when failures exceed a threshold percentage, the circuit trips immediately, rejecting all subsequent calls with an instant fallback or error without touching the downstream service), and **Half-Open** (after a timeout, a limited number of canary probe requests are permitted; if they succeed, the circuit resets to Closed; if they fail, it trips back to Open).
**Key Points:**
- Exponential Backoff: Progressively doubles wait duration between retries: t = base * 2^attempt.
- Jitter: Injects random noise into backoff intervals to prevent synchronized thundering herd retry spikes.
- Circuit Breaker States: Closed (normal operation), Open (fast-failing immediately), Half-Open (canary testing recovery).
- Prevents cascading microservice collapses by giving failing downstream dependencies time to heal.
**Evaluation Criteria:** Candidate should explain exponential backoff and why jitter is mathematically necessary, describe all three circuit breaker states, and explain how they prevent cascading service failures.

### Q10: What is Database Indexing (B+ Trees vs Hash Index vs LSM Trees) and how does indexing speed up reads while slowing down writes?
**Answer:** Database indexing is a data structure technique that allows the database engine to locate specific records without performing expensive full-table scans (O(N)). **B+ Trees** are self-balancing search trees used in standard relational databases (PostgreSQL, MySQL InnoDB); all data pointers reside in leaf nodes linked as a doubly linked list, enabling both O(log N) point lookups and fast O(log N + K) range scans. **Hash Indexes** provide O(1) point lookups using a memory hash table, but cannot support range queries or sorting (`>`, `<`, `BETWEEN`). **Log-Structured Merge-Trees (LSM Trees)** (used in Cassandra, RocksDB) optimize for high-throughput writes: writes are appended in-memory to a sorted MemTable and write-ahead log, and periodically flushed to disk as immutable SSTables, deferring cost to background compaction. While indexes accelerate read queries dramatically, they impose a direct penalty on write throughput (INSERT, UPDATE, DELETE) because every modifying transaction must synchronously update the data table *and* rebalance/update every associated index structure on disk.
**Key Points:**
- B+ Trees: Balanced multi-way search trees; leaf nodes form linked lists; industry standard for point and range queries in SQL.
- Hash Index: O(1) point lookups; completely incapable of range scans or ordering.
- LSM Trees: In-memory MemTable flushed to immutable disk SSTables; optimized for massive write-heavy distributed workloads.
- Read vs Write Trade-off: Speeds up queries from O(N) to O(log N); slows down writes due to index maintenance overhead.
**Evaluation Criteria:** Candidate should contrast the internal structures of B+ Trees, Hash Indexes, and LSM Trees, explain why B+ Trees excel at range queries, and articulate the write amplification penalty.

---

## Hard

### Q1: Design a globally distributed, highly available URL Shortener service (e.g., bit.ly) handling 10 billion URLs and 100k reads/second.
**Answer:** A global URL shortener service requires low-latency redirection (p99 < 15ms), high availability (99.999%), and robust unique key generation. For 10 billion URLs, a 7-character Base62 string (`[a-zA-Z0-9]`, 62^7 approx 3.5 trillion combinations) provides ample collision-free namespace capacity. To generate unique IDs without centralized database bottlenecks, we deploy a distributed ID generator (e.g., Twitter Snowflake or zookeeper-allocated token ranges) that assigns 64-bit integer IDs, which are encoded into Base62. The write path passes through an API Gateway to a Shortening Service that persists the mapping `(short_key, original_url, user_id, created_at)` in a horizontally partitioned NoSQL database (e.g., DynamoDB or Cassandra) partitioned on `short_key`. The read path handles 100k requests/sec: requests hit Anycast GeoDNS to route to the nearest Cloudflare/CloudFront CDN edge PoP, which caches popular 301/302 redirects. Cache misses hit an edge-located Redis cluster storing the top 20% most active URLs (Pareto 80/20 rule, ~20GB RAM required). Only Redis misses reach the primary database.
**Key Points:**
- Capacity estimation: 10 billion URLs * 500 bytes = 5 TB total storage; Base62 with length 7 yields 3.5 trillion URLs.
- ID Generation: Pre-allocated range-based counter servers or 64-bit Snowflake IDs converted to Base62.
- Read path caching: Multi-tiered caching (CDN Edge -> Redis Cluster -> NoSQL Key-Value Store).
- HTTP Redirection: 301 Permanent (browser caches redirect, saves server traffic but loses analytics) vs 302 Found (server tracks click analytics).
- Partitioning: Horizontally partitioned DynamoDB/Cassandra using `short_key` as primary hash partition key.
**Evaluation Criteria:** Candidate should calculate capacity and bandwidth estimates, explain Base62 encoding math, detail 301 vs 302 redirect trade-offs, and design a multi-tiered caching architecture for 100k reads/sec.

### Q2: Analyze Distributed Consensus Protocols: Explain Paxos and Raft consensus algorithms, leader election, and log replication mechanics.
**Answer:** Distributed consensus ensures that a cluster of independent machines agree on a shared state or sequence of log entries, even in the presence of network partitions and node crashes (handling f failures with 2f+1 nodes). While Multi-Paxos historically pioneered this, its monolithic specification made it notoriously difficult to implement. **Raft** was designed for operational understandability by decomposing consensus into three orthogonal subproblems: Leader Election, Log Replication, and Safety. Raft relies on randomized election timers (e.g., 150-300ms) to avoid split votes: when a follower node's timer expires without receiving a heartbeat, it increments its Term counter, transitions to Candidate, and broadcasts `RequestVote` RPCs. A candidate wins if it receives votes from a strict quorum (majority: (N/2) + 1). Once elected, the Leader accepts client commands, appends them to its log, and broadcasts `AppendEntries` RPCs to followers. A log entry is committed once replicated across a majority of nodes, after which the leader applies it to its local state machine and responds to the client. Raft enforces strict Safety invariants: a candidate cannot be elected unless its log is at least as up-to-date as any majority node, preventing uncommitted leader logs from overwriting committed history.
**Key Points:**
- Solves state machine replication across 2f+1 nodes tolerating up to f crash failures.
- Raft decomposes consensus into Leader Election, Log Replication, and Safety invariants.
- Randomized election timeouts prevent split-vote deadlocks during leader elections.
- Quorum-based commits: Leader commits an entry only after a strict majority confirms disk write.
- Leader Completeness: Raft guarantees the elected leader contains all committed entries from prior terms.
**Evaluation Criteria:** Candidate should explain quorum requirements (2f+1), contrast Paxos and Raft conceptual models, detail Raft's randomized election timer mechanism, and explain how Raft ensures log safety.

### Q3: Design a distributed real-time collaborative document editor (like Google Docs) using Operational Transformation (OT) vs CRDTs (Conflict-free Replicated Data Types).
**Answer:** A real-time collaborative editor allows multiple geographically dispersed users to concurrently insert and delete text in a shared document without locking or data divergence. Two primary mathematical frameworks govern this. **Operational Transformation (OT)** (used by Google Docs) relies on a centralized server that acts as the single source of truth for operation ordering. When client operations arrive out of order, the server and clients apply transformation functions: T(op1, op2) = (op1', op2') such that applying op1 followed by op2' achieves the identical document state as applying op2 followed by op1'. OT requires maintaining complex transformation matrices across all editing operation permutations. **Conflict-free Replicated Data Types (CRDTs)** (e.g., Yjs, Automerge, used in Figma) eliminate the need for a central coordinator by assigning every inserted character a globally unique, immutable identifier with fractional positioning (e.g., LSEQ or Logoot) and logical timestamps (Lamport timestamps). CRDTs are mathematically designed so that all character operations are commutative, associative, and idempotent: any peer node receiving operations in any arbitrary order converges deterministically to the identical document state. While CRDTs have higher memory overhead per character (storing metadata and tombstone markers for deleted characters), they excel in peer-to-peer, offline-first, and decentralized architectures.
**Key Points:**
- OT: Centralized coordination; operations transformed relative to concurrent operations: op1' = T(op1, op2).
- OT challenges: Combinatorial explosion of transformation functions and strict requirement for central ordering server.
- CRDTs: Decentralized mathematical structures; character operations are commutative and associative: A + B = B + A.
- CRDT mechanics: Fractional positioning IDs and logical Lamport clocks ensure deterministic convergence without central coordination.
- CRDT trade-off: Higher memory footprint due to metadata overhead and tombstoning deleted text.
**Evaluation Criteria:** Candidate should clearly articulate the mathematical divergence problem in concurrent edits, contrast OT's centralized transformation with CRDT's commutative properties, and discuss memory overhead vs offline resilience.

### Q4: Design a distributed Message Broker like Apache Kafka from scratch: Partitioning, log compaction, ISR (In-Sync Replicas), and zero-copy OS transfers.
**Answer:** Apache Kafka achieves multi-gigabyte-per-second throughput by designing its broker as an append-only, partitioned commit log. Topics are horizontally split into **Partitions**, which are the fundamental unit of parallelism; each partition is an immutable ordered sequence of records appended sequentially to disk, enabling sequential disk I/O that approaches bare-metal hardware speeds. Consumers belong to **Consumer Groups**, where each partition is consumed by exactly one consumer within the group. High availability is maintained via **In-Sync Replicas (ISR)**: a partition leader coordinates writes with followers; when a producer writes with `acks=all`, the leader acknowledges only after all nodes currently in the ISR pool have written the record to their local write-ahead log, dynamically evicting lagging followers. Kafka achieves near-zero read latency by leveraging the OS **Page Cache** rather than JVM heap memory, and executing the **Zero-Copy** Linux `sendfile()` system call: data is transferred directly from disk page cache to the network socket buffer via DMA (Direct Memory Access), completely bypassing CPU context switches between kernel and user space. Finally, **Log Compaction** retains only the latest key-value record for each unique key, enabling compact event-driven state hydration.
**Key Points:**
- Append-only partitioned commit logs convert random I/O into lightning-fast sequential disk writes.
- Partitioning is the unit of concurrency: Messages with the same key route to the same partition, preserving order.
- ISR (In-Sync Replicas): Dynamic pool of fully caught-up replicas; `acks=all` guarantees durability across ISR.
- Zero-Copy optimization: Linux `sendfile()` streams bytes directly from OS Page Cache to NIC buffer via DMA.
- JVM heap bypass: Stores cached messages in kernel page cache, eliminating garbage collection pauses.
**Evaluation Criteria:** Candidate must explain sequential disk write advantages, detail consumer group partition balancing, explain the ISR consensus model, and describe the Zero-Copy OS `sendfile()` data path.

### Q5: Analyze distributed unique ID generation at scale (Twitter Snowflake vs UUIDv4 vs Ticket Servers) ensuring monotonicity and high throughput.
**Answer:** Generating 64-bit unique, roughly time-ordered (monotonic) IDs across thousands of distributed servers is a critical infrastructure requirement for database indexing and event sequencing. **UUIDv4** generates 128-bit random strings without coordination; however, their 128-bit size doubles index storage overhead, and their total lack of temporal ordering causes catastrophic B+ Tree fragmentation, random disk I/O, and page splits in relational databases. **Centralized Ticket Servers** (Flickr approach) use dedicated MySQL instances with auto-incrementing IDs (`auto-increment-increment` and `auto-increment-offset`); while monotonic, they introduce a single point of failure, require network round-trips for every ID, and cannot scale past a few thousand requests/sec. **Twitter Snowflake** generates 64-bit sortable integers locally without network coordination using bit-packing: 1 sign bit (unused), 41 bits for epoch millisecond timestamp (providing ~69 years of IDs), 10 bits for Worker/Node ID (supporting 1024 independent server nodes), and 12 bits for a local sequence counter (permitting 4096 IDs per millisecond per node, totaling 4.096 million IDs/sec/node). Snowflake IDs are 64-bit (fitting in standard integer DB columns), k-sortable by creation time, and avoid network bottlenecks, requiring only synchronization to handle clock drift (NTP backwards stepping).
**Key Points:**
- UUIDv4: 128-bit random; causes severe B+ Tree index fragmentation and random I/O page splits.
- Ticket Servers: Centralized auto-increment databases; bottlenecked by network I/O and single-point-of-failure risk.
- Twitter Snowflake: 64-bit integer bit-packed layout (41-bit timestamp + 10-bit worker ID + 12-bit sequence counter).
- Throughput: Generates 4096 unique IDs per millisecond per node locally with zero network RPC overhead.
- Clock drift vulnerability: Requires system clock monitoring to reject or pause generation if NTP steps backward.
**Evaluation Criteria:** Candidate should compare the three approaches, break down the exact bit-allocation of Snowflake, explain why sequential ordering protects B+ Tree performance, and address NTP clock drift.

### Q6: Explain the PACELC theorem as an extension of CAP theorem, and analyze practical system trade-offs (e.g., DynamoDB vs Cassandra vs Spanner).
**Answer:** The CAP theorem is incomplete because it only describes system behavior during rare network partitions (P). The **PACELC Theorem** (formulated by Daniel Abadi) provides a comprehensive framework: **If there is a Partition (P)**, how does the system trade off **Availability (A)** and **Consistency (C)**; **Else (E)**, when the network is operating normally, how does the system trade off **Latency (L)** and **Consistency (C)**? This yields four distinct system archetypes. **PA/EL systems** (such as Amazon DynamoDB or Apache Cassandra in default configurations) choose Availability during partitions and Latency during normal operations: writes and reads are served locally using quorum tuning (e.g., R=1, W=1) for minimal latency, accepting eventual consistency. **PC/EC systems** (such as traditional relational RDBMS with synchronous replication, or Bigtable) prioritize Consistency during partitions (rejecting writes if primary is isolated) and Consistency during normal operations (paying high latency for cross-node replication and locks). **Google Cloud Spanner** operates as a **PC/EC** system that achieves both global consistency and external consistency (linearizability) using synchronized atomic clocks (TrueTime API) to bound clock uncertainty, sacrificing latency on writes to ensure global linearizable ACID transactions.
**Key Points:**
- Extends CAP to model steady-state system behavior: (P/A vs P/C) Else (E/L vs E/C).
- Solves the blind spot: CAP ignores latency costs when network connections are healthy.
- PA/EL (Cassandra, DynamoDB): High availability and low latency via eventual consistency and configurable quorums.
- PC/EC (Spanner, HBase, PostgreSQL): Enforces absolute consistency at all times, accepting latency overhead on normal writes.
- Highlights that distributed consistency guarantees impose latency penalties even in the complete absence of network failures.
**Evaluation Criteria:** Candidate must state the PACELC acronym components, explain why CAP's partition-only focus is insufficient, and categorize at least two real-world databases within the PACELC framework.

### Q7: Design a high-throughput, real-time distributed Rate Limiting engine capable of handling millions of requests per second using Redis cluster and Lua scripting.
**Answer:** Handling millions of requests per second requires a low-latency, linearly scalable rate limiter that eliminates network round-trips and race conditions. The architecture deploys lightweight rate-limiting middleware in the API Gateway layer (Envoy or Nginx) communicating with a sharded Redis Cluster over persistent connection pools. To track limits without multi-step network round-trips (GET count -> check -> INCR), the entire rate-limiting decision is executed atomically inside Redis via a pre-loaded **Lua script**. The Lua script implements a Sliding Window Counter: it computes the current minute key and previous minute key, executes `MGET`, applies the fractional weight formula `Count = Prev * (1 - fraction) + Curr`, and if under limit, executes `INCR` and sets `EXPIRE`. To handle millions of RPS without bottlenecking Redis CPU cores, we implement **Local Gateway Batching**: API gateways maintain a small local in-memory token buffer (e.g., 50 tokens), decrementing locally and syncing with Redis asynchronously in batches. If the Redis cluster encounters network degradation, the gateway fails open gracefully (allowing traffic) while alerting operators, ensuring that rate-limiter downtime never causes total API outage.
**Key Points:**
- Executes rate limit logic atomically inside Redis using Lua scripts to eliminate check-and-set race conditions.
- Sliding Window Counter formula executed server-side in a single atomic Redis round-trip.
- Sharding: Keys sharded across Redis cluster using hash tags: `{tenant_id:user_id}:rate_limit`.
- Local gateway token caching buffers micro-batches to reduce Redis command throughput by 10x-50x.
- Fail-open architecture: Defaults to allowing traffic if Redis cluster becomes unreachable to preserve availability.
**Evaluation Criteria:** Candidate should explain why Redis Lua scripts are required for atomicity, describe the sliding window counter implementation, detail local caching to scale to millions of RPS, and discuss fail-open resilience.

### Q8: Design a distributed ACID-compliant globally distributed database (e.g., Google Spanner) using TrueTime API, Paxos, and Two-Phase Locking (2PL).
**Answer:** Google Spanner is the first globally distributed database to provide external consistency (linearizability) and distributed ACID transactions at planetary scale. Spanner achieves this by integrating three core technologies: **Paxos state machines**, **Two-Phase Locking (2PL)**, and the proprietary **TrueTime API**. Data is partitioned into Paxos groups distributed globally for high availability. For intra-Paxos writes, standard Paxos consensus suffices. For cross-Paxos distributed transactions, Spanner combines 2PL (to acquire strict read/write locks on participating rows) with Two-Phase Commit (2PC) to coordinate multi-group atomicity. The foundational breakthrough that prevents 2PC distributed reads from blocking writes is TrueTime. TrueTime uses GPS receivers and atomic clocks across datacenters to expose physical time as a bounded interval `[earliest, latest]` with guaranteed uncertainty epsilon (typically <= 7ms). When a transaction commits at coordinate time t_commit, the coordinator waits out the uncertainty interval (commit wait: 2 * epsilon) before exposing the commit. This guarantees that if transaction T2 starts after T1 commits in the real world, T2's timestamp is mathematically greater than T1's (t2 > t1). As a result, read-only transactions execute with zero locks and zero 2PC overhead, serving historical snapshot reads across the entire globe with absolute linearizability.
**Key Points:**
- External Consistency (Linearizability): Real-world sequential ordering reflected globally across all distributed transactions.
- TrueTime API: Exposes time as bounded interval [t - eps, t + eps] using synchronized GPS and atomic rubidium clocks.
- Commit Wait Rule: Coordinator pauses for 2*epsilon before publishing commit, ensuring global timestamp ordering.
- Concurrency: Uses 2PL for read/write transactions and Paxos-coordinated 2PC across distributed partition groups.
- Lock-free Reads: Read-only transactions require zero locks and zero coordination, reading consistent snapshot MVCC data.
**Evaluation Criteria:** Candidate must explain external consistency, describe TrueTime's bounded uncertainty interval [t-eps, t+eps], explain the Commit Wait mechanism, and explain why TrueTime enables lock-free distributed reads.

### Q9: Design a scalable Video Streaming Platform (like Netflix or YouTube) handling massive upload, adaptive bitrate chunking (HLS/DASH), and global CDN delivery.
**Answer:** A global video streaming architecture consists of three distinct subsystems: Ingestion/Transcoding, Storage/Content Management, and Delivery. In the **Ingestion Pipeline**, client uploads chunked video files directly to an S3 object store via pre-signed URLs. An S3 `ObjectCreated` event publishes a message to a Kafka/SQS queue, triggering a distributed transcoding cluster. Transcoder worker nodes (using FFmpeg on GPU clusters) split the source video into discrete temporal segments (typically 2-6 seconds each) and transcode them into multiple resolutions (1080p, 720p, 480p) and codecs (H.264, AV1, VP9). It generates adaptive bitrate streaming manifest files—**HLS (m3u8)** or **DASH (mpd)**—which index available bitrates and segment URIs. In the **Delivery Pipeline**, when a user presses play, the video player downloads the manifest file and continually measures available network bandwidth, dynamically requesting segment files corresponding to the highest playable bitrate without buffering. Video segments are cached globally across tier-1 CDN edge servers. Because video segments are immutable, CDNs achieve >98% cache hit ratios, offloading nearly all streaming traffic from origin infrastructure.
**Key Points:**
- Ingestion: Direct-to-object-store multipart uploads using temporary pre-signed URLs.
- Transcoding: Distributed GPU workers slice video into 2-6 second chunks across multiple resolutions and bitrates.
- Adaptive Bitrate Streaming (ABR): HLS (.m3u8) / MPEG-DASH (.mpd) manifests allow client player to dynamically switch bitrates.
- Delivery: Highly optimized edge CDN caching for immutable video segment chunks (.ts / .m4s).
- Metadata & Recommendation: Cassandra/DynamoDB for user watch history, Elasticsearch for catalog search.
**Evaluation Criteria:** Candidate should break down the architecture into Ingestion, Transcoding, and Delivery, explain how Adaptive Bitrate Streaming works via manifests, and explain why immutable segment caching enables CDN scalability.

### Q10: Analyze the Split-Brain scenario in distributed systems and explain quorum-based fencing tokens, generation clocks, and epoch numbers.
**Answer:** Split-Brain occurs in distributed systems when a network partition divides a cluster into isolated subnetworks, leading nodes in separate partitions to simultaneously believe they are the legitimate leader. If two nodes act as active leaders and execute writes against shared storage or external services concurrently, it causes catastrophic data corruption, state divergence, and lost updates. The primary defense is **Quorum-based leadership**: a node can only assume or maintain leadership if it can communicate with a strict majority of nodes: Quorum = floor(N / 2) + 1. In a partition, only the subnetwork containing the majority can elect a leader, while the minority partition steps down. To guard against situations where an isolated former leader continues executing commands during a garbage-collection pause before detecting its deposition, distributed systems implement **Fencing Tokens (Epoch Numbers / Generation Clocks)**. Every time a new leader is elected, the consensus term counter or generation clock increments monotonically (e.g., Epoch 4 -> Epoch 5). Every command dispatched by the leader carries this fencing token. The underlying shared storage layer or downstream service inspects the token: if a write arrives with an outdated epoch (e.g., token 4 arriving after token 5), the write is rejected immediately.
**Key Points:**
- Split-Brain: Network partition causes multiple nodes to simultaneously claim leadership and execute conflicting writes.
- Quorum requirement: Requires strict majority (N/2 + 1) to elect or maintain leader, ensuring at most one active partition.
- Fencing Tokens / Generation Clocks: Monotonically increasing counter assigned during each leader transition.
- Storage validation: Downstream storage rejects any write containing an epoch number lower than the latest seen token.
- Neutralizes zombie leader hazards caused by long GC pauses or asynchronous network delays.
**Evaluation Criteria:** Candidate should define split-brain and identify the conditions leading to dual leaders, explain majority quorum logic, and detail how monotonically increasing fencing tokens prevent zombie leader write corruption.

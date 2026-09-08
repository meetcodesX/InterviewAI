# SQL Interview Questions

## Easy

### Q1: What is the basic purpose of the SELECT statement, and how do WHERE, ORDER BY, and LIMIT work together?
**Answer:** The `SELECT` statement retrieves data from one or more database tables by specifying the columns of interest or using `*` to fetch all attributes. The `WHERE` clause filters rows before any aggregation, returning only records that satisfy specified boolean conditions. The `ORDER BY` clause sorts the resulting dataset by one or more columns in either ascending (`ASC`, default) or descending (`DESC`) order. Finally, `LIMIT` (or `TOP` / `FETCH FIRST` depending on the dialect) restricts the maximum number of rows returned to the client. Together, these clauses allow efficient, selective, and ordered querying of relational datasets.
**Key Points:**
- `SELECT`: Specifies columns or expressions to project from the data source.
- `WHERE`: Row-level filtering applied before grouping or aggregation.
- `ORDER BY`: Sorts the result set by specified columns or expressions (`ASC`/`DESC`).
- `LIMIT` / `OFFSET`: Restricts row count and enables pagination.
**Evaluation Criteria:** Candidate should state the correct logical order of execution and explain the distinct role of each clause in filtering, sorting, and restricting rows.

### Q2: What is the fundamental difference between an INNER JOIN and a LEFT (OUTER) JOIN?
**Answer:** An `INNER JOIN` returns only the rows that have matching values in both joined tables based on the specified `ON` condition; non-matching rows from either table are excluded. A `LEFT JOIN` (or `LEFT OUTER JOIN`) returns all records from the left table, regardless of whether a match exists in the right table. For rows in the left table that have no matching record in the right table, columns from the right table are populated with `NULL`. Choosing between them depends on whether unmatched records from the primary table must be preserved in the analysis.
**Key Points:**
- `INNER JOIN`: Returns strict intersection where join predicates evaluate to true in both tables.
- `LEFT JOIN`: Preserves all rows from left table; injects `NULL` for missing right-table matches.
- Cartesian product prevention via appropriate join conditions.
- Performance implications: `INNER JOIN` can be filtered more aggressively by the query planner.
**Evaluation Criteria:** Look for a clear explanation of matching behavior, handling of non-matching records, and the presence of `NULL` values in outer joins.

### Q3: How do aggregate functions operate in SQL, and why must non-aggregated columns appear in the GROUP BY clause?
**Answer:** Aggregate functions—such as `COUNT()`, `SUM()`, `AVG()`, `MIN()`, and `MAX()`—perform calculations across sets of rows to return a single summarized scalar value per group. When using `GROUP BY`, the database collapses rows sharing identical values in the grouped columns into summary rows. Any column included in the `SELECT` list that is not wrapped in an aggregate function must be explicitly specified in the `GROUP BY` clause. This requirement ensures deterministic results, because without it, the database engine would not know which individual row's value to display for that non-aggregated column within the collapsed group.
**Key Points:**
- Common aggregates: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- `GROUP BY` collapses identical row values into distinct summary groups.
- Determinism rule: Non-aggregated columns in `SELECT` must be listed in `GROUP BY`.
- Null handling: Most aggregates ignore `NULL` values, except `COUNT(*)`.
**Evaluation Criteria:** Candidate must explain what aggregation does and clearly articulate *why* non-aggregated columns must appear in `GROUP BY` (determinism of projection).

### Q4: What is the difference between the WHERE clause and the HAVING clause?
**Answer:** The `WHERE` clause filters individual rows before any grouping or aggregation takes place, meaning it cannot evaluate aggregate functions like `SUM()` or `COUNT()`. In contrast, the `HAVING` clause filters summarized groups after the `GROUP BY` operation has been performed. For example, you use `WHERE status = 'ACTIVE'` to filter records before aggregation, but use `HAVING COUNT(*) > 5` to filter groups that meet aggregate criteria. While some queries can place non-aggregate conditions in either clause, filtering rows as early as possible with `WHERE` is significantly more performant because it reduces the volume of data processed during grouping.
**Key Points:**
- `WHERE`: Row-level filter applied before grouping and aggregation.
- `HAVING`: Group-level filter applied after grouping and aggregation.
- `WHERE` cannot evaluate aggregate functions; `HAVING` can and does.
- Performance best practice: Filter early with `WHERE` before aggregating.
**Evaluation Criteria:** Candidate should identify the order of operations (WHERE before GROUP BY, HAVING after GROUP BY) and explain why aggregate functions are forbidden in WHERE clauses.

### Q5: What are Primary Keys and Foreign Keys, and what role do they play in relational databases?
**Answer:** A Primary Key is a column or combination of columns that uniquely identifies each row in a database table, enforcing entity integrity by requiring that values are unique and non-null (`UNIQUE NOT NULL`). A Foreign Key is a column or set of columns in one table that references the Primary Key of another table, establishing a relationship between them. Foreign Keys enforce referential integrity, ensuring that child records cannot reference non-existent parent records and defining cascade behaviors (`CASCADE DELETE`, `SET NULL`) when parent records change. Together, they form the structural foundation that guarantees relational consistency and prevents orphan records.
**Key Points:**
- Primary Key: Unique, non-null identifier for rows in a table (entity integrity).
- Foreign Key: Column that references a Primary Key in another table (referential integrity).
- Referential actions: `ON DELETE CASCADE`, `ON DELETE RESTRICT`, `ON DELETE SET NULL`.
- Prevents orphaned records and enforces structural integrity across tables.
**Evaluation Criteria:** Candidate should explain entity integrity vs. referential integrity and describe what happens during updates or deletions via cascade rules.

### Q6: What is the difference between the UNION and UNION ALL operators?
**Answer:** Both `UNION` and `UNION ALL` combine the result sets of two or more `SELECT` queries into a single output, requiring identical column counts, compatible data types, and matching ordering. The fundamental difference is that `UNION` removes all duplicate rows from the final result set, whereas `UNION ALL` retains all rows, including duplicates. Because `UNION` must eliminate duplicates, it performs an expensive internal sorting or hashing operation on the combined dataset. Therefore, `UNION ALL` is significantly faster and should always be preferred unless duplicate elimination is explicitly required by the business logic.
**Key Points:**
- Both combine row sets from queries with matching column schemas.
- `UNION`: Deduplicates rows; incurs sorting/hashing computational overhead.
- `UNION ALL`: Preserves all rows including duplicates; executes without deduplication overhead.
- Performance guideline: Always use `UNION ALL` when data is known to be distinct or duplicates are acceptable.
**Evaluation Criteria:** Look for understanding of duplicate removal and the associated performance cost (in-memory sorting or hashing) of `UNION` compared to `UNION ALL`.

### Q7: How do NULL values behave in SQL comparisons and aggregate functions?
**Answer:** In SQL, `NULL` represents the absence of a value or unknown data rather than zero or an empty string, operating under three-valued logic (`TRUE`, `FALSE`, `UNKNOWN`). Standard equality comparisons such as `= NULL` or `!= NULL` always evaluate to `UNKNOWN` (which evaluates as false in a `WHERE` clause); developers must use `IS NULL` or `IS NOT NULL` instead. In aggregate functions like `SUM()`, `AVG()`, and `COUNT(column)`, `NULL` values are ignored, which can skew averages if not handled with `COALESCE()`. The only exception is `COUNT(*)`, which counts all rows regardless of nullability.
**Key Points:**
- Three-valued logic: `TRUE`, `FALSE`, and `UNKNOWN`.
- Comparisons with `NULL` using `=`, `<>`, or `!=` yield `UNKNOWN`; must use `IS NULL`.
- Aggregates (`SUM`, `AVG`, `MIN`, `MAX`, `COUNT(col)`) ignore nulls.
- `COUNT(*)` counts rows, including those with null fields; `COALESCE()` provides default values.
**Evaluation Criteria:** Candidate must explain three-valued logic, correct usage of `IS NULL`, and the difference between `COUNT(*)` and `COUNT(column)`.

### Q8: What does the DISTINCT keyword do, and what are its performance implications?
**Answer:** The `DISTINCT` keyword eliminates duplicate rows from the query output, ensuring that every row in the result set contains a unique combination of selected column values. When `DISTINCT` is evaluated, the database engine must compare every returned row, which typically requires sorting the entire intermediate result set in memory or building an in-memory hash table. On large datasets, this causes significant CPU and memory overhead and may spill to temporary disk storage if memory limits are exceeded. Frequently, developers use `DISTINCT` as a quick fix to hide duplicate rows caused by improper join conditions, which masks underlying query defects instead of fixing them.
**Key Points:**
- Filters out duplicate rows across the selected column tuple.
- Requires internal sorting or hash aggregation, adding substantial query latency.
- Can spill to disk if memory buffers (`work_mem`) are exceeded on large row counts.
- Anti-pattern: Masking accidental Cartesian joins with `DISTINCT` instead of correcting join keys.
**Evaluation Criteria:** Candidate should identify the algorithmic overhead (sorting/hashing) and highlight the common bad practice of using `DISTINCT` to mask flawed joins.

### Q9: What is the difference between the CHAR and VARCHAR data types?
**Answer:** `CHAR` is a fixed-length character data type, whereas `VARCHAR` is a variable-length character data type. If a column is defined as `CHAR(10)` and you store the string `'SQL'`, the database pads the remaining seven characters with trailing spaces to consume the full 10 bytes. With `VARCHAR(10)`, storing `'SQL'` stores only the three characters plus a 1- or 2-byte length prefix, saving storage space for variable inputs. `CHAR` is best suited for predictable, fixed-length strings such as country codes (`US`, `CA`), currency codes, or MD5/UUID hashes, where storage overhead is minimal and processing avoids length calculation.
**Key Points:**
- `CHAR`: Fixed length, space-padded to declared size, zero variable length prefix overhead.
- `VARCHAR`: Variable length, stores actual characters plus a 1–2 byte length prefix.
- `CHAR` is ideal for uniform strings (state codes, hashes, status codes).
- `VARCHAR` is ideal for unpredictable string lengths (names, emails, descriptions).
**Evaluation Criteria:** Look for an understanding of space padding, length prefix storage overhead, and criteria for choosing between fixed and variable string types.

### Q10: What is a database View, and what are the primary benefits of using views in production databases?
**Answer:** A database View is a virtual table defined by a stored SQL query; it does not store physical data itself (unless created as a Materialized View), but dynamically generates data whenever queried. Views provide abstraction by encapsulating complex joins, aggregations, and business logic behind a simple interface, making queries easier to read and maintain for client applications. They also enhance security by implementing row- and column-level access controls, exposing only non-sensitive data to specific user roles while restricting access to underlying base tables. Furthermore, views create a stable API layer that insulates client applications from changes to the underlying database schema.
**Key Points:**
- Virtual table representing the stored output of an underlying SQL query.
- Security: Implements column/row-level permissions without exposing base tables.
- Modularity & Abstraction: Encapsulates complex joins and calculations into clean reusable interfaces.
- Schema insulation: Allows physical schema changes without breaking upstream client queries.
**Evaluation Criteria:** Candidate should explain virtual tables vs. materialized storage, security access control benefits, and schema abstraction advantages.

---

## Medium

### Q1: Explain database normalization from First Normal Form (1NF) through Third Normal Form (3NF).
**Answer:** Database normalization organizes tables to reduce data redundancy and eliminate update, insertion, and deletion anomalies. **First Normal Form (1NF)** requires that all column values are atomic (no repeating groups or comma-separated lists) and that each row is uniquely identifiable via a primary key. **Second Normal Form (2NF)** requires satisfying 1NF and ensuring that all non-key attributes are fully functionally dependent on the entire primary key, eliminating partial dependencies on composite keys. **Third Normal Form (3NF)** requires satisfying 2NF and eliminating transitive dependencies, meaning non-key columns must depend directly on the primary key and not on other non-key attributes ("the key, the whole key, and nothing but the key").
**Key Points:**
- 1NF: Atomic values, no repeating groups, unique primary key identified.
- 2NF: Meets 1NF; eliminates partial functional dependencies on composite keys.
- 3NF: Meets 2NF; eliminates transitive dependencies between non-key columns.
- Prevents update, delete, and insert anomalies while preserving data integrity.
**Evaluation Criteria:** Candidate should define all three normal forms sequentially, explain functional dependencies, and describe the specific anomalies normalization solves.

### Q2: How do SQL Window Functions work, and what is the difference between ROW_NUMBER(), RANK(), and DENSE_RANK()?
**Answer:** Window functions perform calculations across a specified set of table rows (a "window") related to the current row, without collapsing the individual rows into a single summary output like standard `GROUP BY` aggregates. The window is defined using the `OVER (PARTITION BY ... ORDER BY ...)` clause. When ranking ties (identical values in the sort order), `ROW_NUMBER()` assigns sequential unique integers arbitrarily without ties (e.g., 1, 2, 3, 4). `RANK()` assigns identical ranks to ties and skips subsequent rank numbers by the number of ties (e.g., 1, 2, 2, 4). `DENSE_RANK()` assigns identical ranks to ties but increments sequentially without gaps (e.g., 1, 2, 2, 3).
**Key Points:**
- Operates across row partitions while preserving individual row identity.
- Defined using `OVER (PARTITION BY ... ORDER BY ...)`.
- `ROW_NUMBER()`: Unique sequential integers, breaks ties arbitrarily (1, 2, 3, 4).
- `RANK()`: Ties get identical rank; skips subsequent positions (1, 2, 2, 4).
- `DENSE_RANK()`: Ties get identical rank; no gaps in subsequent sequence (1, 2, 2, 3).
**Evaluation Criteria:** Candidate must explain how window functions differ from `GROUP BY` and clearly demonstrate tie-breaking behavior across the three ranking functions.

### Q3: What is a Common Table Expression (CTE), and how do Recursive CTEs work?
**Answer:** A Common Table Expression (CTE) is a temporary, named result set defined within the scope of a single `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement using the `WITH` clause. CTEs enhance readability, modularity, and maintainability compared to deeply nested subqueries, and can be referenced multiple times within the same query. A Recursive CTE references itself to iteratively traverse hierarchical or graph data, such as organizational charts, bill-of-materials, or category trees. A recursive CTE consists of an Anchor Member (base case query), a `UNION ALL` operator, and a Recursive Member that joins back to the CTE itself until an empty result set terminates the recursion.
**Key Points:**
- Defined using the `WITH cte_name AS (...)` syntax for modular query organization.
- Improves readability and maintainability compared to nested derived tables.
- Recursive CTEs traverse hierarchical structures (trees, parent-child graphs).
- Recursive structure: Anchor query + `UNION ALL` + Recursive query with termination condition.
**Evaluation Criteria:** Look for an understanding of readability/reusability advantages and the anatomy of recursive CTEs (anchor query, recursive step, termination condition).

### Q4: What is the difference between Correlated and Non-Correlated Subqueries, and what are the performance implications?
**Answer:** A non-correlated subquery is an independent query that can run on its own without referencing columns from the outer query; it executes once, and its result is reused by the outer query during execution. A correlated subquery references columns from the outer query table, meaning it cannot execute independently and conceptually must be evaluated once for every candidate row processed by the outer query. Consequently, correlated subqueries can suffer from $O(N \times M)$ nested-loop performance degradation on large datasets. Modern query optimizers often attempt to unnest or transform correlated subqueries into equivalent joins, but developers should proactively rewrite them as explicit `JOIN`s or CTEs with window functions to ensure optimal performance.
**Key Points:**
- Non-Correlated: Independent query; executes once; output used globally by outer query.
- Correlated: References outer query columns; conceptually re-evaluates per row.
- Performance: Correlated subqueries risk $O(N \times M)$ performance bottlenecks without query unnesting.
- Best practice: Refactor correlated subqueries into `JOIN`s or window functions where possible.
**Evaluation Criteria:** Candidate should contrast execution mechanics (independent execution once vs. per-row evaluation) and discuss query optimizer unnesting.

### Q5: How do B-Tree indexes work, and why do they speed up reads while slowing down writes?
**Answer:** A B-Tree (Balanced Tree) index is a self-balancing tree data structure that maintains sorted keys, allowing logarithmic time complexity ($O(\log N)$) for lookups, range searches, insertions, and deletions. When a query filters with `WHERE id = 500` or `WHERE id BETWEEN 100 AND 200`, the database traverses the tree from root to leaf nodes rather than scanning millions of rows sequentially. While B-Tree indexes drastically reduce disk I/O for read queries, every `INSERT`, `UPDATE`, and `DELETE` operation must update both the base table and all associated index trees. Furthermore, write operations can trigger expensive node splits and rebalancing, which introduces significant write latency when tables have many indexes.
**Key Points:**
- Self-balancing search tree keeping keys in sorted order.
- Provides $O(\log N)$ search, range scans, and sorted traversals.
- Drastically reduces I/O by replacing full table scans with index seeks.
- Write trade-off: `INSERT`/`UPDATE`/`DELETE` must update every index on the table, causing node splits and write overhead.
**Evaluation Criteria:** Candidate should explain $O(\log N)$ tree traversal, leaf-node range scanning, and the write penalty caused by tree rebalancing and node splits.

### Q6: What are the ACID properties in database transactions, and what guarantee does each property provide?
**Answer:** ACID properties guarantee reliable transaction processing in database management systems. **Atomicity** ensures that all operations within a transaction succeed together or fail together; if any statement fails, the entire transaction rolls back completely ("all or nothing"). **Consistency** guarantees that a transaction moves the database from one valid state to another, strictly enforcing all constraints, cascades, and schema rules. **Isolation** ensures that concurrent transactions execute independently without interfering with each other's intermediate uncommitted states. **Durability** guarantees that once a transaction commits, its changes are permanently recorded in non-volatile storage (via write-ahead logging) and will survive subsequent power outages or system crashes.
**Key Points:**
- Atomicity: All-or-nothing execution with automatic rollback on failure.
- Consistency: Preserves all defined schema constraints, foreign keys, and invariants.
- Isolation: Controls concurrency visibility across simultaneous transactions.
- Durability: Committed updates persist permanently via Write-Ahead Logging (WAL).
**Evaluation Criteria:** Candidate should clearly define each acronym component with technical precision and mention the underlying mechanisms (e.g., rollback logs, WAL).

### Q7: What are Stored Procedures, and what are their trade-offs compared to handling business logic in application code with ORMs?
**Answer:** Stored Procedures are pre-compiled collections of SQL statements and procedural logic stored directly in the database engine and executed via calls. Their advantages include reduced network traffic (executing complex multi-step routines directly on the database server), centralized data access control, and pre-compiled execution plans. However, their trade-offs are substantial: business logic becomes tightly coupled to a proprietary database dialect (hurting portability), version control and CI/CD testing are far more difficult than in application code, and debugging tools are primitive. Additionally, scaling database CPU to execute procedural logic is significantly more expensive and complex than scaling stateless application servers running ORM queries.
**Key Points:**
- Stored, pre-compiled SQL routines running directly inside the database engine.
- Advantages: Zero network back-and-forth for multi-step tasks, fine-grained DB security.
- Disadvantages: Vendor lock-in, poor version control integration, difficult unit testing.
- Scalability cost: Application servers scale horizontally cheaply; database compute is expensive and stateful.
**Evaluation Criteria:** Look for a balanced evaluation of network optimization vs. software engineering maintainability, version control challenges, and compute scalability costs.

### Q8: What is the difference between Clustered and Non-Clustered indexes?
**Answer:** A clustered index determines the actual physical ordering of data rows on disk, meaning a table can have only one clustered index (typically assigned automatically to the Primary Key). The leaf nodes of a clustered index contain the actual data pages of the table. In contrast, a non-clustered index is a separate structure from the data rows; its leaf nodes contain the indexed key values paired with a row locator or pointer (such as the clustered index key or tuple ID) that points to the actual data location. Lookups using a non-clustered index may require a secondary "bookmark lookup" or "table scan" to fetch columns not contained within the index itself, unless satisfied entirely by a covering index.
**Key Points:**
- Clustered index: Dictates physical storage order on disk; exactly one per table; leaf nodes are the data pages.
- Non-Clustered index: Separate B-Tree structure; multiple allowed per table; leaf nodes contain pointers.
- Lookup overhead: Non-clustered queries may require bookmark/key lookups to retrieve non-indexed columns.
- Primary key default: Most RDBMS default the primary key to the clustered index.
**Evaluation Criteria:** Candidate must explain physical storage arrangement, the one-clustered-index-per-table constraint, and the concept of row pointers in non-clustered indexes.

### Q9: What are SQL Transaction Isolation Levels, and what concurrency anomalies does each level prevent?
**Answer:** SQL standard defines four transaction isolation levels that trade off concurrency against isolation: **Read Uncommitted** allows transactions to see uncommitted changes from others, exposing systems to Dirty Reads. **Read Committed** guarantees transactions only read committed data, preventing Dirty Reads but allowing Non-Repeatable Reads (reading the same row twice yields different values). **Repeatable Read** ensures that any row read during a transaction remains identical on subsequent reads, preventing Non-Repeatable Reads, but may allow Phantom Reads (new rows inserted by concurrent transactions matching a range query). **Serializable** is the strictest level, executing transactions as if they occurred in a strictly serial sequence, preventing all anomalies at the cost of substantial locking and concurrency contention.
**Key Points:**
- Dirty Read: Reading uncommitted, potentially rolled-back data.
- Non-Repeatable Read: Re-reading the same row returns modified committed values.
- Phantom Read: Re-executing a range query returns newly inserted committed rows.
- Isolation Levels: Read Uncommitted $\to$ Read Committed $\to$ Repeatable Read $\to$ Serializable.
**Evaluation Criteria:** Candidate must list the four isolation levels in order and explicitly map which anomalies (Dirty, Non-Repeatable, Phantom reads) each level prevents.

### Q10: How do you use EXPLAIN and EXPLAIN ANALYZE to identify performance bottlenecks in slow SQL queries?
**Answer:** `EXPLAIN` shows the execution plan generated by the database query planner—including cost estimates, projected row counts, join strategies, and index usage—without actually running the query. `EXPLAIN ANALYZE` (or dialect equivalents) actually executes the query, outputting both the planner's estimates and the true runtime statistics, such as actual elapsed time, actual row counts, and buffer cache hits versus disk reads. Bottlenecks are identified by looking for full table scans (`Seq Scan`) on large tables, severe discrepancies between estimated rows and actual rows (indicating stale statistics), high startup or total execution costs, and disk-spilling hash operations. These insights direct developers to add missing indexes, rewrite joins, or execute `ANALYZE` to refresh statistics.
**Key Points:**
- `EXPLAIN`: Shows hypothetical execution plan, operations, and cost estimates without execution.
- `EXPLAIN ANALYZE`: Executes the query; displays real execution timings, memory, and actual row counts.
- Red flags: Sequential/Full Table scans on large tables, disk spills (`Sort Method: external merge Disk`).
- Cardinality mismatch: Large variance between estimated and actual rows signals out-of-date table statistics.
**Evaluation Criteria:** Candidate should clearly distinguish between cost estimation (`EXPLAIN`) and actual execution measurement (`EXPLAIN ANALYZE`), highlighting specific execution plan red flags.

---

## Hard

### Q1: How do database query planners choose between Nested Loop, Hash Join, and Merge Join algorithms?
**Answer:** The query planner evaluates cost models to select the most efficient physical join operator based on table sizes, indexes, available memory, and sort orders. A **Nested Loop Join** iterates through an outer table and scans the inner table for each row; it is optimal when the outer table is small and the inner table has a highly selective index on the join key. A **Hash Join** builds an in-memory hash table from the smaller relation and probes it with rows from the larger relation; it excels for large, unsorted, unindexed datasets where equality joins are used, provided the hash table fits within `work_mem`. A **Merge Join** requires both inputs to be sorted on the join key, simultaneously advancing pointers across both inputs; it is exceptionally fast when indexes already supply sorted order or for very large datasets where sorting can be streamed.
**Key Points:**
- Nested Loop: Best for small driving tables joined against indexed inner tables ($O(N \log M)$).
- Hash Join: Best for large, unsorted, unindexed equality joins; requires adequate in-memory work buffers.
- Merge Join: Best when inputs are already sorted (e.g., via B-Tree index); efficient for large range or equality joins.
- Planner choice is driven by cost estimation, available memory (`work_mem`), and presence of B-Tree indexes.
**Evaluation Criteria:** Candidate must compare algorithmic mechanics of all three joins, identify memory and index prerequisites, and explain when the planner picks each strategy.

### Q2: What causes database deadlocks in high-concurrency applications, and how do you systematically prevent and resolve them?
**Answer:** A deadlock occurs when two or more concurrent transactions hold locks on resources that the other transactions need to proceed, creating a cyclic dependency graph (e.g., Transaction A holds Lock 1 and waits for Lock 2, while Transaction B holds Lock 2 and waits for Lock 1). The database engine detects deadlocks by periodically traversing a "wait-for graph" for cycles; when detected, it forcibly terminates and rolls back the "cheapest" transaction (the deadlock victim). Prevention strategies include acquiring locks in a strictly uniform global order across all application code paths, keeping transactions as short as possible, avoiding user interaction during open transactions, and utilizing lower isolation levels or optimistic concurrency where appropriate. Applications must also implement exponential backoff retry logic to automatically handle deadlock victim exceptions.
**Key Points:**
- Cause: Cyclic dependencies in lock acquisition order across concurrent transactions.
- Detection: Database engine builds and checks a "wait-for graph" and aborts a victim transaction.
- Prevention: Enforce uniform global lock ordering (e.g., update Table A before Table B in all queries).
- Application resilience: Keep transactions short, lock minimal rows, and implement automated retry loops with jitter.
**Evaluation Criteria:** Candidate should explain cyclic dependencies, the database's wait-for graph cycle detection, prevention via consistent acquisition ordering, and application retry mechanisms.

### Q3: Explain the Leftmost Prefix Rule for composite indexes and how to leverage Covering Indexes (Index-Only Scans) for zero-table-access querying.
**Answer:** A composite index on columns `(A, B, C)` is structured in a single B-Tree sorted primarily by `A`, then by `B` within equal `A`, and by `C` within equal `B`. According to the Leftmost Prefix Rule, the index can accelerate queries filtering on `(A)`, `(A, B)`, or `(A, B, C)`, but cannot be used as an index seek for queries filtering on `(B)` or `(C)` alone because the tree is not ordered by those columns independently. A Covering Index includes all columns referenced in the query—including those in `SELECT`, `WHERE`, `JOIN`, and `ORDER BY`—either as key columns or via the `INCLUDE` clause. When a query is covered, the database satisfies the request entirely within the index leaf pages via an Index-Only Scan, eliminating expensive random I/O heap table fetches.
**Key Points:**
- Composite B-Trees are sorted lexicographically by columns in declared order.
- Leftmost Prefix Rule: Queries must filter on leading prefix columns to utilize index seeks.
- Covering Index: Index contains every column requested by the query.
- Index-Only Scan: Database answers the entire query from the index tree without fetching heap table pages.
**Evaluation Criteria:** Look for an explanation of composite lexicographical sorting, why non-prefix filters cannot perform seeks, and how Index-Only Scans bypass table heap lookups.

### Q4: How does Multi-Version Concurrency Control (MVCC) work in PostgreSQL or MySQL InnoDB to achieve non-blocking reads?
**Answer:** MVCC allows concurrent read and write operations to proceed without blocking each other by ensuring that "readers never block writers, and writers never block readers." When a row is updated or deleted, the database does not overwrite the existing physical data in place; instead, it writes a new version of the row tuple with metadata tracking transaction identifiers (such as `xmin` and `xmax` in Postgres, or Rollback Segments with Undo Logs in MySQL InnoDB). When a transaction executes a query, it operates against a point-in-time snapshot of the database, reading only row versions committed prior to its snapshot timestamp. A background vacuum process (in Postgres) or purge thread (in MySQL) periodically cleans up obsolete row versions that are no longer visible to any active transaction snapshot, preventing table bloat.
**Key Points:**
- Core principle: Readers do not lock out writers, and writers do not lock out readers.
- Implementation: Appending tuple versions with transaction IDs (`xmin`/`xmax`) or Undo Logs.
- Transaction Snapshots: Transactions view consistent point-in-time snapshots based on commit history.
- Dead tuple cleanup: Postgres Vacuuming and MySQL Undo Purging reclaim storage from obsolete versions.
**Evaluation Criteria:** Candidate must explain tuple versioning, snapshot isolation mechanics, and the requirement for garbage collection (Vacuuming / Undo purge) to prevent storage bloat.

### Q5: How do you architect horizontal database scaling through Sharding, Read Replicas, and Write Scaling strategies?
**Answer:** Horizontal database scaling overcomes single-server hardware limits by distributing data and query loads across multiple nodes. Read Replicas handle read-heavy workloads by replicating data asynchronously from a primary write node using binary logs (WAL streaming), though applications must tolerate replication lag and eventual consistency. For write-heavy workloads, Sharding partitions the entire database horizontally across multiple independent database instances based on a Shard Key (e.g., Hash-based, Range-based, or Directory-based). Sharding introduces major distributed systems challenges: cross-shard joins become slow and complex, distributed two-phase commit transactions are required for multi-shard consistency, and resharding data requires complex rebalancing. Consequently, techniques like caching, query optimization, and vertical scaling should always be exhausted before sharding.
**Key Points:**
- Read Replicas: Asynchronous WAL replication offloads read traffic; subject to replication lag.
- Sharding: Horizontal partitioning of rows across disparate server clusters using a Shard Key.
- Sharding strategies: Hash-based (uniform distribution) vs. Range-based (range scan efficient).
- Operational trade-offs: Cross-shard joins are disabled/expensive; distributed transaction complexity ($2PC$).
**Evaluation Criteria:** Candidate should contrast read-scaling (replicas) with write-scaling (sharding) and address distributed system trade-offs like replication lag and cross-shard queries.

### Q6: What are Partial (Filtered) Indexes and Functional (Expression) Indexes, and in what scenarios do they provide massive performance advantages?
**Answer:** A Partial (or Filtered) Index indexes only a subset of rows in a table that satisfy a specific `WHERE` predicate (e.g., `CREATE INDEX idx_unpaid ON orders(created_at) WHERE status = 'UNPAID'`). This drastically reduces index size, memory footprint, and write maintenance overhead on skewed data where 99% of orders are completed and queries only search for the 1% pending orders. A Functional (or Expression) Index indexes the computed result of an expression or function applied to a column (e.g., `CREATE INDEX idx_lower_email ON users(LOWER(email))`). Standard B-Trees cannot be used when functions wrap column names in queries, but functional indexes allow direct index seeks on calculated values, transforming slow full table scans into immediate index lookups.
**Key Points:**
- Partial Index: Built on a row subset defined by a `WHERE` condition; saves disk/RAM and write overhead.
- Partial Index use case: Skewed status columns (e.g., indexing only active/unprocessed records).
- Functional Index: Indexes results of expressions/functions (`LOWER(col)`, `jsonb->>'field'`).
- Functional Index use case: Enables index seeks when queries apply transformations to columns.
**Evaluation Criteria:** Candidate should identify the mechanics and storage efficiency of both index types, providing practical real-world scenarios where standard indexes fail.

### Q7: Explain the difference between `ROWS BETWEEN` and `RANGE BETWEEN` window frame specifications with concrete examples.
**Answer:** The window frame clause specifies the exact subset of rows within a partition over which an aggregate window function computes its result. `ROWS BETWEEN` defines the frame by counting physical row offsets relative to the current row (e.g., `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` includes exactly three physical rows regardless of duplicate values). In contrast, `RANGE BETWEEN` defines the frame logically based on the values in the `ORDER BY` column (e.g., `RANGE BETWEEN INTERVAL '7 DAYS' PRECEDING AND CURRENT ROW`). Crucially, if you use `RANGE` with duplicate values in the sort column, all duplicate rows are treated as a single peer group and aggregated together, whereas `ROWS` evaluates each row sequentially without grouping peers.
**Key Points:**
- `ROWS`: Physical row offset boundaries (e.g., 3 physical rows before the current row).
- `RANGE`: Logical value offset boundaries based on sorting values (e.g., numeric differences or time intervals).
- Peer handling: `RANGE` bundles tied/duplicate values into the same window calculation.
- Default frame: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` can cause unexpected performance and calculation surprises on duplicates.
**Evaluation Criteria:** Candidate must clearly distinguish physical row counting (`ROWS`) from logical value calculation (`RANGE`) and describe how tied sort values impact calculations.

### Q8: Contrast Table Partitioning strategies (Range, List, Hash) and explain the concept and benefits of Partition Pruning.
**Answer:** Table Partitioning splits a large logical table into smaller physical tables while maintaining a unified interface for queries. **Range Partitioning** assigns rows based on contiguous value ranges (ideal for time-series data partitioned by month or year); **List Partitioning** assigns rows based on explicit discrete values (e.g., country codes or departments); and **Hash Partitioning** assigns rows using a hash function modulus to distribute data evenly across a fixed number of partitions. Partition Pruning is an optimization where the query planner analyzes `WHERE` clauses to completely bypass scanning partitions that cannot possibly contain matching records. This reduces disk I/O, speeds up maintenance (dropping an old month partition via `DROP TABLE` is instant and generates zero write-ahead log bloat), and enhances query throughput.
**Key Points:**
- Range Partitioning: Best for sequential time series data (e.g., monthly sales logs).
- List Partitioning: Best for discrete categorical values (e.g., regions, currencies).
- Hash Partitioning: Even data distribution without natural range keys.
- Partition Pruning: Planner skips non-relevant partitions entirely, drastically minimizing I/O.
- Maintenance: `DROP TABLE` on old partitions avoids slow, log-heavy `DELETE` operations.
**Evaluation Criteria:** Candidate should define all three partitioning methods, explain how the optimizer leverages Partition Pruning to eliminate I/O, and cite bulk drop maintenance benefits.

### Q9: How do you detect, diagnose, and resolve slow queries caused by Parameter Sniffing or stale cardinality statistics?
**Answer:** Database query planners rely on data distribution histograms and statistics collected via `ANALYZE` to estimate row counts (cardinality) and pick optimal execution plans. Parameter Sniffing occurs in stored procedures or parameterized queries when the planner compiles an execution plan tailored to the parameters passed during the initial call; if that first execution uses an atypical, highly skewed parameter, subsequent executions with typical parameters are forced into an inappropriate plan (e.g., a Nested Loop instead of a Hash Join). Stale statistics happen when rapid data modifications render table histograms obsolete, causing the optimizer to severely underestimate rows. Diagnosis involves using `EXPLAIN ANALYZE` to compare estimated rows against actual rows. Resolution includes running `ANALYZE` to refresh statistics, using query hints/recompile flags (`OPTIMIZE FOR` or `RECOMPILE`), or parameter masking via local variables.
**Key Points:**
- Cardinality estimation relies on statistical histograms gathered via `ANALYZE`.
- Parameter Sniffing: Initial parameter compile-time plan cached and reused inappropriately for skewed inputs.
- Diagnosis: Discrepancy between "estimated rows" and "actual rows" in `EXPLAIN ANALYZE`.
- Remediation: Executing `ANALYZE`, compiling with `RECOMPILE` or `OPTIMIZE FOR UNKNOWN`, and breaking stored procedures into smaller specialized units.
**Evaluation Criteria:** Candidate should explain how parameter caching works, recognize cardinality misestimates in query plans, and provide concrete database tuning remediations.

### Q10: Contrast Optimistic Concurrency Control (OCC) with Pessimistic Concurrency Control (`SELECT ... FOR UPDATE`). When should each be chosen?
**Answer:** Pessimistic Concurrency Control assumes conflicts are frequent and locks rows immediately upon reading them using constructs like `SELECT ... FOR UPDATE`, blocking other transactions from modifying or locking those rows until the transaction commits. Optimistic Concurrency Control (OCC) assumes conflicts are rare and allows transactions to read and update data without acquiring explicit row locks. Instead, OCC tracks a version number or timestamp column; during the final update, it checks `WHERE id = :id AND version = :old_version`, failing or rolling back if another transaction incremented the version in the interim. Pessimistic locking is ideal for high-contention, low-latency financial balances or inventory reservation where collisions are common and rolling back complex operations is costly. OCC is superior for read-heavy systems, stateless microservices, and distributed web applications where maintaining long-lived database locks degrades throughput.
**Key Points:**
- Pessimistic: `SELECT ... FOR UPDATE`; acquires exclusive row locks immediately; prevents concurrent updates.
- Optimistic (OCC): Version column checking at update time (`WHERE version = @v`); zero read-locking overhead.
- Contention trade-off: Pessimistic handles high-conflict write queues without retries; OCC degrades under high collision.
- System architecture: OCC is suited for stateless web apps and microservices; Pessimistic is suited for critical financial ledgers and seat bookings.
**Evaluation Criteria:** Candidate must describe the technical mechanics of both patterns (version checking vs. lock acquisition) and map them accurately to contention levels and application architectures.

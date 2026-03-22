# The Agentic Hive
## Assignment 1: The Multi-Tenant User Directory

## Overview
The Agentic Hive is a B2B SaaS platform for managing AI agents. It demonstrates strict transactional updates for user billing (ACID compliance) and horizontal scaling using a dynamic In-Memory Sharded Architecture.

## Architecture

### 1. Data Modeling
- **SQL (Relational & ACID)**: Handled via `init_schema.sql` (defining Tenants, Users, Agents, and Billing). Billing updates are wrapped inside `BEGIN TRANSACTION` blocks to guarantee ACID compliance.
- **NoSQL (Key-Value)**: Simulated via `nosql_store.py` using a fast memory dictionary to instantly retrieve AI Agent session states, bypassing relational queries.

### 2. Sharding
- Application routing is managed by `sharding.py`. The script utilizes Consistent Hashing to dynamically route tenant data exclusively to their assigned shards (`Shard_A`, `Shard_B`, or `Shard_C`).

### 3. Replication
- Every Shard opens dual connections: a **Primary** and a **Replica**. 
- Write updates mirror to the Replica instantly. 
- Analytics queries are routed strictly to the **Replica node** to protect the Primary database from performance degradation.

## File Structure
- `agentic_hive.py` — The core CLI application.
- `sharding.py` — The router that handles the SQLite DBs, Hashing logic, and Replication.
- `nosql_store.py` — The isolated NoSQL caching module.
- `init_schema.sql` — Pure SQL definitions for the relational schema.

## How to Run
This project comes with a built-in interactive Command-Line Interface (CLI).

1. Open your terminal natively in this directory.
2. Execute the application:
   ```bash
   python agentic_hive.py
   ```
3. To run full demonstration select **Option 6**.

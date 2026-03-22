-- init_schema.sql
-- Relational Schema

-- 1. Tenants Table
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- 2. Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    tenant_id INTEGER,
    username TEXT NOT NULL,
    FOREIGN KEY(tenant_id) REFERENCES tenants(tenant_id)
);

-- 3. AI Agents
CREATE TABLE IF NOT EXISTS ai_agents (
    agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER,
    agent_name TEXT NOT NULL,
    model_version TEXT,
    FOREIGN KEY(tenant_id) REFERENCES tenants(tenant_id)
);

-- 4. Billing Ledger
CREATE TABLE IF NOT EXISTS billing_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER,
    tokens_spent INTEGER,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

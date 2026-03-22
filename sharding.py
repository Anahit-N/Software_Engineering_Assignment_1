import sqlite3
import hashlib
import sys

# 1. Shard Configuration
shards = {
    'Shard_A': {
        'primary': sqlite3.connect('file:mem_shard_A_primary?mode=memory&cache=shared', uri=True, check_same_thread=False),
        'replica': sqlite3.connect('file:mem_shard_A_replica?mode=memory&cache=shared', uri=True, check_same_thread=False)
    },
    'Shard_B': {
        'primary': sqlite3.connect('file:mem_shard_B_primary?mode=memory&cache=shared', uri=True, check_same_thread=False),
        'replica': sqlite3.connect('file:mem_shard_B_replica?mode=memory&cache=shared', uri=True, check_same_thread=False)
    },
    'Shard_C': {
        'primary': sqlite3.connect('file:mem_shard_C_primary?mode=memory&cache=shared', uri=True, check_same_thread=False),
        'replica': sqlite3.connect('file:mem_shard_C_replica?mode=memory&cache=shared', uri=True, check_same_thread=False)
    }
}

def initialize_databases():
    """Initializes schemas dynamically across all Shards and Replicas."""
    try:
        with open('init_schema.sql', 'r') as f:
            schema_sql = f.read()
    except FileNotFoundError:
        print("Error: Could not find init_schema.sql")
        sys.exit(1)

    for shard_key, dbs in shards.items():
        for db_role, conn in dbs.items():
            conn.executescript(schema_sql)
            conn.commit()
    print("All In-Memory SQLite databases initialized.")


# 2. Consistent Hashing
def get_db_shard(tenant_id):
    """
    Advanced routing: Maps a tenant ID reliably to a shard using SHA-256.
    This mimics real-world enterprise databases mapping UUIDs to shards!
    """
    hash_object = hashlib.sha256(str(tenant_id).encode())
    hash_int = int(hash_object.hexdigest(), 16)
    
    shard_keys = list(shards.keys())
    shard_index = hash_int % len(shard_keys)
    shard_name = shard_keys[shard_index]
    
    return shards[shard_name], shard_name


# 3. Replication
def execute_write(tenant_id, query, params=()):
    shard_conns, shard_name = get_db_shard(tenant_id)
    primary_conn = shard_conns['primary']
    replica_conn = shard_conns['replica']

    # Write to primary 
    p_cursor = primary_conn.cursor()
    p_cursor.execute("BEGIN TRANSACTION")
    p_cursor.execute(query, params)
    primary_conn.commit()
    
    # Mirror exactly to replica
    r_cursor = replica_conn.cursor()
    r_cursor.execute("BEGIN TRANSACTION")
    r_cursor.execute(query, params)
    replica_conn.commit()
    
    return shard_name

def execute_read(tenant_id, query, params=()):
    shard_conns, shard_name = get_db_shard(tenant_id)
    replica_conn = shard_conns['replica']
    
    r_cursor = replica_conn.cursor()
    r_cursor.execute(query, params)
    result = r_cursor.fetchall()
    
    return result, shard_name

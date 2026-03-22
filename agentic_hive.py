import sqlite3
import json
import sys

from nosql_store import agent_nosql_store
from sharding import initialize_databases, execute_write, execute_read

# Interactive CLI
def start_cli():
    initialize_databases()
    print("\n" + "="*40)
    print("Welcome to THE AGENTIC HIVE")
    print("="*40)
    
    while True:
        print("\n[ Main Menu ]")
        print("1. Create Tenant") 
        print("2. Record Billing Transaction (Requires Tenant)")
        print("3. Fetch Tenant Analytics (Reads from Replica)")
        print("4. Update Agent Quick-Memory (NoSQL)")
        print("5. View All NoSQL Memory")
        print("6. Run Automated Demo Script")
        print("7. Exit")
        
        choice = input("\nSelect an option [1-7]: ").strip()
        
        try:
            if choice == '1':
                tid = int(input("Enter Tenant ID (number): "))
                name = input("Enter Tenant Name: ")
                shard = execute_write(tid, "INSERT INTO tenants (tenant_id, name) VALUES (?, ?)", (tid, name))
                print(f"[SUCCESS] Tenant created. Assigned strictly to {shard}.")
                
            elif choice == '2':
                tid = int(input("Enter Tenant ID (number): "))
                tokens = int(input("Enter Tokens Spent: "))
                shard = execute_write(tid, "INSERT INTO billing_ledger (tenant_id, tokens_spent) VALUES (?, ?)", (tid, tokens))
                print(f"[SUCCESS] Wrote to {shard} PRIMARY. Synced instantly to REPLICA.")
                
            elif choice == '3':
                tid = int(input("Enter Tenant ID (number): "))
                result, shard = execute_read(tid, "SELECT SUM(tokens_spent) FROM billing_ledger WHERE tenant_id = ?", (tid,))
                total = result[0][0] if result[0][0] else 0
                print(f"[SUCCESS] Analytics compiled safely from {shard} REPLICA. Total tokens: {total}")
                
            elif choice == '4':
                agent = input("Enter Agent Name: ")
                task = input("What is the agent working on right now? ")
                agent_nosql_store.set(agent, {"current_task": task})
                print("[SUCCESS] Fast NoSQL update complete.")
                
            elif choice == '5':
                print("[In-Memory NoSQL Dump]")
                print(json.dumps(agent_nosql_store.list_all(), indent=2))
                
            elif choice == '6':
                print("\nInitiating Automated Demo Sequence...")
                shard1 = execute_write(150, "INSERT INTO tenants (tenant_id, name) VALUES (?, ?)", (150, "Stark Industries"))
                print(f"-> Stark Industries routed to {shard1}")
                shard2 = execute_write(200, "INSERT INTO tenants (tenant_id, name) VALUES (?, ?)", (200, "Wayne Ent"))
                print(f"-> Wayne Ent routed to {shard2}")
                execute_write(150, "INSERT INTO billing_ledger (tenant_id, tokens_spent) VALUES (?, ?)", (150, 5000))
                print(f"-> Written 5000 tokens for Stark ({shard1} Primary & Replica)")
                
                res, shard_ret = execute_read(150, "SELECT SUM(tokens_spent) FROM billing_ledger WHERE tenant_id = ?", (150,))
                print(f"-> Analytics generated directly from {shard_ret} Replica! Total: {res[0][0]}")
                
                agent_nosql_store.set("stark_bot", {"ping": "analyzing arc reactor"})
                print("-> Updated Stark Bot state via NoSQL")

            elif choice == '7':
                print("Shutting down the Hive")
                break
            else:
                print("Invalid choice, please select 1-7.")
                
        except ValueError:
            print("[ERROR] Please make sure you are typing numbers for Tenant IDs and Tokens.")
        except sqlite3.IntegrityError:
            print("[ERROR] Tenant ID already exists in that Shard! Please use a unique ID.")
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    start_cli()

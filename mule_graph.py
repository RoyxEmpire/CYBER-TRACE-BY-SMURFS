from pathlib import Path
import random

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "TEST DATA GENERATOR"
    / "synthetic_complaints.csv"
)

OUTPUT_PATH = BASE_DIR / "mule_chain_graph.png"


df = pd.read_csv(DATA_PATH)

sample = df.iloc[0]

complaint_id = sample["complaint_id"]
source_count = int(sample["num_source_accounts"])
final_account_flag = int(sample["common_final_account"])
zone = sample["withdrawal_zone"]

graph = nx.DiGraph()

final_account = f"FINAL_ACCOUNT_{complaint_id}"

graph.add_node(
    final_account,
    node_type="final"
)

for index in range(source_count):
    source_account = f"SOURCE_{complaint_id}_{index + 1}"

    graph.add_node(
        source_account,
        node_type="source"
    )

    graph.add_edge(
        source_account,
        final_account,
        relationship="transfers_to"
    )

# Add an intermediate mule account for visualization
if source_count >= 3:
    mule_account = f"MULE_{complaint_id}"

    graph.add_node(
        mule_account,
        node_type="mule"
    )

    first_source = f"SOURCE_{complaint_id}_1"

    graph.remove_edge(first_source, final_account)
    graph.add_edge(
        first_source,
        mule_account,
        relationship="transfers_to"
    )
    graph.add_edge(
        mule_account,
        final_account,
        relationship="forwards_to"
    )

positions = nx.spring_layout(
    graph,
    seed=42
)

node_colors = []

for node in graph.nodes:
    node_type = graph.nodes[node]["node_type"]

    if node_type == "final":
        node_colors.append("red")
    elif node_type == "mule":
        node_colors.append("orange")
    else:
        node_colors.append("skyblue")

plt.figure(figsize=(12, 8))

nx.draw_networkx(
    graph,
    positions,
    node_color=node_colors,
    node_size=2200,
    font_size=8,
    arrows=True,
    edge_color="gray",
    with_labels=True
)

plt.title(
    f"CyberTrace Mule-Chain Visualization\n"
    f"Complaint: {complaint_id} | Zone: {zone}"
)

plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300)
plt.close()

print("Mule-chain graph generated successfully!")
print(f"Complaint ID: {complaint_id}")
print(f"Source accounts: {source_count}")
print(f"Common final account flag: {final_account_flag}")
print(f"Graph saved to:\n{OUTPUT_PATH}")
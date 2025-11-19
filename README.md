# web3_privacy_matrix

A tiny command line tool for exploring and comparing Web3 privacy and soundness stacks.  
The models are inspired by Aztec style zk rollups, Zama style FHE compute, and soundness oriented research labs.

The repository contains exactly two files:
- app.py
- README.md


## Concept

Different privacy and soundness approaches in Web3 have very different trade offs.  
This tool encodes a few high level, illustrative profiles and lets you compare them along simple dimensions:

- Privacy level
- Soundness focus
- Performance cost
- Developer complexity
- Ecosystem maturity

It also provides a composite score that weighs privacy and soundness benefits against cost and complexity.


## Stacks

The following stacks are modeled:

aztec
Aztec style zk rollup with encrypted state and zero knowledge proofs over Ethereum.

zama
Zama style FHE compute where fully homomorphic encryption is used on or around Web3 systems.

soundness
A soundness first lab where the focus is on specifications, proofs, and verification for Web3 protocols.

These entries are conceptual and designed for comparison and intuition building, not as rigorous measurements.


## Installation

Requirements:

- Python 3.10 or newer.

Steps:

1. Create a new GitHub repository with any name.
2. Place app.py and this README.md file in the root folder.
3. Ensure the python executable is on your PATH.
4. No external dependencies are required; only the Python standard library is used.


## Usage

From the root of the repository:

Show all stacks in a pretty table:

python app.py

Show only the Aztec style stack:

python app.py --stack aztec

Sort stacks by soundness focus descending:

python app.py --include-score --sort-by soundness_focus --descending

Show all stacks as CSV:

python app.py --format csv --include-score

Show all stacks as JSON:

python app.py --format json --include-score


## Output

In table mode, the tool prints an ASCII style table with columns:

- key
- name
- family
- privacy_level
- soundness_focus
- performance_cost
- dev_complexity
- ecosystem_maturity
- composite_score (optional)

In CSV mode, it prints comma separated rows suitable for spreadsheets.  
In JSON mode, it prints an array of objects suitable for dashboards or scripts.


## Composite score

The composite_score is a simple heuristic that:

- rewards higher privacy_level and soundness_focus
- penalizes higher performance_cost and dev_complexity

It is not a scientific metric, but a quick way to compare relative trade offs between privacy heavy, FHE heavy, and soundness heavy approaches inspired by Aztec, Zama, and formal verification labs.


## Notes

- All numbers are rough and illustrative.
- The tool does not connect to any blockchain or Web3 RPC endpoint.
- You are encouraged to fork this repository and tune the parameters or add your own stacks to match real world projects.

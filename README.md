# Python Financial Transaction Parser & Audit Tool

## What This Project Does
I built this Python script to solve a common data problem: taking messy, unstructured transaction logs and cleaning them up into a readable financial report. 

The tool reads a large log file (`transactions.txt`), parses individual lines using custom string formatting, and cross-references that data against a directory of 100 separate member profile text files to calculate exactly how much money was sent, received, and what the final balances are for each account.

## Features & Implementation
- **File System Processing:** Used Python's built-in File I/O stream handler (`with open`) to dynamically loop through and read 100+ separate user files sequentially without hardcoding paths.
- **Data Parsing:** Implemented clean string manipulation using `.strip()` and `.split("|")` to isolate specific parameters from raw text blocks.
- **State Aggregation:** Utilized array lookups and index tracking to dynamically add up values, map them to specific user IDs, and calculate final net balances.
- **Reporting:** Automated the clean-up process by outputting the final audited metrics into a clean, tab-separated report file (`analysis.txt`).

## How to Run It
Make sure your python environment has access to the `/members` folder and `transactions.txt` in the same directory, then run:

```bash
python investigate.py

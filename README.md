# Virtual Memory Management Simulator

A Python-based desktop application to simulate virtual memory management processes, built as part of an academic project in Operating Systems. The simulator visualizes key concepts like page tables, Translation Lookaside Buffer (TLB), memory frames, and page replacement algorithms (FIFO, LRU, Optimal), making it an educational tool for understanding system performance.
Features

Interactive GUI: Built with Tkinter, featuring a user-friendly interface with real-time updates.
Page Replacement Algorithms: Supports FIFO, LRU, and Optimal algorithms for handling page faults.
Real-Time Statistics: Displays page faults, TLB hit ratio, hits, and memory utilization during simulation.
Memory Visualization: Includes a scrollable canvas to visualize memory frames (e.g., F0, F1) with dynamic coloring (green for occupied, gray for free).
Customizable Inputs: Configure memory size, page size, processes, and address sequences.
Process Management: Add multiple processes, select specific processes to view their page tables, and simulate address sequences.
Simulation Logging: Detailed logs of each simulation step, including TLB hits/misses and page faults.

## Installation

Clone the Repository:git clone https://github.com/[your-username]/virtual-memory-management-simulator.git
cd virtual-memory-management-simulator


Run the Simulator:python3 main.py


## Interact with the GUI:

Input Parameters:
Enter Memory Size (e.g., 40960 bytes for 10 frames with a 4096-byte page size).
Enter Page Size (e.g., 4096 bytes).
Add processes by entering PID and Size (e.g., PID: P1, Size: 20480), then click Add Process for additional processes.
Specify an Address Sequence (e.g., P1:0,P1:4096,P2:0 in PID:VA format).
Select a Page Replacement Algorithm (FIFO, LRU, or Optimal).
Choose a Display Process to view its page table.


## Simulation Controls:
Click ▶ Start to initialize the simulation.
Click → Step to execute the simulation step-by-step.
Click ↺ Reset to clear inputs and restart.


## Outputs:
View the Page Table, Physical Memory, TLB, and Simulation Log in real-time.
Use the scrollable Memory Frames canvas to visualize frame allocation.
Check Statistics for page faults, hits, TLB hit ratio, and memory utilization.


### Steps

1. Run python3 main.py.
2. Click ▶ Start, then → Step to simulate each address access.




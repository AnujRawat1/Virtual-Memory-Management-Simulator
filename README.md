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

Prerequisites

Python 3.8+: Ensure Python is installed on your system.
Tkinter: Usually included with Python, but can be installed separately if needed (e.g., sudo apt-get install python3-tk on Ubuntu).

Installation

Clone the Repository:git clone https://github.com/[your-username]/virtual-memory-management-simulator.git
cd virtual-memory-management-simulator


Verify Python Installation:python3 --version

Ensure the version is 3.8 or higher.
Install Tkinter (if not already installed):
On Ubuntu/Debian:sudo apt-get update
sudo apt-get install python3-tk


On macOS (usually pre-installed with Python):python3 -m tkinter

If this fails, install Python with Tkinter support via Homebrew.
On Windows, Tkinter is typically included with Python installation.



Usage

Navigate to the Project Directory:cd virtual-memory-management-simulator


Run the Simulator:python3 main.py


Interact with the GUI:
Input Parameters:
Enter Memory Size (e.g., 40960 bytes for 10 frames with a 4096-byte page size).
Enter Page Size (e.g., 4096 bytes).
Add processes by entering PID and Size (e.g., PID: P1, Size: 20480), then click Add Process for additional processes.
Specify an Address Sequence (e.g., P1:0,P1:4096,P2:0 in PID:VA format).
Select a Page Replacement Algorithm (FIFO, LRU, or Optimal).
Choose a Display Process to view its page table.


Simulation Controls:
Click ▶ Start to initialize the simulation.
Click → Step to execute the simulation step-by-step.
Click ↺ Reset to clear inputs and restart.


Outputs:
View the Page Table, Physical Memory, TLB, and Simulation Log in real-time.
Use the scrollable Memory Frames canvas to visualize frame allocation.
Check Statistics for page faults, hits, TLB hit ratio, and memory utilization.





Example
Input

Memory Size: 40960 bytes
Page Size: 4096 bytes
Processes: P1 (20480 bytes), P2 (12288 bytes)
Address Sequence: P1:0,P1:4096,P2:0,P2:8192,P1:8192
Algorithm: FIFO
Display Process: P1

Steps

Run python3 main.py.
Enter the above inputs in the GUI.
Click ▶ Start, then → Step to simulate each address access.

Output (After First Step: P1:0)

Page Table (PID P1):Page Table (PID P1):
Page 0: Frame 0
Page 1: Not in memory
Page 2: Not in memory
Page 3: Not in memory
Page 4: Not in memory


Physical Memory:Physical Memory:
Frame 0: PID P1 Page 0
Frame 1: Free
Frame 2: Free
...
Frame 9: Free


TLB:TLB:
PID P1, Page 0 -> Frame 0


Simulation Log:Process P1: Accessing VA 0 (Page 0, Offset 0): Page Fault! Loaded into Frame 0. Physical Address: 0


Memory Frames Canvas: Frame 0 is green (occupied by P1:0), others are gray (free), labeled as F0, F1, etc.
Statistics: Page Faults: 1 | Hits: 0 | TLB Hit Ratio: 0.00% | Memory Utilization: 10.00%

Project Structure
virtual-memory-management-simulator/
│
├── main.py              # Entry point to run the simulator
├── gui.py               # GUI implementation using Tkinter
├── simulator.py         # Core simulation logic
├── process.py           # Process class for managing processes
├── memory_manager.py    # Memory management and TLB logic
├── algorithms.py        # Page replacement algorithms (FIFO, LRU, Optimal)
└── README.md            # Project documentation

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit (git commit -m "Add new feature").
Push to your branch (git push origin feature-branch).
Create a pull request with a description of your changes.

Built as part of an Operating Systems course to explore virtual memory concepts.
Thanks to the Tkinter community for providing excellent GUI tools for Python.

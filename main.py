import tkinter as tk
from gui import VirtualMemorySimulatorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualMemorySimulatorGUI(root)
    root.mainloop()
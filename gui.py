import tkinter as tk
from tkinter import ttk, messagebox
from simulator import VirtualMemorySimulator


class VirtualMemorySimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Memory Management Simulator")
        self.root.configure(bg="#1e1e1e")

        # Set default window size and center it
        window_width = 1100
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Initialize simulator
        self.simulator = VirtualMemorySimulator(self)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#1e1e1e", foreground="#e0e0e0", font=("Arial", 10))
        self.style.configure("TButton", background="#4169E1", foreground="#ffffff", font=("Arial", 10, "bold"))
        self.style.map("TButton", background=[("active", "#5A82F0")], foreground=[("active", "#ffffff")])
        self.style.configure("Accent.TButton", background="#4169E1", foreground="#ffffff", font=("Arial", 10, "bold"))
        self.style.map("Accent.TButton", background=[("active", "#5A82F0")], foreground=[("active", "#ffffff")])
        self.style.configure("TCombobox", font=("Arial", 10), fieldbackground="#2a2a2a", background="#4169E1",
                             foreground="#e0e0e0")
        self.style.configure("TFrame", background="#1e1e1e")

        # Create GUI
        self.create_gui()

    def create_gui(self):
        # Create main paned window
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True)

        # Left frame for inputs and buttons
        self.left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, weight=1)

        # Right frame for displays with canvas and scrollbar
        self.right_canvas = tk.Canvas(self.paned_window, bg="#1e1e1e", highlightthickness=0)
        self.right_scrollbar = ttk.Scrollbar(self.paned_window, orient="vertical", command=self.right_canvas.yview)
        self.right_scrollable_frame = ttk.Frame(self.right_canvas)

        self.right_scrollable_frame.bind("<Configure>", lambda e: self.right_canvas.configure(
            scrollregion=self.right_canvas.bbox("all")))
        self.right_canvas.create_window((0, 0), window=self.right_scrollable_frame, anchor="nw")
        self.right_canvas.configure(yscrollcommand=self.right_scrollbar.set)

        self.paned_window.add(self.right_canvas, weight=3)
        self.right_scrollbar.pack(side="right", fill="y")

        # Create input and display frames
        self.create_input_frame()
        self.create_control_frame()
        self.create_display_frame()

        # Bind mouse wheel
        self.root.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.right_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_input_frame(self):
        self.input_frame = ttk.LabelFrame(self.left_frame, text="Input Parameters", padding=10)
        self.input_frame.pack(fill="x", padx=10, pady=10)

        # Memory and Page Size
        ttk.Label(self.input_frame, text="Memory Size (bytes):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.input_frame, textvariable=self.simulator.memory_size, width=20).grid(row=0, column=1, padx=5,
                                                                                            pady=5)

        ttk.Label(self.input_frame, text="Page Size (bytes):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.input_frame, textvariable=self.simulator.page_size, width=20).grid(row=1, column=1, padx=5,
                                                                                          pady=5)

        # Process Inputs
        ttk.Label(self.input_frame, text="Processes (PID, Size):").grid(row=2, column=0, columnspan=2, padx=5, pady=5,
                                                                        sticky="w")
        self.process_frame = ttk.Frame(self.input_frame)
        self.process_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Add Process Button
        ttk.Button(self.input_frame, text="Add Process", command=self.add_process_input, style="Accent.TButton").grid(
            row=4, column=0, columnspan=2, padx=5, pady=5)

        # Process Selection for Display
        ttk.Label(self.input_frame, text="Display Page Table:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.pid_menu = ttk.Combobox(self.input_frame, textvariable=self.simulator.selected_pid, state="readonly")
        self.pid_menu.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.pid_menu.bind("<<ComboboxSelected>>", lambda event: self.simulator.update_displays())

        # Address Sequence
        ttk.Label(self.input_frame, text="Address Sequence (PID:VA, ...):").grid(row=6, column=0, columnspan=2, padx=5,
                                                                                 pady=5, sticky="w")
        ttk.Entry(self.input_frame, textvariable=self.simulator.sequence_str, width=30).grid(row=7, column=0,
                                                                                             columnspan=2, padx=5,
                                                                                             pady=5)

        # Algorithm Selection
        ttk.Label(self.input_frame, text="Algorithm:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        algo_menu = ttk.Combobox(self.input_frame, textvariable=self.simulator.algorithm,
                                 values=["FIFO", "LRU", "Optimal"], state="readonly")
        algo_menu.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        # Initialize with one process input
        self.add_process_input()

    def add_process_input(self):
        row = len(self.simulator.process_inputs)
        pid_entry = ttk.Entry(self.process_frame, width=10)
        size_entry = ttk.Entry(self.process_frame, width=15)
        pid_entry.grid(row=row, column=0, padx=5, pady=2)
        size_entry.grid(row=row, column=1, padx=5, pady=2)
        self.simulator.process_inputs.append((pid_entry, size_entry))
        self.update_pid_menu()

    def update_pid_menu(self):
        pids = []
        for pid_entry, _ in self.simulator.process_inputs:
            pid = pid_entry.get().strip()
            if pid:
                pids.append(pid)
        self.pid_menu['values'] = pids
        if pids and not self.simulator.selected_pid.get():
            self.simulator.selected_pid.set(pids[0])

    def create_control_frame(self):
        control_frame = ttk.Frame(self.left_frame, padding=10)
        control_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(control_frame, text="▶ Start", command=self.simulator.start_simulation, style="Accent.TButton").pack(
            fill="x", padx=5, pady=2)
        self.simulator.step_button = ttk.Button(control_frame, text="→ Step", command=self.simulator.step_simulation,
                                                state="disabled", style="Accent.TButton")
        self.simulator.step_button.pack(fill="x", padx=5, pady=2)
        ttk.Button(control_frame, text="↺ Reset", command=self.simulator.reset_simulation, style="Accent.TButton").pack(
            fill="x", padx=5, pady=2)

    def create_display_frame(self):
        display_frame = ttk.LabelFrame(self.right_scrollable_frame, text="Simulation Displays", padding=10)
        display_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Page Table Display
        ttk.Label(display_frame, text="Page Table:", font=("Arial", 12, "bold"), background=None).grid(row=0, column=0,
                                                                                                       padx=5, pady=5,
                                                                                                       sticky="w")
        pt_frame = ttk.Frame(display_frame)
        pt_frame.grid(row=1, column=0, padx=5, pady=5)
        self.simulator.page_table_text = tk.Text(pt_frame, height=8, width=30, bg="#2a2a2a", fg="#e0e0e0",
                                                 font=("Arial", 10))
        self.simulator.page_table_text.pack(side="left")
        pt_scroll = ttk.Scrollbar(pt_frame, orient="vertical", command=self.simulator.page_table_text.yview)
        pt_scroll.pack(side="right", fill="y")
        self.simulator.page_table_text.config(yscrollcommand=pt_scroll.set)

        # Physical Memory Display
        ttk.Label(display_frame, text="Physical Memory:", font=("Arial", 12, "bold"), background=None).grid(row=0,
                                                                                                            column=1,
                                                                                                            padx=5,
                                                                                                            pady=5,
                                                                                                            sticky="w")
        pm_frame = ttk.Frame(display_frame)
        pm_frame.grid(row=1, column=1, padx=5, pady=5)
        self.simulator.physical_memory_text = tk.Text(pm_frame, height=8, width=30, bg="#2a2a2a", fg="#e0e0e0",
                                                      font=("Arial", 10))
        self.simulator.physical_memory_text.pack(side="left")
        pm_scroll = ttk.Scrollbar(pm_frame, orient="vertical", command=self.simulator.physical_memory_text.yview)
        pm_scroll.pack(side="right", fill="y")
        self.simulator.physical_memory_text.config(yscrollcommand=pm_scroll.set)

        # TLB Display
        ttk.Label(display_frame, text="TLB:", font=("Arial", 12, "bold"), background=None).grid(row=2, column=0, padx=5,
                                                                                                pady=5, sticky="w")
        tlb_frame = ttk.Frame(display_frame)
        tlb_frame.grid(row=3, column=0, padx=5, pady=5)
        self.simulator.tlb_text = tk.Text(tlb_frame, height=6, width=40, bg="#2a2a2a", fg="#e0e0e0", font=("Arial", 10))
        self.simulator.tlb_text.pack(side="left")
        tlb_scroll = ttk.Scrollbar(tlb_frame, orient="vertical", command=self.simulator.tlb_text.yview)
        tlb_scroll.pack(side="right", fill="y")
        self.simulator.tlb_text.config(yscrollcommand=tlb_scroll.set)

        # Memory Visualization Canvas with Horizontal Scrollbar
        ttk.Label(display_frame, text="Memory Frames:", font=("Arial", 12, "bold"), background=None).grid(row=2,
                                                                                                          column=1,
                                                                                                          padx=5,
                                                                                                          pady=5,
                                                                                                          sticky="w")
        canvas_frame = ttk.Frame(display_frame)
        canvas_frame.grid(row=3, column=1, padx=5, pady=5)

        self.simulator.canvas = tk.Canvas(canvas_frame, bg="#2a2a2a", height=120, width=300, highlightthickness=0)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.simulator.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.simulator.canvas.yview)

        self.simulator.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

        self.simulator.canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        # Log Display
        ttk.Label(display_frame, text="Simulation Log:", font=("Arial", 12, "bold"), background=None).grid(row=4,
                                                                                                           column=0,
                                                                                                           padx=5,
                                                                                                           pady=5,
                                                                                                           sticky="w")
        log_frame = ttk.Frame(display_frame)
        log_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.simulator.log_text = tk.Text(log_frame, height=6, width=60, bg="#2a2a2a", fg="#e0e0e0", font=("Arial", 10))
        self.simulator.log_text.pack(side="left")
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.simulator.log_text.yview)
        log_scroll.pack(side="right", fill="y")
        self.simulator.log_text.config(yscrollcommand=log_scroll.set)

        # Statistics
        self.simulator.stats_label = ttk.Label(display_frame,
                                               text="Page Faults: 0 | Hits: 0 | TLB Hit Ratio: 0% | Memory Utilization: 0%",
                                               background="#1e1e1e", font=("Arial", 10, "bold"))
        self.simulator.stats_label.grid(row=6, column=0, columnspan=2, pady=10)
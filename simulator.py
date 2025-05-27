import tkinter as tk
from tkinter import messagebox
from process import Process
from memory_manager import MemoryManager
from algorithms import handle_page_fault_fifo, handle_page_fault_lru, replace_page_optimal


class VirtualMemorySimulator:
    def __init__(self, gui):
        self.gui = gui
        self.memory_size = tk.IntVar()
        self.page_size = tk.IntVar()
        self.processes = {}
        self.process_inputs = []
        self.sequence_str = tk.StringVar()
        self.algorithm = tk.StringVar(value="FIFO")
        self.selected_pid = tk.StringVar()
        self.memory_manager = None
        self.sequence = []
        self.current_step = 0
        self.page_faults = 0
        self.hits = 0

    def start_simulation(self):
        try:
            mem_size = self.memory_size.get()
            pg_size = self.page_size.get()
            if mem_size <= 0 or pg_size <= 0:
                raise ValueError("Memory and page sizes must be positive integers.")

            self.processes.clear()
            valid_pids = []
            for pid_entry, size_entry in self.process_inputs:
                pid = pid_entry.get().strip()
                size_str = size_entry.get().strip()
                if not pid:
                    continue
                if not size_str:
                    raise ValueError(f"Size missing for process {pid}.")
                try:
                    size = int(size_str)
                except ValueError:
                    raise ValueError(f"Invalid size for process {pid}: {size_str}")
                if size <= 0:
                    raise ValueError(f"Size for process {pid} must be positive.")
                if pid in self.processes:
                    raise ValueError(f"Duplicate PID: {pid}")
                self.processes[pid] = Process(pid, size, pg_size)
                valid_pids.append(pid)

            if not self.processes:
                raise ValueError("At least one process must be defined.")

            seq = []
            for item in self.sequence_str.get().split(","):
                item = item.strip()
                if not item:
                    continue
                if ":" not in item:
                    raise ValueError("Address sequence must be in PID:VA format.")
                pid, va = item.split(":")
                pid = pid.strip()
                try:
                    va = int(va.strip())
                except ValueError:
                    raise ValueError(f"Invalid virtual address in sequence: {va}")
                if pid not in self.processes:
                    raise ValueError(f"Invalid PID {pid} in sequence.")
                if va < 0 or va >= self.processes[pid].process_size:
                    raise ValueError(f"Address {va} out of range for process {pid}.")
                seq.append((pid, va))

            if not seq:
                raise ValueError("Address sequence cannot be empty.")

            self.memory_manager = MemoryManager(mem_size, pg_size)
            self.sequence = seq
            self.current_step = 0
            self.page_faults = 0
            self.hits = 0

            self.gui.update_pid_menu()
            if valid_pids:
                self.selected_pid.set(valid_pids[0])
            else:
                self.selected_pid.set("")

            self.update_displays()
            self.log_text.delete(1.0, tk.END)
            self.step_button.config(state="normal")
            self.stats_label.config(text="Page Faults: 0 | Hits: 0 | TLB Hit Ratio: 0% | Memory Utilization: 0%")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def step_simulation(self):
        if self.current_step >= len(self.sequence):
            messagebox.showinfo("Simulation", "Simulation completed.")
            self.step_button.config(state="disabled")
            return

        pid, addr = self.sequence[self.current_step]
        process = self.processes[pid]
        page_num = process.get_page_number(addr)
        offset = process.get_offset(addr)

        log = f"Process {pid}: Accessing VA {addr} (Page {page_num}, Offset {offset}): "

        frame = self.memory_manager.check_tlb(pid, page_num)
        if frame is not None:
            self.hits += 1
            phys_addr = frame * self.page_size.get() + offset
            log += f"TLB Hit! Physical Address: {phys_addr}"
        else:
            if process.page_table[page_num] != -1:
                self.hits += 1
                frame = process.page_table[page_num]
                phys_addr = frame * self.page_size.get() + offset
                log += f"TLB Miss, Page Table Hit! Physical Address: {phys_addr}"
                self.memory_manager.update_tlb(pid, page_num, frame)
            else:
                self.page_faults += 1
                log += "Page Fault! "
                if self.algorithm.get() == "FIFO":
                    frame = handle_page_fault_fifo(self.memory_manager, pid, page_num)
                elif self.algorithm.get() == "LRU":
                    frame = handle_page_fault_lru(self.memory_manager, pid, page_num)
                else:
                    frame = replace_page_optimal(self.memory_manager, pid, page_num,
                                                 self.sequence[self.current_step + 1:], self.page_size.get(),
                                                 self.processes)
                process.page_table[page_num] = frame
                # Evict old page if frame was occupied
                if self.memory_manager.frames[frame][1] != -1:
                    old_pid, old_page = self.memory_manager.frames[frame]
                    for p in self.processes.values():
                        if p.pid == old_pid:
                            for i, f in enumerate(p.page_table):
                                if f == frame:
                                    p.page_table[i] = -1
                                    break
                self.memory_manager.frames[frame] = (pid, page_num)
                self.memory_manager.update_tlb(pid, page_num, frame)
                phys_addr = frame * self.page_size.get() + offset
                log += f"Loaded into Frame {frame}. Physical Address: {phys_addr}"

        self.log_text.insert(tk.END, log + "\n")
        self.log_text.see(tk.END)
        self.update_displays()
        tlb_hit_ratio = (self.memory_manager.tlb_hits / (
                    self.memory_manager.tlb_hits + self.memory_manager.tlb_misses) * 100) if (
                                                                                                         self.memory_manager.tlb_hits + self.memory_manager.tlb_misses) > 0 else 0
        mem_util = self.memory_manager.get_memory_utilization()
        self.stats_label.config(
            text=f"Page Faults: {self.page_faults} | Hits: {self.hits} | TLB Hit Ratio: {tlb_hit_ratio:.2f}% | Memory Utilization: {mem_util:.2f}%")
        self.current_step += 1

    def update_displays(self):
        # Update Page Table Display
        self.page_table_text.delete(1.0, tk.END)
        pt_text = f"Page Table (PID {self.selected_pid.get()}):\n"
        if self.selected_pid.get() in self.processes:
            for i, frame in enumerate(self.processes[self.selected_pid.get()].page_table):
                pt_text += f"Page {i}: {'Frame ' + str(frame) if frame != -1 else 'Not in memory'}\n"
        else:
            pt_text += "Select a valid process to view its page table.\n"
        self.page_table_text.insert(tk.END, pt_text)

        # Update Physical Memory Display
        self.physical_memory_text.delete(1.0, tk.END)
        pm_text = "Physical Memory:\n"
        if self.memory_manager:
            for i, (pid, page) in enumerate(self.memory_manager.frames):
                if page != -1 and pid is not None:
                    pm_text += f"Frame {i}: PID {pid} Page {page}\n"
                else:
                    pm_text += f"Frame {i}: Free\n"
        self.physical_memory_text.insert(tk.END, pm_text)

        # Update TLB Display
        self.tlb_text.delete(1.0, tk.END)
        tlb_text = "TLB:\n"
        if self.memory_manager:
            for pid, page_num, frame_num in self.memory_manager.tlb:
                tlb_text += f"PID {pid}, Page {page_num} -> Frame {frame_num}\n"
        self.tlb_text.insert(tk.END, tlb_text)

        # Update Memory Frames Canvas
        self.canvas.delete("all")
        if self.memory_manager:
            frame_width = 40
            frame_height = 60
            total_width = len(self.memory_manager.frames) * (frame_width + 10) + 10  # Total width needed
            total_height = frame_height + 40  # Increased height for frame numbers

            # Set canvas scroll region
            self.canvas.configure(scrollregion=(0, 0, total_width, total_height))

            for i, (pid, page) in enumerate(self.memory_manager.frames):
                x = 10 + i * (frame_width + 10)
                y = 10
                color = "#4CAF50" if page != -1 else "#4a4a4a"
                self.canvas.create_rectangle(x, y, x + frame_width, y + frame_height, fill=color, outline="#e0e0e0")
                # PID:Page or Free label inside the frame
                text = f"{pid}:{page}" if page != -1 and pid is not None else "Free"
                self.canvas.create_text(x + frame_width / 2, y + frame_height / 2, text=text, fill="#e0e0e0",
                                        font=("Arial", 8))
                # Frame number below the frame
                self.canvas.create_text(x + frame_width / 2, y + frame_height + 15, text=f"F{i}", fill="#e0e0e0",
                                        font=("Arial", 8))

    def reset_simulation(self):
        self.memory_size.set(0)
        self.page_size.set(0)
        self.sequence_str.set("")
        self.algorithm.set("FIFO")
        self.selected_pid.set("")
        for pid_entry, size_entry in self.process_inputs:
            pid_entry.delete(0, tk.END)
            size_entry.delete(0, tk.END)
        self.process_inputs = []
        self.process_frame.destroy()
        self.process_frame = ttk.Frame(self.gui.input_frame)
        self.process_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.gui.add_process_input()
        self.processes.clear()
        self.memory_manager = None
        self.page_table_text.delete(1.0, tk.END)
        self.physical_memory_text.delete(1.0, tk.END)
        self.tlb_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.canvas.delete("all")
        self.stats_label.config(text="Page Faults: 0 | Hits: 0 | TLB Hit Ratio: 0% | Memory Utilization: 0%")
        self.step_button.config(state="disabled")
        self.gui.update_pid_menu()
from collections import deque
class MemoryManager:
    def __init__(self, memory_size, page_size, tlb_size=4):
        self.memory_size = memory_size
        self.page_size = page_size
        self.num_frames = memory_size // page_size
        self.frames = [(None, -1)] * self.num_frames  # Store (pid, page_num) tuples
        self.tlb = []
        self.tlb_size = tlb_size
        self.fifo_queue = deque()
        self.lru_stack = []
        self.tlb_hits = 0
        self.tlb_misses = 0

    def check_tlb(self, pid, page_num):
        for entry in self.tlb:
            if entry[0] == pid and entry[1] == page_num:
                self.tlb_hits += 1
                return entry[2]
        self.tlb_misses += 1
        return None

    def update_tlb(self, pid, page_num, frame_num):
        if len(self.tlb) >= self.tlb_size:
            self.tlb.pop(0)
        self.tlb.append((pid, page_num, frame_num))

    def get_memory_utilization(self):
        used_frames = sum(1 for pid, page in self.frames if page != -1)
        return (used_frames / self.num_frames) * 100 if self.num_frames > 0 else 0
def handle_page_fault_fifo(memory_manager, pid, page_num):
    for i in range(memory_manager.num_frames):
        if memory_manager.frames[i][1] == -1:
            memory_manager.fifo_queue.append((pid, page_num))
            return i

    victim_pid, victim_page = memory_manager.fifo_queue.popleft()
    memory_manager.fifo_queue.append((pid, page_num))
    for i, (p, page) in enumerate(memory_manager.frames):
        if p == victim_pid and page == victim_page:
            return i
    return -1


def handle_page_fault_lru(memory_manager, pid, page_num):
    for i in range(memory_manager.num_frames):
        if memory_manager.frames[i][1] == -1:
            memory_manager.lru_stack.append((pid, page_num))
            return i

    victim_pid, victim_page = memory_manager.lru_stack.pop(0)
    memory_manager.lru_stack.append((pid, page_num))
    for i, (p, page) in enumerate(memory_manager.frames):
        if p == victim_pid and page == victim_page:
            return i
    return -1


def replace_page_optimal(memory_manager, new_pid, new_page, future_sequence, page_size, processes):
    frame_entries = [(pid, page) for pid, page in memory_manager.frames if page != -1]
    next_use = {}

    for pid, page in frame_entries:
        next_use[(pid, page)] = float('inf')
        for i, addr in enumerate(future_sequence):
            seq_pid, va = addr
            page_num = va // page_size
            if seq_pid == pid:
                for proc in processes.values():
                    if proc.pid == pid and proc.page_table[page_num] == find_frame(memory_manager, pid, page):
                        next_use[(pid, page)] = i
                        break

    victim_pid, victim_page = max(next_use, key=next_use.get)
    return find_frame(memory_manager, victim_pid, victim_page)


def find_frame(memory_manager, pid, page_num):
    for i, (p, page) in enumerate(memory_manager.frames):
        if p == pid and page == page_num:
            return i
    return -1
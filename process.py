class Process:
    def __init__(self, pid, process_size, page_size):
        self.pid = pid
        self.process_size = process_size
        self.page_size = page_size
        self.num_pages = (process_size + page_size - 1) // page_size
        self.page_table = [-1] * self.num_pages

    def get_page_number(self, virtual_address):
        return virtual_address // self.page_size

    def get_offset(self, virtual_address):
        return virtual_address % self.page_size
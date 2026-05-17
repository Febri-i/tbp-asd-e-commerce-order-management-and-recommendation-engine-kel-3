from typing import Optional
class LLNode:
    def __init__(self, data):
        self.data = data
        self.next: Optional['LLNode'] = None

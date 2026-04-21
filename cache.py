import hashlib
import json
import time
from typing import List, Optional

class SafetyCache:
    def __init__(self):
        # Using an in-memory dict for simplicity as allowed [cite: 31]
        self.storage = {}
        self.ttl = 3600  # 1 hour in seconds [cite: 31]

    def _generate_key(self, proposed: List[str], current: List[str]) -> str:
        # Sort both lists to ensure the hash is deterministic 
        combined = sorted([m.lower().strip() for m in proposed]) + \
                   sorted([m.lower().strip() for m in current])
        
        # Create a unique string and hash it using SHA-256
        data_string = "|".join(combined)
        return hashlib.sha256(data_string.encode()).hexdigest()

    def get(self, proposed: List[str], current: List[str]) -> Optional[dict]:
        key = self._generate_key(proposed, current)
        if key in self.storage:
            entry = self.storage[key]
            # Check if cache has expired [cite: 31]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['data']
            else:
                del self.storage[key]
        return None

    def set(self, proposed: List[str], current: List[str], data: dict):
        key = self._generate_key(proposed, current)
        self.storage[key] = {
            'timestamp': time.time(),
            'data': data
        }
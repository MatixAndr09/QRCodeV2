from functools import lru_cache
import psutil

class MemoryGuard:
    MAX_MEMORY_USAGE = 1024 * 1024 * 1024
    BUFFER_RATIO = 0.2

    @lru_cache(maxsize=1)
    def get_system_memory(self) -> int:
        return psutil.virtual_memory().total

    def check_memory_usage(self) -> bool:
        process = psutil.Process()
        current_usage = process.memory_info().rss
        max_allowed = min(
            self.MAX_MEMORY_USAGE,
            self.get_system_memory() * (1 - self.BUFFER_RATIO)
        )
        return current_usage < max_allowed

    def validate_matrix_size(self, width: int, height: int) -> bool:
        estimated_memory = width * height * 3  # 3 bytes per pixel
        padding_factor = 1.5
        return (estimated_memory * padding_factor) < self.MAX_MEMORY_USAGE
import psutil

class MemoryGuard:
    MAX_MEMORY_USAGE = 1024 * 1024 * 1024

    @staticmethod
    def check_memory_usage() -> bool:
        process = psutil.Process()
        return process.memory_info().rss < MemoryGuard.MAX_MEMORY_USAGE

    @staticmethod
    def validate_matrix_size(width: int, height: int) -> bool:
        estimated_memory = width * height * 3  # 3 bytes per pixel
        return estimated_memory < MemoryGuard.MAX_MEMORY_USAGE // 2
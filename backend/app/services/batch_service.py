from typing import List, Any, Callable, Awaitable
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BatchService:
    def __init__(self, batch_size: int = 10, max_workers: int = 4):
        self.batch_size = batch_size
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def process_batch(
        self,
        items: List[Any],
        process_fn: Callable[[Any], Awaitable[Any]]
    ) -> List[Any]:
        """Process items in batches asynchronously"""
        results = []
        
        # Split items into batches
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            
            # Process batch concurrently
            batch_tasks = [process_fn(item) for item in batch]
            batch_results = await asyncio.gather(*batch_tasks)
            results.extend(batch_results)
            
            # Small delay between batches to prevent overload
            await asyncio.sleep(0.1)
        
        return results

    def process_batch_sync(
        self,
        items: List[Any],
        process_fn: Callable[[Any], Any]
    ) -> List[Any]:
        """Process items in batches using thread pool"""
        results = []
        
        # Split items into batches
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            
            # Process batch using thread pool
            batch_results = list(self.executor.map(process_fn, batch))
            results.extend(batch_results)
        
        return results

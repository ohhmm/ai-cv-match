import pytest
import asyncio
from app.services.batch_service import BatchService

@pytest.fixture
def batch_service():
    return BatchService(batch_size=2)

def test_process_batch_sync(batch_service):
    items = [1, 2, 3, 4, 5]
    def process_fn(x): return x * 2
    
    results = batch_service.process_batch_sync(items, process_fn)
    assert results == [2, 4, 6, 8, 10]

@pytest.mark.asyncio
async def test_process_batch_async(batch_service):
    items = [1, 2, 3, 4, 5]
    async def process_fn(x): 
        await asyncio.sleep(0.1)
        return x * 2
    
    results = await batch_service.process_batch(items, process_fn)
    assert results == [2, 4, 6, 8, 10]

def test_batch_size_respected(batch_service):
    items = [1, 2, 3, 4, 5]
    processed = []
    
    def process_fn(x):
        processed.append(x)
        return x
    
    batch_service.process_batch_sync(items, process_fn)
    
    # Check if items were processed in batches of 2
    assert len(processed) == 5
    # First batch
    assert processed[0:2] == [1, 2]
    # Second batch
    assert processed[2:4] == [3, 4]
    # Last item in its own batch
    assert processed[4:] == [5]

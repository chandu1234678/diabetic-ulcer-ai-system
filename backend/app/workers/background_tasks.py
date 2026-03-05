"""Background task workers."""

import logging
import asyncio
from typing import Callable, Any, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Background task."""
    
    def __init__(
        self,
        task_id: str,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None
    ):
        """
        Initialize task.
        
        Args:
            task_id: Unique task ID
            func: Callable to execute
            args: Positional arguments
            kwargs: Keyword arguments
        """
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
    
    async def execute(self) -> Any:
        """Execute task."""
        try:
            self.status = TaskStatus.RUNNING
            self.started_at = datetime.now()
            
            if asyncio.iscoroutinefunction(self.func):
                self.result = await self.func(*self.args, **self.kwargs)
            else:
                self.result = self.func(*self.args, **self.kwargs)
            
            self.status = TaskStatus.COMPLETED
            self.completed_at = datetime.now()
            
            logger.info(f"Task {self.task_id} completed successfully")
            return self.result
        
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.error = str(e)
            self.completed_at = datetime.now()
            
            logger.error(f"Task {self.task_id} failed: {str(e)}")
            raise
    
    def get_progress(self) -> dict:
        """Get task progress."""
        return {
            "task_id": self.task_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error
        }


class TaskQueue:
    """Background task queue."""
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize task queue.
        
        Args:
            max_workers: Maximum concurrent workers
        """
        self.max_workers = max_workers
        self.tasks = {}
        self.queue = asyncio.Queue()
    
    async def add_task(
        self,
        task_id: str,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None
    ) -> Task:
        """
        Add task to queue.
        
        Args:
            task_id: Unique task ID
            func: Callable to execute
            args: Positional arguments
            kwargs: Keyword arguments
        
        Returns:
            Task object
        """
        task = Task(task_id, func, args, kwargs)
        self.tasks[task_id] = task
        await self.queue.put(task)
        
        logger.debug(f"Added task {task_id} to queue")
        return task
    
    async def get_task_status(self, task_id: str) -> Optional[dict]:
        """Get task status."""
        if task_id not in self.tasks:
            return None
        
        return self.tasks[task_id].get_progress()
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
        
        return False
    
    async def worker(self):
        """Worker coroutine."""
        while True:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=30)
                await task.execute()
            except asyncio.TimeoutError:
                logger.debug("Worker timeout")
                continue
            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
    
    async def start(self):
        """Start worker pool."""
        workers = [
            asyncio.create_task(self.worker())
            for _ in range(self.max_workers)
        ]
        logger.info(f"Started {self.max_workers} workers")
        return workers


class ScheduledTask:
    """Scheduled background task."""
    
    def __init__(
        self,
        task_id: str,
        func: Callable,
        interval: timedelta,
        args: tuple = (),
        kwargs: dict = None
    ):
        """
        Initialize scheduled task.
        
        Args:
            task_id: Unique task ID
            func: Callable to execute
            interval: Execution interval
            args: Positional arguments
            kwargs: Keyword arguments
        """
        self.task_id = task_id
        self.func = func
        self.interval = interval
        self.args = args
        self.kwargs = kwargs or {}
        self.is_running = False
        self.last_execution = None
        self.next_execution = datetime.now() + interval
    
    async def run(self):
        """Run scheduled task."""
        self.is_running = True
        
        while self.is_running:
            try:
                now = datetime.now()
                
                if now >= self.next_execution:
                    logger.debug(f"Executing scheduled task {self.task_id}")
                    
                    if asyncio.iscoroutinefunction(self.func):
                        await self.func(*self.args, **self.kwargs)
                    else:
                        self.func(*self.args, **self.kwargs)
                    
                    self.last_execution = now
                    self.next_execution = now + self.interval
                
                await asyncio.sleep(1)
            
            except Exception as e:
                logger.error(f"Scheduled task {self.task_id} error: {str(e)}")
    
    def stop(self):
        """Stop scheduled task."""
        self.is_running = False
        logger.info(f"Stopped scheduled task {self.task_id}")


class TaskScheduler:
    """Scheduler for background tasks."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.tasks = {}
        self.running = False
    
    def schedule(
        self,
        task_id: str,
        func: Callable,
        interval: timedelta,
        args: tuple = (),
        kwargs: dict = None
    ) -> ScheduledTask:
        """
        Schedule a recurring task.
        
        Args:
            task_id: Unique task ID
            func: Callable to execute
            interval: Execution interval
            args: Positional arguments
            kwargs: Keyword arguments
        
        Returns:
            ScheduledTask object
        """
        task = ScheduledTask(task_id, func, interval, args, kwargs)
        self.tasks[task_id] = task
        
        logger.info(f"Scheduled task {task_id} with interval {interval}")
        return task
    
    async def start(self):
        """Start all scheduled tasks."""
        self.running = True
        
        tasks = [
            asyncio.create_task(task.run())
            for task in self.tasks.values()
        ]
        
        logger.info(f"Started scheduler with {len(tasks)} tasks")
        return tasks
    
    def stop(self):
        """Stop all scheduled tasks."""
        for task in self.tasks.values():
            task.stop()
        
        self.running = False
        logger.info("Stopped scheduler")
    
    def get_task_status(self, task_id: str) -> Optional[dict]:
        """Get scheduled task status."""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return {
            "task_id": task_id,
            "is_running": task.is_running,
            "last_execution": task.last_execution.isoformat() if task.last_execution else None,
            "next_execution": task.next_execution.isoformat(),
            "interval_seconds": task.interval.total_seconds()
        }


# Global instances
task_queue = TaskQueue()
task_scheduler = TaskScheduler()

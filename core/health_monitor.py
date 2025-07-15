
#!/usr/bin/env python3
"""Health monitoring and alerting system"""

import asyncio
import logging
import psutil
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HealthMonitor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alerts = []
        self.last_check = time.time()
    
    async def check_system_health(self) -> Dict[str, Any]:
        """Comprehensive system health check"""
        health_status = {
            "timestamp": time.time(),
            "status": "healthy",
            "checks": {}
        }
        
        # CPU Check
        cpu_percent = psutil.cpu_percent(interval=1)
        health_status["checks"]["cpu"] = {
            "usage_percent": cpu_percent,
            "status": "warning" if cpu_percent > 80 else "healthy"
        }
        
        # Memory Check
        memory = psutil.virtual_memory()
        health_status["checks"]["memory"] = {
            "usage_percent": memory.percent,
            "available_gb": round(memory.available / (1024**3), 2),
            "status": "warning" if memory.percent > 85 else "healthy"
        }
        
        # Disk Check
        disk = psutil.disk_usage('/')
        health_status["checks"]["disk"] = {
            "usage_percent": disk.percent,
            "free_gb": round(disk.free / (1024**3), 2),
            "status": "critical" if disk.percent > 90 else "warning" if disk.percent > 80 else "healthy"
        }
        
        # Determine overall status
        statuses = [check["status"] for check in health_status["checks"].values()]
        if "critical" in statuses:
            health_status["status"] = "critical"
        elif "warning" in statuses:
            health_status["status"] = "warning"
        
        return health_status
    
    async def monitor_loop(self):
        """Continuous monitoring loop"""
        while True:
            try:
                health = await self.check_system_health()
                
                if health["status"] != "healthy":
                    logger.warning(f"Health check status: {health['status']}")
                    logger.warning(f"Details: {health['checks']}")
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(30)

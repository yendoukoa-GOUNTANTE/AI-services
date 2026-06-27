import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VirtualFS:
    """A simulated in-memory file system for Yendoukoa OS."""
    def __init__(self):
        # Initial root structure
        self.files = {
            "/boot/kernel.bin": "Yendoukoa OS Kernel v1.0.0-stable",
            "/etc/hostname": "yendoukoa-ai-node-01",
            "/home/user/welcome.txt": "Welcome to Yendoukoa OS! Your AI-driven workspace is ready."
        }

    def write_file(self, path, content):
        self.files[path] = content
        logger.info(f"FS: Written {len(content)} bytes to {path}")
        return f"Successfully written to {path}"

    def read_file(self, path):
        if path in self.files:
            logger.info(f"FS: Read from {path}")
            return self.files[path]
        return f"Error: File {path} not found"

    def list_files(self, directory="/"):
        # Simple listing logic
        results = [p for p in self.files.keys() if p.startswith(directory)]
        logger.info(f"FS: Listed {len(results)} files in {directory}")
        return results

    def delete_file(self, path):
        if path in self.files:
            del self.files[path]
            logger.info(f"FS: Deleted {path}")
            return f"Successfully deleted {path}"
        return f"Error: File {path} not found"

class VirtualProcessManager:
    """A simulated process manager for Yendoukoa OS."""
    def __init__(self):
        self.processes = {
            1: {"name": "systemd", "status": "running", "cpu": "0.1%", "mem": "1.2MB"},
            2: {"name": "ai-kernel", "status": "running", "cpu": "2.5%", "mem": "128MB"},
            3: {"name": "network-mgr", "status": "running", "cpu": "0.2%", "mem": "4.5MB"}
        }
        self.next_pid = 4

    def spawn_process(self, name, description=""):
        pid = self.next_pid
        self.processes[pid] = {
            "name": name,
            "status": "running",
            "cpu": "0.0%",
            "mem": "0.5MB",
            "description": description
        }
        self.next_pid += 1
        logger.info(f"PROC: Spawned {name} with PID {pid}")
        return pid

    def list_processes(self):
        logger.info(f"PROC: Listing {len(self.processes)} processes")
        return self.processes

    def kill_process(self, pid):
        if pid in self.processes:
            name = self.processes[pid]["name"]
            del self.processes[pid]
            logger.info(f"PROC: Killed {name} (PID {pid})")
            return f"Process {pid} ({name}) terminated."
        return f"Error: PID {pid} not found"

def get_system_status():
    """Returns a general system health status."""
    return {
        "kernel": "v1.0.0-stable",
        "uptime": f"{int(time.time()) % 10000}s",
        "load": "0.15, 0.10, 0.05",
        "memory": "1.2GB / 16GB",
        "storage": "45GB / 512GB"
    }

# Global instances to persist within the application lifecycle
fs = VirtualFS()
proc_mgr = VirtualProcessManager()

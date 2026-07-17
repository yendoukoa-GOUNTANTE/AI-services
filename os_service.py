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

class VirtualDHCPServer:
    """A simulated DHCP server for Yendoukoa OS."""
    def __init__(self):
        self.start_ip = "192.168.1.100"
        self.end_ip = "192.168.1.200"
        self.subnet_mask = "255.255.255.0"
        self.gateway = "192.168.1.1"
        self.dns = "8.8.8.8"
        self.lease_duration = 86400  # 1 day in seconds
        self.leases = {
            "00:1A:2B:3C:4D:5E": {
                "ip": "192.168.1.100",
                "hostname": "yendoukoa-core-node",
                "lease_time": 1715800000,
                "expiry": 1715800000 + 86400
            }
        }

    def get_config(self):
        return {
            "start_ip": self.start_ip,
            "end_ip": self.end_ip,
            "subnet_mask": self.subnet_mask,
            "gateway": self.gateway,
            "dns": self.dns,
            "lease_duration": self.lease_duration
        }

    def configure(self, start_ip=None, end_ip=None, subnet_mask=None, gateway=None, dns=None, lease_duration=None):
        if start_ip: self.start_ip = start_ip
        if end_ip: self.end_ip = end_ip
        if subnet_mask: self.subnet_mask = subnet_mask
        if gateway: self.gateway = gateway
        if dns: self.dns = dns
        if lease_duration is not None: self.lease_duration = int(lease_duration)
        logger.info("DHCP: Server configured successfully")
        return "DHCP server configuration updated successfully"

    def list_leases(self):
        logger.info(f"DHCP: Listing {len(self.leases)} active leases")
        return self.leases

    def _ip_to_int(self, ip):
        parts = list(map(int, ip.split('.')))
        return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

    def _int_to_ip(self, val):
        return f"{(val >> 24) & 0xFF}.{(val >> 16) & 0xFF}.{(val >> 8) & 0xFF}.{val & 0xFF}"

    def allocate_lease(self, mac, hostname, requested_ip=None):
        mac = mac.upper().strip()

        # If already leased, return the current one or renew/update it
        if mac in self.leases:
            self.leases[mac]["hostname"] = hostname
            self.leases[mac]["lease_time"] = int(time.time())
            self.leases[mac]["expiry"] = int(time.time()) + self.lease_duration
            logger.info(f"DHCP: Renewed lease for {mac} -> {self.leases[mac]['ip']}")
            return self.leases[mac]

        # Check requested IP
        if requested_ip:
            req_val = self._ip_to_int(requested_ip)
            start_val = self._ip_to_int(self.start_ip)
            end_val = self._ip_to_int(self.end_ip)

            if start_val <= req_val <= end_val:
                taken_ips = {lease["ip"] for lease in self.leases.values()}
                if requested_ip not in taken_ips:
                    self.leases[mac] = {
                        "ip": requested_ip,
                        "hostname": hostname,
                        "lease_time": int(time.time()),
                        "expiry": int(time.time()) + self.lease_duration
                    }
                    logger.info(f"DHCP: Allocated requested lease for {mac} -> {requested_ip}")
                    return self.leases[mac]

        # Allocate next available IP
        start_val = self._ip_to_int(self.start_ip)
        end_val = self._ip_to_int(self.end_ip)
        taken_ips = {lease["ip"] for lease in self.leases.values()}

        for val in range(start_val, end_val + 1):
            ip_str = self._int_to_ip(val)
            if ip_str not in taken_ips:
                self.leases[mac] = {
                    "ip": ip_str,
                    "hostname": hostname,
                    "lease_time": int(time.time()),
                    "expiry": int(time.time()) + self.lease_duration
                }
                logger.info(f"DHCP: Allocated lease for {mac} -> {ip_str}")
                return self.leases[mac]

        raise ValueError("Error: No available IP addresses in the pool")

    def release_lease(self, mac):
        mac = mac.upper().strip()
        if mac in self.leases:
            ip = self.leases[mac]["ip"]
            del self.leases[mac]
            logger.info(f"DHCP: Released lease for MAC {mac} ({ip})")
            return f"DHCP lease for {mac} ({ip}) released successfully"
        return f"Error: No lease found for MAC {mac}"

# Global instances to persist within the application lifecycle
fs = VirtualFS()
proc_mgr = VirtualProcessManager()
dhcp_server = VirtualDHCPServer()

#!/usr/bin/env python
"""
DHCP Server Administration CLI Tool.
Supports both local simulation mode and API-driven execution.
"""

import argparse
import sys
import json
import os
import requests

def get_default_api_key():
    # Attempt to load from .env file
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.strip().startswith("API_KEY="):
                    return line.strip().split("=", 1)[1].strip("'\" ")
    return os.environ.get("API_KEY", "local_dev_key")

def run_local(args):
    try:
        import os_service
    except ImportError:
        # Add root path to sys.path to resolve imports when running from tools/
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        try:
            import os_service
        except ImportError as e:
            print(f"Error: Could not import os_service in local mode: {e}")
            sys.exit(1)

    server = os_service.dhcp_server

    if args.action == "list":
        leases = server.list_leases()
        print(json.dumps(leases, indent=2))
    elif args.action == "config":
        print(json.dumps(server.get_config(), indent=2))
    elif args.action == "allocate":
        if not args.mac or not args.hostname:
            print("Error: --mac and --hostname are required for allocation.")
            sys.exit(1)
        try:
            lease = server.allocate_lease(args.mac, args.hostname, args.ip)
            print("Successfully allocated lease:")
            print(json.dumps(lease, indent=2))
        except Exception as e:
            print(f"Error during allocation: {e}")
            sys.exit(1)
    elif args.action == "release":
        if not args.mac:
            print("Error: --mac is required for release.")
            sys.exit(1)
        res = server.release_lease(args.mac)
        print(res)
    elif args.action == "configure":
        res = server.configure(
            start_ip=args.start_ip,
            end_ip=args.end_ip,
            subnet_mask=args.subnet_mask,
            gateway=args.gateway,
            dns=args.dns,
            lease_duration=args.lease_duration
        )
        print(res)

def run_api(args):
    url = args.api_url
    api_key = args.api_key or get_default_api_key()

    if not api_key:
        print("Error: API Key is required for API mode. Use --api-key or set API_KEY env variable.")
        sys.exit(1)

    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }

    # Construct prompt representation for AI parser simulation or direct action triggers
    if args.action == "list":
        prompt = "list all active DHCP leases"
    elif args.action == "config":
        prompt = "get current DHCP configurations"
    elif args.action == "allocate":
        if not args.mac or not args.hostname:
            print("Error: --mac and --hostname are required for allocation.")
            sys.exit(1)
        prompt = f"allocate lease for mac {args.mac} and hostname {args.hostname}"
        if args.ip:
            prompt += f" with requested ip {args.ip}"
    elif args.action == "release":
        if not args.mac:
            print("Error: --mac is required for release.")
            sys.exit(1)
        prompt = f"release lease for mac {args.mac}"
    elif args.action == "configure":
        prompt = "configure DHCP pool with properties:"
        config_parts = []
        if args.start_ip: config_parts.append(f"start_ip {args.start_ip}")
        if args.end_ip: config_parts.append(f"end_ip {args.end_ip}")
        if args.subnet_mask: config_parts.append(f"subnet_mask {args.subnet_mask}")
        if args.gateway: config_parts.append(f"gateway {args.gateway}")
        if args.dns: config_parts.append(f"dns {args.dns}")
        if args.lease_duration is not None: config_parts.append(f"lease_duration {args.lease_duration}")
        if not config_parts:
            print("Error: At least one configuration property must be specified.")
            sys.exit(1)
        prompt += " " + ", ".join(config_parts)

    payload = {
        "prompt": prompt,
        "execute": True
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                msg = result.get("message")
                try:
                    # Attempt to parse as JSON if it represents a JSON payload
                    parsed_msg = json.loads(msg)
                    print(json.dumps(parsed_msg, indent=2))
                except:
                    print(msg)
            else:
                print(f"API Error: {result.get('error') or result}")
        else:
            print(f"HTTP Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Failed to connect to DHCP server API: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="DHCP Server Administration Utility")
    parser.add_argument("--mode", choices=["local", "api"], default="local", help="Execution mode (local/api)")
    parser.add_argument("--api-url", default="http://localhost:5000/api/v1/os/dhcp", help="Target API URL for DHCP endpoint")
    parser.add_argument("--api-key", help="API key required for the server connection")

    # Actions
    subparsers = parser.add_subparsers(dest="action", required=True, help="Administrative action to perform")

    # List action
    subparsers.add_parser("list", help="List all active leases")

    # Config action
    subparsers.add_parser("config", help="Get current DHCP server configuration")

    # Allocate action
    allocate_parser = subparsers.add_parser("allocate", help="Request and allocate a DHCP lease")
    allocate_parser.add_argument("--mac", required=True, help="MAC address of the target machine")
    allocate_parser.add_argument("--hostname", required=True, help="Hostname of the target machine")
    allocate_parser.add_argument("--ip", help="Specific requested IP address")

    # Release action
    release_parser = subparsers.add_parser("release", help="Release an active DHCP lease")
    release_parser.add_argument("--mac", required=True, help="MAC address of the machine to release")

    # Configure action
    config_parser = subparsers.add_parser("configure", help="Configure DHCP server pool settings")
    config_parser.add_argument("--start-ip", help="Starting IP of the lease pool")
    config_parser.add_argument("--end-ip", help="Ending IP of the lease pool")
    config_parser.add_argument("--subnet-mask", help="Network subnet mask")
    config_parser.add_argument("--gateway", help="Default gateway IP")
    config_parser.add_argument("--dns", help="Domain Name System IP")
    config_parser.add_argument("--lease-duration", type=int, help="IP lease duration in seconds")

    args = parser.parse_args()

    if args.mode == "local":
        run_local(args)
    else:
        run_api(args)

if __name__ == "__main__":
    main()

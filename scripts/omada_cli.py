#!/usr/bin/env python3
"""
Omada SDN Controller Open API CLI Helper
Supports cross-platform querying and management for Omada SDN Controllers (v5.9+).
"""

import os
import sys
import json
import argparse
from pathlib import Path
import urllib3
import requests

# Disable insecure TLS warnings if local self-signed cert is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_env_file() -> Path:
    current = Path.cwd()
    for p in [current, *current.parents]:
        env_path = p / ".env"
        if env_path.is_file():
            return env_path
    return current / ".env"

def load_env():
    env_file = find_env_file()
    if not env_file.is_file():
        return
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k not in os.environ:
                    os.environ[k] = v
    except Exception as e:
        print(f"[!] Warning: Could not parse .env: {e}", file=sys.stderr)

class OmadaClient:
    def __init__(self):
        load_env()
        self.base_url = (os.getenv("OMADA_URL") or os.getenv("OMADA_BASE_URL") or "https://127.0.0.1:8043").rstrip("/")
        self.client_id = os.getenv("OMADA_CLIENT_ID") or os.getenv("OMADA_CLIENT")
        self.client_secret = os.getenv("OMADA_CLIENT_SECRET") or os.getenv("OMADA_SECRET")
        self.omada_id = os.getenv("OMADA_ID")
        self.site_id = os.getenv("OMADA_SITE_ID")
        self.insecure = os.getenv("OMADA_INSECURE_TLS", "1") in ("1", "true", "True")
        self.token = None

        if not self.client_id or not self.client_secret:
            print("[!] Error: OMADA_CLIENT_ID / OMADA_CLIENT_SECRET not set in environment or .env", file=sys.stderr)
            sys.exit(1)

    def get_token(self) -> str:
        if self.token:
            return self.token
        url = f"{self.base_url}/openapi/authorize/token?grant_type=client_credentials"
        payload = {
            "omadacId": self.omada_id or "",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        resp = requests.post(url, json=payload, verify=not self.insecure, timeout=10)
        data = resp.json()
        if data.get("errorCode") != 0:
            print(f"[!] Authentication failed: {data.get('msg')} (Code: {data.get('errorCode')})", file=sys.stderr)
            sys.exit(1)
        
        result = data.get("result", {})
        self.token = result.get("accessToken")
        if not self.omada_id and result.get("omadacId"):
            self.omada_id = result.get("omadacId")
        return self.token

    def request(self, method: str, path: str, json_body=None, params=None) -> dict:
        token = self.get_token()
        path = path.lstrip("/")
        
        # If relative path, prefix with openapi/v1/{omadacId}
        if not path.startswith("openapi/"):
            if not self.omada_id:
                # discover omada_id from sites if missing
                self.get_sites()
            path = f"openapi/v1/{self.omada_id}/{path}"

        url = f"{self.base_url}/{path}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"AccessToken={token}"
        }
        
        resp = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=json_body,
            params=params,
            verify=not self.insecure,
            timeout=15
        )
        try:
            return resp.json()
        except Exception:
            return {"errorCode": -1, "msg": resp.text, "httpStatus": resp.status_code}

    def get_sites(self) -> list:
        res = self.request("GET", "sites?page=1&pageSize=100")
        if res.get("errorCode") == 0:
            data = res.get("result", {}).get("data", [])
            if data and not self.site_id:
                self.site_id = data[0].get("siteId")
            return data
        return []

    def get_devices(self, site_id: str = None) -> list:
        sid = site_id or self.site_id
        if not sid:
            sites = self.get_sites()
            if sites:
                sid = sites[0].get("siteId")
        res = self.request("GET", f"sites/{sid}/devices?page=1&pageSize=100")
        if res.get("errorCode") == 0:
            return res.get("result", {}).get("data", [])
        return []

    def get_networks(self, site_id: str = None) -> list:
        sid = site_id or self.site_id
        if not sid:
            sites = self.get_sites()
            if sites:
                sid = sites[0].get("siteId")
        res = self.request("GET", f"sites/{sid}/setting/lan/networks?page=1&pageSize=100")
        if res.get("errorCode") == 0:
            return res.get("result", {}).get("data", [])
        return []

    def get_clients(self, site_id: str = None) -> list:
        sid = site_id or self.site_id
        if not sid:
            sites = self.get_sites()
            if sites:
                sid = sites[0].get("siteId")
        res = self.request("GET", f"sites/{sid}/clients?page=1&pageSize=100")
        if res.get("errorCode") == 0:
            return res.get("result", {}).get("data", [])
        return []

def cmd_test(client: OmadaClient, args):
    token = client.get_token()
    print(f"[+] Token acquired successfully: {token[:8]}...{token[-6:]}")
    sites = client.get_sites()
    print(f"[+] Controller reachable at {client.base_url}")
    print(f"[+] Omada ID: {client.omada_id}")
    print(f"[+] Found {len(sites)} site(s):")
    for s in sites:
        print(f"    - {s.get('name')} (Site ID: {s.get('siteId')})")

def cmd_sites(client: OmadaClient, args):
    sites = client.get_sites()
    if args.json:
        print(json.dumps(sites, indent=2))
        return
    print(f"{'Site Name':<20} | {'Site ID':<35}")
    print("-" * 60)
    for s in sites:
        print(f"{s.get('name', ''):<20} | {s.get('siteId', ''):<35}")

def cmd_devices(client: OmadaClient, args):
    devices = client.get_devices(args.site)
    if args.json:
        print(json.dumps(devices, indent=2))
        return
    print(f"{'Name':<22} | {'Model':<15} | {'IP Address':<16} | {'MAC':<18} | {'Status'}")
    print("-" * 85)
    for d in devices:
        status_map = {0: "Disconnected", 1: "Connected", 2: "Pending", 3: "Heartbeat Missed", 4: "Isolated"}
        st = status_map.get(d.get("status"), str(d.get("status")))
        print(f"{d.get('name', 'Unnamed'):<22} | {d.get('model', ''):<15} | {d.get('ip', ''):<16} | {d.get('mac', ''):<18} | {st}")

def cmd_networks(client: OmadaClient, args):
    networks = client.get_networks(args.site)
    if args.json:
        print(json.dumps(networks, indent=2))
        return
    print(f"{'Name':<22} | {'VLAN':<6} | {'Subnet':<20} | {'Gateway':<16} | {'DHCP'}")
    print("-" * 80)
    for n in networks:
        dhcp = "Enabled" if n.get("dhcpEnable") else "Disabled"
        print(f"{n.get('name', ''):<22} | {str(n.get('vlanId', '')):<6} | {n.get('subnet', ''):<20} | {n.get('gateway', ''):<16} | {dhcp}")

def cmd_clients(client: OmadaClient, args):
    clients = client.get_clients(args.site)
    if args.json:
        print(json.dumps(clients, indent=2))
        return
    print(f"{'Name':<22} | {'IP Address':<16} | {'MAC':<18} | {'VLAN':<6} | {'SSID/Port'}")
    print("-" * 80)
    for c in clients:
        vlan = str(c.get("vlanId", "-"))
        conn = c.get("ssid", "") or f"Port {c.get('port', '-')}"
        print(f"{c.get('name', 'Unknown'):<22} | {c.get('ip', ''):<16} | {c.get('mac', ''):<18} | {vlan:<6} | {conn}")

def cmd_request(client: OmadaClient, args):
    body = None
    if args.body:
        try:
            body = json.loads(args.body)
        except Exception as e:
            print(f"[!] Invalid JSON body: {e}", file=sys.stderr)
            sys.exit(1)
    res = client.request(args.method, args.path, json_body=body)
    print(json.dumps(res, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Omada SDN Controller Open API CLI")
    parser.add_argument("--json", action="store_true", help="Output results in raw JSON")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("test", help="Test connectivity and credentials")
    p_sites = subparsers.add_parser("sites", help="List sites")
    
    p_dev = subparsers.add_parser("devices", help="List devices")
    p_dev.add_argument("--site", help="Site ID (optional)")

    p_net = subparsers.add_parser("networks", help="List LAN networks/VLANs")
    p_net.add_argument("--site", help="Site ID (optional)")

    p_cli = subparsers.add_parser("clients", help="List clients")
    p_cli.add_argument("--site", help="Site ID (optional)")

    p_req = subparsers.add_parser("request", help="Send arbitrary API request")
    p_req.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"], help="HTTP Method")
    p_req.add_argument("path", help="Endpoint path (e.g. sites/{siteId}/devices or full path)")
    p_req.add_argument("body", nargs="?", default=None, help="JSON body for POST/PUT/PATCH")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = OmadaClient()
    commands = {
        "test": cmd_test,
        "sites": cmd_sites,
        "devices": cmd_devices,
        "networks": cmd_networks,
        "clients": cmd_clients,
        "request": cmd_request
    }
    commands[args.command](client, args)

if __name__ == "__main__":
    main()

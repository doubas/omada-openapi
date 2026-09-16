# Example Omada Network Topology & Port Allocation

This document provides a reference template for documenting hardware models, MAC addresses, VLAN configurations, and switch port assignments.

---

## 1. Network Hardware (Example)

| Device Name | Hardware Model | MAC Address | IP Address | Role |
|---|---|---|---|---|
| **ROUTER-01** | TP-Link ER707-M2 | `00-11-22-33-44-01` | `192.168.1.1` | Core Gateway / Multi-WAN / DHCP |
| **SWITCH-01** | TP-Link TL-SG2428P | `00-11-22-33-44-02` | `192.168.1.2` | 24-Port Gigabit L2+ PoE+ Core Switch |
| **AP-01** | TP-Link EAP670 | `00-11-22-33-44-03` | `192.168.1.10` | Indoor Access Point |
| **AP-02** | TP-Link EAP225-Outdoor | `00-11-22-33-44-04` | `192.168.1.11` | Outdoor Access Point |

---

## 2. VLAN & Subnet Architecture (Example)

| VLAN ID | Network Name | Subnet / Gateway | DHCP Range | Purpose |
|---|---|---|---|---|
| **1** | `Default` | `192.168.1.0/24` (`.1`) | `.100 - .254` | Network hardware management |
| **10** | `Office_LAN` | `192.168.10.0/24` (`.1`) | `.100 - .254` | Workstations and printers |
| **20** | `VoIP_Voice` | `192.168.20.0/24` (`.1`) | `.100 - .254` | IP Phones & PBX |
| **30** | `CCTV` | `192.168.30.0/24` (`.1`) | `.100 - .254` | Security cameras and NVR |
| **60** | `Guest` | `192.168.60.0/24` (`.1`) | `.100 - .254` | Guest wireless internet |

---

## 3. Core Switch Port Allocation (Template)

| Port | Profile | Native VLAN | Tagged VLANs | Description |
|---|---|---|---|---|
| **1-3** | `AP_Trunk` | 1 | 10, 20, 30, 60 | Access point uplinks (PoE+ enabled) |
| **4** | `All` | 1 | All | Controller host |
| **5-11** | `Office_Access` | 10 | None | Office workstations and printers |
| **12-21** | `VoIP_Desk` | 10 | 20 | Desk Phone (VLAN 20) + Workstation Pass-through (VLAN 10) |
| **22-24** | `All` | 1 | All | Core router uplink and spare capacity |

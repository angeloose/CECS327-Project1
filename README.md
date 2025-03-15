# Cluster Communication System

This project implements a **distributed cluster network** using **UDP-based messaging**.
It enables **intra-cluster and inter-cluster communication** between worker nodes (node.py) and master nodes (master.py).

## Features
- **Master & Worker Nodes**: Masters manage message routing between clusters.
- **UDP Messaging**: Supports Unicast, Broadcast, Multicast.
- **Logging System**: Tracks all communication in a CSV log.
- **Dockerized Deployment**: Easily run the entire system using Docker.

---

## Getting Started

### ️Prerequisites
Before running this system, make sure you have:
- **Docker** installed
- **Python 3** insalled
- A system that supports **Linux**
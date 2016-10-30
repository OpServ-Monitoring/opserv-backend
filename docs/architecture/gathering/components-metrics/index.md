---
layout: doc-entry
title:  "Components & Metrics"
---

This page described the Components and Metrics concept as well as listing all the available data.

# General

Each measurement taken contains the following information

| Concept | Explanation |
| ------------- | ------------- |
| Value  | The measured value. This could be Hz, Usage percentage, temperature etc.  |
| Timestamp  | The time in milliseconds since the Unix epoch at the time the measurement was taken |
| Component | The hardware or general source of the measurement. This could be something like CPU, Process, Network |
| Component_Args | A specification to the source, for CPU-Core the number of the core for example, the processid of procsses, the name of the network interface  |
| Metric | What kind of measurement on the component was taken. Usage or temperature are typical examples, however Info and Name are also metrics that can be "measured". |

# Components & Metrics List

 - CPU
  - Component_Args: Specifies the ID or socket of the CPU in case multiple CPUs are installed on the system

 - GPU
  - Component_Args: Specifies the ID of the installed GPU in case multiple GPUs are installed on the system.

 - Network
  - Component_Args: Specifies the name of the network interface, that will be measured

 - Disk
  - Component_Args: Specifies the location or name of the physical disk that will be measured
 - Partition
  - Component_Args: Specifies the mounting point in the OS of the partition
 - Memory
  - Component_Args: Not needed
 - Process
  - Component_Args: Specifies the process id of the desired process
 - System
  - Component_Args: Not Needed
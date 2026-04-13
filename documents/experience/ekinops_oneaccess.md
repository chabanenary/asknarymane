# Professional Experience — Ekinops / OneAccess (2007–2020)

## Company
Ekinops (formerly OneAccess Networks) is a leading French telecom equipment manufacturer, producing enterprise and carrier-grade CPE routers, residential gateways, Wi-Fi/4G repeaters, and SFP-based network devices. Products are deployed by tier-1 telecom operators including Orange, SFR, and Telefonica, serving tens of thousands of end customers.

## Role
R&D Embedded Systems Developer — Senior embedded Linux engineer within a multidisciplinary R&D team.

## VxWorks RTOS Projects (2007–2012)

### Driver Development and Maintenance
- Developed and maintained low-level drivers on VxWorks RTOS: NAND Flash, memory interfaces, serial connections, ATM/xDSL drivers
- Measured and optimized ATM QoS (Quality of Service) performance on xDSL CPE platforms
- Tuned the software-based GCRA (Generic Cell Rate Algorithm) implementation
- Optimized the SAR (Segmentation and Reassembly) layer to reduce overhead during AAL5 fragmentation
- Adjusted per-class buffer allocation to balance Cell Transfer Delay and Cell Delay Variation across CBR, VBR and ABR service categories
- Optimized task scheduling at OS level for accurate cell scheduling under load
- Correlated CPE-side metrics (output drops, memory pressure, CPU utilization) with network-side QoS measurements to isolate system-rooted degradations

### Boot Loaders and Board Bring-Up
- Developed and maintained boot loaders on Freescale processors (MIPS, PowerPC)
- Responsible for initial board programming with bootloaders and OS images via JTAG
- Used hardware debuggers: Lauterbach Trace32, BDI2000, CodeWarrior, WindRiver Power ICE
- Adapted BSPs for new hardware revisions

### Crash Logging / Software Defense System
- Designed and implemented a software defense system on a dual-core Freescale P1021 processor
- Extracted the exception stack in PowerPC assembly language
- Formatted exception data for crash log exploitation
- Implemented a supervision task on core0 to detect and report crashes on core1
- Integrated core dump data from core1 into the crash log
- Required deep understanding of processor architecture, interrupt handling, and memory layout

### Firmware Loading Engine
- Led the development of an automatic firmware loading engine for network cards (xDSL cards)
- Wrote the complete requirement specification, software design document, and test plan before implementation
- Developed the CLI command for dynamic firmware loading
- Developed the production tools for embedded firmware packaging
- Managed evolutions and maintenance
- This project was a showcase of documentation-first software engineering

### NAND Flash Write Optimization
- Optimized the write algorithm for NAND Flash programming
- Improved block allocation, minimized unnecessary erase cycles, improved sequential write throughput
- Significant reduction in programming time — critical for production line efficiency when thousands of boards go through manufacturing

### Team Coordination
- Coordinated offshore subcontractors (3 people) for driver updates, bootloader patches, and feature development
- Managed corrective and evolutive maintenance cycles

## Linux Embedded Projects (2013–2016)

### Full Embedded Linux Stack
- U-Boot bootloader porting and customization for multiple board revisions
- Kernel configuration and patching, device tree management
- Hardware driver development in kernel-space and user-space:
  - Ethernet controllers, SFP optical transceivers
  - Wi-Fi chipsets, 4G/LTE modems
  - NAND Flash memory interfaces
  - LEDs, watchdog timers, power management ICs
- Board bring-up for new hardware platforms end to end — from JTAG programming to full system validation

### Yocto Build System
- Maintained Yocto-based build environments
- Managed BSP layers, BitBake recipes, cross-compilation toolchains
- Production image generation for ARM (Freescale/NXP QorIQ) and x86 platforms

### Engineering Process
- Wrote functional specifications, architecture documents, and test plans (CMMI Level 3)
- Code reviews and integration managed through a shared internal Git repository
- Authored user guides for board flashing tools, firmware programming utilities, and debug procedures

## Virtual CPE Project (2017–2020)

### Virtual Router on Linux VM
- Developed a virtual router — a full routing solution running as a Debian-based Linux distribution inside a virtual machine
- Integrated system-level components in C: userspace daemons, systemd service management
- Specified, designed, and implemented from scratch a complete software license management framework
- CI/CD with Jenkins: automated builds and integration testing, multi-target firmware compilation, production-ready image generation

### Feature Requests and Client Support
- Treated product evolution needs on system aspects with client support (Orange, SFR, Telefonica)
- Helped write PRQ (Product Requirement) documents
- Evaluated development, integration, and testing workloads
- Managed development or integration follow-up of evolutions

## Earlier Experience

### Eolices / Technology Services Company (2007–2011)
- Developed low-level system components and hardware drivers for xDSL/Wi-Fi routers running VxWorks
- Contributed to firmware integration, BSP adaptation, and validation for telecom-grade CPE devices

### STMicroelectronics (2006–2007)
- 6-month internship during Master's degree at Télécom Paris
- Designed and developed a quality evaluation tool for IPs (Intellectual Properties) before their integration into 3G bandwidth ASICs
- Developed the graphical interface in Perl/Tk
- Developed extraction methods in Shell and Perl scripts
- Wrote the User Guide

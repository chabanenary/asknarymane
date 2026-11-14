# Professional Experience — Narymane Chabane

Narymane's professional background, in chronological order:
- STMicroelectronics, Paris — final-year engineering internship (July to December 2006)
- OneAccess / Ekinops, Paris — one single continuous 13-year experience (May 2007 to March 2020), including 2007-2011 as a contractor through the IT services firm Eolices, then as an employee of OneAccess, which was acquired by Ekinops in 2017
- Parental leave and self-taught career transition into AI (2020 to 2024)
- Independent AI and Android development projects (September 2024 to May 2026)
- Freelance mission in multimodal embedded AI for a start-up (since June 2026, ongoing)

## OneAccess / Ekinops (May 2007 – March 2020) — Overview
- Positions: embedded systems R&D engineer, then senior embedded Linux engineer
- One single continuous experience on the same site and the same products. Eolices is not a separate experience: from 2007 to 2011, Narymane worked at OneAccess as a contractor from the IT services firm Eolices, then she was hired by OneAccess, where she remained an employee until March 2020
- OneAccess Networks, a French network equipment manufacturer, was acquired by Ekinops in 2017 (acquisition completed in October 2017); Narymane therefore worked about two and a half years at OneAccess within the Ekinops group
- Products: production software for carrier-grade network equipment — physical and virtual routers, gateways, Wi-Fi / 4G repeaters, SFP modules — deployed by the thousands at telecom operators (including Orange, SFR and Telefonica), running Linux and VxWorks
- Multidisciplinary R&D team, CMMI Level 3 quality processes
- Scope: from bootloaders and drivers up to the system and application layers — never "firmware only"

## Owner of the Company-Wide Bootloader Component (2007–2020)
- Owner of the bootloaders (U-Boot and VxWorks loaders) for all OneAccess / Ekinops product lines for 13 years
- About ten different boards as telecom technologies and processors evolved: from single-core MIPS to multiprocessor QorIQ and x86
- Porting to each new platform, firmware updates, secure boot, validation, support for the product teams
- Initial board programming (bootloaders and OS images) via JTAG

## Technical Leadership and Project Management
- Technical lead of a team of 4 engineers (in-house and offshore) on development and testing, from 2009 to 2012: task assignment and tracking, code reviews, technical trade-offs
- Led projects from requirements specification to acceptance, with effort estimation and planning — for example the xDSL dynamic firmware loading tool
- Managed the maintenance entrusted to a 3-person offshore team (2011-2013): driver updates, bootloader patches, corrective and evolutionary maintenance

## End-to-End Quality Loop on the Complete OS
- Development of low-level drivers and of system and application libraries
- Delivery of the functional tests for her components; contribution to the specification of integration and functional tests
- Non-regression tracking of the entire OS
- Drove the defect loop: trouble reports created automatically from test failures, tracked fixes, tests reinstated in non-regression
- Writing of functional specifications, architecture documents, test plans and compliance matrices (CMMI Level 3)

## Virtual Routers on x86 (2019–2020)
- Development of the virtual router OS: a complete routing solution running as a Debian Linux distribution in an x86 virtual machine
- System layers: logging, monitoring, memory management; userspace daemons and systemd services
- Application layers: CLI, software license management framework (complete specification, design and implementation)
- System monitoring delivered end to end: requirements specification, choice of the functions to monitor and of the relevant metrics, design, coding, testing, integration, and evaluation of the integration across the whole OS
- CI/CD with Jenkins: automated builds and integration tests, generation of production-ready images
- Languages: C and Python

## Gigabit VoIP Routers (2014–2017) — Freescale T1040, Yocto Linux
- Ethernet, SFP switch, memory, LED and power drivers
- Specifications, test plans, compliance matrices, integration tracking
- Yocto build system: BSP layers, BitBake recipes, cross-compilation toolchains, production image generation
- Shell and Perl scripts

## Gigabit Ethernet/IP Routers (2011–2013) — Freescale P1021, VxWorks
- Dual-core bootloader on the Freescale P1021 processor
- Design and implementation of a software defense and crash log system: exception stack extraction in PowerPC assembly, formatting of exception data for the crash log
- Supervision task on core 0 that detects and reports core 1 crashes, with the core 1 core dump integrated into the crash log
- Follow-up of the Wi-Fi, switch and fiber drivers
- UML modeling

## High-Performance xDSL Routers (2007–2011) — MIPS, PowerPC 83xx, VxWorks
- xDSL, ATM, serial and memory card drivers, bootloaders on MIPS and PowerPC processors
- ATM QoS: performance measurement and optimization on xDSL CPEs — tuning of the GCRA (Generic Cell Rate Algorithm), optimization of the SAR layer for AAL5 fragmentation, buffer allocation per service class (CBR, VBR, ABR), task scheduling for precise cell scheduling under load
- Correlation of CPE-side metrics (drops, memory pressure, CPU) with network-side QoS measurements to isolate software-induced degradations
- Interoperability with Alcatel DSLAMs

## xDSL Dynamic Firmware Loading Tool (2007–2011)
- Project lead for the automatic firmware loading tool for xDSL cards
- Wrote the requirements specification, the needs specification, the software design and the test plan before implementation — a concrete example of "documentation first" engineering
- Development of the CLI command for dynamic loading and of the production tools for firmware packaging
- Follow-up of the offshore team, compliance, evolutions and maintenance

## Other VxWorks Achievements (2007–2013)
- Optimization of the NAND Flash write algorithm for board programming: better block allocation, fewer unnecessary erase cycles, improved sequential write throughput — significant reduction of programming time in production
- Adaptation of BSPs to new hardware revisions
- Hardware debugging with Lauterbach Trace32, BDI2000, CodeWarrior, WindRiver Power ICE

## Embedded Linux — Cross-Cutting Skills (2007–2020)
- Yocto / OpenEmbedded, Debian
- Kernel: configuration, patches, device tree; kernel-space and user-space drivers
- U-Boot: porting and customization for several board revisions
- End-to-end bring-up of new platforms, from JTAG programming to system validation; BSP development
- Firmware updates, secure boot, CI/CD, code reviews, effort estimation, offshore coordination
- Writing of user guides for flashing tools, firmware programming utilities and debugging procedures

## Product Evolutions and Customer Support
- Handling of product evolution requests on system aspects, with the customer support of the operators (Orange, SFR, Telefonica)
- Help in writing PRQ (Product Requirement) documents
- Estimation of development, integration and testing effort; tracking of the development and integration of evolutions

## Technical Environment at OneAccess / Ekinops
C, C++, Python, Bash, Perl, Linux (Yocto, Debian), VxWorks, U-Boot, TCP/IP, UML/SDL, Git, SVN, Mercurial, Jenkins, Jira, Bugzilla.

## Internship — STMicroelectronics, Paris (July – December 2006)
- Final-year engineering internship of the Télécom Paris master's program (6 months)
- Development of an evaluation tool (Perl/Tk) for a database of thousands of intellectual property (IP) blocks intended for 3G mobile chipsets
- Research and definition of the criteria for an uncorrupted, well-designed IP free of manufacturing defects; implementation of these criteria as automated checks; production of evaluation reports
- Graphical interface in Perl/Tk, extraction methods in Shell and Perl scripts, writing of the user guide
- First experience of the approach that defines her: define the quality criteria, code them, apply them at scale, report

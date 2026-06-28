# Container versus virtual machine measurement

Do not fill the report with estimated values. Measure both systems on the same physical host, under the same workload, for at least 60 seconds.

## Procedure

1. Record host CPU model, RAM, operating system, Podman version, hypervisor, VM CPU/RAM allocation, and guest OS.
2. Start the Podman app and database. Let them become idle for two minutes.
3. Run `scripts/measure-container.ps1` to collect 12 samples at five-second intervals.
4. Generate a repeatable load, for example 100 requests with a concurrency of five, and repeat the measurement.
5. Deploy the same app and MySQL inside a VM. Record VM host CPU and memory from Hyper-V/VirtualBox/VMware plus process data inside the guest, first idle and then under the same request load.
6. Calculate average and peak CPU and memory. Attach raw CSV/screenshots and explain measurement limitations.

## Results table to complete

| Environment | Condition | Avg CPU | Peak CPU | Avg memory | Peak memory | Disk footprint | Startup time |
|---|---|---:|---:|---:|---:|---:|---:|
| Podman containers | Idle | TODO | TODO | TODO | TODO | TODO | TODO |
| Podman containers | Load | TODO | TODO | TODO | TODO | TODO | TODO |
| Virtual machine | Idle | TODO | TODO | TODO | TODO | TODO | TODO |
| Virtual machine | Load | TODO | TODO | TODO | TODO | TODO | TODO |

## Discussion prompts

- How much guest-OS overhead did the VM add?
- Did the VM's fixed allocation differ from actual working-set usage?
- Did CPU results change under load?
- Which system started faster and occupied less disk?
- What isolation advantage does a VM retain despite higher overhead?

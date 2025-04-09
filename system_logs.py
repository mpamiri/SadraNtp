import subprocess

def get_boot_log(max_lines=100):
    """
    Fetch the last max_lines lines of the Boot Log using journalctl.
    """
    try:
        result = subprocess.check_output(["journalctl", "-b", "-n", str(max_lines)], text=True)
        return result
    except Exception as e:
        return f"Error reading boot logs: {e}"

def get_dmesg_log(max_lines=100):
    """
    Fetch the last max_lines lines of the dmesg log.
    """
    try:
        result = subprocess.check_output(["dmesg", "--color=never", "--nopager"], text=True)
        lines = result.splitlines()
        return "\n".join(lines[-max_lines:])
    except Exception as e:
        return f"Error reading dmesg logs: {e}"

def get_system_logs():
    """
    Combine Boot Log and dmesg log into one string.
    """
    boot_log = get_boot_log(100)
    dmesg_log = get_dmesg_log(100)
    combined = (
        "=== Boot Log ===\n" + boot_log + "\n\n" +
        "=== Dmesg Log ===\n" + dmesg_log
    )
    return combined

# For testing independently:
if __name__ == "__main__":
    logs = get_system_logs()
    print("------ SYSTEM LOGS ------")
    print(logs)

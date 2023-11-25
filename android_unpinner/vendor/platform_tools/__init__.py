import logging
import subprocess
import sys
from pathlib import Path

here = Path(__file__).absolute().parent

if sys.platform == "win32":
    adb_binary = here / "win32" / "adb.exe"
elif sys.platform == "darwin":
    adb_binary = here / "darwin" / "adb"
else:
    adb_binary = here / "linux" / "adb"


def adb(cmd: str) -> subprocess.CompletedProcess[str]:
    """Helper function to call adb and capture stdout."""
    # Get a list of all connected devices
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
    devices = result.stdout.splitlines()[1:-1]  # Skip first and last line

    # Extract the serial numbers from the list
    serial_numbers = [line.split('\t')[0] for line in devices]

    # Choose a device to perform the operations on
    target_device = serial_numbers[0]

    cmd = f"{adb_binary} -s {target_device} {cmd}"
    try:
        proc = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logging.debug(f"cmd='{cmd}'\n"
                      f"{e.stdout=}\n"
                      f"{e.stderr=}")
        raise
    logging.debug(f"cmd='{cmd}'\n"
                  f"{proc.stdout=}\n"
                  f"{proc.stderr=}")
    return proc

import pytest
from os_service import fs, proc_mgr, get_system_status

def test_virtual_fs():
    # Test writing
    res = fs.write_file("/tmp/test.txt", "Hello World")
    assert "Successfully written" in res

    # Test reading
    content = fs.read_file("/tmp/test.txt")
    assert content == "Hello World"

    # Test listing
    files = fs.list_files("/tmp/")
    assert "/tmp/test.txt" in files

    # Test deletion
    del_res = fs.delete_file("/tmp/test.txt")
    assert "Successfully deleted" in del_res
    assert fs.read_file("/tmp/test.txt").startswith("Error")

def test_virtual_process_manager():
    # Test spawning
    pid = proc_mgr.spawn_process("test-worker", "Background AI task")
    assert pid >= 4

    # Test listing
    procs = proc_mgr.list_processes()
    assert pid in procs
    assert procs[pid]["name"] == "test-worker"

    # Test killing
    kill_res = proc_mgr.kill_process(pid)
    assert f"Process {pid}" in kill_res
    assert pid not in proc_mgr.list_processes()

def test_system_status():
    status = get_system_status()
    assert "kernel" in status
    assert "uptime" in status
    assert "memory" in status
    assert status["kernel"] == "v1.0.0-stable"

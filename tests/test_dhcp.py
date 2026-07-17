import pytest
import json
from unittest.mock import patch
from os_service import VirtualDHCPServer

def test_dhcp_server_unit_logic():
    server = VirtualDHCPServer()

    # 1. Test get_config
    config = server.get_config()
    assert config["start_ip"] == "192.168.1.100"
    assert config["end_ip"] == "192.168.1.200"

    # 2. Test configure
    res = server.configure(start_ip="10.0.0.100", end_ip="10.0.0.150")
    assert "updated successfully" in res
    new_config = server.get_config()
    assert new_config["start_ip"] == "10.0.0.100"
    assert new_config["end_ip"] == "10.0.0.150"

    # 3. Test list_leases
    leases = server.list_leases()
    assert isinstance(leases, dict)

    # 4. Test allocate_lease
    mac = "00:AA:BB:CC:DD:EE"
    hostname = "test-node"
    lease = server.allocate_lease(mac, hostname)
    assert lease["ip"] == "10.0.0.100"
    assert lease["hostname"] == hostname

    # 5. Test allocate_lease with specific requested IP
    mac2 = "11:22:33:44:55:66"
    lease2 = server.allocate_lease(mac2, "node-2", requested_ip="10.0.0.110")
    assert lease2["ip"] == "10.0.0.110"

    # 6. Test lease release
    release_res = server.release_lease(mac)
    assert "released successfully" in release_res
    assert mac not in server.list_leases()


def test_dhcp_assistance_endpoint_no_execute(client, auth_headers):
    with patch('google_ai.provide_os_dhcp_assistance') as mock_ai:
        mock_ai.return_value = "Mocked DHCP advice from AI"
        response = client.post('/api/v1/os/dhcp',
                               json={'prompt': 'How to set up a DHCP server?'},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['status'] == "success"
        assert response.json['message'] == "Mocked DHCP advice from AI"


def test_dhcp_assistance_endpoint_with_execute_allocate(client, auth_headers):
    # Simulate an allocation command extraction
    with patch('google_ai.provide_os_dhcp_assistance') as mock_ai:
        mock_ai.return_value = '{"action": "allocate", "mac": "22:33:44:55:66:77", "hostname": "exec-node"}'
        response = client.post('/api/v1/os/dhcp',
                               json={'prompt': 'allocate lease', 'execute': True},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['status'] == "success"

        # The result message should be a JSON string of the allocated lease
        allocated_lease = json.loads(response.json['message'])
        assert allocated_lease["hostname"] == "exec-node"
        assert "ip" in allocated_lease


def test_dhcp_assistance_endpoint_with_execute_list(client, auth_headers):
    with patch('google_ai.provide_os_dhcp_assistance') as mock_ai:
        mock_ai.return_value = '{"action": "list"}'
        response = client.post('/api/v1/os/dhcp',
                               json={'prompt': 'list leases', 'execute': True},
                               headers=auth_headers)
        assert response.status_code == 200
        assert response.json['status'] == "success"

        leases = json.loads(response.json['message'])
        assert isinstance(leases, dict)

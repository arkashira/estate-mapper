import pytest
from estate_mapper import collect_syslog_entries, parse_authentication_logs, identify_dormant_services, LogEntry
from datetime import datetime, timedelta

@pytest.fixture
def log_entries():
    return [
        LogEntry(datetime.now() - timedelta(days=1), "service1", "user1"),
        LogEntry(datetime.now() - timedelta(days=2), "service2", "user2"),
        LogEntry(datetime.now() - timedelta(days=30), "service3", "user3"),
    ]

def test_collect_syslog_entries(log_entries):
    collected_entries = collect_syslog_entries(30)
    assert len(collected_entries) == 3

def test_parse_authentication_logs(log_entries):
    active_users = parse_authentication_logs(log_entries)
    assert len(active_users) == 3
    assert "user1" in active_users
    assert "user2" in active_users
    assert "user3" in active_users

def test_identify_dormant_services(log_entries):
    dormant_services = identify_dormant_services(log_entries)
    assert len(dormant_services) == 1
    assert "service3" in dormant_services

def test_collect_syslog_entries_edge_case():
    collected_entries = collect_syslog_entries(0)
    assert len(collected_entries) == 0

def test_parse_authentication_logs_edge_case():
    log_entries = []
    active_users = parse_authentication_logs(log_entries)
    assert len(active_users) == 0

def test_identify_dormant_services_edge_case():
    log_entries = []
    dormant_services = identify_dormant_services(log_entries)
    assert len(dormant_services) == 0

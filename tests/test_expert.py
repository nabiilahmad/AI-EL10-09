import os

import pytest

from expert_system import diagnose
from search_algorithm import TransitNetwork

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "jaringan.json")


@pytest.fixture(scope="module")
def net():
    return TransitNetwork.from_json(DATA)


def test_direct_normal_is_lancar(net):
    d = diagnose(net, "pasar_barat", "bandara")
    assert d.status == "LANCAR" and "R7" in d.fired_rules and "R9" in d.fired_rules


def test_many_transfers_is_perhatian(net):
    d = diagnose(net, "pasar_barat", "bandara", {"pusat"})
    assert d.status == "PERHATIAN" and "R3" in d.fired_rules and "R4" in d.fired_rules


def test_long_trip_rule(net):
    assert "R5" in diagnose(net, "sekolah", "bandara").fired_rules


def test_rush_hour_rule(net):
    d = diagnose(net, "pasar_barat", "bandara", rush_hour=True)
    assert "R6" in d.fired_rules and d.status == "PERHATIAN"


def test_no_route_is_terganggu(net):
    d = diagnose(net, "bandara", "taman_kota", closed_lines={"biru"})
    assert d.status == "TERGANGGU" and "R2" in d.fired_rules


def test_closed_destination_is_terganggu(net):
    d = diagnose(net, "sekolah", "bandara", closed_stations={"bandara"})
    assert d.status == "TERGANGGU" and "R1" in d.fired_rules and "R2" not in d.fired_rules


def test_same_place(net):
    d = diagnose(net, "pusat", "pusat")
    assert d.status == "LANCAR" and "R8" in d.fired_rules


def test_route_text_mentions_transfer(net):
    d = diagnose(net, "sekolah", "bandara")
    assert any(t.startswith("Pindah ke") for t in d.route_text)


def test_unknown_inputs(net):
    with pytest.raises(KeyError):
        diagnose(net, "x", "bandara")
    with pytest.raises(KeyError):
        diagnose(net, "sekolah", "bandara", closed_lines={"ungu"})
    with pytest.raises(KeyError):
        diagnose(net, "sekolah", "bandara", algorithm="XYZ")

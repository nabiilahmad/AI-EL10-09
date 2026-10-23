import os

import pytest

from expert_system import diagnose
from search_algorithm import TransitNetwork

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "jaringan.json")


@pytest.fixture(scope="module")
def net():
    return TransitNetwork.from_json(DATA)


def test_dua_stasiun_tutup_memicu_r10(net):
    d = diagnose(net, "pasar_barat", "bandara", {"pusat", "mal_timur"})
    assert "R10" in d.fired_rules
    assert d.status == "PERHATIAN"


def test_satu_stasiun_tutup_tidak_memicu_r10(net):
    d = diagnose(net, "pasar_barat", "bandara", {"pusat"})
    assert "R10" not in d.fired_rules
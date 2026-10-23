import os

import pytest

from search_algorithm import ALGORITHMS, TransitNetwork, segments

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "jaringan.json")


@pytest.fixture(scope="module")
def net():
    return TransitNetwork.from_json(DATA)


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_path_valid(name, net):
    r = ALGORITHMS[name](net, "sekolah", "bandara")
    assert r.found
    assert r.path[0][0] == "sekolah" and r.path[-1][0] == "bandara"
    assert r.minutes == net.path_minutes(r.path)


def test_ucs_and_astar_same_minutes_everywhere(net):
    ids = list(net.stations)
    for a in ids:
        for b in ids:
            assert ALGORITHMS["UCS"](net, a, b).minutes == ALGORITHMS["A*"](net, a, b).minutes


def test_astar_expands_not_more_than_ucs(net):
    ids = list(net.stations)
    for a in ids:
        for b in ids:
            assert ALGORITHMS["A*"](net, a, b).expanded <= ALGORITHMS["UCS"](net, a, b).expanded


def test_ucs_never_slower_than_bfs(net):
    ids = list(net.stations)
    for a in ids:
        for b in ids:
            assert ALGORITHMS["UCS"](net, a, b).minutes <= ALGORITHMS["BFS"](net, a, b).minutes


def test_bfs_slower_example(net):
    assert ALGORITHMS["BFS"](net, "pusat", "stadion").minutes > ALGORITHMS["UCS"](net, "pusat", "stadion").minutes


def test_direct_route_has_no_transfer(net):
    r = ALGORITHMS["UCS"](net, "pasar_barat", "bandara")
    assert r.transfers == 0 and r.minutes == 27.0


def test_transfer_costs_time(net):
    r = ALGORITHMS["UCS"](net, "sekolah", "bandara")
    assert r.transfers == 1 and r.minutes == 41.0


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_closed_station_avoided(name, net):
    r = ALGORITHMS[name](net, "pasar_barat", "bandara", {"pusat"})
    assert r.found and all(s != "pusat" for s, _ in r.path)


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_closed_line_avoided(name, net):
    r = ALGORITHMS[name](net, "pasar_barat", "pelabuhan", (), {"kuning"})
    assert r.found and all(l != "kuning" for _, l in r.path)


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_no_route(name, net):
    assert not ALGORITHMS[name](net, "bandara", "taman_kota", (), {"biru"}).found
    assert not ALGORITHMS[name](net, "sekolah", "bandara", {"bandara"}).found
    assert not ALGORITHMS[name](net, "sekolah", "bandara", {"sekolah"}).found


def test_segments_group_by_line(net):
    r = ALGORITHMS["UCS"](net, "sekolah", "bandara")
    segs = segments(r.path)
    assert [l for l, _ in segs] == ["kuning", "biru"]
    assert segs[0][1][-1] == segs[1][1][0] == "pasar_barat"

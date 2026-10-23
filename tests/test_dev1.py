   import os

   import pytest

   from search_algorithm import ALGORITHMS, TransitNetwork

   DATA = os.path.join(os.path.dirname(__file__), "..", "data", "jaringan.json")


   @pytest.fixture(scope="module")
   def net():
       return TransitNetwork.from_json(DATA)


   @pytest.mark.parametrize("name", list(ALGORITHMS))
   def test_stadion_tutup_dihindari(net, name):
       r = ALGORITHMS[name](net, "kampus_timur", "pelabuhan", {"stadion"})
       assert r.found
       assert all(s != "stadion" for s, _ in r.path)


   def test_ucs_dan_astar_waktu_sama(net):
       ucs = ALGORITHMS["UCS"](net, "kampus_timur", "pelabuhan", {"stadion"})
       astar = ALGORITHMS["A*"](net, "kampus_timur", "pelabuhan", {"stadion"})
       assert ucs.minutes == astar.minutes == 25.0

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import recap


class TestRecapHelpers:
    def test_generate_recap(self):
        r = recap.generate_recap(365)
        assert "Recap: Last 365 Days" in r
        assert "Sessions:" in r or "Activity Summary" in r


class TestLoadFunctions:
    def test_load_recent_sessions(self):
        s = recap.load_recent_sessions(365)
        assert isinstance(s, list)
        if s:
            assert "skill" in s[0]

    def test_load_recent_decisions(self):
        d = recap.load_recent_decisions(365)
        assert isinstance(d, list)

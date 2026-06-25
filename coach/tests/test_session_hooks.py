import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import coach.tools.session_hooks as sh

# Force disable the stdin/stdout hack for test environments
import io
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class TestHooksHelpers:
    def test_pre_session_returns_list(self):
        result = sh.pre_session()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_read_checkpoint_summary(self):
        result = sh._read_checkpoint_summary()
        assert isinstance(result, list)

    def test_read_goals_summary(self):
        result = sh._read_goals_summary()
        assert result is None or "Goals" in result

    def test_read_habits_count(self):
        result = sh._read_habits_count()
        assert result is None or "Habits" in result

    def test_read_last_session_summary(self):
        result = sh._read_last_session_summary()
        assert result is None or "Last session" in result

    def test_read_recent_decisions(self):
        result = sh._read_recent_decisions()
        assert result is None or "Recent decisions" in result

    def test_top_insights(self):
        result = sh._top_insights(3)
        assert isinstance(result, list)

    def test_load_evolution_suggestions(self):
        result = sh._load_evolution_suggestions()
        assert isinstance(result, list)

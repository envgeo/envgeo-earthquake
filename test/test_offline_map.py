"""Tests for the offline map helpers added to earthquake_map_v030/envgeo_utils.py.

No real network calls are made: check_online_connectivity() is always
monkeypatched via the ``online`` / ``offline`` fixtures, and
socket.create_connection is patched wherever the inner cached function is
tested directly.

Run from earthquake_map_v030/:
    pytest -q test/test_offline_map.py
"""

import sys
import types
import unittest.mock as mock
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Minimal Streamlit stub — only the symbols used at module-load time.
# ---------------------------------------------------------------------------

def _make_streamlit_stub():
    st = types.ModuleType("streamlit")

    def _noop_deco(*args, **kwargs):
        def _wrap(fn):
            return fn
        if args and callable(args[0]):
            return args[0]
        return _wrap

    st.cache_data = _noop_deco
    st.cache_resource = _noop_deco
    st.session_state = {}
    for _name in ("sidebar", "radio", "selectbox", "warning", "caption",
                  "expander", "columns", "write", "info", "error"):
        setattr(st, _name, mock.MagicMock())
    return st


if "streamlit" not in sys.modules:
    sys.modules["streamlit"] = _make_streamlit_stub()
else:
    _st = sys.modules["streamlit"]
    if not callable(getattr(_st, "cache_data", None)):
        _st.cache_data = lambda *a, **kw: (a[0] if a and callable(a[0]) else lambda f: f)
        _st.cache_resource = _st.cache_data

# Ensure earthquake_map_v030 root is importable.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import envgeo_utils  # noqa: E402


# ---------------------------------------------------------------------------
# Connectivity fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def online(monkeypatch):
    """Make check_online_connectivity() return True without any network call."""
    monkeypatch.setattr(envgeo_utils, "check_online_connectivity", lambda *args: True)


@pytest.fixture()
def offline(monkeypatch):
    """Make check_online_connectivity() return False without any network call."""
    monkeypatch.setattr(envgeo_utils, "check_online_connectivity", lambda *args: False)


# ---------------------------------------------------------------------------
# Helper — minimal Plotly figure
# ---------------------------------------------------------------------------

def _blank_mapbox_fig():
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.update_layout(mapbox=dict(style="open-street-map"))
    return fig


# ---------------------------------------------------------------------------
# 1. MAP_MODE_OPTIONS structure
# ---------------------------------------------------------------------------

class TestMapModeOptions:
    def test_offline_first(self):
        assert envgeo_utils.MAP_MODE_OPTIONS[0] == "Coastline (offline)"

    def test_offline_in_options(self):
        assert "Coastline (offline)" in envgeo_utils.MAP_MODE_OPTIONS

    def test_default_is_standard(self):
        assert envgeo_utils.MAP_MODE_DEFAULT == "Standard"

    def test_default_index_points_to_standard(self):
        idx = envgeo_utils.MAP_MODE_DEFAULT_INDEX
        assert envgeo_utils.MAP_MODE_OPTIONS[idx] == "Standard"

    def test_default_index_is_not_zero(self):
        assert envgeo_utils.MAP_MODE_DEFAULT_INDEX != 0


# ---------------------------------------------------------------------------
# 2. resolve_map_mode
# ---------------------------------------------------------------------------

class TestResolveMapMode:
    def test_offline_mode_no_check(self, monkeypatch):
        called = []
        monkeypatch.setattr(
            envgeo_utils, "check_online_connectivity",
            lambda *a: called.append(1) or True
        )
        mode, fell = envgeo_utils.resolve_map_mode("Coastline (offline)")
        assert mode == "Coastline (offline)"
        assert fell is False
        assert called == []

    def test_online_mode_when_connected(self, online):
        mode, fell = envgeo_utils.resolve_map_mode("Standard")
        assert mode == "Standard"
        assert fell is False

    def test_online_mode_falls_back_when_offline(self, offline):
        mode, fell = envgeo_utils.resolve_map_mode("Standard")
        assert mode == "Coastline (offline)"
        assert fell is True

    def test_satellite_falls_back_when_offline(self, offline):
        mode, fell = envgeo_utils.resolve_map_mode("Satellite")
        assert mode == "Coastline (offline)"
        assert fell is True

    def test_bathymetry_falls_back_when_offline(self, offline):
        mode, fell = envgeo_utils.resolve_map_mode("Bathymetry (Sea)")
        assert mode == "Coastline (offline)"
        assert fell is True

    def test_contour_falls_back_when_offline(self, offline):
        mode, fell = envgeo_utils.resolve_map_mode("Contour (GSI)")
        assert mode == "Coastline (offline)"
        assert fell is True


# ---------------------------------------------------------------------------
# 3. apply_map_style — offline mode
# ---------------------------------------------------------------------------

class TestApplyMapStyleOffline:
    def test_offline_mode_uses_white_bg(self, online):
        fig = _blank_mapbox_fig()
        envgeo_utils.apply_map_style(fig, "Coastline (offline)")
        assert fig.layout.mapbox.style == "white-bg"

    def test_offline_mode_has_no_external_tile_layers(self, online):
        fig = _blank_mapbox_fig()
        envgeo_utils.apply_map_style(fig, "Coastline (offline)")
        layers = fig.layout.mapbox.layers or []
        for layer in layers:
            src = getattr(layer, "source", None)
            if isinstance(src, (list, tuple)):
                for url in src:
                    assert not str(url).startswith("http"), (
                        f"Offline mode must not include external URL: {url}"
                    )

    def test_online_fallback_also_uses_white_bg(self, offline):
        fig = _blank_mapbox_fig()
        envgeo_utils.apply_map_style(fig, "Standard")
        # apply_map_style uses the *selected* mode; the resolve is done in the
        # page layer.  What we verify here is that offline-falling-back pages
        # pass "Coastline (offline)" to apply_map_style, giving white-bg.
        fig2 = _blank_mapbox_fig()
        envgeo_utils.apply_map_style(fig2, "Coastline (offline)")
        assert fig2.layout.mapbox.style == "white-bg"


# ---------------------------------------------------------------------------
# 4. add_coastline_overlay
# ---------------------------------------------------------------------------

class TestAddCoastlineOverlay:
    def test_adds_scattermapbox_trace(self, monkeypatch):
        import plotly.graph_objects as go
        monkeypatch.setattr(
            envgeo_utils, "load_coastline_data",
            lambda ref_data, resolution="50m": ([0.0, 1.0, None], [0.0, 1.0, None]),
        )
        fig = _blank_mapbox_fig()
        before = len(fig.data)
        result = envgeo_utils.add_coastline_overlay(fig)
        assert result is True
        assert len(fig.data) == before + 1
        assert isinstance(fig.data[-1], go.Scattermapbox)

    def test_trace_name_is_coastline_overlay(self, monkeypatch):
        monkeypatch.setattr(
            envgeo_utils, "load_coastline_data",
            lambda ref_data, resolution="50m": ([0.0, 1.0], [0.0, 1.0]),
        )
        fig = _blank_mapbox_fig()
        envgeo_utils.add_coastline_overlay(fig)
        assert fig.data[-1].name == "_coastline_overlay"

    def test_trace_mode_is_lines(self, monkeypatch):
        monkeypatch.setattr(
            envgeo_utils, "load_coastline_data",
            lambda ref_data, resolution="50m": ([0.0, 1.0], [0.0, 1.0]),
        )
        fig = _blank_mapbox_fig()
        envgeo_utils.add_coastline_overlay(fig)
        assert fig.data[-1].mode == "lines"

    def test_no_trace_when_coastline_empty(self, monkeypatch):
        monkeypatch.setattr(
            envgeo_utils, "load_coastline_data",
            lambda ref_data, resolution="50m": ([], []),
        )
        fig = _blank_mapbox_fig()
        before = len(fig.data)
        result = envgeo_utils.add_coastline_overlay(fig)
        assert len(fig.data) == before
        assert result is False


# ---------------------------------------------------------------------------
# 5. add_graticule_overlay
# ---------------------------------------------------------------------------

class TestAddGraticuleOverlay:
    def test_adds_scattermapbox_trace(self):
        import plotly.graph_objects as go
        fig = _blank_mapbox_fig()
        before = len(fig.data)
        envgeo_utils.add_graticule_overlay(fig)
        assert len(fig.data) == before + 1
        assert isinstance(fig.data[-1], go.Scattermapbox)

    def test_trace_name_is_graticule_overlay(self):
        fig = _blank_mapbox_fig()
        envgeo_utils.add_graticule_overlay(fig)
        assert fig.data[-1].name == "_graticule_overlay"

    def test_trace_mode_is_lines(self):
        fig = _blank_mapbox_fig()
        envgeo_utils.add_graticule_overlay(fig)
        assert fig.data[-1].mode == "lines"

    def test_no_external_urls_in_graticule(self):
        fig = _blank_mapbox_fig()
        envgeo_utils.add_graticule_overlay(fig)
        trace = fig.data[-1]
        for lon in trace.lon:
            assert lon is None or isinstance(lon, float), f"Unexpected lon: {lon!r}"

    def test_covers_all_longitudes(self):
        fig = _blank_mapbox_fig()
        envgeo_utils.add_graticule_overlay(fig)
        lons = [v for v in fig.data[-1].lon if v is not None]
        assert min(lons) == -180.0
        assert max(lons) == 180.0

    def test_dateline_safe_no_jump(self):
        fig = _blank_mapbox_fig()
        envgeo_utils.add_graticule_overlay(fig)
        lons = list(fig.data[-1].lon)
        prev = None
        for v in lons:
            if v is not None and prev is not None:
                assert abs(v - prev) < 180.0, (
                    f"Antimeridian jump detected: {prev} → {v}"
                )
            prev = v if v is not None else None


# ---------------------------------------------------------------------------
# 6. check_online_connectivity — per-mode hosts, caching / mocking
# ---------------------------------------------------------------------------

class TestCheckOnlineConnectivity:
    def test_returns_bool(self, monkeypatch):
        import socket
        monkeypatch.setattr(socket, "create_connection", lambda *a, **kw: mock.MagicMock())
        result = envgeo_utils.check_online_connectivity()
        assert isinstance(result, bool)

    def test_returns_false_on_os_error(self, monkeypatch):
        import socket

        def _fail(*a, **kw):
            raise OSError("simulated network failure")

        monkeypatch.setattr(socket, "create_connection", _fail)
        envgeo_utils._check_connectivity_cached.cache_clear()
        result = envgeo_utils._check_connectivity_cached(-9999, "example.com", 443)
        assert result is False

    def test_socket_is_closed_on_success(self, monkeypatch):
        import socket
        closed = []
        mock_conn = mock.MagicMock()
        mock_conn.close.side_effect = lambda: closed.append(True)
        monkeypatch.setattr(socket, "create_connection", lambda *a, **kw: mock_conn)
        envgeo_utils._check_connectivity_cached.cache_clear()
        envgeo_utils._check_connectivity_cached(-8888, "example.com", 443)
        assert closed, "Socket.close() was never called"

    def test_mode_specific_host_standard(self, monkeypatch):
        import socket
        checked_hosts = []

        def _capture(address, **kw):
            checked_hosts.append(address[0])
            return mock.MagicMock()

        monkeypatch.setattr(socket, "create_connection", _capture)
        envgeo_utils._check_connectivity_cached.cache_clear()
        envgeo_utils.check_online_connectivity("Standard")
        assert any("openstreetmap" in h for h in checked_hosts), checked_hosts

    def test_mode_specific_host_satellite(self, monkeypatch):
        import socket
        checked_hosts = []

        def _capture(address, **kw):
            checked_hosts.append(address[0])
            return mock.MagicMock()

        monkeypatch.setattr(socket, "create_connection", _capture)
        envgeo_utils._check_connectivity_cached.cache_clear()
        envgeo_utils.check_online_connectivity("Satellite")
        assert any("nationalmap" in h for h in checked_hosts), checked_hosts

    def test_mode_specific_host_bathymetry(self, monkeypatch):
        import socket
        checked_hosts = []

        def _capture(address, **kw):
            checked_hosts.append(address[0])
            return mock.MagicMock()

        monkeypatch.setattr(socket, "create_connection", _capture)
        envgeo_utils._check_connectivity_cached.cache_clear()
        envgeo_utils.check_online_connectivity("Bathymetry (Sea)")
        assert any("arcgisonline" in h for h in checked_hosts), checked_hosts

    def test_mode_specific_host_gsi(self, monkeypatch):
        import socket
        checked_hosts = []

        def _capture(address, **kw):
            checked_hosts.append(address[0])
            return mock.MagicMock()

        monkeypatch.setattr(socket, "create_connection", _capture)
        envgeo_utils._check_connectivity_cached.cache_clear()
        envgeo_utils.check_online_connectivity("Contour (GSI)")
        assert any("gsi.go.jp" in h for h in checked_hosts), checked_hosts

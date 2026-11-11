"""
Tests for frontend component logic and import integrity.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_frontend_imports():
    """Verify frontend imports and dependencies load properly."""
    from frontend.app import show_product, main
    assert callable(show_product)
    assert callable(main)


def test_root_app_import():
    """Verify root app entry point can access frontend.app.main."""
    import app
    assert hasattr(app, "main")

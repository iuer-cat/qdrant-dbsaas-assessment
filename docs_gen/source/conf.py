project = "Qdrant DBaaS prototype"
copyright = "Albert Monfa"
author = "Albert Monfa"
version = "latest"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

autosummary_generate = True
autosummary_imported_members = True
autosummary_options = ["members"]


html_theme = "sphinx_rtd_theme"
html_show_sphinx = False

html_theme_options = {
    "display_version": False,
    "vcs_pageview_mode": "raw",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": True,
}

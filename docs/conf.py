import datetime
import os
import textwrap

# Configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.
#
# If you're new to Sphinx and don't want any advanced or custom features,
# just go through the items marked 'TODO'.
#
# A complete list of built-in Sphinx configuration values:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# The Sphinx Stack uses the Canonical Sphinx theme to keep all documentation
# consistent and on brand:
# https://github.com/canonical/canonical-sphinx

#######################
# Project information #
#######################

# Project name
# TODO: Update with the official name of your project or product (e.g., "Ubuntu Server")
project = "Robotics"

# Author name; used in the default copyright statement in the page footer
author = "Canonical Ltd."

# The year in the copyright statement
copyright = f"{datetime.date.today().year}"

# Sidebar documentation title
# To disable the title, set it to an empty string.
html_title = project + " documentation"

# Documentation website URL
ogp_site_url = os.environ.get("READTHEDOCS_CANONICAL_URL", "https://canonical-robotics.readthedocs-hosted.com/")

# Preview name of the documentation website
# TODO: To use a different name for the project in previews, update the next line.
ogp_site_name = project

# Preview image URL
# TODO: To customise the preview image, update the next line.
ogp_image = "https://assets.ubuntu.com/v1/cc828679-docs_illustration.svg"

# Product favicon; shown in bookmarks, browser tabs, etc.
# TODO: To customise the favicon, uncomment and update the next line.
# html_favicon = "_static/favicon.png"

# Dictionary of values to pass into the Sphinx context for all pages:
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context
html_context = {
    # Product page URL; can be different from product docs URL.
    "product_page": "ubuntu.com/robotics",
    # Your Discourse instance URL.
    "discourse": "https://discourse.ubuntu.com",
    # Your Mattermost channel URL.
    "mattermost": "https://chat.canonical.com/canonical/channels/documentation",
    # Your Matrix channel URL.
    "matrix": "https://matrix.to/#/#documentation:ubuntu.com",
    # Your documentation GitHub repository URL.
    "github_url": "https://github.com/canonical/robotics_documentation/",
    # Docs branch in the repo; used in links for viewing the source files.
    "repo_default_branch": "main",
    # Docs location in the repo; used in links for viewing the source files.
    "repo_folder": "/docs/",
    # Previous / Next buttons at the bottom of pages.
    "sequential_nav": "both",
    # Listing contributors on individual pages.
    "display_contributors": False,
    # Required for feedback button.
    "github_issues": "enabled",
    # Passes the top-level 'author' value to the theme.
    "author": author,
    # Documentation license information.
    "license": {
        "name": "CC-BY-SA-3.0",
        "url": "https://creativecommons.org/licenses/by-sa/3.0/",
    },
}

# TODO: To enable the edit button on pages, uncomment and change the link to a
# public repository on GitHub or Launchpad.
# html_theme_options = {
#     "source_edit_link": "https://github.com/canonical/robotics_documentation",
# }

# Project slug
# TODO: If your documentation is hosted on https://documentation.ubuntu.com/,
# uncomment and set to the RTD slug.
# slug = ""

#######################
# Sitemap configuration
#######################

# Use RTD canonical URL to ensure duplicate pages have a specific canonical URL.
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "https://canonical-robotics.readthedocs-hosted.com/")

# sphinx-sitemap uses html_baseurl to generate the full URL for each page.
sitemap_url_scheme = "{link}"

# Include `lastmod` dates in the sitemap.
sitemap_show_lastmod = True

# Pages excluded from the sitemap.
sitemap_excludes = [
    "404/",
    "genindex/",
    "search/",
]

################################
# Template and asset locations #
################################

html_static_path = ["_static"]
templates_path = ["_templates"]

#############
# Redirects #
#############

# Keep using the existing in-repo redirects mapping while remaining on
# sphinx-reredirects for this repository.
redirects = {
    # The migration from Discourse to ReadTheDocs stripped the 'docs/' prefix
    "docs/tutorials/": "../../tutorials/",
    "docs/tutorials/snapcraft/": "../../../tutorials/snapcraft/",
    "docs/tutorials/packaging-ros-application-as-snap/": "../../../tutorials/packaging-ros-application-as-snap/",
    "docs/tutorials/packaging-complex-robotics-software-with-snaps/": "../../../tutorials/packaging-complex-robotics-software-with-snaps/",
    "docs/tutorials/distribute-ros-apps-with-snap-store/": "../../../tutorials/distribute-ros-apps-with-snap-store/",
    "docs/tutorials/building-ros-snaps-with-content-sharing/": "../../../tutorials/building-ros-snaps-with-content-sharing/",
    "docs/tutorials/create-ubuntu-core-image-for-turtlebot3/": "../../../tutorials/create-ubuntu-core-image-for-turtlebot3/",
    "docs/tutorials/ubuntu-pro/ros-esm-intro/": "../../../../tutorials/ubuntu-pro/ros-esm-intro/",
    "docs/how-to-guides/": "../../how-to-guides/",
    "docs/how-to-guides/packaging/build-and-publish-snap-with-github-actions/": "../../../../how-to-guides/packaging/build-and-publish-snap-with-github-actions/",
    "docs/how-to-guides/packaging/migrate_from_docker_to_snap": "../../../../how-to-guides/packaging/migrate_from_docker_to_snap",
    "docs/how-to-guides/packaging/ros-2-shared-memory-in-snaps": "../../../../how-to-guides/packaging/ros-2-shared-memory-in-snaps",
    "docs/how-to-guides/packaging/ros-distributions-with-no-extensions/": "../../../../how-to-guides/packaging/ros-distributions-with-no-extensions/",
    "docs/how-to-guides/packaging/config-a-snap-pull-from-a-server.html": "../../../../how-to-guides/packaging/config-a-snap-pull-from-a-server.html",
    "docs/how-to-guides/packaging/config-a-snap-using-content-snap": "../../../../how-to-guides/packaging/config-a-snap-using-content-snap/",
    "docs/how-to-guides/packaging/config-a-snap-make-config-overwritable": "../../../../how-to-guides/packaging/config-a-snap-make-config-overwritable/",
    "docs/references/snapcraft/": "../../../references/snapcraft/",
    "docs/references/plugins/": "../../../references/plugins/",
    "docs/references/extensions/": "../../../references/extensions/",
    "docs/references/faq/": "../../../references/faq/",
    "docs/explanations/": "../../explanations/",
    "docs/explanations/ubuntu-core/": "../../../explanations/ubuntu-core/",
    "docs/explanations/security/securing-ros-robotic-platforms/": "../../../../explanations/security/securing-ros-robotic-platforms/",
    "docs/explanations/snaps/ros-architectures-with-snaps/": "../../../../explanations/snaps/ros-architectures-with-snaps/",
    "docs/explanations/snaps/identify-functionalities-and-apps-of-robotics-snap/": "../../../../explanations/snaps/identify-functionalities-and-apps-of-robotics-snap/",
    "docs/explanations/snaps/snap-configurations-and-hooks/": "../../../../explanations/snaps/snap-configurations-and-hooks/",
    "docs/explanations/snaps/snap-data-and-file-storage/": "../../../../explanations/snaps/snap-data-and-file-storage/",
    "docs/explanations/snaps/snap-environment-variables/": "../../../../explanations/snaps/snap-environment-variables/",
    "docs/explanations/snaps/application-orchestration/": "../../../../explanations/snaps/application-orchestration/",
    "docs/explanations/snaps/vcstool-and-rosinstall-file/": "../../../../explanations/snaps/vcstool-and-rosinstall-file/",
    "docs/explanations/snaps/debug-the-build-of-a-snap/": "../../../../explanations/snaps/debug-the-build-of-a-snap/",
    "docs/explanations/snaps/debug-a-snap-application/": "../../../../explanations/snaps/debug-a-snap-application/",
    "docs/explanations/iot-app-store/": "../../../../explanations/dedicated-snap-store/",
    # The snaps/core tutorials were moved to a subfolder
    "tutorials/snapcraft/": "../../tutorials/snaps-core/",
    "tutorials/packaging-ros-application-as-snap/": "../../tutorials/snaps-core/packaging-ros-application-as-snap/",
    "tutorials/packaging-complex-robotics-software-with-snaps/": "../../tutorials/snaps-core/packaging-complex-robotics-software-with-snaps/",
    "tutorials/distribute-ros-apps-with-snap-store/": "../../tutorials/snaps-core/distribute-ros-apps-with-snap-store/",
    "tutorials/building-ros-snaps-with-content-sharing/": "../../tutorials/snaps-core/building-ros-snaps-with-content-sharing/",
    "tutorials/create-ubuntu-core-image-for-turtlebot3/": "../../tutorials/snaps-core/create-ubuntu-core-image-for-turtlebot3/",
    # These intermediate pages were removed
    "tutorials/ubuntu-pro/": "../../tutorials/ubuntu-pro/ros-esm-intro/",
    "explanations/iot-app-store/": "../../explanations/dedicated-snap-store/",
    # The snapcraft references were moved to a subfolder
    "references/plugins/": "../../references/snapcraft/plugins/",
    "references/extensions/": "../../references/snapcraft/extensions/",
    # The unique ESM tutorial was broken down into how-tos & explanations
    "tutorials/ubuntu-pro/ros-esm-intro/": "../../../explanations/security/what-is-ros-esm/",
    "explanations/security/securing-ros-robotic-platforms/": "../../../how-to-guides/security/hardening-your-robot/",
    "explanations/security/hardening-your-robot/": "../../../how-to-guides/security/hardening-your-robot/",
}

############################
# sphinx-llm configuration #
############################

llms_txt_description = textwrap.dedent(
    """\
    This is the documentation for the Canonical Robotics stack, including packaging and
    deployment with snaps, observability with COS for Robotics, and security maintenance
    with ROS ESM.
    """
)

# The base URL for references built by sphinx-markdown-builder.
if os.environ.get("READTHEDOCS"):
    markdown_http_base = html_baseurl

###########################
# Link checker exceptions #
###########################

linkcheck_ignore = [
    "http://127.0.0.1:8000",
    "https://github.com/canonical/ACME/*",
    r"https://developer\.hashicorp\.com/terraform.*",
    "https://linux.die.net/man/1/curl",
    "https://ubuntu.com/robotics/ros-esm#get-in-touch",
    "https://ubuntu.com/core/features/secure-boot#get-in-touch",
    "https://ubuntu.com/robotics#get-in-touch",
    "https://canonical-juju.readthedocs-hosted.com/en/latest/user/explanation/kubernetes-in-juju/",
    "https://snapcraft.io/docs/catkin-*",
]

linkcheck_anchors_ignore_for_url = [
    r"https://github\.com/.*",
    r"https://snapcraft.io/docs/.*",
    r"https://ubuntu.com/robotics#get-in-touch",
    r"https://ubuntu.com/robotics/ros-esm#get-in-touch",
    r"https://ubuntu.com/core/features/secure-boot#get-in-touch",
]

# Give linkcheck multiple tries on transient failure.
linkcheck_retries = 3

# Reduce parallelism to avoid remote rate limits/connection resets in CI.
linkcheck_workers = 1

########################
# Configuration extras #
########################

# Custom Sphinx extensions.
extensions = [
    "canonical_sphinx",
    "notfound.extension",
    "sphinx_design",
    "sphinx_reredirects",
    "sphinx_tabs.tabs",
    "sphinxcontrib.jquery",
    "sphinxext.opengraph",
    "sphinx_config_options",
    "sphinx_contributor_listing",
    "sphinx_filtered_toctree",
    "sphinx_llm.txt",
    "sphinx_related_links",
    "sphinx_roles",
    "sphinx_terminal",
    "sphinx_ubuntu_images",
    "sphinx_youtube_links",
    "sphinxcontrib.cairosvgconverter",
    "sphinx_last_updated_by_git",
    "sphinx.ext.intersphinx",
    "sphinx_sitemap",
    "sphinxcontrib.mermaid",
]

exclude_patterns = ["doc-cheat-sheet*", ".venv*", "content"]

# Additional CSS and JavaScript.
html_css_files = [
    "cookie-banner.css",
]
html_js_files = [
    "bundle.js",
]

rst_epilog = """
.. include:: /reuse/links.txt
"""

rst_prolog = """
.. role:: center
   :class: align-center
.. role:: h2
   :class: hclass2
.. role:: woke-ignore
   :class: woke-ignore
.. role:: vale-ignore
   :class: vale-ignore

"""

# Workaround for https://github.com/canonical/canonical-sphinx/issues/34
if "discourse_prefix" not in html_context and "discourse" in html_context:
    html_context["discourse_prefix"] = html_context["discourse"] + "/t/"

myst_heading_anchors = 2
myst_substitutions = {"COS_ROB": "COS for robotics", "COS": "COS Lite"}

# Mermaid theming is still handled in individual diagrams for this repo.
# mermaid_init_js = "mermaid.initialize({startOnLoad:false,theme:'dark'});"
# mermaid_params = ["--theme", "dark"]

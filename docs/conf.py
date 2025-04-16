import ast
import datetime

# Configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.
#
# If you're new to Sphinx and don't want any advanced or custom features,
# just go through the items marked 'TODO'.
#
# A complete list of built-in Sphinx configuration values:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Our starter pack uses the custom Canonical Sphinx extension
# to keep all documentation based on it consistent and on brand:
# https://github.com/canonical/canonical-sphinx


#######################
# Project information #
#######################

# Project name
#
# TODO: Update with the official name of your project or product

project = "Robotics"
author = "Canonical Ltd."


# Sidebar documentation title; best kept reasonably short
#
# TODO: To include a version number, add it here (hardcoded or automated).
#
# TODO: To disable the title, set to an empty string.

html_title = project + " documentation"


# Copyright string; shown at the bottom of the page
#
# Now, the starter pack uses CC-BY-SA as the license
# and the current year as the copyright year.
#
# TODO: If your docs need another license, specify it instead of 'CC-BY-SA'.
#
# TODO: If your documentation is a part of the code repository of your project,
#       it inherits the code license instead; specify it instead of 'CC-BY-SA'.
#
# NOTE: For static works, it is common to provide the first publication year.
#       Another option is to provide both the first year of publication
#       and the current year, especially for docs that frequently change,
#       e.g. 2022–2023 (note the en-dash).
#
#       A way to check a repo's creation date is to get a classic GitHub token
#       with 'repo' permissions; see https://github.com/settings/tokens
#       Next, use 'curl' and 'jq' to extract the date from the API's output:
#
#       curl -H 'Authorization: token <TOKEN>' \
#         -H 'Accept: application/vnd.github.v3.raw' \
#         https://api.github.com/repos/canonical/<REPO> | jq '.created_at'

copyright = "%s CC-BY-SA, %s" % (datetime.date.today().year, author)


# Documentation website URL
#
# TODO: Update with the official URL of your docs or leave empty if unsure.
#
# NOTE: The Open Graph Protocol (OGP) enhances page display in a social graph
#       and is used by social media platforms; see https://ogp.me/

ogp_site_url = "https://canonical-robotics.readthedocs-hosted.com/"


# Preview name of the documentation website
#
# TODO: To use a different name for the project in previews, update as needed.

ogp_site_name = project


# Preview image URL
#
# TODO: To customise the preview image, update as needed.

ogp_image = "https://assets.ubuntu.com/v1/253da317-image-document-ubuntudocs.svg"


# Product favicon; shown in bookmarks, browser tabs, etc.

# TODO: To customise the favicon, uncomment and update as needed.

# html_favicon = '.sphinx/_static/favicon.png'


# Dictionary of values to pass into the Sphinx context for all pages:
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context

html_context = {
    # Product page URL; can be different from product docs URL
    #
    # TODO: Change to your product website URL,
    #       dropping the 'https://' prefix, e.g. 'ubuntu.com/lxd'.
    #
    # TODO: If there's no such website,
    #       remove the {{ product_page }} link from the page header template
    #       (usually .sphinx/_templates/header.html; also, see README.rst).
    "product_page": "ubuntu.com/robotics",
    # Product tag image; the orange part of your logo, shown in the page header
    #
    # TODO: To add a tag image, uncomment and update as needed.
    # 'product_tag': '_static/tag.png',
    # Your Discourse instance URL
    #
    # TODO: Change to your Discourse instance URL or leave empty.
    #
    # NOTE: If set, adding ':discourse: 123' to an .rst file
    #       will add a link to Discourse topic 123 at the bottom of the page.
    "discourse": "https://discourse.ubuntu.com",
    # Your Mattermost channel URL
    #
    # TODO: Change to your Mattermost channel URL or leave empty.
    "mattermost": "https://chat.canonical.com/canonical/channels/documentation",
    # Your Matrix channel URL
    #
    # TODO: Change to your Matrix channel URL or leave empty.
    "matrix": "https://matrix.to/#/#documentation:ubuntu.com",
    # Your documentation GitHub repository URL
    #
    # TODO: Change to your documentation GitHub repository URL or leave empty.
    #
    # NOTE: If set, links for viewing the documentation source files
    #       and creating GitHub issues are added at the bottom of each page.
    "github_url": "https://github.com/canonical/sphinx-docs-starter-pack",
    # Docs branch in the repo; used in links for viewing the source files
    #
    # TODO: To customise the branch, uncomment and update as needed.
    "repo_default_branch": "main",
    # Docs location in the repo; used in links for viewing the source files
    #
    # TODO: To customise the directory, uncomment and update as needed.
    "repo_folder": "/docs/",
    # TODO: To enable or disable the Previous / Next buttons at the bottom of pages
    # Valid options: none, prev, next, both
    "sequential_nav": "both",
    # TODO: To enable listing contributors on individual pages, set to True
    "display_contributors": False,
    # Required for feedback button
    "github_issues": "enabled",
}

# TODO: To enable the edit button on pages, uncomment and change the link to a
# public repository on GitHub or Launchpad. Any of the following link domains
# are accepted:
# - https://github.com/example-org/example"
# - https://launchpad.net/example
# - https://git.launchpad.net/example
#
# html_theme_options = {
# 'source_edit_link': 'https://github.com/canonical/sphinx-docs-starter-pack',
# }

# Project slug; see https://meta.discourse.org/t/what-is-category-slug/87897
#
# TODO: If your documentation is hosted on https://docs.ubuntu.com/,
#       uncomment and update as needed.

# slug = ''


# Template and asset locations

# html_static_path = [".sphinx/_static"]
# templates_path = [".sphinx/_templates"]


#############
# Redirects #
#############

# To set up redirects: https://documatt.gitlab.io/sphinx-reredirects/usage.html
# For example: 'explanation/old-name.html': '../how-to/prettify.html',

# To set up redirects in the Read the Docs project dashboard:
# https://docs.readthedocs.io/en/stable/guides/redirects.html

# NOTE: If undefined, set to None, or empty,
#       the sphinx_reredirects extension will be disabled.

redirects = {
    "docs/tutorials/": "/tutorials/",
    "docs/tutorials/snapcraft/#": "/tutorials/snapcraft/#",
    "docs/tutorials/packaging-ros-application-as-snap/": "/tutorials/packaging-ros-application-as-snap/",
    "docs/tutorials/packaging-complex-robotics-software-with-snaps/": "/tutorials/packaging-complex-robotics-software-with-snaps/",
    "docs/tutorials/distribute-ros-apps-with-snap-store/": "/tutorials/distribute-ros-apps-with-snap-store/",
    "docs/tutorials/building-ros-snaps-with-content-sharing/": "/tutorials/building-ros-snaps-with-content-sharing/",
    "docs/tutorials/create-ubuntu-core-image-for-turtlebot3/": "/tutorials/create-ubuntu-core-image-for-turtlebot3/",
    "docs/tutorials/ubuntu-pro/ros-esm-intro/": "/tutorials/ubuntu-pro/ros-esm-intro/",
    "docs/how-to-guides/": "/how-to-guides/",
    "docs/how-to-guides/packaging/build-and-publish-snap-with-github-actions/": "/how-to-guides/packaging/build-and-publish-snap-with-github-actions/",
    "docs/how-to-guides/packaging/migrate_from_docker_to_snap": "how-to-guides/packaging/migrate_from_docker_to_snap",
    "docs/how-to-guides/packaging/ros-2-shared-memory-in-snaps": "../how-to-guides/packaging/ros-2-shared-memory-in-snaps",
    "docs/how-to-guides/packaging/ros-distributions-with-no-extensions/": "../how-to-guides/packaging/ros-distributions-with-no-extensions/",
    "docs/how-to-guides/packaging/config-a-snap-pull-from-a-server.html": "../how-to-guides/packaging/config-a-snap-pull-from-a-server.html",
    "docs/how-to-guides/packaging/config-a-snap-using-content-snap": "../../../how-to-guides/packaging/config-a-snap-using-content-snap/",
    "docs/how-to-guides/packaging/config-a-snap-make-config-overwritable": "../../how-to-guides/packaging/config-a-snap-make-config-overwritable/",
    "docs/references/snapcraft/": "/references/snapcraft/",
    "docs/references/plugins/": "/references/plugins/",
    "docs/references/extensions/": "/references/extensions/",
    "docs/references/faq/": "/references/faq/",
    "docs/explanations/": "/explanations/",
    "docs/explanations/ubuntu-core/": "/explanations/ubuntu-core/",
    "docs/explanations/security/securing-ros-robotic-platforms/": "/explanations/security/securing-ros-robotic-platforms/",
    "docs/explanations/snaps/ros-architectures-with-snaps/": "/explanations/snaps/ros-architectures-with-snaps/",
    "docs/explanations/snaps/identify-functionalities-and-apps-of-robotics-snap/": "/explanations/snaps/identify-functionalities-and-apps-of-robotics-snap/",
    "docs/explanations/snaps/snap-configurations-and-hooks/": "/explanations/snaps/snap-configurations-and-hooks/",
    "docs/explanations/snaps/snap-data-and-file-storage/": "/explanations/snaps/snap-data-and-file-storage/",
    "docs/explanations/snaps/snap-environment-variables/": "/explanations/snaps/snap-environment-variables/",
    "docs/explanations/snaps/application-orchestration/": "/explanations/snaps/application-orchestration/",
    "docs/explanations/snaps/vcstool-and-rosinstall-file/": "/explanations/snaps/vcstool-and-rosinstall-file/",
    "docs/explanations/snaps/debug-the-build-of-a-snap/": "/explanations/snaps/debug-the-build-of-a-snap/",
    "docs/explanations/snaps/debug-a-snap-application/": "/explanations/snaps/debug-a-snap-application/",
    "docs/explanations/iot-app-store/": "/explanations/iot-app-store/",
}


###########################
# Link checker exceptions #
###########################

# A regex list of URLs that are ignored by 'make linkcheck'
#
# TODO: Remove or adjust the ACME entry after you update the contributing guide

linkcheck_ignore = [
    "http://127.0.0.1:8000",
    "https://github.com/canonical/ACME/*",
    "https://linux.die.net/man/1/curl",
    "https://ubuntu.com/robotics/ros-esm#get-in-touch",
    "https://ubuntu.com/core/features/secure-boot#get-in-touch",
    "https://ubuntu.com/robotics#get-in-touch",
    "https://canonical-juju.readthedocs-hosted.com/en/latest/user/explanation/kubernetes-in-juju/",
]


# A regex list of URLs where anchors are ignored by 'make linkcheck'

linkcheck_anchors_ignore_for_url = [
    r"https://github\.com/.*",
    r"https://snapcraft.io/docs/.*",
    r"https://ubuntu.com/robotics#get-in-touch",
    r"https://ubuntu.com/robotics/ros-esm#get-in-touch",
    r"https://ubuntu.com/core/features/secure-boot#get-in-touch",
]

# give linkcheck multiple tries on failure
# linkcheck_timeout = 30
linkcheck_retries = 3

########################
# Configuration extras #
########################

# Custom MyST syntax extensions; see
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
#
# NOTE: By default, the following MyST extensions are enabled:
#       substitution, deflist, linkify

# myst_enable_extensions = set()


# Custom Sphinx extensions; see
# https://www.sphinx-doc.org/en/master/usage/extensions/index.html

# NOTE: The canonical_sphinx extension is required for the starter pack.
#       It automatically enables the following extensions:
#       - custom-rst-roles
#       - myst_parser
#       - notfound.extension
#       - related-links
#       - sphinx_copybutton
#       - sphinx_design
#       - sphinx_reredirects
#       - sphinx_tabs.tabs
#       - sphinxcontrib.jquery
#       - sphinxext.opengraph
#       - terminal-output
#       - youtube-links

extensions = [
    "canonical_sphinx",
    "sphinxcontrib.cairosvgconverter",
    "sphinx_last_updated_by_git",
]

# Excludes files or directories from processing

exclude_patterns = ["doc-cheat-sheet*", "content"]

# Adds custom CSS files, located under 'html_static_path'

# html_css_files = []


# Adds custom JavaScript files, located under 'html_static_path'

# html_js_files = []


# Specifies a reST snippet to be appended to each .rst file

rst_epilog = """
.. include:: /reuse/links.txt
"""

# Feedback button at the top; enabled by default
#
# TODO: To disable the button, uncomment this.

# disable_feedback_button = True


# Your manpage URL
#
# TODO: To enable manpage links, uncomment and replace {codename} with required
#       release, preferably an LTS release (e.g. noble). Do *not* substitute
#       {section} or {page}; these will be replaced by sphinx at build time
#
# NOTE: If set, adding ':manpage:' to an .rst file
#       adds a link to the corresponding man section at the bottom of the page.

# manpages_url = 'https://manpages.ubuntu.com/manpages/{codename}/en/' + \
#     'man{section}/{page}.{section}.html'


# Specifies a reST snippet to be prepended to each .rst file
# This defines a :center: role that centers table cell content.
# This defines a :h2: role that styles content for use with PDF generation.

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

myst_substitutions = {"COS_ROB": "COS for robotics"}

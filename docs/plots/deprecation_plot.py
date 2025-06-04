from pylab import *
from operator import attrgetter
from copy import deepcopy
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable
from importlib.metadata import PackageNotFoundError
import warnings

from linkml.utils.deprecation import DEPRECATIONS, SemVer, Deprecation

theme = {
    "bg": "#202020",
    "primary": "#cccccc",
    "good": "#6ebf26",
    "bad": "#ee5151"
}

# collect all versions to use as X axis
try:
    current_version = SemVer.from_package('linkml')
except PackageNotFoundError:
    current_version = SemVer.from_str('0.0.0')

# --------------------------------------------------
# Sort and extract data
# --------------------------------------------------

def sort_deps():
    deps = list(deepcopy(DEPRECATIONS))
    deps = sorted(deps, key=attrgetter('deprecated_in'))
    return deps


def sort_versions(deps):
    versions = [current_version]
    for dep in deps:
        versions.append(dep.deprecated_in)
        if dep.removed_in is not None:
            versions.append(dep.removed_in)
    versions = sorted(versions)
    return versions

# --------------------------------------------------
# Collect data for graph elements
# --------------------------------------------------
def make_plot_data(versions, deps):

    versions = list(dict.fromkeys([str(v) for v in versions]))
    versions_idx = {i:v for i, v in enumerate(versions)}
    idx_versions = {v:k for k,v in versions_idx.items()}

    # make lines for each deprecation with a deprecated_in and completed_in spec
    labels = []
    starts = []
    ends = []
    colors = []

    points_x = []
    points_labels = []
    points_colors = []
    for d in deps:
        if d.removed_in is not None:
            labels.append(d.name)
            starts.append(idx_versions[str(d.deprecated_in)])
            ends.append(idx_versions[str(d.removed_in)])
            if d.removed:
                colors.append('gray')
            elif d.deprecated:
                colors.append(theme['bad'])
            else:
                colors.append(theme['good'])
        else:
            points_labels.append(d.name)
            points_x.append(idx_versions[str(d.deprecated_in)])
            if d.deprecated:
                points_colors.append('gray')
            else:
                points_colors.append(theme['good'])

    return labels, starts, ends, colors, points_x, points_labels, points_colors, versions_idx, idx_versions





# --------------------------------------------------
# Make graph elements
# --------------------------------------------------
def plot(deps, labels, starts, ends, colors, points_x, points_labels, points_colors, idx_versions, versions_idx):
    # plt.subplots(layout="constrained")
    fig = plt.figure(figsize=(15,len(deps)+2)) # type: plt.Figure
    ax = fig.add_subplot(111) # type: plt.Axes

    ax.hlines(labels, starts, ends, colors, linewidths=10)
    ax.scatter(points_x, points_labels, marker='D', color=points_colors, s=200)

    # line for current version
    cur_line = ax.axvline(idx_versions[str(current_version)], color=theme['primary'])
    ax.annotate("Current version",
                (0,1.1), xycoords=cur_line,
                horizontalalignment="center",
                fontsize=20,
                c=theme['primary']
                #(idx_versions[str(current_version)], len(deps)),
                )

    ax.set_xticks(list(versions_idx.keys()), labels=list(versions_idx.values()))
    return fig, ax

# --------------------------------------------------
# Combine and style
# --------------------------------------------------

def style_plot(fig, ax, theme):
    # style plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    fig.set_facecolor(theme['bg'])
    ax.set_facecolor(theme['bg'])
    ax.tick_params(axis="x", colors=theme['primary'], labelsize=20, width=2, length=10, pad=10)
    ax.tick_params(axis="y", colors=theme['primary'], labelsize=20)
    make_axes_area_auto_adjustable(ax)
    return fig, ax


def main():
    deps = sort_deps()
    versions = sort_versions(deps)

    # worse return signature ever
    labels, starts, ends, colors, points_x, points_labels, points_colors, versions_idx, idx_versions = make_plot_data(versions, deps)

    fig, ax = plot(deps, labels, starts, ends, colors, points_x, points_labels, points_colors, idx_versions, versions_idx)
    fig, ax = style_plot(fig, ax, theme)
    show()

try:
    main()
except Exception as e:
    warnings.warn('Could not plot deprecations!\n' + str(e))

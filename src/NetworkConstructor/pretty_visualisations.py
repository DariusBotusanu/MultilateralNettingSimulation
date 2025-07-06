import os
import sys
from pathlib import Path

PACKAGE_PATH = Path(os.path.abspath(__file__)).parent
SOURCE_PATH = PACKAGE_PATH.parent

sys.path.append(str(SOURCE_PATH))

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Circle


def create_beautiful_visualization(G, style="modern", save_path=None):
    """
    Create aesthetically pleasing network visualizations with different styles

    Styles:
    - 'modern': Clean, minimalist with gradient edges
    - 'neon': Dark background with glowing edges
    - 'watercolor': Soft, artistic style
    - 'tech': Futuristic tech company style
    - 'finance': Professional financial sector style
    """

    # Style configurations
    styles = {
        "modern": {
            "bg_color": "#FFFFFF",
            "fig_facecolor": "#FAFAFA",
            "edge_cmap": "viridis",
            "node_edge_color": "#333333",
            "node_edge_width": 0.5,
            "edge_alpha": 0.6,
            "font_color": "#2C3E50",
            "title_color": "#2C3E50",
            "glow": False,
        },
        "neon": {
            "bg_color": "#0A0A0A",
            "fig_facecolor": "#0F0F0F",
            "edge_cmap": "plasma",
            "node_edge_color": "#FFFFFF",
            "node_edge_width": 2,
            "edge_alpha": 0.8,
            "font_color": "#FFFFFF",
            "title_color": "#00FFFF",
            "glow": True,
        },
        "watercolor": {
            "bg_color": "#FFF8F0",
            "fig_facecolor": "#FFFAF5",
            "edge_cmap": "RdYlBu",
            "node_edge_color": "#8B7355",
            "node_edge_width": 0.3,
            "edge_alpha": 0.4,
            "font_color": "#5D4E37",
            "title_color": "#5D4E37",
            "glow": False,
        },
        "tech": {
            "bg_color": "#1A1A2E",
            "fig_facecolor": "#16213E",
            "edge_cmap": "cool",
            "node_edge_color": "#0F4C75",
            "node_edge_width": 1.5,
            "edge_alpha": 0.7,
            "font_color": "#EAEAEA",
            "title_color": "#00D9FF",
            "glow": True,
        },
        "finance": {
            "bg_color": "#F5F5F5",
            "fig_facecolor": "#FFFFFF",
            "edge_cmap": "RdBu",
            "node_edge_color": "#2C3E50",
            "node_edge_width": 1,
            "edge_alpha": 0.5,
            "font_color": "#34495E",
            "title_color": "#2C3E50",
            "glow": False,
        },
    }

    # Get style configuration
    config = styles.get(style, styles["modern"])

    # Create figure with style
    fig, ax = plt.subplots(figsize=(20, 16), facecolor=config["fig_facecolor"])
    ax.set_facecolor(config["bg_color"])

    # Enhanced color palettes for sectors
    sector_palettes = {
        "modern": {
            "manufacturing": "#E74C3C",
            "retail": "#3498DB",
            "technology": "#9B59B6",
            "financial": "#1ABC9C",
            "energy": "#F39C12",
            "healthcare": "#2ECC71",
            "telecommunications": "#E67E22",
            "transportation": "#34495E",
            "real_estate": "#16A085",
            "agriculture": "#27AE60",
            "materials": "#D35400",
            "services": "#8E44AD",
        },
        "neon": {
            "manufacturing": "#FF006E",
            "retail": "#00F5FF",
            "technology": "#FF00FF",
            "financial": "#00FF00",
            "energy": "#FFFF00",
            "healthcare": "#00FFAA",
            "telecommunications": "#FF8C00",
            "transportation": "#FF1493",
            "real_estate": "#00CED1",
            "agriculture": "#32CD32",
            "materials": "#FF4500",
            "services": "#DA70D6",
        },
    }

    # Select color palette based on style
    if style == "neon":
        sector_colors = sector_palettes["neon"]
    else:
        sector_colors = sector_palettes["modern"]

    # Calculate metrics for visual enhancements
    degree_centrality = nx.degree_centrality(G)
    edge_betweenness = nx.edge_betweenness_centrality(G) if len(G.edges()) < 500 else {}

    # Create layout with improved algorithms
    if len(G.nodes()) < 50:
        pos = nx.kamada_kawai_layout(G, weight="amount")
    else:
        pos = nx.spring_layout(
            G, k=3 / np.sqrt(len(G.nodes())), iterations=100, weight="amount"
        )

    # Apply force-directed adjustments for better spacing
    pos = adjust_layout_spacing(pos, min_distance=0.15)

    # Calculate node sizes with better scaling
    node_sizes = calculate_node_sizes(G, base_size=300, max_size=3000)

    # Draw edges with gradients and curves
    draw_beautiful_edges(G, pos, ax, config, edge_betweenness)

    # Draw nodes with effects
    draw_beautiful_nodes(
        G, pos, ax, node_sizes, sector_colors, config, degree_centrality
    )

    # Add labels with smart positioning
    add_smart_labels(G, pos, ax, config, degree_centrality)

    # Add decorative elements
    if style in ["modern", "finance"]:
        add_grid_lines(ax, config)

    # Add title and legend
    add_title_and_legend(ax, G, sector_colors, config, style)

    # Remove axes
    ax.set_xlim(
        min(x for x, y in pos.values()) - 0.5, max(x for x, y in pos.values()) + 0.5
    )
    ax.set_ylim(
        min(y for x, y in pos.values()) - 0.5, max(y for x, y in pos.values()) + 0.5
    )
    ax.axis("off")

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path, dpi=300, bbox_inches="tight", facecolor=config["fig_facecolor"]
        )
        print(f"Saved beautiful visualization to {save_path}")

    return fig, ax


def adjust_layout_spacing(pos, min_distance=0.1):
    """Adjust node positions to ensure minimum spacing"""
    adjusted_pos = pos.copy()
    nodes = list(pos.keys())

    for _ in range(10):  # Multiple iterations for better results
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i + 1 :]:
                x1, y1 = adjusted_pos[node1]
                x2, y2 = adjusted_pos[node2]

                dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                if dist < min_distance and dist > 0:
                    # Push nodes apart
                    dx = x2 - x1
                    dy = y2 - y1

                    factor = (min_distance - dist) / (2 * dist)

                    adjusted_pos[node1] = (x1 - dx * factor, y1 - dy * factor)
                    adjusted_pos[node2] = (x2 + dx * factor, y2 + dy * factor)

    return adjusted_pos


def calculate_node_sizes(G, base_size=300, max_size=3000):
    """Calculate node sizes based on importance metrics"""
    node_sizes = {}

    # Calculate combined importance score
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())

    for node in G.nodes():
        # Consider both degree and debt amount
        total_debt = 0
        for _, _, d in G.in_edges(node, data=True):
            total_debt += d.get("amount", 0)
        for _, _, d in G.out_edges(node, data=True):
            total_debt += d.get("amount", 0)

        # Normalize and combine metrics
        degree_score = (in_degree[node] + out_degree[node]) / (2 * len(G.nodes()))
        debt_score = total_debt / 10000000  # Normalize debt

        combined_score = 0.7 * degree_score + 0.3 * debt_score
        node_sizes[node] = base_size + combined_score * (max_size - base_size)

    return node_sizes


def draw_beautiful_edges(G, pos, ax, config, edge_betweenness):
    """Draw edges with various aesthetic enhancements"""
    edges = G.edges()

    # Group edges by weight for different styling
    edge_weights = [(u, v, d.get("amount", 0)) for u, v, d in G.edges(data=True)]

    if config["glow"]:
        # Draw glow effect for neon/tech styles
        for u, v, weight in edge_weights:
            x1, y1 = pos[u]
            x2, y2 = pos[v]

            # Multiple layers for glow
            for width, alpha in [(8, 0.1), (5, 0.2), (3, 0.3), (1.5, 0.6)]:
                ax.plot(
                    [x1, x2],
                    [y1, y2],
                    color="white",
                    alpha=alpha * config["edge_alpha"],
                    linewidth=width,
                    zorder=1,
                )

    # Draw main edges with color mapping
    edge_colors = []
    edge_widths = []

    max_weight = max(weight for _, _, weight in edge_weights) if edge_weights else 1

    for u, v, weight in edge_weights:
        # Color based on weight
        normalized_weight = weight / max_weight
        edge_colors.append(normalized_weight)

        # Width based on importance
        importance = edge_betweenness.get((u, v), 0.5)
        edge_widths.append(0.5 + importance * 4)

    # Draw edges with matplotlib for more control
    edge_collection = []
    for (u, v), color, width in zip(edges, edge_colors, edge_widths):
        x1, y1 = pos[u]
        x2, y2 = pos[v]

        # Add slight curve to edges for aesthetic appeal
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        # Curve factor based on node distance
        dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        curve_factor = 0.1 * dist

        # Perpendicular offset
        dx = x2 - x1
        dy = y2 - y1
        perp_x = -dy / (dist + 0.001)
        perp_y = dx / (dist + 0.001)

        control_x = mid_x + curve_factor * perp_x
        control_y = mid_y + curve_factor * perp_y

        # Create curved path
        t = np.linspace(0, 1, 50)
        x_curve = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * control_x + t**2 * x2
        y_curve = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * control_y + t**2 * y2

        ax.plot(
            x_curve,
            y_curve,
            color=plt.cm.get_cmap(config["edge_cmap"])(color),
            alpha=config["edge_alpha"],
            linewidth=width,
            zorder=2,
        )

        # Add arrow for directed edges
        arrow_pos = 0.85  # Position along the curve
        idx = int(arrow_pos * len(t))
        ax.annotate(
            "",
            xy=(x_curve[idx + 1], y_curve[idx + 1]),
            xytext=(x_curve[idx], y_curve[idx]),
            arrowprops=dict(
                arrowstyle="->",
                color=plt.cm.get_cmap(config["edge_cmap"])(color),
                alpha=config["edge_alpha"],
                lw=width * 0.7,
            ),
        )


def draw_beautiful_nodes(
    G, pos, ax, node_sizes, sector_colors, config, degree_centrality
):
    """Draw nodes with various visual effects"""
    for node in G.nodes():
        x, y = pos[node]
        size = node_sizes[node]
        sector = G.nodes[node].get("sector", "services")
        color = sector_colors.get(sector, "#95A5A6")

        # Importance factor for visual emphasis
        importance = degree_centrality[node]

        if config["glow"]:
            # Glow effect for important nodes
            if importance > 0.1:
                for glow_size, glow_alpha in [
                    (size * 1.5, 0.2),
                    (size * 1.3, 0.3),
                    (size * 1.1, 0.4),
                ]:
                    circle = Circle(
                        (x, y),
                        glow_size / 10000,
                        color=color,
                        alpha=glow_alpha,
                        zorder=3,
                    )
                    ax.add_patch(circle)

        # Main node
        circle = Circle(
            (x, y),
            size / 10000,
            facecolor=color,
            edgecolor=config["node_edge_color"],
            linewidth=config["node_edge_width"],
            alpha=0.9,
            zorder=5,
        )
        ax.add_patch(circle)

        # Add inner gradient effect for large nodes
        if size > 1000:
            inner_circle = Circle(
                (x, y), size / 15000, facecolor="white", alpha=0.3, zorder=6
            )
            ax.add_patch(inner_circle)


def add_smart_labels(G, pos, ax, config, degree_centrality):
    """Add labels with smart positioning to avoid overlaps"""
    # Only label important nodes
    important_nodes = sorted(
        degree_centrality.items(), key=lambda x: x[1], reverse=True
    )[:20]

    labels = {}
    for node, importance in important_nodes:
        label = node
        if len(label) > 15:
            label = label[:12] + "..."
        labels[node] = label

    # Smart label positioning
    label_pos = {}
    for node in labels:
        x, y = pos[node]
        # Offset labels based on local density
        offset = 0.05
        neighbors = list(G.neighbors(node))

        if neighbors:
            # Calculate average direction away from neighbors
            avg_dx = 0
            avg_dy = 0
            for neighbor in neighbors:
                nx, ny = pos[neighbor]
                avg_dx += x - nx
                avg_dy += y - ny

            # Normalize
            norm = np.sqrt(avg_dx**2 + avg_dy**2)
            if norm > 0:
                avg_dx /= norm
                avg_dy /= norm
                label_pos[node] = (x + offset * avg_dx, y + offset * avg_dy)
            else:
                label_pos[node] = (x, y + offset)
        else:
            label_pos[node] = (x, y + offset)

    # Draw labels with background
    for node, (lx, ly) in label_pos.items():
        # Background box
        bbox_props = dict(
            boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.8
        )

        ax.text(
            lx,
            ly,
            labels[node],
            fontsize=9,
            fontweight="bold",
            color=config["font_color"],
            ha="center",
            va="center",
            bbox=bbox_props,
            zorder=10,
        )


def add_grid_lines(ax, config):
    """Add subtle grid lines for modern/finance styles"""
    ax.grid(True, linestyle="--", alpha=0.1, color="gray", zorder=0)

    # Add subtle frame
    for spine in ax.spines.values():
        spine.set_edgecolor(config["node_edge_color"])
        spine.set_alpha(0.3)
        spine.set_linewidth(0.5)


def add_title_and_legend(ax, G, sector_colors, config, style):
    """Add title and legend with style-appropriate formatting"""
    # Title
    title_text = f"Business Ecosystem Network\n{G.number_of_nodes()} Companies • {G.number_of_edges()} Relationships"

    ax.text(
        0.5,
        0.98,
        title_text,
        transform=ax.transAxes,
        fontsize=20,
        fontweight="bold",
        color=config["title_color"],
        ha="center",
        va="top",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor=config["bg_color"],
            edgecolor=config["title_color"],
            alpha=0.8,
        ),
    )

    # Legend
    legend_elements = []
    for sector, color in sorted(sector_colors.items()):
        if any(G.nodes[n].get("sector") == sector for n in G.nodes()):
            legend_elements.append(
                mpatches.Circle(
                    (0, 0),
                    1,
                    facecolor=color,
                    edgecolor=config["node_edge_color"],
                    label=sector.replace("_", " ").title(),
                )
            )

    legend = ax.legend(
        handles=legend_elements[:6],  # Show max 6 sectors
        loc="upper right",
        bbox_to_anchor=(0.98, 0.98),
        frameon=True,
        fancybox=True,
        shadow=True,
        ncol=1,
        fontsize=10,
    )

    legend.get_frame().set_facecolor(config["bg_color"])
    legend.get_frame().set_edgecolor(config["node_edge_color"])
    legend.get_frame().set_alpha(0.9)


from NetworkConstructor.network import create_complex_network

# Example usage
if __name__ == "__main__":
    G = create_complex_network()

    # Create beautiful visualizations in different styles
    styles = ["modern", "neon", "watercolor", "tech", "finance"]

    for style in styles:
        print(f"Creating {style} style visualization...")
        fig, ax = create_beautiful_visualization(
            G,
            style=style,
            save_path=os.path.join(
                PACKAGE_PATH, "figures", f"beautiful_network_{style}.png"
            ),
        )
        plt.close()

import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np
from configuration_Matplotlib import *
from Item import create_items_bulk
from BestFit import bin_packing_best_fit_var_capa
from FirstFit import bin_packing_first_fit_var_capa
from NextFit import bin_packing_next_fit_var_capa
from WorstFit import bin_packing_worst_fit_var_capa

FIGURE_MARGIN = 0.1
FAILURE_MARKING_TRANSPARENCY = 0.5

def determine_start_position_and_direction(amount_rows, amount_columns, amount_items):
    start_from_left = amount_rows % 2 == 1 or amount_rows * \
        amount_columns == amount_items
    if start_from_left:
        next_cell = (0, 0)
        horizontal_direction = 1  # 1=go right, -1=go left
    else:
        next_cell = (amount_columns, 0)
        horizontal_direction = -1  # 1=go right, -1=go left
    return next_cell, horizontal_direction


def draw_separation_vertical_line(ax, x, y, height=1, color=GRID_COLOR):
    ax.vlines([x], y, y+height, colors=color, linestyles="dotted")


def draw_grid_around_cell(ax, x, y, width=1, height=1, color=GRID_COLOR):
    ax.hlines([y], x, x+width, colors=color)
    ax.hlines([y+height], x, x+width, colors=color)
    ax.vlines([x], y, y+height, colors=color)
    ax.vlines([x+width], y, y+height, colors=color)


def how_much_can_be_inserted_in_row(next_cell, horizontal_direction, max_x, unit=1):
    next_x, next_y = next_cell
    potential_next_x = next_x + horizontal_direction * unit
    if potential_next_x > max_x:
        can_insert = unit - abs(max_x - potential_next_x)
    elif potential_next_x < 0:
        can_insert = unit - abs(potential_next_x)
    else:
        can_insert = unit
    return can_insert


def insert_cell(next_cell, horizontal_direction, max_x, item, ax, unit=1):
    x, y = next_cell
    width_to_be_inserted = how_much_can_be_inserted_in_row(
        next_cell, horizontal_direction, max_x, unit)
    x_offset = -0.5 * width_to_be_inserted + \
        horizontal_direction/2 * width_to_be_inserted
    ax.add_patch(plt.Rectangle((x + x_offset, y),
                 width_to_be_inserted, 1, facecolor=item._color))
    next_cell, horizontal_direction = get_next_position(
        next_cell, horizontal_direction, max_x, unit=width_to_be_inserted)
    return unit - width_to_be_inserted, next_cell, horizontal_direction


def get_next_position(next_cell, horizontal_direction, max_x, unit=1):
    next_x, next_y = next_cell
    potential_next_x = next_x + horizontal_direction * unit
    next_x = potential_next_x
    if potential_next_x >= max_x:
        next_y += 1
        next_x = max_x
        horizontal_direction = -1
    if potential_next_x <= 0:
        next_y += 1
        next_x = 0
        horizontal_direction = 1
    next_cell = (next_x, next_y)
    return next_cell, horizontal_direction


def visualize_container(label, capacity, items, ax, max_bin_count, is_leftover_bin, visualize_in_2d):
    if capacity <= 0:
        return
    
    total_size = sum(items)
    
    # Set up the plot with vertical orientation and very narrow bins
    ax.set_xlim(0, 0.15)  # Make bins even narrower
    ax.set_ylim(0, capacity)  # Height represents capacity
    ax.set_aspect('auto')
    
    # Draw the bin outline
    ax.add_patch(plt.Rectangle((0, 0), 0.15, capacity, 
                              fill=False, edgecolor=GRID_COLOR, linewidth=2))
    
    # Draw grid lines for better readability and capacity indicators
    for i in range(0, int(capacity) + 1):
        # Make lines at numbered positions darker
        if i % 5 == 0:  # Every 5 units
            ax.axhline(y=i, color=GRID_COLOR, linestyle='-', alpha=0.7, linewidth=1.5)
            # Add capacity numbers on the right side
            ax.text(0.17, i, str(i), ha='left', va='center', 
                   color='black', fontsize=8, fontweight='bold')
        else:
            ax.axhline(y=i, color=GRID_COLOR, linestyle='--', alpha=0.3)
    
    # Place items in the bin
    current_position = 0
    for item in items:
        # Draw the item
        ax.add_patch(plt.Rectangle((0, current_position), 0.15, item.size,
                                  facecolor=item._color, edgecolor='black'))
        # Add item size label
        ax.text(0.075, current_position + item.size/2, str(item.size),
                ha='center', va='center', color='black', fontweight='bold',
                fontsize=8, rotation=0)
        current_position += item.size
    
    # Set ticks and labels
    ax.set_yticks(range(0, int(capacity) + 1, max(1, int(capacity/10))))
    ax.set_yticklabels(range(0, int(capacity) + 1, max(1, int(capacity/10))))
    ax.set_xticks([])
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Set title with adjusted position
    if is_leftover_bin:
        ax.set_title(label, fontsize=10, loc="left", pad=15)  # Removed capacity from title for leftover bins
    else:
        ax.set_title(label + f"\ncapacity: {capacity}\nused: {total_size}", 
                    fontsize=10, loc="left", pad=15)


def bin_packing(bin_capacities, elements, approach, fixed_size=True):
    if approach == "BEST":
        return bin_packing_best_fit_var_capa(bin_capacities, elements)
    elif approach == "FIRST":
        return bin_packing_first_fit_var_capa(bin_capacities, elements)
    elif approach == "NEXT":
        return bin_packing_next_fit_var_capa(bin_capacities, elements)
    elif approach == "WORST":
        return bin_packing_worst_fit_var_capa(bin_capacities, elements)
    else:
        print(r'Please select "BEST", "FIRST", "NEXT", or "WORST" as approach.')
        return None


def create_overview(approach, could_not_place_size, amount_bins, ax):
    if approach == "BEST":
        approach_text = "Best-fit"
    elif approach == "FIRST":
        approach_text = "First-fit"
    elif approach == "NEXT":
        approach_text = "Next-fit"
    elif approach == "WORST":
        approach_text = "Worst-fit"
    
    status = "✓" if could_not_place_size == 0 else "✗"
    status_size = 30  # Larger status symbol
    overview_text = f"{approach_text}\nBins: {amount_bins}"
    if could_not_place_size > 0:
        overview_text += f"\nLeftover: {could_not_place_size}"
    
    # Draw status symbol
    ax.text(0.5, 0.5, status, 
            ha="center", va="center", 
            fontsize=status_size, fontweight='bold',
            color='green' if could_not_place_size == 0 else 'red')
    
    # Draw text below status
    ax.text(0.5, 0.2, overview_text, 
            ha="center", va="center", 
            fontsize=10, fontweight='bold')


def visualize_bin_packing(capacities, items, visualize_in_2d=False):
    fixed_size = len(set(capacities)) == 1
    items = create_items_bulk(*items)
    if fixed_size:
        capacities = [capacities[0] for _ in range(len(capacities))]
    colors = mpl.colormaps[BIN_PACKING_COLORMAP_NAME](
        np.linspace(0, 1, len(items)))
    for item, color in zip(items, colors):
        item._color = color
    approaches = ["BEST", "FIRST", "NEXT", "WORST"]
    results = []
    for approach in approaches:
        results.append(bin_packing(
            capacities, items, approach, fixed_size))
    max_bin_count = 0
    for is_possible, used_bins in results:
        bin_count = len(used_bins) + (1 if not is_possible else 0)
        if bin_count > max_bin_count:
            max_bin_count = bin_count
    
    # Calculate figure size based on maximum capacity
    max_capacity = max(capacities)
    if max_capacity > 20:
        fig_width = 12
        fig_height = 12
    elif max_capacity > 15:
        fig_width = 10
        fig_height = 10
    else:
        fig_width = 8
        fig_height = 8
    
    # Create figure with adjusted spacing
    fig, axs = plt.subplots(
        len(approaches), max_bin_count + 1, 
        figsize=(fig_width, fig_height),
        gridspec_kw={'wspace': 0.5, 'hspace': 0.2},
        constrained_layout=True, 
        sharex="col")
    
    for i, (is_possible, used_bins) in enumerate(results):
        approach = approaches[i]
        axs_row = axs[i]
        for ax in axs_row:
            ax.axis("off")
            ax.set_yticks([])
        if not is_possible:
            used_items = [item for item in used_bins for item in item]
            leftover_items = [item for item in items if item not in used_items]
        could_not_place_size = 0 if is_possible else sum(
            map(lambda item: item.size, leftover_items))
        create_overview(approach, could_not_place_size,
                        len([used_bin for used_bin in used_bins if used_bin]), axs_row[0])
        for i, used_bin in enumerate(used_bins):
            ax = axs_row[1:][i]
            visualize_container(
                f"Bin {i+1}", capacities[i], used_bin, ax, max_bin_count, is_leftover_bin=False, visualize_in_2d=visualize_in_2d)
        if not is_possible:
            leftover_size = sum(map(lambda item: item.size, leftover_items))
            visualize_container(f"Leftover: {leftover_size}", leftover_size,
                                leftover_items, axs_row[-1], max_bin_count, is_leftover_bin=True, visualize_in_2d=visualize_in_2d)
            
            # Get the axes that contain bins (excluding the overview)
            axs_with_bins = axs_row[1:]
            
            # Draw call required to get accurate bounding box values
            fig.canvas.draw()
            
            # Get the position of the first bin (Bin 1)
            first_bin = axs_with_bins[0]
            min_x = first_bin.get_position().x0 - first_bin.get_position().width  # Start from beginning of Bin 1
            
            # Get the vertical position from the first bin
            min_y = first_bin.get_position().y0 + (first_bin.get_position().height * 0.1)  # Move up slightly
            max_y = first_bin.get_position().y1 - (first_bin.get_position().height * 0.1)  # Move down slightly
            
            # Find the last bin that has content (including leftover)
            last_bin = axs_with_bins[-1]
            max_x = last_bin.get_position().x1

            # Draw a cross across all bins indicating that bin-packing was unsuccessful for a given approach
            line = plt.Line2D([min_x, max_x], [min_y, max_y], transform=fig.transFigure,
                            color="red", linewidth=10, alpha=FAILURE_MARKING_TRANSPARENCY)
            outline = plt.Line2D([min_x, max_x], [min_y, max_y], transform=fig.transFigure,
                                color="black", linewidth=12, alpha=FAILURE_MARKING_TRANSPARENCY)
            fig.lines.extend([outline, line])

            line = plt.Line2D([min_x, max_x], [max_y, min_y], transform=fig.transFigure,
                            color="red", linewidth=10, alpha=FAILURE_MARKING_TRANSPARENCY)
            outline = plt.Line2D([min_x, max_x], [max_y, min_y], transform=fig.transFigure,
                                color="black", linewidth=12, alpha=FAILURE_MARKING_TRANSPARENCY)
            fig.lines.extend([outline, line])
    
    plt.show()
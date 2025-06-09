import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np
import os
from configuration_Matplotlib import *
from Class_Items import create_items_bulk
from BinPackingAlgorithms import bin_packing_best_fit_var_capa, bin_packing_first_fit_var_capa, bin_packing_next_fit_var_capa, bin_packing_worst_fit_var_capa

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


def draw_separation_vertical_line(ax, x, y, height=1, linestyle="dotted", color=GRID_COLOR):
    ax.vlines([x], y, y+height, colors=color, linestyles=linestyle)


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


def visualize_container(label, capacity, items, ax, include_packed_after_failure_padding, is_leftover_bin, visualize_in_2d):
    if not visualize_in_2d and ALLOW_SCALE_UNITS:
        unit_scale = 1 if capacity < 10 else 1 / (capacity // 10)
    else:
        unit_scale = 1
    # No capacity, therefore nothing to visualize
    if capacity <= 0:
        return
    total_size = sum(items)
    # Determine how many rows and columns are required
    amount_columns = capacity * \
        unit_scale if not visualize_in_2d else math.ceil(math.sqrt(capacity))
    amount_rows = 1 if not visualize_in_2d else math.ceil(
        capacity / amount_columns)
    # Determine size of figure and define grid boundaries
    grid_height_to_width_ratio = min(amount_rows/amount_columns, 1)
    y_max_additional_padding = 0
    if not is_leftover_bin and include_packed_after_failure_padding and not visualize_in_2d:
        y_max_additional_padding = PACKED_AFTER_FAILURE_MARKER_SIZE - 1
    ax.axis([0 - FIGURE_MARGIN, amount_columns + FIGURE_MARGIN, 0 -
            FIGURE_MARGIN, amount_rows + FIGURE_MARGIN + y_max_additional_padding])  # xmin, xmax, ymin, ymax
    ax.apply_aspect()
    # Make sure that X and Y axes are scaled equally
    ax.set_aspect("equal", adjustable="box")
    # Create entire capacity cells
    capacity_units = [1 for full_cell in range(
        math.floor(capacity*unit_scale))]
    fractional_capacity = capacity*unit_scale - math.floor(capacity*unit_scale)
    # Fractional capacity e.g., capacity = 10.5, where 10 full capacity cells are drawn (see above)
    # And then one fractional capacity cell will be drawn (in this example half a cell)
    if fractional_capacity > 0:
        capacity_units.append(fractional_capacity)
    for i, capacity_unit in enumerate(capacity_units):
        column = i % amount_columns
        row = math.floor(i / amount_columns)
        draw_grid_around_cell(ax, column, row, capacity_unit)
    # Determine whether to start filling from right or left
    # to make sure, that the empty space will be in the top right corner
    next_cell, horizontal_direction = determine_start_position_and_direction(
        amount_rows, amount_columns, len(items))
    # Track whether the item belongs to those packed after failure or not (if there was a failure)
    already_packed_after_failure = False
    # Iterate over all items and place them
    for item in items:
        if not is_leftover_bin and not visualize_in_2d:
            if not already_packed_after_failure and item.is_packed_after_failure:
                already_packed_after_failure = True
                draw_separation_vertical_line(ax, *next_cell, height=PACKED_AFTER_FAILURE_MARKER_SIZE, linestyle="solid")
                packed_after_failure_text_x, packed_after_failure_text_y = next_cell
                ax.text(packed_after_failure_text_x + PACKED_AFTER_FAILURE_TEXT_PADDING, packed_after_failure_text_y + 1 + PACKED_AFTER_FAILURE_TEXT_PADDING, AFTER_FAILURE_TEXT, ha="left", va="bottom", fontsize=12)
        # Draw a separating vertical line to indicate two separate items.
        # Depending on color gradient, adjacent items could have similar colors.
        # This makes them more distinguishable.
        draw_separation_vertical_line(ax, *next_cell)
        # Place one cell for each unit of size into the grid
        cell_units = [1 for full_cell in range(math.floor(item.size))]
        # In case one item consists not entirely of integers,
        # but instead also a fractional part, then also draw the fractional part.
        # For e.g. size=4.53 one would first draw the 4 full cells and then the 0.53 fractional cell
        fractional_unit_width = item.size - math.floor(item.size)
        if fractional_unit_width > 0:
            cell_units.append(fractional_unit_width)
        for cell_unit in cell_units:
            leftover_width, next_cell, horizontal_direction = insert_cell(
                next_cell, horizontal_direction, amount_columns, item, ax, unit=cell_unit*unit_scale)
            # Leftover refers to a cell unit not being able to be placed,
            # as it would otherwise be out of bounds on the left or right side.
            if leftover_width > 0:
                _, next_cell, horizontal_direction = insert_cell(
                    next_cell, horizontal_direction, amount_columns, item, ax, unit=leftover_width*unit_scale)
    # Purpose is to eliminate edge cases, where the capacity should be entirely used up,
    # but there is a small piece left due to machine precision.
    # In those cases, the next location to place
    FULL_CAPACITY_EPSILON = 0.0001
    if abs(capacity - total_size) > FULL_CAPACITY_EPSILON:
        draw_separation_vertical_line(ax, *next_cell)
    ax.set_yticks([])
    amount_of_ticks = math.floor(amount_columns * unit_scale)+1
    ax.set_xticks(range(amount_of_ticks))
    # Adjust tick label size and rotation
    ax.set_xticklabels(
        list(map(lambda xtick: round(xtick / unit_scale), ax.get_xticks())),
        fontsize=10,
    )
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=True)
    if not visualize_in_2d and ALLOW_SCALE_UNITS:
        ax.axis("on")
    else:
        plt.axis("off")
    if is_leftover_bin:
        ax.set_title(label + f"\n{capacity}", fontsize=18, loc="left")
    else:
        ax.set_title(
            label + f"\ncapacity: {capacity}\nused: {total_size}", fontsize=18, loc="left")


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
    ax.figure.set_size_inches(BASE_GRID_WIDTH, BASE_GRID_WIDTH)
    if approach == "BEST":
        approach_text = "Best-fit bin packing"
    elif approach == "FIRST":
        approach_text = "First-fit bin packing"
    elif approach == "NEXT":
        approach_text = "Next-fit bin packing"
    elif approach == "WORST":
        approach_text = "Worst-fit bin packing"
    
    # Create the text with success status
    success_status = "Successful" if could_not_place_size == 0 else "Not successful"
    
    # Create the text with minimal spacing
    overview_text = f"{approach_text}\n({success_status})\nbins used: {amount_bins}"
    if could_not_place_size > 0:
        overview_text += f"\nleftover: {could_not_place_size}"
    
    # Position text with reduced spacing
    ax.text(0.5, 0.5, overview_text, ha="center", va="center", fontsize=18, 
            color="black", linespacing=1.2)  # All text in black


def visualize_bin_packing(capacities, items, visualize_in_2d=False, algorithms=None):
    # Only support single algorithm for tight cropping
    if algorithms:
        approach = algorithms[0]
    else:
        approach = "BEST"
    fixed_size = len(set(capacities)) == 1
    items = create_items_bulk(*items)
    if fixed_size:
        capacities = [capacities[0] for _ in range(len(capacities))]
    colors = mpl.colormaps[BIN_PACKING_COLORMAP_NAME](
        np.linspace(0, 1, len(items)))
    for item, color in zip(items, colors):
        item._color = color
    # Run the algorithm
    if approach == "BEST":
        is_possible, used_bins, bins_packed_after_failure = bin_packing_best_fit_var_capa(capacities, items)
    elif approach == "FIRST":
        is_possible, used_bins, bins_packed_after_failure = bin_packing_first_fit_var_capa(capacities, items)
    elif approach == "NEXT":
        is_possible, used_bins, bins_packed_after_failure = bin_packing_next_fit_var_capa(capacities, items)
    elif approach == "WORST":
        is_possible, used_bins, bins_packed_after_failure = bin_packing_worst_fit_var_capa(capacities, items)
    else:
        raise ValueError(f"Unknown approach: {approach}")
    for bin_packed_after_failure in bins_packed_after_failure:
        for item in bin_packed_after_failure:
            item.is_packed_after_failure = True
    # Prepare for manual layout
    n_bins = len(used_bins)
    has_leftover = not is_possible
    n_blocks = n_bins + (1 if has_leftover else 0)
    # Layout parameters
    text_width = 4.2
    bin_width = 4.0
    bin_height = 0.6
    gap = 1.2  # Gap between bins
    top_padding = 1.5
    text_height = 0.5  # Reduced from 0.8 to 0.5
    
    # Calculate total height and width for vertical layout
    total_height = top_padding + n_bins * (bin_height + gap + text_height) + (bin_height + gap + text_height if has_leftover else 0)
    total_width = text_width + bin_width + 1.0
    
    fig, ax = plt.subplots(figsize=(total_width, total_height))
    
    # Place overview text
    if not is_possible:
        used_items = [item for item in used_bins for item in item]
        leftover_items = [item for item in items if item not in used_items]
    could_not_place_size = 0 if is_possible else sum(map(lambda item: item.size, leftover_items))
    
    # Compose overview text
    if approach == "BEST":
        approach_text = "Best-fit bin packing"
    elif approach == "FIRST":
        approach_text = "First-fit bin packing"
    elif approach == "NEXT":
        approach_text = "Next-fit bin packing"
    elif approach == "WORST":
        approach_text = "Worst-fit bin packing"
    success_status = "Successful" if is_possible else "Not successful"
    overview_text = f"{approach_text}\n({success_status})\nbins used: {len([b for b in used_bins if b])}"
    if not is_possible:
        overview_text += f"\nleftover: {could_not_place_size}"
    
    # Place text in the center of the left side
    ax.text(0.02, 0.5, overview_text, ha="left", va="center", fontsize=18, transform=ax.transAxes)
    
    # Place bins vertically
    x = text_width
    y = total_height - top_padding - bin_height - text_height
    bin_rects = []
    
    for i, used_bin in enumerate(used_bins):
        bin_y = y - i * (bin_height + gap + text_height)
        rect = _draw_bin(ax, x, bin_y, bin_width, bin_height, capacities[i], used_bin, f"Bin {i+1}")
        bin_rects.append(rect)
    
    # Place leftover if needed
    if has_leftover:
        leftover_y = y - n_bins * (bin_height + gap + text_height)
        rect = _draw_bin(ax, x, leftover_y, bin_width, bin_height, 
                        sum(map(lambda item: item.size, leftover_items)), 
                        leftover_items, "Leftover")
        bin_rects.append(rect)
    
    # Draw red cross if not successful
    if not is_possible and bin_rects:
        # Get bounding box covering all bins
        min_x = min([r[0] for r in bin_rects])
        max_x = max([r[0] + r[2] for r in bin_rects])
        min_y = min([r[1] for r in bin_rects])
        max_y = max([r[1] + r[3] for r in bin_rects])
        # Extend the cross a bit beyond the bins
        x_margin = 0.02 * (max_x - min_x)
        y_margin = 0.02 * (max_y - min_y)
        min_xe = min_x - x_margin
        max_xe = max_x + x_margin
        min_ye = min_y - y_margin
        max_ye = max_y + y_margin
        # Draw black outline first
        ax.plot([min_xe, max_xe], [min_ye, max_ye], color='black', linewidth=12, alpha=0.5, zorder=10)
        ax.plot([min_xe, max_xe], [max_ye, min_ye], color='black', linewidth=12, alpha=0.5, zorder=10)
        # Draw red cross on top
        ax.plot([min_xe, max_xe], [min_ye, max_ye], color='red', linewidth=8, alpha=0.5, zorder=11)
        ax.plot([min_xe, max_xe], [max_ye, min_ye], color='red', linewidth=8, alpha=0.5, zorder=11)
    
    # Remove all axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlim(0, total_width)
    ax.set_ylim(0, total_height)
    return fig

def _draw_bin(ax, x, y, width, height, capacity, items, label):
    # Draw bin rectangle
    rect = plt.Rectangle((x, y), width, height, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    # Draw items as colored rectangles
    if len(items) > 0:
        total_size = sum(item.size for item in items)
        curr_x = x
        after_failure_drawn = False
        for idx, item in enumerate(items):
            item_width = width * (item.size / capacity)
            # Draw separation line and label if this is the first 'after failure' item
            if not after_failure_drawn and getattr(item, "is_packed_after_failure", False):
                sep_x = curr_x
                # Line goes through the bin and above, but not below
                margin = 0.2 * height
                ax.plot([sep_x, sep_x], [y, y + height + margin], color="red", linewidth=4, linestyle="solid", zorder=20)
                # Draw label above the line
                ax.text(sep_x + 0.05, y + height + margin + 0.02, "after failure", ha="left", va="bottom", fontsize=10, color="red", zorder=21)
                after_failure_drawn = True
            ax.add_patch(plt.Rectangle((curr_x, y), item_width, height, color=item._color, ec='black', linewidth=1))
            curr_x += item_width
    # Draw label and capacity info
    if label == "Leftover":
        ax.text(x + width/2, y + height + 0.25, f"Leftover: {int(sum(item.size for item in items))}",
                ha="center", va="bottom", fontsize=14)
    else:
        ax.text(x + width/2, y + height + 0.25, f"{label}\ncapacity: {int(capacity)}\nused: {int(sum(item.size for item in items))}",
                ha="center", va="bottom", fontsize=14)
    # Draw ticks for each unit, but only show every Nth label if too many
    max_ticks = 15
    if capacity > max_ticks:
        step = int(capacity // max_ticks) + 1
    else:
        step = 1
    for tick in range(int(capacity)+1):
        tick_x = x + width * (tick / capacity)
        ax.plot([tick_x, tick_x], [y, y-0.08], color='black', linewidth=1)
        if tick % step == 0 or tick == capacity:
            ax.text(tick_x, y-0.13, str(tick), ha='center', va='top', fontsize=9)
    return (x, y, width, height)
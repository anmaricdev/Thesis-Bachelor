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
    ax.set_xticklabels(
        list(map(lambda xtick: round(xtick / unit_scale), ax.get_xticks())))
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
        if fixed_size:
            return bin_packing_best_fit_fixed_capa(bin_capacities[0], len(bin_capacities), elements)
        else:
            return bin_packing_best_fit_var_capa(bin_capacities, elements)
    elif approach == "FIRST":
        if fixed_size:
            return bin_packing_first_fit_fixed_capa(bin_capacities[0], len(bin_capacities), elements)
        else:
            return bin_packing_first_fit_var_capa(bin_capacities, elements)
    elif approach == "NEXT":
        if fixed_size:
            return bin_packing_next_fit_fixed_capa(bin_capacities[0], len(bin_capacities), elements)
        else:
            return bin_packing_next_fit_var_capa(bin_capacities, elements)
    elif approach == "WORST":
        if fixed_size:
            return bin_packing_worst_fit_fixed_capa(bin_capacities[0], len(bin_capacities), elements)
        else:
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
    overview_text = approach_text
    overview_text += "\n" + \
        ("(Successful)" if could_not_place_size == 0 else "(Not successful)")
    overview_text += "\n" + f"bins used: {amount_bins}"
    if could_not_place_size > 0:
        overview_text += "\n" + f"leftover: {could_not_place_size}"
    ax.text(0.5, 0.5, overview_text, ha="center", va="center", fontsize=18)


def visualize_bin_packing(capacities, items, visualize_in_2d=False):
    fixed_size = len(set(capacities)) == 1
    items = create_items_bulk(*items)
    # If doing fixed size bin packing, then assume capacity of first bin for all bins
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
    for is_possible, used_bins, bins_packed_after_failure in results:
        bin_count = len(used_bins) + (1 if not is_possible else 0)
        if bin_count > max_bin_count:
            max_bin_count = bin_count
    fig, axs = plt.subplots(
        len(approaches), max_bin_count + 1, constrained_layout=True)
    for i, (is_possible, used_bins, bins_packed_after_failure) in enumerate(results):
        include_packed_after_failure_padding = False
        for bin_packed_after_failure in bins_packed_after_failure:
            for item in bin_packed_after_failure:
                item.is_packed_after_failure = True
                include_packed_after_failure_padding = True
        approach = approaches[i]
        axs_row = axs[i]
        for ax in axs_row:
            ax.axis("off")
            ax.set_xticks([])
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
                f"Bin {i+1}", capacities[i], used_bin, ax, include_packed_after_failure_padding, is_leftover_bin=False, visualize_in_2d=visualize_in_2d)
        if not is_possible:
            visualize_container(f"Leftover", sum(map(lambda item: item.size, leftover_items)),
                                leftover_items, axs_row[-1], include_packed_after_failure_padding, is_leftover_bin=True, visualize_in_2d=visualize_in_2d)
        # Draw call required to get accurate bounding box values
        fig.canvas.draw()
        # Only look at bins, which exist (i.e., leftover bin does not exist if bin-packing is possible for a given approach.)
        axs_with_bins = [ax for ax in axs_row if len(ax.get_xticks()) > 0]
        # Get the bin in the row with the highest amount of cells
        max_x_in_row = max(map(lambda ax: ax.get_xlim()[-1], axs_with_bins))
        max_y_in_row = max(map(lambda ax: ax.get_ylim()[-1], axs_with_bins))
        # Get starting position of first bin
        current_x = axs_with_bins[0].get_position().x0
        for ax in axs_with_bins:
            # This makes it so, that each bin will have the same size (and therefore same scaling on X-/Y-axes)
            # Since the rest of the axis is invisible, it does not make much difference.
            ax.set_xlim(right=max_x_in_row)
            ax.set_ylim(top=max_y_in_row)
            # A few bins may have been artifically enlarged to a given size, if they are not all of the same size.
            # But now there are inconsitent spaces between bins, since the area that came with the enlargement is invisible.
            # Solve this by overlapping them, making sure that all real content is still visible.
            # With this line one can calculate how large the fraction of actual content compared to padded space is for a bin.
            content_ratio = (len(ax.get_xticks()) - 1) / \
                (ax.get_xlim()[-1] - ax.get_xlim()[0])
            bbox = ax.get_position()
            _x0, y0, width, height = bbox.x0, bbox.y0, bbox.width, bbox.height
            # Update position
            ax.set_position([current_x, y0, width, height])
            # Prepare position for next bin. Next position will be the end of the real content of the current bin (with gap).
            current_x += width * content_ratio + GAP_BETWEEN_BINS
        if not is_possible:
            # Draw call required to get accurate bounding box values
            fig.canvas.draw()
            bboxes = list(map(lambda ax: ax.get_tightbbox(fig.canvas.get_renderer(
            )).transformed(fig.transFigure.inverted()), axs_with_bins))
            min_y = min(bboxes, key=lambda bbox: bbox.y0).y0
            max_y = max(bboxes, key=lambda bbox: bbox.y1).y1
            min_x = min(bboxes, key=lambda bbox: bbox.x0).x0
            # Since the last bin may have been artificially enlarged, the x1 coordinate is not correct,
            # since that includes the invisible section. Instead look at the last bin and use the content ratio to
            # find out where the actual content ends.
            last_ax = axs_with_bins[-1]
            content_ratio_last_ax = (
                len(last_ax.get_xticks()) - 1) / (last_ax.get_xlim()[-1] - FIGURE_MARGIN)
            max_x = last_ax.get_position().x0 + last_ax.get_position().width * \
                content_ratio_last_ax

            # Draw a cross accross the bins indicating, that bin-packing was unsuccessful for a given approach.
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
def calculate_midpoint(posA, posB, rad):
    # Calculate the control point for the arc
    control = (
        (posA[0] + posB[0]) / 2 + rad * (posA[1] - posB[1]),
        (posA[1] + posB[1]) / 2 + rad * (posB[0] - posA[0])
    )

    # Calculate the midpoint along the arc
    t = 0.5  # Parameter for the Bezier curve (0.5 for midpoint)
    midpoint = (
        (1 - t) ** 2 * posA[0] + 2 * (1 - t) * t * control[0] + t ** 2 * posB[0],
        (1 - t) ** 2 * posA[1] + 2 * (1 - t) * t * control[1] + t ** 2 * posB[1]
    )

    return midpoint

def remove_duplicates(input_list):
    seen = set()
    output_list = []

    for item in input_list:
        if item not in seen:
            seen.add(item)
            output_list.append(item)

    return output_list


def draw_arrow(ax, posA, posB, radius, c='0.4', tickness=0.1):
    
  
    ax.annotate("",
                xy=posA,
                xytext=posB,
                arrowprops=dict(
                    arrowstyle="-", color=c,
                    connectionstyle="arc3,rad=rrr".replace('rrr',str(radius)),
                    linewidth=tickness
                )
            )

def draw_label(ax, label, posA, posB,radius):
    ax.annotate(
                label,
                xy=posA,
                xytext=calculate_midpoint(posA, posB, radius),
                fontsize=6
            )

def plot_pointer(ax, pos, size):
    # Define the points of the arrow/triangle
    x = pos[0]
    y = pos[1]
    arrow_points = [(x - size, y - size), (x + size, y - size), (x, y + size)]

    ax.annotate(
        "",
        xy=pos, xytext=(x, y - size),
        arrowprops=dict(
                    arrowstyle="->", color="gold",
                    linewidth=5
                )
    )

def solution_to_string(solution):
    in_string = ''
    for node, via in solution:
        if node:
            in_string += node.upper() + " "
        if via:
            in_string += f"({via.upper()}) "

    return in_string

from .utils import read_json_tasks

def generate_checklist_text(json_path):
    rows = read_json_tasks(json_path)

    # Determine column widths
    task_width = max(len("Task"), max(len(task) for task, _ in rows))
    status_width = max(len("Status"), max(len(status) for _, status in rows))

    # Format border pieces
    top_border = f"┌{'─' * (task_width + 2)}┬{'─' * (status_width + 2)}┐"
    header = f"│ {'Task'.ljust(task_width)} │ {'Status'.ljust(status_width)} │"
    separator = f"╞{'═' * (task_width + 2)}╪{'═' * (status_width + 2)}╡"

    # Generate each row
    row_lines = []
    for task, status in rows[:-1]:
        line = f"├{'─' * (task_width + 2)}┼{'─' * (status_width + 2)}┤"
        content = f"│ {task.ljust(task_width)} │ {status.ljust(status_width)} │"
        row_lines.extend([content, line])

    # Last row without line below
    last_task, last_status = rows[-1]
    row_lines.append(f"│ {last_task.ljust(task_width)} │ {last_status.ljust(status_width)} │")
    bottom_border = f"└{'─' * (task_width + 2)}┴{'─' * (status_width + 2)}┘"

    # Combine all parts
    table = [top_border, header, separator] + row_lines + [bottom_border]
    final_output = "### Update Checklist\n\n```\n" + "\n".join(table) + "\n```"
    return final_output
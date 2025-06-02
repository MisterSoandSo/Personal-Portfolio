from PIL import Image, ImageDraw, ImageFont
from .utils import read_json_tasks, ChecklistStyle

# Color-coding dictionary (customizable)
status_colors = {
    "Done": (34, 139, 34),  # Green
    "Not Started": (255, 0, 0),  # Red
    "In-Progress": (255, 165, 0),  # Orange
    # Add more custom statuses here
}

def generate_checklist_image(json_path, output_path="checklist.png",style=ChecklistStyle()):
    rows = read_json_tasks(json_path)

    # Load monospace font
    try:
        font = ImageFont.truetype(style.font_path, 20)
    except IOError:
        font = ImageFont.load_default()

    # Calculate column widths
    col1_width = max(font.getlength(row[0]) for row in rows) + style.col_padding
    col2_width = max(font.getlength(row[1]) for row in rows) + style.col_padding
    img_width = int(col1_width + col2_width + style.padding_x * 2)
    img_height = int(style.row_height * len(rows) + style.padding_y * 2)

    # Create image
    img = Image.new("RGB", (img_width, img_height), color=style.bg_color)
    draw = ImageDraw.Draw(img)

    # Draw rows and text
    for i, (task, status) in enumerate(rows):
        y = style.padding_y + i * style.row_height
        draw.line([(style.padding_x, y), (img_width - style.padding_x, y)], fill=style.line_color)

        # Task text
        draw.text((style.padding_x + 5, y + 8), task, font=font, fill=style.text_color)

        # Determine color for the status
        status_color = status_colors.get(status, (240, 240, 240))  # Default to white if not found
        draw.text((style.padding_x + col1_width + 10, y + 8), status, font=font, fill=status_color)

    # Final bottom line
    y_end = style.padding_y + len(rows) * style.row_height
    draw.line([(style.padding_x, y_end), (img_width - style.padding_x, y_end)], fill=style.line_color)

    # Vertical lines
    x1 = style.padding_x
    x2 = style.padding_x + col1_width
    x3 = img_width - style.padding_x
    draw.line([(x1, style.padding_y), (x1, y_end)], fill=style.line_color)
    draw.line([(x2, style.padding_y), (x2, y_end)], fill=style.line_color)
    draw.line([(x3, style.padding_y), (x3, y_end)], fill=style.line_color)

    # Save image
    img.save(output_path)
    print(f"Checklist image saved as '{output_path}'")
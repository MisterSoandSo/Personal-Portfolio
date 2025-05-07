import TaskView

# Example usage
if __name__ == "__main__":
    TaskView.generate_checklist_image("task.json")
    checklist = TaskView.generate_checklist_text("task.json")
    print(checklist)

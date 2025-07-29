import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLineEdit,
    QMessageBox, QComboBox, QLabel, QDateEdit
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate



class Task:
    def __init__(self, title, category, priority, due_date):
        self.__title = title
        self.__category = category
        self.__priority = priority
        self.__due_date = due_date
        self.__completed = False

    def __str__(self):
        status = "✔" if self.__completed else "⏳"
        return f"{status} {self.__title} | {self.__category} | {self.__priority} | {self.__due_date.toString('yyyy-MM-dd')}"

    def mark_completed(self):
        self.__completed = True

    def is_completed(self):
        return self.__completed

    def get_priority(self):
        return self.__priority

    def get_summary(self):
        return str(self)


class TaskManager:
    def __init__(self):
        self.__tasks = []

    def add_task(self, task):
        self.__tasks.append(task)

    def remove_task(self, index):
        if 0 <= index < len(self.__tasks):
            del self.__tasks[index]

    def complete_task(self, index):
        if 0 <= index < len(self.__tasks):
            self.__tasks[index].mark_completed()

    def get_all_tasks(self):
        return self.__tasks

    def get_task(self, index):
        return self.__tasks[index]

    def total_tasks(self):
        return len(self.__tasks)

    def completed_tasks(self):
        return sum(task.is_completed() for task in self.__tasks)

    def remaining_tasks(self):
        return self.total_tasks() - self.completed_tasks()


class ToDoListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 650, 600)
        self.manager = TaskManager()
        self.setup_ui()

    def setup_ui(self):
        
        with open("style.css", "r") as f:
            self.setStyleSheet(f.read())
        
        self.setFont(QFont("Segoe UI", 10))
        layout = QVBoxLayout()

        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter a task")

        self.category_combo = QComboBox()
        self.category_combo.addItems(["General", "Work", "Study", "Personal"])

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])

        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.category_combo)
        input_layout.addWidget(self.priority_combo)
        input_layout.addWidget(self.date_picker)
        layout.addLayout(input_layout)

        self.add_button = QPushButton("Add")
        self.complete_button = QPushButton("Complete")
        self.remove_button = QPushButton("Remove")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.remove_button)
        layout.addLayout(button_layout)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_task)
        self.complete_button.clicked.connect(self.complete_task)
        self.remove_button.clicked.connect(self.remove_task)
        self.input_line.returnPressed.connect(self.add_task)

        self.update_stats()

    def update_stats(self):
        total = self.manager.total_tasks()
        done = self.manager.completed_tasks()
        remaining = self.manager.remaining_tasks()
        self.stats_label.setText(f"📊 Total: {total} | ✅ Done: {done} | 🕗 Remaining: {remaining}")

    def add_task(self):
        title = self.input_line.text().strip()
        if not title:
            QMessageBox.warning(self, "Input Error", "Task title cannot be empty.")
            return

        category = self.category_combo.currentText()
        priority = self.priority_combo.currentText()
        due_date = self.date_picker.date()

        task = Task(title, category, priority, due_date)
        self.manager.add_task(task)

        item = QListWidgetItem(task.get_summary())
        color_map = {"Low": "black", "Medium": "orange", "High": "red"}
        item.setForeground(QColor(color_map[priority]))
        self.list_widget.addItem(item)

        self.input_line.clear()
        self.update_stats()

    def remove_task(self):
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
            index = self.list_widget.row(item)
            self.list_widget.takeItem(index)
            self.manager.remove_task(index)
        self.update_stats()

    def complete_task(self):
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
            index = self.list_widget.row(item)
            self.manager.complete_task(index)
            task = self.manager.get_task(index)
            item.setText(task.get_summary())
            item.setForeground(QColor("gray"))
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
        self.update_stats()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoListApp()
    window.show()
    sys.exit(app.exec_())

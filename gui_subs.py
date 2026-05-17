#!/bin/python3

import sys
from PyQt6.QtWidgets import (
    QApplication as Qapp,
    QWidget,
    QLabel,
    QLineEdit as Qline,
    QPushButton as Qpush,
    QTextEdit as Qtext,
    QCheckBox as Qcheck,
    QVBoxLayout as QVbox,
    QHBoxLayout as QHbox,
    QGridLayout as Qgrid
)

from PyQt6.QtGui import QPalette, QColor
import ModSubs

class SubnetCalculatorApp(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main Layout
        main_layout = QHbox(self)

        # Left Side (Input Fields)
        input_layout = Qgrid()

        self.ip_label = QLabel("IP Address:")
        self.ip_entry = Qline()
        self.subnet_label = QLabel("Subnet Mask:")
        self.subnet_entry = Qline()
        self.multiple_subnets_checkbox = Qcheck("Enable Multiple Subnets")
        self.vlsm_checkbox = Qcheck("Enable VLSM")
        self.vlsm_label = QLabel("VLSM Subnet Sizes:")
        self.vlsm_entry = Qline()
        self.run_button = Qpush("Run")
        self.run_button.clicked.connect(self.run_subnet_script)

        # Add widgets to input layout
        input_layout.addWidget(self.ip_label, 0, 0)
        input_layout.addWidget(self.ip_entry, 0, 1)
        input_layout.addWidget(self.subnet_label, 1, 0)
        input_layout.addWidget(self.subnet_entry, 1, 1)
        input_layout.addWidget(self.multiple_subnets_checkbox, 2, 0, 1, 2)
        input_layout.addWidget(self.vlsm_checkbox, 3, 0, 1, 2)
        input_layout.addWidget(self.vlsm_label, 4, 0)
        input_layout.addWidget(self.vlsm_entry, 4, 1)
        input_layout.addWidget(self.run_button, 5, 0, 1, 2)

        # Right Side (Output Box)
        self.output_box = Qtext()
        self.output_box.setReadOnly(True)

        # Add to Main Layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.output_box)
        self.setLayout(main_layout)

        # Window Settings
        self.setWindowTitle("Subnet Calculator (PyQt6)")
        self.resize(600, 400)

    def run_subnet_script(self):
        """Runs subnet calculations and updates the output box."""

        ip = self.ip_entry.text().strip()
        subnet = self.subnet_entry.text().strip()
        multiple_subnets = self.multiple_subnets_checkbox.isChecked()
        use_vlsm = self.vlsm_checkbox.isChecked()
        vlsm_sizes = self.vlsm_entry.text().strip()

        if not ip or not subnet:
            self.output_box.setText("Error: Please enter both IP and Subnet Mask")
            return
        try:
            result = ModSubs.run_subnet_calculations(ip, subnet, multiple_subnets, vlsm_sizes if use_vlsm else None)
            self.output_box.setText(result)
        except Exception as e:
            self.output_box.setText(f"Execution Error: {str(e)}")

if __name__ == "__main__":

    app = Qapp(sys.argv)

    # Ensure Dark Mode applies to all widgets
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#1E1E1E"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#2D2D2D"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#3A3A3A"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
    app.setPalette(palette)

    window = SubnetCalculatorApp()
    window.show()

    sys.exit(app.exec())



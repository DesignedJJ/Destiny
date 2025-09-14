import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
    QComboBox
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

# Replace this with your actual outbound_call logic
# or adapt as needed
from outbound_call import make_outbound_call


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Destiny")
        self.resize(800, 700)  # Increased size for better layout with logos

        # -------- Colors and Style constants --------
        self.BG_NAVY = "#001F3F"      # Matte navy-blue background
        self.CARD_COLOR = "#102040"   # Slightly different navy for the card
        self.TAN_COLOR = "#F5DEB3"    # Light tan for text
        self.ENTRY_BG = "#333333"     # Dark gray for entry widgets

        # -------- Agent Information --------
        self.agent_number = "Designed.JJ"  # Replace with dynamic agent number as needed

        # Set the default font for the application
        # Use "Gill Sans" with fallback to "Arial" and "Sans-serif"
        app_font = QFont("Gill Sans", 12)
        app_font.setStyleHint(QFont.SansSerif)
        self.setFont(app_font)

        # Create a central widget with a main layout
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(20)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # -------- Background Styling --------
        # Apply a style sheet to the entire window for the navy background.
        # Minimal QComboBox styling to maintain default dropdown functionality.
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.BG_NAVY};
            }}
            QLabel {{
                color: {self.TAN_COLOR};
            }}
            QComboBox {{
                background-color: {self.ENTRY_BG};
                color: {self.TAN_COLOR};
                border: 1px solid {self.TAN_COLOR};
                border-radius: 8px;
                padding: 8px;
                min-width: 150px;
            }}
            QComboBox::down-arrow {{
                image: url("icons/dropdown.png");
                width: 16px;
                height: 16px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: {self.TAN_COLOR};
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                background-color: transparent;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.ENTRY_BG};
                color: {self.TAN_COLOR};
                border: 1px solid {self.TAN_COLOR};
                selection-background-color: #555555;
                selection-color: {self.BG_NAVY};
                border-radius: 4px;
            }}
            QComboBox::item {{
                padding: 5px 10px;
            }}
            QComboBox::item:selected {{
                background-color: #555555;
                color: {self.TAN_COLOR};
            }}
        """)

        # -------- Top Bar with Logos and Agent Number --------
        top_bar = QHBoxLayout()

        # Left Logo
        self.left_logo = QLabel()
        left_pixmap = QPixmap("icons/logo_left.png")
        if not left_pixmap.isNull():
            self.left_logo.setPixmap(left_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.left_logo.setText("Left Logo")
            self.left_logo.setAlignment(Qt.AlignCenter)
            self.left_logo.setStyleSheet(f"color: {self.TAN_COLOR};")
        self.left_logo.setFixedSize(100, 100)  # Adjust size as needed
        top_bar.addWidget(self.left_logo)

        # Spacer
        top_bar.addStretch(1)

        # Agent Number Label
        self.agent_label = QLabel(f"Agent: {self.agent_number}")
        self.agent_label.setFont(QFont("Gill Sans", 14, QFont.Bold))
        self.agent_label.setStyleSheet(f"color: {self.TAN_COLOR};")
        self.agent_label.setAlignment(Qt.AlignCenter)
        top_bar.addWidget(self.agent_label)

        # Spacer
        top_bar.addStretch(1)

        # Right Logo
        self.right_logo = QLabel()
        right_pixmap = QPixmap("icons/logo_right.png")
        if not right_pixmap.isNull():
            self.right_logo.setPixmap(right_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.right_logo.setText("Right Logo")
            self.right_logo.setAlignment(Qt.AlignCenter)
            self.right_logo.setStyleSheet(f"color: {self.TAN_COLOR};")
        self.right_logo.setFixedSize(100, 100)  # Adjust size as needed
        top_bar.addWidget(self.right_logo)

        # Add the top bar to the central layout
        central_layout.addLayout(top_bar)

        # -------- Card Frame --------
        self.card_frame = QFrame()
        self.card_frame.setObjectName("cardFrame")
        self.card_frame.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {self.CARD_COLOR};
                border: 2px solid {self.TAN_COLOR};
                border-radius: 20px;
            }}
        """)

        # Layout inside the card
        self.card_layout = QVBoxLayout()
        self.card_layout.setContentsMargins(20, 20, 20, 20)
        self.card_layout.setSpacing(15)
        self.card_frame.setLayout(self.card_layout)

        # Insert the card into the central layout with stretch
        row_layout = QHBoxLayout()
        row_layout.addStretch(1)
        row_layout.addWidget(self.card_frame)
        row_layout.addStretch(1)

        central_layout.addLayout(row_layout)

        # Build the content inside the card
        self.build_content()

    def build_content(self):
        """
        Create the phone input, contact dropdown, logs, notes, etc.
        All placed inside self.card_layout
        """

        # -------- PHONE ROW --------
        phone_row = QHBoxLayout()
        phone_label = QLabel("Phone Number:")
        phone_label.setFont(QFont("Gill Sans", 12))
        phone_row.addWidget(phone_label)

        self.phone_edit = QLineEdit()
        self.phone_edit.setFont(QFont("Gill Sans", 12))
        self.phone_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.ENTRY_BG};
                color: {self.TAN_COLOR};
                border: 1px solid {self.TAN_COLOR};
                border-radius: 8px;
                padding: 8px;
            }}
            QLineEdit:focus {{
                border: 1px solid #FFD700;  /* Gold color on focus */
            }}
        """)
        phone_row.addWidget(self.phone_edit, 1)

        # Call Button with Icon
        call_btn = QPushButton()
        call_icon = QIcon("icons/callicon.png")
        call_btn.setIcon(call_icon)
        # Set a standard icon size
        call_btn.setIconSize(QSize(24, 24))
        call_btn.setToolTip("Call")
        # Set fixed size to ensure consistency
        call_btn.setFixedSize(40, 40)
        call_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: black;
                border-radius: 8px;
                padding: 5px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #45A049;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """)
        call_btn.clicked.connect(self.initiate_call)
        phone_row.addWidget(call_btn)

        # Disconnect Button with Icon
        disconnect_btn = QPushButton()
        disconnect_icon = QIcon("icons/disconnect.png")
        disconnect_btn.setIcon(disconnect_icon)
        # Set the same standard icon size
        disconnect_btn.setIconSize(QSize(24, 24))
        disconnect_btn.setToolTip("Disconnect")
        # Set the same fixed size as call_btn
        disconnect_btn.setFixedSize(40, 40)
        disconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: black;
                border-radius: 8px;
                padding: 5px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #d32f2f;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """)
        disconnect_btn.clicked.connect(self.disconnect_call)
        phone_row.addWidget(disconnect_btn)

        self.card_layout.addLayout(phone_row)

        # -------- CONTACTS ROW --------
        contacts_row = QHBoxLayout()
        contacts_label = QLabel("Contacts:")
        contacts_label.setFont(QFont("Gill Sans", 12))
        contacts_row.addWidget(contacts_label)

        self.contacts_map = {
            "Alice": "+12345670001",
            "Bob": "+12345670002",
            "Charlie": "+12345670003"
        }

        self.contacts_combo = QComboBox()
        self.contacts_combo.setFont(QFont("Gill Sans", 12))
        self.contacts_combo.addItem("Select Contact")
        self.contacts_combo.addItems(list(self.contacts_map.keys()))
        # The dropdown arrow is already customized in the stylesheet
        contacts_row.addWidget(self.contacts_combo, 1)

        contact_call_btn = QPushButton()
        contact_call_icon = QIcon("icons/call.png")
        contact_call_btn.setIcon(contact_call_icon)
        # Set the same standard icon size
        contact_call_btn.setIconSize(QSize(24, 24))
        contact_call_btn.setToolTip("Call Contact")
        # Set fixed size to ensure consistency
        contact_call_btn.setFixedSize(40, 40)
        contact_call_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: black;
                border-radius: 8px;
                padding: 5px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #45A049;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """)
        contact_call_btn.clicked.connect(self.call_selected_contact)
        contacts_row.addWidget(contact_call_btn)

        self.card_layout.addLayout(contacts_row)

        # -------- LOGS LABEL --------
        logs_label = QLabel("Logs:")
        logs_label.setFont(QFont("Gill Sans", 15))
        self.card_layout.addWidget(logs_label)

        # -------- LOGS BOX --------
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setFont(QFont("Gill Sans", 13))
        self.log_box.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.ENTRY_BG};
                color: {self.TAN_COLOR};
                border: 1px solid {self.TAN_COLOR};
                border-radius: 8px;
                padding: 8px;
            }}
            QTextEdit:focus {{
                border: 1px solid #FFD700;  /* Gold color on focus */
            }}
        """)
        self.card_layout.addWidget(self.log_box)

        # -------- NOTES LABEL --------
        notes_label = QLabel("Notes:")
        notes_label.setFont(QFont("Gill Sans", 12))
        self.card_layout.addWidget(notes_label)

        # -------- NOTES BOX --------
        self.notes_box = QTextEdit()
        self.notes_box.setFont(QFont("Gill Sans", 11))
        self.notes_box.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.ENTRY_BG};
                color: {self.TAN_COLOR};
                border: 1px solid {self.TAN_COLOR};
                border-radius: 8px;
                padding: 8px;
            }}
            QTextEdit:focus {{
                border: 1px solid #FFD700;  /* Gold color on focus */
            }}
        """)
        self.card_layout.addWidget(self.notes_box)

        # Connect the QComboBox selection change to a method
        self.contacts_combo.currentIndexChanged.connect(self.contact_selected)

    # ------------------ Methods ------------------
    def initiate_call(self):
        phone_number = self.phone_edit.text().strip()
        if phone_number:
            call_sid = make_outbound_call(phone_number)
            self.log_message(f"Initiated AI call to {phone_number}, Call SID: {call_sid}")
        else:
            self.log_message("Please enter a phone number.")

    def disconnect_call(self):
        # Implement your disconnect logic here
        # For demonstration, we'll log the disconnection
        self.log_message("Call disconnected.")

    def call_selected_contact(self):
        contact_name = self.contacts_combo.currentText()
        if contact_name in self.contacts_map:
            phone_number = self.contacts_map[contact_name]
            call_sid = make_outbound_call(phone_number)
            self.log_message(f"Initiated AI call to {contact_name} ({phone_number}), Call SID: {call_sid}")
            # Update the phone_edit field with the contact's number
            self.phone_edit.setText(phone_number)
        else:
            self.log_message("Please select a valid contact.")

    def log_message(self, msg):
        """Append a line to the logs box."""
        self.log_box.append(msg)

    def contact_selected(self, index):
        """Display the phone number of the selected contact in the phone_edit field."""
        contact_name = self.contacts_combo.currentText()
        if contact_name in self.contacts_map:
            phone_number = self.contacts_map[contact_name]
            self.phone_edit.setText(phone_number)
        else:
            self.phone_edit.clear()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

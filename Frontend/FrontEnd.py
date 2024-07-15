import json
import os
import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QFormLayout, QMessageBox, QGridLayout, QHBoxLayout, QScrollArea
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QDateTime, QTimer


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cinema Hall POS - Login')
        self.setGeometry(100, 100, 400, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: white;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #ecf0f1;
            }
            QLineEdit {
                background-color: #34495e;
                color: white;
                border: 1px solid #ecf0f1;
                padding: 5px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.login_screen()

    def login_screen(self):
        self.header_label = QLabel('Cinema Hall POS')
        self.header_label.setFont(QFont('Arial', 24))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.header_label)

        self.logo_label = QLabel(self)
        pixmap = QPixmap('/loginWindowLogo.png')  # Replace with the path to your logo image

        self.logo_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.logo_label)

        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setFont(QFont('Arial', 14))
        form_layout.addRow('Username:', self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setFont(QFont('Arial', 14))
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow('Password:', self.password_input)

        self.main_layout.addLayout(form_layout)

        self.login_button = QPushButton('Login')
        self.login_button.setFont(QFont('Arial', 14))
        self.login_button.clicked.connect(self.handle_login)
        self.main_layout.addWidget(self.login_button)

        self.register_button = QPushButton('Register')
        self.register_button.setFont(QFont('Arial', 14))
        self.register_button.clicked.connect(self.open_registration)
        self.main_layout.addWidget(self.register_button)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        response = requests.post('http://127.0.0.1:5000/login', json={'username': username, 'password': password})

        if response.status_code == 200:
            self.user_id = response.json()['user_id']
            self.open_main_menu()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials.')

    def open_main_menu(self):
        self.main_menu = MainMenuWindow(self.user_id)
        self.main_menu.show()
        self.close()

    def open_registration(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cinema Hall POS - Register')
        self.setGeometry(100, 100, 400, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: white;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #ecf0f1;
            }
            QLineEdit {
                background-color: #34495e;
                color: white;
                border: 1px solid #ecf0f1;
                padding: 5px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.header_label = QLabel('Register New User')
        self.header_label.setFont(QFont('Arial', 24))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.header_label)

        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setFont(QFont('Arial', 14))
        form_layout.addRow('Username:', self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setFont(QFont('Arial', 14))
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow('Password:', self.password_input)

        self.mobileNo_input = QLineEdit()
        self.mobileNo_input.setFont(QFont('Arial', 14))
        form_layout.addRow('Mobile Number:', self.mobileNo_input)

        self.main_layout.addLayout(form_layout)

        self.register_button = QPushButton('Register')
        self.register_button.setFont(QFont('Arial', 14))
        self.register_button.clicked.connect(self.handle_registration)
        self.main_layout.addWidget(self.register_button)

    def handle_registration(self):
        username = self.username_input.text()
        password = self.password_input.text()
        mobileNo = self.mobileNo_input.text()
        response = requests.post('http://127.0.0.1:5000/register', json={'username': username, 'password': password,'mobile_number':mobileNo})

        if response.status_code == 200:
            QMessageBox.information(self, 'Success', 'User registered successfully!')
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Registration failed.')


# class MainMenuWindow(QWidget):
#     def __init__(self, user_id):
#         super().__init__()
#         self.user_id = user_id
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Cinema Hall POS - Main Menu')
#         self.setGeometry(100, 100, 800, 600)
#
#         self.setStyleSheet("""
#             QWidget {
#                 background-color: #2c3e50;
#                 color: white;
#                 font-family: Arial, sans-serif;
#             }
#             QPushButton {
#                 background-color: #2980b9;
#                 color: white;
#                 border: none;
#                 padding: 10px;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #3498db;
#             }
#         """)
#
#         self.main_layout = QVBoxLayout()
#         self.setLayout(self.main_layout)
#
#         self.header_label = QLabel('Welcome to Cinema Hall POS')
#         self.header_label.setFont(QFont('Arial', 24))
#         self.header_label.setAlignment(Qt.AlignCenter)
#         self.main_layout.addWidget(self.header_label)
#
#         self.now_showing_button = QPushButton('Now Showing')
#         self.now_showing_button.setFont(QFont('Arial', 14))
#         self.now_showing_button.clicked.connect(self.show_now_showing)
#         self.main_layout.addWidget(self.now_showing_button)
#
#         self.coming_soon_button = QPushButton('Coming Soon')
#         self.coming_soon_button.setFont(QFont('Arial', 14))
#         self.main_layout.addWidget(self.coming_soon_button)
#
#     def show_now_showing(self):
#         response = requests.get('http://127.0.0.1:5000/movies')
#         if response.status_code == 200:
#             movies = response.json()
#             self.display_movies(movies[:5])  # Display the first 5 movies
#         else:
#             QMessageBox.warning(self, 'Error', 'Failed to fetch movie list.')
#
#     def display_movies(self, movies):
#         self.movie_layout = QGridLayout()
#         row = 0
#         col = 0
#
#         for movie in movies:
#             movie_widget = QWidget()
#             movie_layout = QVBoxLayout()
#             movie_widget.setLayout(movie_layout)
#
#             poster_label = QLabel()
#             pixmap = QPixmap()
#             pixmap.loadFromData(requests.get(movie['poster_url']).content)
#             poster_label.setPixmap(pixmap.scaled(150, 200, Qt.KeepAspectRatio))
#
#             title_label = QLabel(movie['title'])
#             title_label.setFont(QFont('Arial', 14))
#             title_label.setAlignment(Qt.AlignCenter)
#
#             buy_button = QPushButton('Buy Ticket')
#             buy_button.setFont(QFont('Arial', 12))
#             buy_button.clicked.connect(lambda checked, movie_id=movie['id']: self.buy_ticket(movie_id))
#
#             movie_layout.addWidget(poster_label)
#             movie_layout.addWidget(title_label)
#             movie_layout.addWidget(buy_button)
#
#             self.movie_layout.addWidget(movie_widget, row, col)
#             col += 1
#             if col > 2:  # 3 movies per row
#                 col = 0
#                 row += 1
#
#         self.main_layout.addLayout(self.movie_layout)
#
#     def buy_ticket(self, movie_id):
#         # Handle ticket buying logic here
#         QMessageBox.information(self, 'Info', f'Buying ticket for movie ID: {movie_id}')


# class MainMenuWindow(QWidget):
#     def __init__(self, user_id):
#         super().__init__()
#         self.user_id = user_id
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Cinema Hall POS - Main Menu')
#         self.setGeometry(100, 100, 600, 400)
#
#         self.setStyleSheet("""
#             QWidget {
#                 background-color: #2c3e50;
#                 color: white;
#                 font-family: Arial, sans-serif;
#             }
#             QPushButton {
#                 background-color: #2980b9;
#                 color: white;
#                 border: none;
#                 padding: 10px;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #3498db;
#             }
#         """)
#
#         self.main_layout = QVBoxLayout()
#         self.setLayout(self.main_layout)
#
#         self.header_label = QLabel('Welcome to Cinema Hall POS')
#         self.header_label.setFont(QFont('Arial', 24))
#         self.header_label.setAlignment(Qt.AlignCenter)
#         self.main_layout.addWidget(self.header_label)
#
#         self.now_showing_button = QPushButton('Now Showing')
#         self.now_showing_button.setFont(QFont('Arial', 14))
#         self.main_layout.addWidget(self.now_showing_button)
#
#         self.coming_soon_button = QPushButton('Coming Soon')
#         self.coming_soon_button.setFont(QFont('Arial', 14))
#         self.main_layout.addWidget(self.coming_soon_button)
#region mainMenu working prototype
# class MainMenuWindow(QWidget):
#     def __init__(self, user_id):
#         super().__init__()
#         self.user_id = user_id
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Cinema Hall POS - Main Menu')
#         self.setGeometry(100, 100, 800, 600)
#
#         self.setStyleSheet("""
#             QWidget {
#                 background-color: #2c3e50;
#                 color: white;
#                 font-family: Arial, sans-serif;
#             }
#             QPushButton {
#                 background-color: #2980b9;
#                 color: white;
#                 border: none;
#                 padding: 10px;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #3498db;
#             }
#         """)
#
#         self.main_layout = QVBoxLayout()
#         self.setLayout(self.main_layout)
#
#         self.header_label = QLabel('Welcome to Cinema Hall POS')
#         self.header_label.setFont(QFont('Arial', 24))
#         self.header_label.setAlignment(Qt.AlignCenter)
#         self.main_layout.addWidget(self.header_label)
#
#         self.fetch_movies_and_display()
#
#     def fetch_movies_and_display(self):
#         response = requests.get('http://127.0.0.1:5000/movies')
#         if response.status_code == 200:
#             movies = response.json()
#             self.display_movies(movies[:5])  # Display the first 5 movies
#         else:
#             QMessageBox.warning(self, 'Error', 'Failed to fetch movie list.')
#
#     def display_movies(self, movies):
#         self.movie_layout = QGridLayout()
#         row = 0
#         col = 0
#
#         for movie in movies:
#             movie_widget = QWidget()
#             movie_layout = QVBoxLayout()
#             movie_widget.setLayout(movie_layout)
#
#             poster_label = QLabel()
#             pixmap = QPixmap()
#             pixmap.loadFromData(requests.get(movie['poster_url']).content)
#             poster_label.setPixmap(pixmap.scaled(150, 200, Qt.KeepAspectRatio))
#
#             title_label = QLabel(movie['title'])
#             title_label.setFont(QFont('Arial', 14))
#             title_label.setAlignment(Qt.AlignCenter)
#
#             buy_button = QPushButton('Buy Ticket')
#             buy_button.setFont(QFont('Arial', 12))
#             buy_button.clicked.connect(lambda checked, movie_id=movie['id']: self.buy_ticket(movie_id))
#
#             movie_layout.addWidget(poster_label)
#             movie_layout.addWidget(title_label)
#             movie_layout.addWidget(buy_button)
#
#             self.movie_layout.addWidget(movie_widget, row, col)
#             col += 1
#             if col > 2:  # 3 movies per row
#                 col = 0
#                 row += 1
#
#         self.main_layout.addLayout(self.movie_layout)
#
#     def buy_ticket(self, movie_id):
#         # Handle ticket buying logic here
#         QMessageBox.information(self, 'Info', f'Buying ticket for movie ID: {movie_id}')
#endregion

class MainMenuWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cinema Hall POS - Main Menu')
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: white;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Header layout for date and time
        self.header_layout = QHBoxLayout()
        self.main_layout.addLayout(self.header_layout)

        self.time_label = QLabel()
        self.time_label.setFont(QFont('Arial', 12))
        self.header_layout.addWidget(self.time_label)

        self.date_label = QLabel()
        self.date_label.setFont(QFont('Arial', 12))
        self.header_layout.addWidget(self.date_label, alignment=Qt.AlignRight)

        self.header_label = QLabel('Welcome to Cinema Hall POS')
        self.header_label.setFont(QFont('Arial', 24))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.header_label)

        self.update_date_time()
        self.fetch_movies_and_display()

        # Timer to update the time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)

    def update_date_time(self):
        current_datetime = QDateTime.currentDateTime()
        self.time_label.setText(current_datetime.toString("hh:mm:ss AP"))
        self.date_label.setText(current_datetime.toString("dddd, MMMM d, yyyy"))

    def fetch_movies_and_display(self):
        response = requests.get('http://127.0.0.1:5000/movies')
        if response.status_code == 200:
            movies = response.json()
            self.display_movies(movies[:5])  # Display the first 5 movies
        else:
            QMessageBox.warning(self, 'Error', 'Failed to fetch movie list.')

    def fetch_showtimes(self, movie_id):
        response = requests.get(f'http://127.0.0.1:5000/showtimes/{movie_id}')
        if response.status_code == 200:
            data = response.json()
            showtimes = data['showtimes']  # Access the nested 'showtimes' list
            return [showtime['showtime'] for showtime in showtimes]
        else:
            return []

    def display_movies(self, movies):
        self.movie_layout = QGridLayout()
        row = 0
        col = 0

        for movie in movies:
            movie_widget = QWidget()
            movie_layout = QVBoxLayout()
            movie_widget.setLayout(movie_layout)

            showtimes = self.fetch_showtimes(movie['id'])
            showtimes_label = QLabel(f"Showtimes: {', '.join(showtimes)}")
            showtimes_label.setFont(QFont('Arial', 10))
            showtimes_label.setAlignment(Qt.AlignCenter)

            poster_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(movie['poster_url']).content)
            poster_label.setPixmap(pixmap.scaled(150, 200, Qt.KeepAspectRatio))

            title_label = QLabel(movie['title'])
            title_label.setFont(QFont('Arial', 14))
            title_label.setAlignment(Qt.AlignCenter)

            buy_button = QPushButton('Buy Ticket')
            buy_button.setFont(QFont('Arial', 12))
            buy_button.clicked.connect(lambda checked, movie_id=movie['id']: self.buy_ticket(movie_id))

            movie_layout.addWidget(showtimes_label)
            movie_layout.addWidget(poster_label)
            movie_layout.addWidget(title_label)
            movie_layout.addWidget(buy_button)

            self.movie_layout.addWidget(movie_widget, row, col)
            col += 1
            if col > 2:  # 3 movies per row
                col = 0
                row += 1

        self.main_layout.addLayout(self.movie_layout)
    # Assuming MainMenuWindow inherits from QWidget or similar
    def buy_ticket(self, movie_id):
        # Handle ticket buying logic here
        QMessageBox.information(self, 'Info', f'Buying ticket for movie ID: {movie_id}')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

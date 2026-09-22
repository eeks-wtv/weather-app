import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QFrame, QDesktopWidget, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weather App")
        self.setFixedSize(420, 560)

        # Outer layout just holds the card, centered with margins
        outer = QVBoxLayout()
        outer.setContentsMargins(30, 30, 30, 30)

        card = QFrame(self)
        card.setObjectName("card")

        vbox = QVBoxLayout(card)
        vbox.setSpacing(16)
        vbox.setContentsMargins(25, 30, 25, 30)

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addSpacing(10)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        outer.addWidget(card)
        self.setLayout(outer)

        for w in (self.city_label, self.city_input, self.temperature_label,
                  self.emoji_label, self.description_label):
            w.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Drop shadow behind the card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 90))
        card.setGraphicsEffect(shadow)

        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4facfe, stop:1 #00f2fe
                );
                font-family: 'Segoe UI';
            }
            QFrame#card {
                background-color: white;
                border-radius: 20px;
            }
            QLabel#city_label {
                font-size: 22px;
                font-weight: bold;
                color: #333;
                background: transparent;
            }
            QLineEdit#city_input {
                font-size: 22px;
                padding: 8px;
                border-radius: 10px;
                border: 1px solid #ccc;
                background-color: #f5f7fa;
                color: #333;
            }
            QPushButton#get_weather_button {
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
                background-color: #4facfe;
                color: white;
                border: none;
            }
            QPushButton#get_weather_button:hover {
                background-color: #3d94e0;
            }
            QPushButton#get_weather_button:pressed {
                background-color: #2f7dc4;
            }
            QLabel#temperature_label {
                font-size: 48px;
                font-weight: bold;
                color: #222;
                background: transparent;
            }
            QLabel#emoji_label {
                font-size: 70px;
                font-family: 'Segoe UI Emoji';
                background: transparent;
            }
            QLabel#description_label {
                font-size: 22px;
                font-style: italic;
                color: #555;
                background: transparent;
                font-weight: bold;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_weather(self):
        api_key = "ca7edb3789f330a080251cbcd58d685f"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\ncheck your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("Not Found\nCity not found")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nYour request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"RequestError\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 22px; color: #c0392b;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setStyleSheet("font-size: 48px; color: #222;")
        self.temperature_label.setText(f"{temperature_c:.0f}°C")

        self.description_label.setStyleSheet("font-size: 22px; font-style: italic; color: #555;")
        self.description_label.setText(f"{weather_description}")

        self.emoji_label.setText(self.get_weather_emoji(weather_id))

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌥️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "😶‍🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
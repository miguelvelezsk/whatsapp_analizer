import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from utils.emojis import emoji_to_filename
from services.analizer import analize_chat
import random
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QTimer
from pathlib import Path

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        #Music
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        #Music Path
        music_path = Path(__file__).parent / '..' / 'music' / 'Hostage.mp3'
        music_path = music_path.resolve()
        print(music_path)
        if music_path.exists():
            self.player.setSource(QUrl.fromLocalFile(str(music_path)))  
            self.audio_output.setVolume(1.0)
            self.player.play()
            QTimer.singleShot(15000, self.player.stop)
            print(f"Reproduciendo {music_path}")
        else:
            print("No existe la ruta")

        # Window configuration
        self.setWindowTitle("Amor en datos 💕")
        self.setGeometry(100, 100, 450, 230)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.center()
        self.analysis = None

        # Layout
        layout = QVBoxLayout()

        # Text label
        label = QLabel("Analiza nuestro chat de WhatsApp con amor 💑", self)
        layout.addWidget(label)

        # Buttons
        self.upload_button = QPushButton("📁 Cargar chat", self)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        self.phrases_button = QPushButton("💌 Ver frases románticas", self)
        self.phrases_button.clicked.connect(self.show_phrases)
        layout.addWidget(self.phrases_button)

        self.emojis_button = QPushButton("💙 Ver emojis más usados", self)
        self.emojis_button.clicked.connect(self.show_emojis)
        layout.addWidget(self.emojis_button)

        self.words_button = QPushButton("💬 Ver palabras más usadas", self)
        self.words_button.clicked.connect(self.show_words)
        layout.addWidget(self.words_button)

        self.random_button = QPushButton("🎰 Ver un mensaje random(Peligro💀)", self)
        self.random_button.clicked.connect(self.random_message)
        layout.addWidget(self.random_button)

        # Establecer el layout
        self.setLayout(layout)

    def center(self):
            frame = self.frameGeometry()
            center_point = QApplication.primaryScreen().availableGeometry().center()
            frame.moveCenter(center_point)
            self.move(frame.topLeft())

    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            base_path = Path(__file__).parent()
        return base_path / relative_path

    def upload_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecciona el archivo de chat")
        if file:
            self.analysis = analize_chat(file)
            QMessageBox.information(self, "Éxito", "¡Archivo cargado y analizado con éxito!")

    def show_phrases(self):
        if not self.analysis:
            return
        te_amo, te_quiero, _, _, total, _ = self.analysis
        QMessageBox.information(self, "Frases de amor 💌", f"Mensajes totales: {total}\nTe amo: {te_amo} veces\nTe quiero: {te_quiero} veces")

    def show_emojis(self):
        if not self.analysis:
            return
        _, _, emoji_freq, *_ = self.analysis
        common = emoji_freq.most_common(5)
        if not common:
            return
        print("Todos los emojis en el chat:")
        for emoji, count in emoji_freq.items():
            print(f"{emoji}: {count} veces")
        emojis, freqs = zip(*common)

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.canvas.manager.set_window_title('Emojis más usados 😍')
        bars = ax.bar(range(len(emojis)), freqs, color='blue')
        ax.set_xticks([])

        for i, emoji in enumerate(emojis):
            filename = emoji_to_filename(emoji)
            image_path = MyApp.resource_path(Path("emojis_images") / filename)

            if os.path.exists(image_path):
                img = plt.imread(image_path)
                img = OffsetImage(img, zoom=0.2)
                ab = AnnotationBbox(img, (i, freqs[i] + 10), frameon=False)
                ax.add_artist(ab)

        ax.set_title("")
        plt.tight_layout()
        plt.show()

    def show_words(self):
        if not self.analysis:
            return
        _, _, _, freq_words, *_ = self.analysis
        common = freq_words.most_common(5)
        words, freqs = zip(*common)
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.bar(words, freqs, color='blue')
        fig.canvas.manager.set_window_title('Palabras más frecuentes 📝')
        plt.title(" ")
        plt.xticks(rotation=45)
        plt.show()

    def random_message(self):
        if not self.analysis:
            return
        
        _, _, _, _, _, random_lines = self.analysis

        if not random_lines:
            QMessageBox.warning(self, "Error", "No hay mensajes disponibles.")
            return
        
        random_message = random.choice(random_lines)

        QMessageBox.information(self, "Mensaje random, ¿saldrá uno lindo? 😆", f"{random_message}")




    
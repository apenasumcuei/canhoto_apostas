import sys
import csv
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QComboBox, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon


class Lotofacil(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Bilhete da Lotofácil')
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon('D:\Downloads\lotofacil.png'))  # Define o ícone na barra de título

        self.setStyleSheet("background-color: lightyellow;")  # Define o fundo como amarelo claro

        self.buttons = []
        gridLayout = QGridLayout()

        numeros = list(range(1, 26))

        row, column = 0, 0
        for numero in numeros:
            button = QPushButton(str(numero), self)
            button.setCheckable(True)
            button.clicked[bool].connect(self.onButtonClick)
            button.setStyleSheet("background-color: white; color: purple;")  # Define o fundo como branco e texto em roxo
            button.setFixedSize(40, 30)  # Definindo um tamanho fixo para os botões
            self.buttons.append(button)
            gridLayout.addWidget(button, row, column)  # Adiciona o botão na próxima linha e na mesma coluna
            column += 1
            if column == 5:  # Limite de colunas
                column = 0
                row += 1

        self.confirmButton = QPushButton('Confirmar', self)
        self.confirmButton.clicked.connect(self.confirmSelection)
        self.confirmButton.setStyleSheet("background-color: white; color: purple;")  # Define o fundo como branco e texto em roxo

        self.showSavedButton = QPushButton('Jogos Salvos', self)
        self.showSavedButton.clicked.connect(self.showSavedGames)
        self.showSavedButton.setStyleSheet("background-color: white; color: purple;")

        layout = QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addWidget(self.confirmButton)
        layout.addWidget(self.showSavedButton)

        self.setLayout(layout)

        self.selectedNumbers = []

    def onButtonClick(self, checked):
        sender = self.sender()
        number = int(sender.text())
        if checked:
            if len(self.selectedNumbers) < 20:  # Verifica se já foram selecionados menos de 20 números
                self.selectedNumbers.append(number)
                sender.setStyleSheet("background-color: lightgreen; color: purple;")  # Destaca o botão em verde claro quando selecionado
            else:
                sender.setChecked(False)  # Desmarca o botão
                QMessageBox.warning(self, 'Aviso', 'Você pode selecionar no máximo 20 números.')
        else:
            self.selectedNumbers.remove(number)
            sender.setStyleSheet("background-color: white; color: purple;")  # Volta ao estilo original quando desselecionado

    def confirmSelection(self):
        if len(self.selectedNumbers) >= 15 and len(self.selectedNumbers) <= 20:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

            with open('jogos_salvos.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([timestamp] + self.selectedNumbers)

            QMessageBox.information(self, 'Números Selecionados', 'Números selecionados: {}'.format(self.selectedNumbers))
        else:
            QMessageBox.warning(self, 'Aviso', 'Por favor, selecione entre 15 e 20 números.')

    def showSavedGames(self):
        savedDates = self.getSavedDates()
        if savedDates:
            savedGamesDialog = QDialog(self)
            savedGamesDialog.setWindowTitle('Jogos Salvos')

            savedGamesLayout = QVBoxLayout()

            comboLabel = QLabel("Escolha a data:")
            savedGamesLayout.addWidget(comboLabel)

            comboBox = QComboBox()
            comboBox.addItems(savedDates)
            savedGamesLayout.addWidget(comboBox)

            viewButton = QPushButton("Visualizar")
            viewButton.clicked.connect(lambda: self.showSavedNumbers(comboBox.currentText(), savedGamesDialog))
            savedGamesLayout.addWidget(viewButton)

            savedGamesDialog.setLayout(savedGamesLayout)
            savedGamesDialog.exec_()
        else:
            QMessageBox.information(self, 'Jogos Salvos', 'Nenhum jogo salvo.')

    def getSavedDates(self):
        dates = []
        try:
            with open('jogos_salvos.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:
                        dates.append(row[0].split()[0])
        except FileNotFoundError:
            pass
        return dates

    def showSavedNumbers(self, selectedDate, parentDialog):
        numbersDialog = QDialog(parentDialog)
        numbersDialog.setWindowTitle(f'Números Gerados em {selectedDate}')

        layout = QHBoxLayout()
        label = QLabel()
        layout.addWidget(label)
        numbersDialog.setLayout(layout)

        with open('jogos_salvos.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    date, numbers = row[0].split()[0], row[1:]
                    if date == selectedDate:
                        numbers = ', '.join(numbers)
                        label.setText(f"Números Gerados em {selectedDate}: {numbers}")
                        break

        numbersDialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Lotofacil()
    window.show()
    sys.exit(app.exec_())

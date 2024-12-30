import os
import zipfile
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QLabel, QTextEdit, QDialog
from PyQt5.QtCore import QDir, QTime, QDate, Qt
from PyQt5.QtGui import QIcon

class BackupRestoreApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('米塔存档备份恢复工具')
        self.setWindowIcon(QIcon("data/9.ico"))
        self.setFixedSize(300, 250)  

        layout = QVBoxLayout()

        self.backup_button = QPushButton('备份', self)
        self.backup_button.clicked.connect(self.backup)
        layout.addWidget(self.backup_button)

        self.restore_button = QPushButton('恢复', self)
        self.restore_button.clicked.connect(self.restore)
        layout.addWidget(self.restore_button)

        self.open_folder_button = QPushButton('打开备份文件夹', self)
        self.open_folder_button.clicked.connect(self.open_backup_folder)
        layout.addWidget(self.open_folder_button)

        self.usage_button = QPushButton('疑难解答', self)  
        self.usage_button.clicked.connect(self.show_usage)  
        layout.addWidget(self.usage_button)

        self.note_label = QLabel('本软件不提供任何技术上的支持！', self)
        self.note_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.note_label)

        self.note_label = QLabel('版本号：0.1.1Beta', self)
        self.note_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.note_label)

        self.setLayout(layout)

    def backup(self):
        source_folder = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], 'AppData', 'LocalLow', 'AIHASTO', 'MiSideFull')
        desktop_path = QDir.homePath()
        current_time = QTime.currentTime().toString('hhmmss')
        current_date = QDate.currentDate().toString('yyyyMMdd')
        zip_filename = os.path.join(desktop_path, f'MiSideFull_backup_{current_date}_{current_time}.zip')

        if not os.path.exists(source_folder):
            QMessageBox.warning(self, '警告', '存档文件夹不存在')
            return

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=source_folder)
                    zipf.write(file_path, arcname)

        QMessageBox.information(self, '成功', f'备份已保存到 {zip_filename}')

    def restore(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "选择备份文件", "", "ZIP Files (*.zip);;All Files (*)", options=options)

        if file_path:
            target_folder = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], 'AppData', 'LocalLow', 'AIHASTO', 'MiSideFull')

            with zipfile.ZipFile(file_path, 'r') as zipf:
                zipf.extractall(target_folder)

            QMessageBox.information(self, '成功', f'备份已恢复到 {target_folder}')

    def open_backup_folder(self):
        desktop_path = QDir.homePath()
        if os.path.exists(desktop_path):
            os.startfile(desktop_path)
        else:
            QMessageBox.warning(self, '警告', '桌面路径不存在')

    def show_usage(self):
        usage_dialog = QDialog(self)
        usage_dialog.setWindowTitle('使用须知')
        usage_dialog.setFixedSize(400, 300)

        layout = QVBoxLayout()

        usage_text = QTextEdit(self)
        usage_text.setReadOnly(True)
        usage_text.setPlainText("""
疑难解答：
----------------
----空内容----
----------------
        """)

        layout.addWidget(usage_text)
        usage_dialog.setLayout(layout)
        usage_dialog.exec_()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = BackupRestoreApp()
    ex.show()
    sys.exit(app.exec_())
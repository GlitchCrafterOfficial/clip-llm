import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QLineEdit, QTextEdit, QFormLayout,
                            QPushButton, QSlider, QSpinBox, QDoubleSpinBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class CliLLMConfig(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_file_path = self.get_config_path()
        self.initUI()
        self.setDarkMode()
        # Cargar la configuración después de inicializar la UI
        self.load_config()
        
    def get_config_path(self):
        """Determina la ruta del archivo de configuración según el SO"""
        home_dir = os.path.expanduser("~")  # Funciona en Windows y Linux
        config_dir = os.path.join(home_dir, ".clillm")
        
        # Crear el directorio si no existe
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        return os.path.join(config_dir, "config.json")
        
    def initUI(self):
        self.setWindowTitle('CliLLM Configuration')
        self.setGeometry(100, 100, 500, 500)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Crear pestañas
        tabs = QTabWidget()
        tab_basic = QWidget()
        tab_advanced = QWidget()
        
        tabs.addTab(tab_basic, "Configuración Básica")
        tabs.addTab(tab_advanced, "Configuración Avanzada")
        
        # Configurar pestaña básica
        self.setup_basic_tab(tab_basic)
        
        # Configurar pestaña avanzada
        self.setup_advanced_tab(tab_advanced)
        
        # Añadir pestañas al layout principal
        main_layout.addWidget(tabs)
        
        # Botones de guardar y cancelar
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Guardar")
        cancel_button = QPushButton("Cancelar")
        
        save_button.clicked.connect(self.save_config)
        cancel_button.clicked.connect(self.close)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Mostrar ruta de configuración
        config_path_label = QLabel(f"Configuración: {self.config_file_path}")
        config_path_label.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(config_path_label)
    
    def setup_basic_tab(self, tab):
        layout = QFormLayout(tab)
        layout.setSpacing(15)
        
        # LLM Provider
        self.provider_combo = QComboBox()
        providers = [
            {"provider": "OpenAI", "value": "OPENAI_API_KEY"},
            {"provider": "Google AI Studio", "value": "GEMINI_API_KEY"},
            {"provider": "Anthropic", "value": "ANTHROPIC_API_KEY"},
            {"provider": "Mistral AI", "value": "MISTRAL_API_KEY"},
            {"provider": "Cohere", "value": "COHERE_API_KEY"}
        ]
        
        for p in providers:
            self.provider_combo.addItem(p["provider"], p["value"])
            
        provider_label = QLabel("LLM Provider:")
        layout.addRow(provider_label, self.provider_combo)
        
        # ModelID
        self.model_id = QLineEdit()
        model_label = QLabel("ModelID:")
        model_desc = QLabel("Es la id del modelo, ej. 'gemini-flash-2.0', 'gpt-4', etc.")
        model_desc.setStyleSheet("color: gray; font-size: 10px;")
        
        layout.addRow(model_label, self.model_id)
        layout.addRow("", model_desc)
        
        # ApiKey
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.Password)
        api_label = QLabel("ApiKey:")
        layout.addRow(api_label, self.api_key)
        
        # Initial Prompt
        self.initial_prompt = QTextEdit()
        prompt_label = QLabel("Initial Prompt:")
        prompt_desc = QLabel("Es el prompt inicial para generar un mensaje al usuario")
        prompt_desc.setStyleSheet("color: gray; font-size: 10px;")
        
        layout.addRow(prompt_label, self.initial_prompt)
        layout.addRow("", prompt_desc)
    
    def setup_advanced_tab(self, tab):
        layout = QFormLayout(tab)
        layout.setSpacing(15)
        
        # Temperatura
        temp_layout = QHBoxLayout()
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setRange(0, 100)
        self.temp_slider.setValue(70)
        
        self.temp_value = QDoubleSpinBox()
        self.temp_value.setRange(0.0, 1.0)
        self.temp_value.setSingleStep(0.01)
        self.temp_value.setValue(0.7)
        
        # Conectar slider y spinbox
        self.temp_slider.valueChanged.connect(lambda v: self.temp_value.setValue(v/100))
        self.temp_value.valueChanged.connect(lambda v: self.temp_slider.setValue(int(v*100)))
        
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_value)
        
        layout.addRow("Temperatura:", temp_layout)
        
        # Top P
        top_p_layout = QHBoxLayout()
        self.top_p_slider = QSlider(Qt.Horizontal)
        self.top_p_slider.setRange(0, 100)
        self.top_p_slider.setValue(95)
        
        self.top_p_value = QDoubleSpinBox()
        self.top_p_value.setRange(0.0, 1.0)
        self.top_p_value.setSingleStep(0.01)
        self.top_p_value.setValue(0.95)
        
        self.top_p_slider.valueChanged.connect(lambda v: self.top_p_value.setValue(v/100))
        self.top_p_value.valueChanged.connect(lambda v: self.top_p_slider.setValue(int(v*100)))
        
        top_p_layout.addWidget(self.top_p_slider)
        top_p_layout.addWidget(self.top_p_value)
        
        layout.addRow("Top P:", top_p_layout)
        
        # Top K
        top_k_layout = QHBoxLayout()
        self.top_k_slider = QSlider(Qt.Horizontal)
        self.top_k_slider.setRange(0, 100)
        self.top_k_slider.setValue(40)
        
        self.top_k_value = QSpinBox()
        self.top_k_value.setRange(0, 100)
        self.top_k_value.setValue(40)
        
        self.top_k_slider.valueChanged.connect(self.top_k_value.setValue)
        self.top_k_value.valueChanged.connect(self.top_k_slider.setValue)
        
        top_k_layout.addWidget(self.top_k_slider)
        top_k_layout.addWidget(self.top_k_value)
        
        layout.addRow("Top K:", top_k_layout)
        
        # Max Tokens
        max_tokens_layout = QHBoxLayout()
        self.max_tokens_slider = QSlider(Qt.Horizontal)
        self.max_tokens_slider.setRange(100, 8000)
        self.max_tokens_slider.setValue(1000)
        
        self.max_tokens_value = QSpinBox()
        self.max_tokens_value.setRange(100, 8000)
        self.max_tokens_value.setValue(1000)
        
        self.max_tokens_slider.valueChanged.connect(self.max_tokens_value.setValue)
        self.max_tokens_value.valueChanged.connect(self.max_tokens_slider.setValue)
        
        max_tokens_layout.addWidget(self.max_tokens_slider)
        max_tokens_layout.addWidget(self.max_tokens_value)
        
        layout.addRow("Max Tokens:", max_tokens_layout)
    
    def setDarkMode(self):
        # Configuración del modo oscuro
        app = QApplication.instance()
        
        dark_palette = QPalette()
        
        # Colores para el tema oscuro
        dark_color = QColor(45, 45, 45)
        disabled_color = QColor(70, 70, 70)
        text_color = QColor(210, 210, 210)
        highlight_color = QColor(42, 130, 218)
        
        # Configuración de la paleta
        dark_palette.setColor(QPalette.Window, dark_color)
        dark_palette.setColor(QPalette.WindowText, text_color)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, dark_color)
        dark_palette.setColor(QPalette.ToolTipBase, dark_color)
        dark_palette.setColor(QPalette.ToolTipText, text_color)
        dark_palette.setColor(QPalette.Text, text_color)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, disabled_color)
        dark_palette.setColor(QPalette.Button, dark_color)
        dark_palette.setColor(QPalette.ButtonText, text_color)
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, disabled_color)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, highlight_color)
        dark_palette.setColor(QPalette.Highlight, highlight_color)
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        dark_palette.setColor(QPalette.Disabled, QPalette.HighlightedText, disabled_color)
        
        app.setPalette(dark_palette)
        
        # Estilos adicionales
        app.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3A3A3A;
                background-color: #2D2D2D;
            }
            QTabBar::tab {
                background-color: #1E1E1E;
                color: #AAAAAA;
                padding: 8px 15px;
                margin: 2px;
                border: 1px solid #3A3A3A;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3A3A3A;
                color: #FFFFFF;
            }
            QTabBar::tab:hover {
                background-color: #333333;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #1A1A1A;
                border: 1px solid #3A3A3A;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #2A82DA;
                color: white;
                border: none;
                padding: 8px 15px;
                margin: 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3A92EA;
            }
            QPushButton:pressed {
                background-color: #1A72CA;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #1A1A1A;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2A82DA;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QDoubleSpinBox, QSpinBox {
                background-color: #1A1A1A;
                border: 1px solid #3A3A3A;
                padding: 5px;
                border-radius: 3px;
                width: 70px;
            }
        """)
    
    def save_config(self):
        """Guarda la configuración en un archivo JSON en el directorio home"""
        config = {
            "provider": {
                "name": self.provider_combo.currentText(),
                "value": self.provider_combo.currentData()
            },
            "model_id": self.model_id.text(),
            "api_key": self.api_key.text(),
            "initial_prompt": self.initial_prompt.toPlainText(),
            "advanced": {
                "temperature": self.temp_value.value(),
                "top_p": self.top_p_value.value(),
                "top_k": self.top_k_value.value(),
                "max_tokens": self.max_tokens_value.value()
            }
        }
        
        try:
            with open(self.config_file_path, 'w') as f:
                json.dump(config, f, indent=4)
                
            QMessageBox.information(self, "Éxito", 
                                   f"Configuración guardada exitosamente en:\n{self.config_file_path}")
            # Cerrar la ventana
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                                f"Error al guardar la configuración: {str(e)}")
    
    def load_config(self):
        """Carga la configuración desde el archivo JSON si existe"""
        if not os.path.exists(self.config_file_path):
            print(f"No se encontró archivo de configuración en: {self.config_file_path}")
            return
            
        try:
            print(f"Cargando configuración desde: {self.config_file_path}")
            with open(self.config_file_path, 'r') as f:
                config = json.load(f)
                
            # Cargar valores básicos
            provider_name = config.get("provider", {}).get("name", "")
            print(f"Cargando proveedor: {provider_name}")
            index = self.provider_combo.findText(provider_name)
            if index >= 0:
                self.provider_combo.setCurrentIndex(index)
                print(f"Proveedor seleccionado: {provider_name}")
            else:
                print(f"No se encontró el proveedor: {provider_name}")
                
            self.model_id.setText(config.get("model_id", ""))
            self.api_key.setText(config.get("api_key", ""))
            self.initial_prompt.setPlainText(config.get("initial_prompt", ""))
            print("Configuración básica cargada")
            
            # Cargar valores avanzados
            advanced = config.get("advanced", {})
            
            temp = advanced.get("temperature", 0.7)
            self.temp_value.setValue(temp)
            self.temp_slider.setValue(int(temp * 100))
            
            top_p = advanced.get("top_p", 0.95)
            self.top_p_value.setValue(top_p)
            self.top_p_slider.setValue(int(top_p * 100))
            
            top_k = advanced.get("top_k", 40)
            self.top_k_value.setValue(top_k)
            self.top_k_slider.setValue(top_k)
            
            max_tokens = advanced.get("max_tokens", 1000)
            self.max_tokens_value.setValue(max_tokens)
            self.max_tokens_slider.setValue(max_tokens)
            
            print("Configuración avanzada cargada")

        except Exception as e:
            print(f"Error al cargar la configuración: {str(e)}")
            QMessageBox.warning(self, "Advertencia", 
                               f"Error al cargar la configuración: {str(e)}")

def main():
    app = QApplication(sys.argv)
    ex = CliLLMConfig()
    ex.show()
    sys.exit(app.exec_())
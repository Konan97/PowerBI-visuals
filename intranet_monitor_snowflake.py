import time
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, 
                             QFormLayout, QLineEdit, QTextEdit, QVBoxLayout)
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon

# Only needed for access to command line arguments
import sys

import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col
 
import pandas as pd
from snowflake.snowpark import Session

class snowflakeConnection(object):
    def __init__(self, user_input, mix_number):
        self.user_input = user_input
        self.mix_number = mix_number

    def getConnection(self):
        connections = {"account": "VOLVOCARS-MANUFACTURINGANALYTICS",
            "authenticator": "externalbrowser",
            "role": "SELF_SERVICE_USER",
            "warehouse": "REPORTING",
            "database": "VCC",
            "schema": "PROD_CONTROL"}
        

        connection_parameters = {
            "account": connections['account'],
            "user": self.user_input,
            "role": connections['role'],
            "database": connections['database'],
            "schema": connections['schema'],
            "warehouse": connections['warehouse'],
            "authenticator": connections['authenticator']
            
        }
        session = Session.builder.configs(connection_parameters).create()
        return session

    def getTable(self, session: snowpark.Session, tableName: str, BODY_NUM) -> pd.DataFrame:
        
        if tableName == 'VCC.PROD_CONTROL.ORDER_EVENTS':
            filter_cols = ['"MIX_NUMBER"', '"BODY_NUMBER"']
            dataframe = session.table(tableName)\
                .filter(
                    (col('"MIX_NUMBER"') == self.mix_number)
                ).select(filter_cols)
            
        elif tableName == 'VCC.PROD_CONTROL.BODY_EVENTS':
            filter_cols = ['"REGISTRATION_POINT"', '"REGISTRATION_POINT_DESCRIPTION"', '"BODY_NUMBER"',
                    '"TOPCOAT_COLOR_DESCRIPTION"', '"MAIN_TYPE_DESCRIPTION"', '"LOCAL_UPDATE_TIMESTAMP"']
            
            dataframe = session.table(tableName)\
                .filter(
                    #(col('""').isNotNull()) &
                    #(col('"Attribute"').like('%SN SWDL%')) &
                    #(col('""').like('%$%')) &
                    (col('"BODY_NUMBER"') == BODY_NUM)
                ).select(filter_cols)
    
        # convert to Pandas for analysis 
        data = dataframe.to_pandas()
        return data
        
class WorkerThread:
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run_task(self):
        """Long-running task."""
        for i in range(5):
            time.sleep(1)
            self.progress.emit(i + 1)
        self.finished.emit()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Factory MIX Monitor")
        self.setGeometry(200, 200, 600, 400)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Snowflake Credentials form
        self.form_layout = QFormLayout()
        self.user_account = QLineEdit()
        self.form_layout.addRow("Snowflake Account:", self.user_account)
        self.mix_input = QLineEdit()
        self.form_layout.addRow("Enter 7-digit MIX Number:", self.mix_input)
        
        # Result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.form_layout.addRow("Results:", self.result_display)
        # Process Button
        self.process_button = QPushButton("Start Monitoring")
        self.process_button.clicked.connect(self.start_monitoring)

        # Status Bar
        self.status_bar = self.statusBar()
        self.setStatusBar(self.status_bar)

        # Main layout assembly
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.process_button)
    
    def start_monitoring(self):
        try: 
            mix_number = self.mix_input.text()
            if len(mix_number) != 7 or not mix_number.isdigit():
                raise ValueError("MIX number must be exactly 7 digits.")
            else:
                
                snowflakeConnection_instance = snowflakeConnection(self.user_account.text(), mix_number)
                session = snowflakeConnection_instance.getConnection()
                car_fyon = snowflakeConnection_instance.getTable(session, 'VCC.PROD_CONTROL.ORDER_EVENTS', None)
                
                while True:
                    data = snowflakeConnection_instance.getTable(session, 'VCC.PROD_CONTROL.BODY_EVENTS', car_fyon['BODY_NUMBER'].values[0])
                    # self.result_display.append(data.to_string())
                    # Check if the car has reached the final registration point
                    if (data['REGISTRATION_POINT'] == '31550').any():
                        self.result_display.append(f"MIX {mix_number} has reached the registration point:")
                        break
                    else:
                        # get the latest status
                        latest_loc = data.loc[data['LOCAL_UPDATE_TIMESTAMP'] == data['LOCAL_UPDATE_TIMESTAMP'].max()]
                        self.result_display.append(f"MIX {mix_number} is still in production. Current status:\n{latest_loc.to_string()}\n")
                        time.sleep(10)  # Simulate some processing time
                        

                
                
                
                self.statusBar().showMessage("Monitoring started successfully.")
        except Exception as e:
            if str(e)[:5] == "25001":
                self.statusBar().showMessage("Snowflake connection error. Please check your credentials.")
            else:
                self.statusBar().showMessage(str(e))
    
    @pyqtSlot()
    def start_task(self):

        self.status_label.setText("Task started...")
        self.progress_bar.setValue(0)

        self.worker_thread = QThread()
        self.worker = WorkerThread()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run_task)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.task_finished)

        self.thread.start()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    window = MainApp()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
    # window.setWindowIcon(QIcon('favicon.ico'))
    # Start the event loop.
    app.exec()

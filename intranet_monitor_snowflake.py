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

        
class WorkerThread(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)

    is_running = True

    def __init__(self, user_input, mix_number):
        self.user_input = user_input
        self.mix_number = mix_number
        self.conn = None
        self.session = None

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
    

    @pyqtSlot()
    def run_task(self):
        """Long-running task executed inside the worker thread.

        Uses self.user_input and self.mix_number (provided at construction).
        Creates the Snowpark Session on this thread, polls for BODY_EVENTS,
        emits `progress` updates and `finished` when done. Ensures the
        session is closed in a finally block.
        """
        # Defensive defaults
        mix_number = getattr(self, 'mix_number', None)
        user_input = getattr(self, 'user_input', None)

        if not mix_number:
            self.finished.emit('Missing mix number for monitoring.')
            return

        # Create session on worker thread
        try:
            self.session = self.getConnection()
        except Exception as e:
            self.finished.emit(f'Failed to create Snowflake session: {e}')
            return

        if not self.session:
            self.finished.emit('Failed to connect to Snowflake.')
            return

        # Optionally fetch the ORDER_EVENTS row for the mix to get the body number
        try:
            car_fyon = self.getTable(self.session, 'VCC.PROD_CONTROL.ORDER_EVENTS', None)
        except Exception as e:
            # emit error and close session in finally
            self.finished.emit(f'Failed to fetch order events: {e}')
            try:
                self.session.close()
            except Exception:
                pass
            self.session = None
            return

        try:
            # Main polling loop
            while getattr(self, 'is_running', True):
                try:
                    body_number = None
                    # Support a couple of shapes for car_fyon
                    if isinstance(car_fyon, dict) and 'BODY_NUMBER' in car_fyon:
                        body_number = car_fyon['BODY_NUMBER']
                        if hasattr(body_number, 'values'):
                            body_number = body_number.values[0]
                    else:
                        # assume pandas DataFrame / Series-like
                        body_number = car_fyon['BODY_NUMBER'].values[0]

                    data = self.getTable(self.session, 'VCC.PROD_CONTROL.BODY_EVENTS', body_number)
                except Exception as query_err:
                    # transient query error: emit progress and retry
                    self.progress.emit(f'Query error: {query_err}')
                    time.sleep(5)
                    continue

                # Check final registration point
                try:
                    if (data['REGISTRATION_POINT'] == '31550').any():
                        self.progress.emit(f'MIX {mix_number} has reached the registration point.')
                        self.is_running = False
                        self.finished.emit(f'MIX {mix_number} monitoring finished.')
                        break
                    else:
                        latest_loc = data.loc[data['LOCAL_UPDATE_TIMESTAMP'] == data['LOCAL_UPDATE_TIMESTAMP'].max()]
                        self.progress.emit(f'MIX {mix_number} is still in production. Current status:\n{latest_loc.to_string()}\n')
                except Exception as proc_err:
                    self.progress.emit(f'Data processing error: {proc_err}')

                # Sleep with interrupt checks
                for _ in range(10):
                    if not getattr(self, 'is_running', False):
                        break
                    time.sleep(1)

        except Exception as e:
            self.finished.emit(f'Unexpected error during monitoring: {e}')
        finally:
            if self.session is not None:
                try:
                    self.session.close()
                except Exception:
                    pass
                self.session = None

    @pyqtSlot()
    def stop_task(self):
        """Stop the task."""
        self._is_running = False
        self.status_signal.emit("Task stopped.")


        


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Factory MIX Monitor")
        self.setGeometry(200, 200, 600, 400)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.status_label = QTextEdit("Status: Ready")
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
        self.start_button = QPushButton("Start Monitoring")
        self.stop_button = QPushButton("Stop Monitoring")

        main_layout.addWidget(self.start_button)
        main_layout.addWidget(self.stop_button)

        self.start_button_button.clicked.connect(self.start_task)
        self.stop_button.clicked.connect(self.stop_task)

        # Status Bar
        self.status_bar = self.statusBar()
        self.setStatusBar(self.status_bar)

        # Main layout assembly
        main_layout.addLayout(self.form_layout)

        # Threading setup
        self.worker = None
        self.worker_thread = None
    
    @pyqtSlot()
    def start_task(self):

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.status_label.setText("Task started...")

        self.worker_thread = QThread()
        self.worker = WorkerThread()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run_task)
        
        self.worker.status_signal.connect(self.update_status)
        self.worker.result_signal.connect(self.update_results)
        self.worker.finished.connect(self.task_finished)

        self.worker_thread.start()

    @pyqtSlot(str)
    def update_status(self, message):
        self.status_label.setText(message)

    @pyqtSlot(str)
    def update_results(self, message):
        self.result_display.append(message)
    
    @pyqtSlot()
    def task_finished(self):
        self.status_label.setText("Task finished.")
        self.worker_thread.quit()
        self.worker_thread.wait()

        self.worker = None
        self.worker_thread = None
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    window = MainApp()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
    # window.setWindowIcon(QIcon('favicon.ico'))
    # Start the event loop.
    app.exec()

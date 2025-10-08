import time
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, 
                             QFormLayout, QLineEdit, QTextEdit, QVBoxLayout, QProgressBar)
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QMetaObject, Qt
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

    # default signals
    is_running = True

    def __init__(self, user_input: str = None, mix_number: str = None):
        super().__init__()
        # make running an instance attribute so multiple workers don't share it
        self.is_running = True
        # Use the constructor arguments so each new WorkerThread gets current inputs
        self.user_input = user_input
        self.mix_number = mix_number
        self.conn = None
        self.session = None

    def getConnection(self, user_input=None) -> snowpark.Session:
        connections = {"account": "VOLVOCARS-MANUFACTURINGANALYTICS",
            "authenticator": "externalbrowser",
            "role": "SELF_SERVICE_USER",
            "warehouse": "REPORTING",
            "database": "VCC",
            "schema": "PROD_CONTROL"}
        

        connection_parameters = {
            "account": connections['account'],
            "user": user_input,
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
        """Long-running task executed inside the worker thread."""
        # Defensive defaults
        mix_number = getattr(self, 'mix_number', None)
        user_input = getattr(self, 'user_input', None)

        if not mix_number:
            self.finished.emit('Missing mix number for monitoring.')
            return

        # Create session on worker thread
        try:
            self.session = self.getConnection(user_input)
        except Exception as e:
            self.finished.emit(f'Failed to create Snowflake session: {e}')
            return

        if not self.session:
            self.finished.emit('Failed to connect to Snowflake.')
            return

        # Optionally fetch the ORDER_EVENTS row for the mix to get the body number
        try:
            BODY_df = self.getTable(self.session, 'VCC.PROD_CONTROL.ORDER_EVENTS', None)
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
                body_number = BODY_df['BODY_NUMBER'].values[0]
                data = self.getTable(self.session, 'VCC.PROD_CONTROL.BODY_EVENTS', body_number)

                # Check final registration point
                try:
                    if (data['REGISTRATION_POINT'] == '31550').any():
                        self.progress.emit(f'MIX {mix_number} has reached the registration point.')
                        self.is_running = False
                        break
                    else:
                        latest_loc = data.loc[data['LOCAL_UPDATE_TIMESTAMP'] == data['LOCAL_UPDATE_TIMESTAMP'].max()]

                        desc = latest_loc['REGISTRATION_POINT_DESCRIPTION'].to_string()
                        ts = latest_loc['LOCAL_UPDATE_TIMESTAMP'].to_string()
                        self.progress.emit(f"MIX {mix_number} is still in production. Current status:\n{desc}\n{ts}\n")
                        # Responsive sleep: check every 1s so stop requests are handled quickly
                        for _ in range(120):
                            if not getattr(self, 'is_running', False):
                                break
                            time.sleep(1)
                        
                except Exception as proc_err:
                    self.progress.emit(f'Data processing error: {proc_err}')
            print('Exited monitoring loop.')
            self.finished.emit(f'MIX {mix_number} monitoring finished.')

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
        """Slot to request the worker stop. Executes on the worker thread."""
        # Set the running flag so the run loop exits promptly
        self.is_running = False
        # Close session if open
        try:
            if self.session is not None:
                try:
                    self.session.close()
                except Exception:
                    pass
                self.session = None
        except Exception:
            pass


        


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
        self.start_button = QPushButton("Start Monitoring")
        self.stop_button = QPushButton("Stop Monitoring")

        # Busy indicator (indeterminate progress bar)
        self.busy_bar = QProgressBar()
        self.busy_bar.setRange(0, 0)  # indeterminate mode
        self.busy_bar.setVisible(False)

        self.start_button.clicked.connect(self.start_task)
        self.stop_button.clicked.connect(self.stop_task)

        # Status Bar
        self.status_bar = self.statusBar()
        self.setStatusBar(self.status_bar)

        # Main layout assembly
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.start_button)
        main_layout.addWidget(self.stop_button)
        main_layout.addWidget(self.busy_bar)
        # Threading setup
        self.worker = None
        self.worker_thread = None
    
    @pyqtSlot()
    def start_task(self):
        # Prevent creating a new worker if a previous thread object still exists
        if self.worker_thread is not None:
            self.status_bar.showMessage("Previous worker still shutting down. Please wait...")
            return

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.status_bar.showMessage("Task started...")
        # Show busy indicator
        try:
            self.busy_bar.setVisible(True)
        except Exception:
            pass

        self.worker_thread = QThread()

        self.worker = WorkerThread(self.user_account.text(), self.mix_input.text())
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run_task)
        self.worker.finished.connect(self.task_finished)
        # Connect worker signals
        self.worker.progress.connect(self.update_results)
        # Optionally also mirror progress to status label
        self.worker.progress.connect(self.update_status)

        self.worker_thread.start()

    @pyqtSlot()
    def stop_task(self):
        """Stop monitoring: request the worker to stop and update UI."""
        if not self.worker or not self.worker_thread:
            return
        self.worker.stop_task()
        self.worker_thread.quit()
        

        # Update UI: don't re-enable Start here; wait for task_finished to clean up
        self.status_bar.showMessage("Stopping...")
        self.busy_bar.setVisible(True)   # optional
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    @pyqtSlot(str)
    def update_status(self, message):
        self.status_bar.showMessage(message)

    @pyqtSlot(str)
    def update_results(self, message):
        self.result_display.append(message)
    
    @pyqtSlot()
    def task_finished(self):
        self.status_bar.showMessage("Task finished.")

        # Ensure thread stops and cleaned up
        if self.worker is not None:
            try:
                self.worker.deleteLater()
            except Exception:
                pass
            self.worker = None
        if self.worker_thread is not None:
            try:
                self.worker_thread.quit()
                self.worker_thread.wait()
                self.worker_thread.deleteLater()
            except Exception:
                pass
            self.worker_thread = None
        
        self.busy_bar.setVisible(False)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    window = MainApp()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
    # window.setWindowIcon(QIcon('favicon.ico'))
    # Start the event loop.
    app.exec()

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)

from connection.process_observer_server_socket import *
from view.GUI import *

if __name__ == "__main__":
    process_observer_socket_thread = threading.Thread(target=start_process_observer_server_socket)
    process_observer_socket_thread.daemon = True
    process_observer_socket_thread.start()

    GUI()

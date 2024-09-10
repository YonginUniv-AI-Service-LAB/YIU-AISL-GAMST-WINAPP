import os
import sys
import multiprocessing

from GAMST_OBSERVER.view.HomeView import *

if __name__ == '__main__':
    multiprocessing.freeze_support()

    process_observer_socket_thread = threading.Thread(target=start_process_observer_server_socket)
    process_observer_socket_thread.daemon = True
    process_observer_socket_thread.start()

    homeView = HomeView()

    # processInformationModel = ProcessInformationModel()
    # controller = HomeController(homeView)

import atexit
import json

class BaseResource(object):
    def __init__(self, args):
        """
        Load the history data.
        Save the program arguments.
        """
        self.args = args
        with open(self.history_filename, 'r') as file:
            self.history = json.load(file)
        atexit.register(self.exit_handler)

    def exit_handler(self):
        """
        Update the history data when the program terminates.
        """
        with open(self.history_filename, 'w') as file:
            json.dump(self.history, file, indent=2)

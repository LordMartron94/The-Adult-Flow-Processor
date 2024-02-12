class ConfigurationError(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        message = "There has been an error with your configuration...\n" + message + "\nFix it. Now. Really. Go fix it. You fucking jerkhead!"
        super().__init__(message)

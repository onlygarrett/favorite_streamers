class ConfigImportError(Exception):
    """ Error to be thrown when incorrect config selected """
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        return 'The selected config for upload is invalid.'
    
class ConfigInputError(Exception):
    """ Error to be thrown when incorrect config inputted """
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        return 'The input given for a new config was invalid.'
    
class ApiError(Exception):
    """ Error to be thrown when hitting the API returns bad data or wrong data sent """
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        return 'Error when retrieving Streamer data, please confirm config is correct and try again.'
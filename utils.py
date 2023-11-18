import logging
from pathlib import Path 

def create_logger(logger_name, logfolder, logfile_name):
    
    filename = create_logfile(logfolder, logfile_name)
    
    # Configure the logger to write to a file
    logging.basicConfig(
        filename=f'/home/pi/team-papa/logs/{logfolder}/{filename}.log',  # Specify the file to write logs
        level=logging.INFO,       # Set the logging level to INFO
        format='%(asctime)s [%(levelname)s] %(message)s',  # Define the log message format
    )

    LOGGER = logging.getLogger(logger_name)
    LOGGER.info(f"started up {logger_name}")

    return LOGGER


def create_logfile(logfolder, filename):
    logfile = Path("/home/pi/team-papa/logs", logfolder, f'{filename}.log')
    counter = 1
    
    new_name = filename
    while logfile.exists():
        new_name = f"{filename}_({counter})"
        logfile = Path("/home/pi/team-papa/logs", logfolder, f'{new_name}.log')
        counter += 1

    return new_name

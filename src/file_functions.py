"""Function for manipulating files"""
import os
from datetime import date
from src.config import logger


def processed_file(file_path, delete_file=False):
    """
    Create a folder processed, if not exists, create a folder with process date and copy the file to folder
    :param file_path: Processed file path
    :param delete_file: True or False for delete file after copy
    :return: None
    """
    base_path = os.getcwd()
    file_path_root = '/'.join(file_path.split('/')[:-1])
    # create folder processed if not exist
    if not os.path.exists(f'{base_path}/{file_path_root}/processed'):
        os.mkdir(f'{base_path}/{file_path_root}/processed')
    # create folder for day if not exist
    if not os.path.exists(f'{base_path}/{file_path_root}/processed/{date.today()}'):
        os.mkdir(f'{base_path}/{file_path_root}/processed/{date.today()}')

    logger.info('Moving file to processed folder ...')
    # copy file
    os.system(f'cp {base_path}/{file_path} {base_path}/{file_path_root}/processed/{date.today()}/')
    logger.info('Coped')

    if delete_file:
        logger.info('Deleting file ...')
        # delete file.
        os.remove(file_path)
        logger.info('Deleted')

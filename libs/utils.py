from libs.logger import logger


def register_sub_bp(dir_path, parent_bp):
    from libs.scanner import SourceScanner
    for _, name in SourceScanner(dir_path, r'sub_(\w+)_bp').apply_scanned_function(parent_bp):
        logger.info('Append sub blueprint <{}> for {}'.format(name, parent_bp))

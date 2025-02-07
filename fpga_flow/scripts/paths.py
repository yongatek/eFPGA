#----------------------------------------------------------------#
# Module:       paths.py
# Company:      Yongatek Microelectronics
# Author:       Ahmad Houraniah
# Version:      0.1.0
# Description:  This script is contains helper functions to get 
#               the paths of the efpga-design-flow directory and
#----------------------------------------------------------------#

import os

def get_TRISTAN_EFPGA_PATH():
    # Get the current working directory path
    try:
        dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    except Exception as e:
        print(f"Error getting TRISTAN_EFPGA_PATH: {e}")
        raise

    # Ensure the path contains the necessary part of the directory
    try:
        efpga_base_path = dir_path[:dir_path.index("eFPGA/") + len("eFPGA/")]
    except ValueError:
        print("Error: 'eFPGA/' not found in the path.")
        raise
    return efpga_base_path

def get_fabric_path():
    return os.path.join(get_TRISTAN_EFPGA_PATH(), "yonga_archs/Fabric/")

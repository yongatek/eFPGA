#!/bin/bash
set -e
source /opt/openfpga/openfpga.sh
export TRISTAN_EFPGA_PATH=$(pwd)
cd /home/openfpga_user/fpga_flow/config/	
run-task ../ --show_thread --debug
exit


rm -r ./run*
rm processed_modules_index.txt
rm results.csv
rm latest
find . -type d -name "__pycache__" -exec rm -r {} +

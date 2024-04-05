from os import path
import sys
import os
import re
import datetime

def delay_subtitle_entries(input_file, delay_seconds):
    input_dir = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    file_name_parts = input_filename.rsplit(".", 1)
    output_filename = f'{file_name_parts[0]}-delayed-by-{delay_seconds}s.{file_name_parts[1]}'
    output_file = os.path.join(input_dir, output_filename)
    
    with open(input_file, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            start_time_str, end_time_str = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', line)
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M:%S,%f')
            end_time = datetime.datetime.strptime(end_time_str, '%H:%M:%S,%f')
            start_time += datetime.timedelta(seconds=delay_seconds)
            end_time += datetime.timedelta(seconds=delay_seconds)
            new_line = f'{start_time.strftime("%H:%M:%S,%f")[:-3]} --> {end_time.strftime("%H:%M:%S,%f")[:-3]}\n'
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(output_file, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file delay_seconds")
    else:
        input_file = sys.argv[1]
        delay_seconds = int(sys.argv[2])
        delay_subtitle_entries(input_file, delay_seconds)
        output_filename = f"{os.path.join(os.path.dirname(input_file), input_file.split('.')[0])}-delayed-by-{delay_seconds}.srt"
        print(f"Subtitle file '{input_file}' delayed by {delay_seconds} seconds. New file saved as '{output_filename}'")

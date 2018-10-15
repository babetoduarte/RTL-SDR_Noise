#!/usr/bin/python3
'''
RTL-SDR Noise Floor Level Recording, v1.0
by Jorge Duarte, KI5ANA // HJ3JDG
email: KI5ANA@arrl.org // HJ3JDG@gmail.com

LICENSE: 

    RTL-SDR Noise Floor Level Recording, v1.0
    Copyright (C) 2018  Jorge A. Duarte, KI5ANA

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

DESCRIPTION:

    This program is based on the rtl_power utility, which is part of the rx_tools
    included in the librtlsdr package under Linux and MacOS.

    BEFORE RUNNING THE SCRIPT MAKE SURE librtlsdr IS INSTALLED AND RUNNING CORRECTLY!!!

    This program provides an interface to the following rtp_power script usage:

    rtl_power -f <min_freq>:<max_freq>:<bin_width> -p <ppm_correction> -g <rx_gain> -1 <output_file>

    By default it logs measurements between 144MHz and 148MHz in 500kHz increments,
    which yields 10 power measurements covering the Amateur Radio 2m band. The 
    default output filename is 'HAM_VHF_Noise.csv'. If the file doesn't exist it 
    will be created, and if it does, new measurements will be appended at the end
    of the file. 

    MIN_FREQ:

        Minimum scanning frequency. For kHz use the k suffix, for MHz use the M
        suffix (i.e. 500k, 144M).IF NO VALUE IS PROVIDED, IT WILL DEFAULT TO 144M.

    MAX_FREQ:

        Maximum scanning frequency. For kHz use the k suffix, for MHz use the M
        suffix (i.e. 500k, 144M). IF NO VALUE IS PROVIDED, IT WILL DEFAULT TO 148M.


    BIN WIDTH:

        Bin size can be in any range between 1Hz and 2.8MHz, but the total number of
        bins has to be smaller than the maximum sample rate. For kHz use the k
        suffix, for MHz use the M suffix (i.e. 500k, 144M). IF NO VALUE IS PROVIDED, 
        IT WILL DEFAULT TO 500k.

    PPM CORRECTION:

        ppm correction has to be determined apriori to running this program in
        production, in order to accurately tune to the desired frequencies. Using
        an SDR client such as GQRX or SDR# determine the ppm correction needed FOR
        EACH DONGLE, and use that value to execute this program. For the development
        dongle, this was determined to be 107ppm. IF NO VALUE IS PROVIDED, IT WILL 
        DEFAULT TO 107ppm!!!

    RX GAIN:

        RTL-SDR supports 29 different gain values in db:
            [0.0 0.9 1.4 2.7 3.7 7.7 8.7 12.5 14.4 15.7 16.6 19.7 20.7 22.9 25.4
            28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0 49.6]
        IF NO VALUE IS PROVIDED, IT WILL DEFAULT TO 28db.

    SINGLE SHOT MODE (-1):

        This argument tells the rtl_power utility to perform this measurement only
        just once, and then save it to a file. THIS PROGRAM WILL ALWAYS EXECUTE 
        rtl_power IN THIS MODE.

    OUTPUT FILE:

        The oputput file will be a CSV file containing the following columns:

        Date | Time | Hz low | Hz high | Hz step | samples | dbm | dbm | ... | Average |
'''

import subprocess
import os
import csv
import sys, getopt

def main(argv):

    n_min_f = "144M"
    n_max_f = "148M"
    n_bin_width = "500k"
    n_ppm = "107"
    n_gain = "28"
    n_output_file = "HAM_VHF_Noise.csv"

    try:
        opts, _ = getopt.getopt(argv,"hwl:f:b:p:g:o:",["lfreq=","hfreq=", "bwidth=", "ppm=", "gain=", "ofile="])
    except getopt.GetoptError:
        print("\t$python rtl-sdr_noise.py [-p <ppm_correction>] [-l <min_freq> -f <max_freq> -b <bin_width> -g <rx_gain> -o <output_file>]")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("\n\t\tRTL-SDR Noise Floor Level Recording \n USAGE: \n")
            print("\t$python rtl-sdr_noise.py [-p <ppm_correction>] [-l <min_freq> -f <max_freq> -b <bin_width> -g <rx_gain> -o <output_file>]\n\n")
            sys.exit()
        elif opt == "-w":
            print("\n\t\t GNU-GPLv3 LICENSE: \n")
            print('''
            RTL-SDR Noise Floor Level Recording, v1.0
            Copyright (C) 2018  Jorge A. Duarte, KI5ANA

            This program is free software: you can redistribute it and/or modify
            it under the terms of the GNU General Public License as published by
            the Free Software Foundation, either version 3 of the License, or
            (at your option) any later version.

            This program is distributed in the hope that it will be useful,
            but WITHOUT ANY WARRANTY; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
            GNU General Public License for more details.

            You should have received a copy of the GNU General Public License
            along with this program.  If not, see <https://www.gnu.org/licenses/>.
            ''')
            sys.exit()
        elif opt in ("-l", "--lfreq"):
            n_min_f = arg
        elif opt in ("-f", "--hfreq"):
            n_max_f = arg
        elif opt in ("-b", "--bwidth"):
            n_bin_width = arg
        elif opt in ("-p", "--ppm"):
            n_ppm = arg
        elif opt in ("-g", "--gain"):
            n_gain = arg
        elif opt in ("-o", "--ofile"):
            n_output_file = arg

    scan_noise_levels(min_f=n_min_f, max_f=n_max_f, bin_width=n_bin_width, ppm=n_ppm, gain=n_gain, output_file=n_output_file)


def scan_noise_levels(min_f="144M", max_f="148M", bin_width="500k", ppm=107, gain=28, output_file="HAM_VHF_Noise.csv"):
    cmd = ['rtl_power']

    args = ('-f ' + min_f + ':' + max_f+ ':' + bin_width + ' -p ' + str(ppm) + ' -g ' + str(gain) + ' -1 ' +'').split()
    
    output = subprocess.Popen(cmd+args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    response, _ = output.communicate()
    #print(response.decode().split('\n')[:-1])
    raw_data = response.decode().split('\n')[:-1]
    raw_data_1 = raw_data[0].split(',')
    raw_data_2 = raw_data[1].split(',')
    data_info = [str(x) for x in raw_data_1[0:3]] + [str(x) for x in raw_data_2[3:5]] + [str(int(raw_data_1[5])+int(raw_data_2[5]))]
    data_db1 = [float(x) for x in raw_data_1[6:]]
    data_db2 = [float(x) for x in raw_data_2[6:]]
    data = data_info + data_db1 + data_db2
    num_measurements = len(data[6:])
    average = round(sum(data[6:])/num_measurements,4)
    data.append(average)
    #print(data)
    file_exists = os.path.isfile(output_file)
    header = ['Date', 'Time', 'Hz low', 'Hz high', 'Hz step', 'Samples']
    for _ in range(num_measurements):
        header.append('db')
    header.append('Average')
    with open(output_file, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        if file_exists:
            wr.writerow(data)
        else:
            wr.writerow(header)
            wr.writerow(data)

if __name__ == "__main__":
    main(sys.argv[1:])

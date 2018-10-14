# RTL-SDR Noise Floor Level Recoring 

by Jorge Duarte, KI5ANA // HJ3JDG

Email: KI5ANA@arrl.org // HJ3JDG@gmail.com

Version: v1.0

## USAGE:

        $ python rtl-sdr_noise.py [-p <ppm_correction>] [-l <min_freq> -f <max_freq> -b <bin_width> -g <rx_gain> -o <output_file>]


## DESCRIPTION:

This program is based on the rtl_power utility, which is part of the rx_tools included in the librtlsdr package under Linux and MacOS. BEFORE RUNNING THE SCRIPT MAKE SURE librtlsdr IS INSTALLED AND RUNNING CORRECTLY!!! This program provides an interface to the following rtp_power script usage: rtl_power -f <min_freq>:<max_freq>:<bin_width> -p <ppm_correction> -g <rx_gain> -1 <output_file> By default it logs measurements between 144MHz and 148MHz in 500kHz increments, which yields 10 power measurements covering the Amateur Radio 2m band. The default output filename is 'HAM_VHF_Noise.csv'. If the file doesn't exist it will be created, and if it does, new measurements will be appended at the end of the file. 

### MIN_FREQ:

Minimum scanning frequency. For kHz use the k suffix, for MHz use the M suffix (i.e. 500k, 144M).IF NO VALUE IS PROVIDED, IT WILL DEFAULT TO 144M.

### MAX_FREQ:

Maximum scanning frequency. For kHz use the k suffix, for MHz use the M suffix (i.e. 500k, 144M). IF NO VALUE IS PROVIDED, IT WILL DEFAULT TO 148M.

### BIN WIDTH:

Bin size can be in any range between 1Hz and 2.8MHz, but the total number of bins has to be smaller than the maximum sample rate. For kHz use the k suffix, for MHz use the M suffix (i.e. 500k, 144M). IF NO VALUE IS PROVIDED, IT WILL DEFAULT TO 500k.

### PPM CORRECTION:

ppm correction has to be determined apriori to running this program in production, in order to accurately tune to the desired frequencies. Using an SDR client such as GQRX or SDR# determine the ppm correction needed FOR EACH DONGLE, and use that value to execute this program. For the development dongle, this was determined to be 107ppm. IF NO VALUE IS PROVIDED, IT WILL DEFAULT TO 107ppm!!!

### RX GAIN:

RTL-SDR supports 29 different gain values in db:

    [0.0 0.9 1.4 2.7 3.7 7.7 8.7 12.5 14.4 15.7 16.6 19.7 20.7 22.9 25.4 28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0 49.6]

IF NO VALUE IS PROVIDED, IT WILL DEFAULT TO 28db.

### SINGLE SHOT MODE (-1):

This argument tells the rtl_power utility to perform this measurement only just once, and then save it to a file. THIS PROGRAM WILL ALWAYS EXECUTE rtl_power IN THIS MODE.

### OUTPUT FILE:

The oputput file will be a CSV file containing the following columns:

    Date | Time | Hz low | Hz high | Hz step | samples | dbm | dbm | ... | Average |
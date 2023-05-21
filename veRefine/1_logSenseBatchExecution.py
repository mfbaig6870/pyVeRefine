import os
import subprocess
import sys

print(sys.executable)

scripts = {
    'a_logTransientThrottleFilter.py': '../outputs/logSansTt.csv',
    'b_logHitCount.py': '../outputs/logHitCount.csv',
    'c_logHitCountThreshold.py': '../outputs/logHitCountThreshold.csv',
    'd_avgAfrBins.py': '../outputs/avgAfrBins.csv',
    'e_avgTargetAfrBins.py': '../outputs/avgTargetAfrBins.csv',
    'f_avgAfrDelta.py': '../outputs/avgAfrDelta.csv',
    'g_1_correctedVeTable.py': '../outputs/correctedVeTable_g1.csv',
    'g_2_correctedVeTableHitFilter.py': '../outputs/correctedVeTable.csv',
    'h_2dSmoothing.py': '../outputs/smoothedVeTable.csv',
    'i_veTableRefPct.py': '../outputs/veTableRefPct.csv'
}

for script, output_file in scripts.items():
    # Execute the script
    subprocess.run(['python', script])

    # Check if the output file has been updated
    if os.path.exists(output_file):
        print(f'{output_file} has been updated')
    else:
        print(f'{output_file} has not been created or updated')

#!/usr/bin/env python
import sensors
import os
import time
sensors.init()
try:
    logfile = open('/tmp/temperature-log.txt','a')
    for chip in sensors.iter_detected_chips():
        logfile.write('%s at %s \n' % (chip, chip.adapter_name))
        for feature in chip:
            logfile.write('  %s: %.2f \n' % (feature.label, feature.get_value()))
            if feature.get_value() > 80: 
                print 'going down for 5 minutes.'
                logfile.write('HOTHOTHOTHOTHOTHOTHOTHOT')
                os.system('systemctl stop plexmediaserver')                
                time.sleep(300) #sleep for 5 minutes
                os.system('systemctl start plexmediaserver')
    logfile.write('\ntime: %s\n\n' % time.strftime("%H:%M:%S"))
finally:
    sensors.cleanup()


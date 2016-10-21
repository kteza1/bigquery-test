#! /usr/bin/python3
from systemd import journal
import threading
import sys
import time
import datetime

CAN_COUNT = 0
def generate_can_frames():
    global CAN_COUNT
    for i in range(200):
        #timestamp = 'TIMESTAMP=' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        timestamp = 'TIMESTAMP='+str(int(time.time() * 1000))
        can_id = 'CAN_ID='+str(410)
        CAN_COUNT += 1
        seq_num = 'SEQUENCE_NUMBER='+str(int(CAN_COUNT))
        journal.sendv('CHANNEL=canFrame',
                          can_id,
                          'DATA=100',
                          seq_num,
                          timestamp)
    print('Can burst ... COUNT = {}'.format(CAN_COUNT))
    if CAN_COUNT >= 1000000:
        return
    else:
        threading.Timer(1, generate_can_frames).start()

LSMSENSOR_COUNT = 0
def generate_lsmsensor_frames():
    global LSMSENSOR_COUNT
    for i in range(20):
        LSMSENSOR_COUNT += 1
        seq_num = 'SEQUENCE_NUMBER='+str(int(LSMSENSOR_COUNT))
        timestamp = 'TIMESTAMP='+str(int(time.time() * 1000))
        journal.sendv('CHANNEL=lsmsensor', 
                              'ACC_X=0.87',
                              'ACC_Y=0.87',
                              'ACC_Z=9.80',
                              'MAG_X=1.0',
                              'MAG_Y=2.0',
                              'MAG_Z=-3.0',
                              'GYR_X=-1.23',
                              'GYR_Y=-1.23',
                              'GYR_Z=1.23',
                              seq_num, 
                              timestamp)
    print('Lsm Sensor burst ... COUNT = {}'.format(LSMSENSOR_COUNT))
    if LSMSENSOR_COUNT >= 10000:
        return
    else:
        threading.Timer(1, generate_lsmsensor_frames).start()

SENSOR_COUNT = 0
def generate_sensor_frames():
    global SENSOR_COUNT
    for i in range(20):
        SENSOR_COUNT += 1
        seq_num = 'SEQUENCE_NUMBER='+str(int(SENSOR_COUNT))
        timestamp = 'TIMESTAMP='+str(int(time.time() * 1000))
        journal.sendv('CHANNEL=sensor', 
                              'D_QUATERNION_X=7657.0',
                              'D_QUATERNION_Y=7657.0',
                              'D_QUATERNION_Z=7657.0',
                              'D_QUATERNION_W=7657.0',
                              'D_ACCEL_X=0.87',
                              'D_ACCEL_Y=0.87',
                              'D_ACCEL_Z=9.80',
                              'D_MAG_X=0.0',
                              'D_MAG_Y=0.0',
                              'D_MAG_Z=0.0',
                              'D_GYRO_X=-1.23',
                              'D_GYRO_Y=-1.23',
                              'D_GYRO_Z=1.23',
                              'D_EULER_H=4.15',
                              'D_EULER_P=4.15',
                              'D_EULER_R=4.15',
                              'D_LINEAR_ACCEL_X=4.19',
                              'D_LINEAR_ACCEL_Y=4.19',
                              'D_LINEAR_ACCEL_Z=4.19',
                              'D_GRAVITY_X=-4.55',
                              'D_GRAVITY_Y=-4.55',
                              'D_GRAVITY_Z=-4.55',
                              'ACCEL_CALIB_STAT=1',
                              'GYRO_CALIB_STAT=0',
                              'MAG_CALIB_STAT=0',
                              'SYS_CALIB_STAT=0',
                              seq_num, 
                              timestamp)
    print('Sensor burst ... COUNT = {}'.format(SENSOR_COUNT))
    if SENSOR_COUNT >= 10000:
        return
    else:
        threading.Timer(1, generate_sensor_frames).start()

GPS_COUNT = 0
def generate_gps_frames():
    global GPS_COUNT
    GPS_COUNT += 1
    seq_num = 'SEQUENCE_NUMBER='+str(int(GPS_COUNT))
    timestamp = 'TIMESTAMP='+str(int(time.time() * 1000))
    journal.sendv('CHANNEL=gpsData',
                      'CLASS=TPV',
                      'TAG=dummy',
                      'DEVICE=ttyMX3',
                      'MODE=3',
                      'TIME=0',
                      'EPT=0.005',
                      'LAT=12.92831016',
                      'LON=77.637049078',
                      'ALT=878.655',
                      'EPX=17.529',
                      'EPY=17.529',
                      'EPV=0.0',
                      'TRACK=99.6513',
                      'SPEED=0.525',
                      'CLIMB=0.294',
                      'EPD=0.0',
                      'EPS=0.96',
                      'EPC=0.0',
                      seq_num,
                      timestamp)
    print('Gps frame ... COUNT = {}'.format(GPS_COUNT))
    if GPS_COUNT >= 1000:
        return
    else:
        threading.Timer(1, generate_gps_frames).start()

PERI_COUNT = 0
def generate_peri_state_frames():
    global PERI_COUNT
    PERI_COUNT += 1
    timestamp = 'TIMESTAMP='+str(int(time.time() * 1000))
    seq_num = 'SEQUENCE_NUMBER='+str(int(PERI_COUNT))
    journal.sendv('CHANNEL=peripheralState', 
                      'NETWORKSTATUS=Up',
                      'NETWORKSIGNAL=50',
                      'ISL29023LUXVALUE=10',
                      'ISL29023AVGLUXVALUE=10',
                      'ISL29023DEVICESTATUS=on',
                      'GPSDEVICESTATUS=on',
                      'SCREENBRIGHTNESS=1',
                      'SCREENBRIGHTNESSCONTROL=auto',
                      'HEADLIGHTCONTROL=auto',
                      'BLUTOOTHDEVICESTATUS=on',
                      seq_num,
                      timestamp)
    print('Peripheral frame ... COUNT = {}'.format(PERI_COUNT))
    if PERI_COUNT >= 300:
        return
    else:
        threading.Timer(1, generate_peri_state_frames).start()

VEH_STATS_COUNT = 0
def generate_veh_stats_frames():
    global VEH_STATS_COUNT
    VEH_STATS_COUNT += 1
    seq_num = 'SEQUENCE_NUMBER='+str(int(VEH_STATS_COUNT))
    timestamp = 'TIMESTAMP='+str(int(time.time() * 1000))
    journal.sendv('CHANNEL=vehicleStats',
                      'CHARGELEFT=100',
                      'MCUSTATUS=up',
                      'SPEED=0.0',
                      'THROTTLE=0.0',
                      'REGEN=0.0',
                      'RANGE=100.00',
                      seq_num,
                      timestamp)
    print('Vehicle stats frame ... COUNT = {}'.format(VEH_STATS_COUNT))
    if VEH_STATS_COUNT >= 300:
        return
    else:
        threading.Timer(1, generate_veh_stats_frames).start()

VEH_STATE_COUNT = 0
def generate_veh_state_frames():
    global VEH_STATE_COUNT
    VEH_STATE_COUNT += 1
    seq_num = 'SEQUENCE_NUMBER='+str(int(VEH_STATE_COUNT))
    timestamp = 'TIMESTAMP='+str(int(time.time() * 1000))
    journal.sendv('CHANNEL=vehicleState',
                      'KEYIN=on',
                      'LEFTINDICATOR=off',
                      'RIGHTINDICATOR=off',
                      'MOTORMODE=economy',
                      'HEADLIGHTSTATE=off',
                      'STARTSWITCH=off',
                      'LEFTBRAKE=off',
                      'RIGHTBRAKE=off',
                      'HORN=off',
                      seq_num,
                      timestamp)
    print('Vehicle state frame ... COUNT = {}'.format(VEH_STATE_COUNT))
    if VEH_STATE_COUNT >= 300:
        return
    else:
        threading.Timer(1, generate_veh_state_frames).start()

generate_can_frames()
#generate_sensor_frames()
#generate_lsmsensor_frames()
#generate_gps_frames()
#generate_peri_state_frames()
#generate_veh_stats_frames()
#generate_veh_state_frames()


t1 = time.time()
while True:
    time.sleep(10)
    t2 = time.time()
    if t2 - t1 > 1 * 2000:
        sys.exit()



#journal.sendv('MESSAGE=Hello, again, world', 'FIELD2=Greetings!',
#               'FIELD3=Guten tag')
#journal.sendv('MESSAGE=Binary message', b'BINARY=\xde\xad\xbe\xef')

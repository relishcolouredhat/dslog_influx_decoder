# dslog_influx_decoder

from dslog2csv import *

import datetime

def process_file(input_file):

    #file_name = '2019_03_01 14_29_08 Fri'
    file_name = input_file.split('.')[0]

    output_file = str(file_name+'.lineproto')
    #dslog_file = str(file_name+'.dslog')
    dslog_file = input_file

    af = open(output_file,'w')

    dsparser = DSLogParser(dslog_file)


    col = ['time_of_day',]

    col.extend(DSLogParser.OUTPUT_COLUMNS)

    fn = file_name.split(' ')

    raw_date = fn[0]
    raw_date = raw_date.split('_')
    year = int(raw_date[0])
    month = int(raw_date[1])
    day = int(raw_date[2])

    raw_time = fn[1]
    raw_time = raw_time.split('_')
    hour = int(raw_time[0]) 
    minute = int(raw_time[1]) 
    second = int(raw_time[2]) 

    start_time = datetime.datetime(year, month, day, hour, minute, second)

    #print(start_time+'.')

    epoch = datetime.datetime.utcfromtimestamp(0)
         
    def unix_time_nanos(dt):
        return (dt - epoch).total_seconds() * 1000000
        
    for rec in dsparser.read_records():
         
         
         #rec['time_of_day'] = '01-01-1970-00-00-00'
         rec['time_of_day'] = str(start_time)
         for i in range(16):
             rec['pdp_{}'.format(i)] = rec['pdp_currents'][i]
         #print(str(rec)+'\r\n\r\n')
         #print(rec.keys())
         #print(rec.values())
         
         td = datetime.timedelta(0,0,0,rec['time'])
         t = start_time+td
         
         t = unix_time_nanos(t)
         t = str(str(int(t))+'000')
         
         line = (\
         'robo-pdp,'+
         #'filetime='+rec['time_of_day']+\
         'team=3985 '+
         'robot_auto='+str(int(rec['robot_auto']))+
         ',robot_disabled='+str(int(rec['robot_disabled']))+
         ',robot_tele='+str(int(rec['robot_tele']))+
         ',ds_tele='+str(int(rec['ds_tele']))+
         ',ds_disabled='+str(int(rec['robot_auto']))+
         ',brownout='+str(int(rec['brownout'])) +
         ',watchdog='+str(int(rec['watchdog'])) +
         ',packet_loss='+str(rec['packet_loss'])+
         ',pdp_temp='+str(rec['pdp_temp'])+
         ',pdp_voltage='+str(rec['pdp_voltage'])+
         ',pdp_id='+str(rec['pdp_id'])+
         ',bandwidth='+str(rec['bandwidth'])+
         ',wifi_db='+str(rec['wifi_db'])+
         ',rio_cpu='+str(rec['rio_cpu'])+
         ',pdp_total_current='+str(rec['pdp_total_current'])+
         ',round_trip_time='+str(rec['round_trip_time'])+
         ',pdp_resistance='+str(rec['pdp_resistance'])+
         ',ds_auto='+str(int(rec['ds_auto']))+
         ',time='+str(rec['time'])+
         ',can_usage='+str(rec['can_usage'])+
         ',voltage='+str(rec['voltage'])+
         ',pdp_1='+str(rec['pdp_1'])+
         ',pdp_2='+str(rec['pdp_2'])+
         ',pdp_3='+str(rec['pdp_3'])+
         ',pdp_4='+str(rec['pdp_4'])+
         ',pdp_5='+str(rec['pdp_5'])+
         ',pdp_6='+str(rec['pdp_6'])+
         ',pdp_7='+str(rec['pdp_7'])+
         ',pdp_8='+str(rec['pdp_8'])+
         ',pdp_9='+str(rec['pdp_9'])+
         ',pdp_10='+str(rec['pdp_10'])+
         ',pdp_11='+str(rec['pdp_11'])+
         ',pdp_12='+str(rec['pdp_12'])+
         ',pdp_13='+str(rec['pdp_13'])+
         ',pdp_14='+str(rec['pdp_14'])+
         ',pdp_15='+str(rec['pdp_15'])+
         ' '+t+'\n'
         )
         print(line)
         af.write(line)
         
         #break

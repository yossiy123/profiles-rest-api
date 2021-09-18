from datetime import datetime

EMPTY_STRING = ''

class TimeStemp():
    
    @staticmethod
    def get_time_stemp(i_date_time_object = None, 
                        i_microsecond = True, 
                        i_second = True, 
                        i_minute = True, 
                        i_hour = True, 
                        i_day = True, 
                        i_month = True, 
                        i_year = True, 
                        ):
        date_time_object = datetime.now() if (i_date_time_object is None) else i_date_time_object

        string_to_return = ''

        # Year
        string_to_return += (("{:04d}".format(date_time_object.year)) if (i_year) else (''))
        # Month
        string_to_return += (("{:02d}".format(date_time_object.month)) if (i_month) else (''))
        # Day
        string_to_return += (("{:02d}".format(date_time_object.day)) if (i_day) else (''))

        if ((i_microsecond or i_second or i_minute or i_hour) and (i_day or i_month or i_year)):
            string_to_return += '_'
        
        # Hours
        string_to_return += (("{:02d}".format(date_time_object.hour)) if (i_hour) else (''))
        # Minutes
        string_to_return += (("{:02d}".format(date_time_object.minute)) if (i_minute) else (''))
        # Seconds
        string_to_return += (("{:02d}".format(date_time_object.second)) if (i_second) else (''))
        # Microsecond
        string_to_return += (("{:06d}".format(date_time_object.microsecond)) if (i_microsecond) else (''))

        # {Year}{Month}{Day}{Hour}{Minute}{Second}{MicroSecond} as string
        return string_to_return
                #(str(date_time_object.microsecond) if (i_microsecond) else ('')) 
                #(str(date_time_object.second) if (i_second) else ('')) + 
                #str(date_time_object.minute) if (i_minute) else '' + 
                #str(date_time_object.hour) if (i_hour) else '' + 
                #str(date_time_object.day) if (i_day) else '' + 
                #str(date_time_object.month) if (i_month) else '' + 
                #str(date_time_object.year) if (i_year) else ''
    
    @staticmethod
    def get_time(i_date_time_object = None, 
                        i_time = True, 
                        i_date = True, 
                        i_microsecond = True, 
                        i_second = True, 
                        i_minute = True, 
                        i_hour = True, 
                        i_day = True, 
                        i_month = True, 
                        i_year = True, 
                        ):
        date_time_object = datetime.now() if (i_date_time_object is None) else i_date_time_object
        # {MicroSecond}{Second}{Minute}{Hour}{Day}{Month}{Year} as string
        i_time = (i_time and (i_hour or i_minute or i_second or i_microsecond))
        i_date = (i_date and (i_day or i_month or i_year))

        string_to_return = ''
        
        # Time
        if (i_time):
            # Hours
            string_to_return += ((str(date_time_object.hour)) if (i_hour) else (''))
            # Between hour - minute
            string_to_return += ((':') if ((i_hour) and (i_minute or i_second or i_microsecond)) else (''))
            # Minutes
            string_to_return += ((str(date_time_object.minute)) if (i_minute) else (''))
            # Between minute - second
            string_to_return += ((':') if ((i_hour or i_minute) and (i_second or i_microsecond)) else (''))
            # Seconds
            string_to_return += ((str(date_time_object.second)) if (i_second) else (''))
            # Between second - microsecond
            string_to_return += (('.') if ((i_hour or i_minute or i_second) and (i_microsecond)) else (''))
            # Microsecond
            string_to_return += ((str(date_time_object.microsecond)) if (i_microsecond) else (''))
            
        # Between Time - Date
        if (i_time and i_date):
            string_to_return += ' '
            
        # Date
        if (i_date):
            # Day
            string_to_return += ((str(date_time_object.day)) if (i_day) else (''))
            # Between day - month
            string_to_return += (('.') if ((i_day) and (i_month or i_year)) else (''))
            # Month
            string_to_return += ((str(date_time_object.month)) if (i_month) else (''))
            # Between month - year
            string_to_return += (('.') if ((i_day or i_month) and (i_year)) else (''))
            # Year
            string_to_return += ((str(date_time_object.year)) if (i_year) else (''))

        return string_to_return
        #return ((((str(date_time_object.hour) + ':') if (i_hour) else ('')) + (str(date_time_object.minute) + ':') if (i_minute) else '' + (str(date_time_object.second) + ':') if (i_second) else '' + (str(date_time_object.microsecond) + ':') if (i_microsecond) else '') + ' ') if (i_time) else '' + ((str(date_time_object.day) + '.') if (i_day) else '' + (str(date_time_object.month) + '.') if (i_month) else '' + str(date_time_object.year) if (i_year) else '') if (i_date) else ''

if (__name__ == '__main__'):
    print(TimeStemp.get_time())
    print(TimeStemp.get_time_stemp())
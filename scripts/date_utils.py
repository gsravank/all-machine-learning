import csv, math
import io, sys, yaml, os
from optparse import OptionParser
from datetime import datetime
from datetime import timedelta
import calendar


Holidays_exchange = ['20190304','20190321','20190417','20190419','20190429','20190501','20190605',
        '20190812','20190815','20190902','20190910','20191002','20191008', '20191021', '20191028','20191112',
        '20191202', '20191203', '20191206', '20191225', '20200221', '20200310', '20200313', '20200402', '20200406',
        '20200410', '20200414', '20200501', '20200525', '20201002', '20201116', '20201130', '20201225', '20200602',
        '20210126', '20210311', '20210329', '20210402', '20210414', '20210421', '20210513', '20210721', '20210819', 
        '20210910', '20211015', '20211105', '20211119']
Holidays_exchange += ['20220126', '20220301', '20220318', '20220414', '20220415', 
                      '20220503', '20220809', '20220815', '20220831', '20221005', 
                      '20221024', '20221026', '20221108', '20220912', '20220913', 
                      '20220923', '20220926']
Holidays_exchange += ['20230126', '20230307', '20230330', '20230404', '20230407', '20230414', '20230501', '20230628',
                      '20230815', '20230919', '20231002', '20231024', '20231114', '20231127', '20231225']
HOLIDAYS_B3 = ['20220101', '20220228', '20220301', '20220302', '20220415', '20220421', 
               '20220616', '20220907', '20221012', '20221102', '20221115', '20221230']
HOLIDAYS_B3 += ['20230220', '20230221', '20230407', '20230421', '20230501', '20230608',
                '20230907', '20231012',' 20231102', '20231115', '20231225', '20231229']               

EXCH_HOLIDAY_MAP = dict()
for _exch in ['NSECM', 'NSEFO', 'NSECD', 'BSECM', 'BSECD']:
    EXCH_HOLIDAY_MAP[_exch] = Holidays_exchange
for _exch in ['B3FO', 'b3fo', 'B3CD', 'b3cd', 'B3', 'b3']:
    EXCH_HOLIDAY_MAP[_exch] = HOLIDAYS_B3


def get_cl_formatted_date(date):
    return date[0:4] + '-' + date[4:6]+ '-' + date[6:] + '  00:00:00'


def get_implied_weekly_for_monthly_expiry(date):
    monthly_expiry = get_nsefo_monthly_expiry_date(date)
    count = 0
    curr_date = date
    while curr_date != monthly_expiry:
        curr_date = get_nsefo_weekly_expiry_date(curr_date)
        if curr_date != monthly_expiry:
            curr_date = get_next_date(curr_date)
            count += 1
    return f"W.{count}"

def convert_bhav_date_to_readable(date):
    day = date.split('-')[0]
    year = date[-4:]
    short_months = [x[:3].lower() for x in list(calendar.month_name)]
    month = short_months.index(date.split('-')[1].lower())
    return f'{year}0{month}{day}' if month < 10 else f'{year}{month}{day}'

def get_dates_of_weekday(year, month, weekday_name='thursday'):
    """Get all dates in given month which fall on the given weekday
    
    Args:
        year (str): Year in YYYY format
        month (str): Month in MM format
        weekday_name (str): One of the seven weekday names
    
    Returns:
        list : List of dates matching given weekday
    """
    year = str(year)
    month = f"{int(month):02d}"
    
    date = f"{year}{month}01"
    weekday_name = weekday_name.strip().lower()
    weekdays = list()
    
    done = False
    while not done:
        if get_weekday_name(date).lower().strip() == weekday_name:
            weekdays.append(date)
        
        date = get_next_date(date)
        if date[4:6] != month:
            done = True
            
    return weekdays


def get_nsefo_monthly_expiry_date(date, holidays=Holidays_exchange):
    """Get monthly expiry date for an NSEFO contract of given date
    
    Args:
        date (str): Date in YYYYMMDD format
        holidays (list): List of holidays to ignore
        
    Returns:
        str : Expiry date in YYYYMMDD format
    """
    last_thursday = get_dates_of_weekday(date[:4], date[4:6], 'thursday')[-1]
    
    if date > last_thursday:
        curr_month_num = int(date[4:6])
        curr_year = int(date[:4])
        
        if curr_month_num == 12:
            next_month_num = 1
            next_year_num = curr_year + 1
        else:
            next_month_num = curr_month_num + 1
            next_year_num = curr_year
        next_month = f"{next_month_num:02d}"
        next_year = f"{next_year_num}"

        last_thursday = get_dates_of_weekday(next_year, next_month, 'thursday')[-1]
    
    if last_thursday in holidays:
        return get_prev_working_day(last_thursday, holidays)
    else:
        return last_thursday


def get_nsefo_prev_monthly_expiry_date(date, holidays=Holidays_exchange):
    """Get prev monthly expiry date for an NSEFO contract of given date
    
    Args:
        date (str): Date in YYYYMMDD format
        holidays (list): List of holidays to ignore
        
    Returns:
        str : Expiry date in YYYYMMDD format
    """
    curr_monthly_expiry_date = get_nsefo_monthly_expiry_date(date, holidays)
    curr_date = curr_monthly_expiry_date
    count = 0
    while True:
        count += 1
        prev_working_date = get_prev_working_day(curr_date)
        if curr_monthly_expiry_date != get_nsefo_monthly_expiry_date(prev_working_date, holidays):
            return get_nsefo_monthly_expiry_date(prev_working_date, holidays)
        else:
            curr_date = prev_working_date
        
        if count >= 60:
            print("Could not find prev monthly expiry!")
            return None
            
    return

    
def get_nsefo_weekly_expiry_date(date, holidays=Holidays_exchange):
    """Get weekly expiry date for an NSEFO contract of given date
    
    Args:
        date (str): Date in YYYYMMDD format
        holidays (list): List of holidays to ignore
        
    Returns:
        str : Expiry date in YYYYMMDD format
    """
    next_thursdays = [x for x in get_dates_of_weekday(date[:4], date[4:6], 'thursday') if x >= date]
    
    if len(next_thursdays) == 0:
        curr_month_num = int(date[4:6])
        curr_year = int(date[:4])
        
        if curr_month_num == 12:
            next_month_num = 1
            next_year_num = curr_year + 1
        else:
            next_month_num = curr_month_num + 1
            next_year_num = curr_year
        next_month = f"{next_month_num:02d}"
        next_year = f"{next_year_num}"
        
        next_thursday = get_dates_of_weekday(next_year, next_month, 'thursday')[0]
    else:
        next_thursday = next_thursdays[0]

    if next_thursday in holidays:
        return get_prev_working_day(next_thursday, holidays)
    else:
        return next_thursday


def get_todays_date():
    return datetime.today().strftime("%Y%m%d")

def get_prev_date(date):
    dt = datetime.strptime(date, "%Y%m%d")
    prev_dt = dt - timedelta(days=1)
    return prev_dt.strftime("%Y%m%d")

def get_next_date(date):
    dt = datetime.strptime(date, "%Y%m%d")
    next_dt = dt + timedelta(days=1)
    return next_dt.strftime("%Y%m%d")

def get_weekday_name(date):
    return calendar.day_name[datetime.strptime(date, "%Y%m%d").weekday()]

def get_holidays( exchange ):
    return EXCH_HOLIDAY_MAP.get(exchange, Holidays_exchange)

def get_next_working_day( date, holidays=Holidays_exchange):
    next_day = datetime.strptime( date, "%Y%m%d" )
    while True:
        next_day += timedelta(days=1)
        if next_day.weekday() >=5:
            continue
        if next_day.strftime("%Y%m%d") in holidays:
            continue
        return next_day.strftime("%Y%m%d")

def get_prev_working_day( date, holidays=Holidays_exchange):
    prev_day = datetime.strptime(date, "%Y%m%d" )
    while True:
        prev_day -= timedelta(days=1)
        if prev_day.weekday() >=5:
            continue
        if prev_day.strftime("%Y%m%d") in holidays:
            continue
        return prev_day.strftime("%Y%m%d")
    return "-1"


def convert_date_to_bhav_style(date):
    """Convert date from YYYYMMDD to DD-MMM-YYYY format
    Example: 20210624 -> 24-Jun-2021
    """
    month = calendar.month_name[int(date[4:6])][:3].title()
    return f"{date[6:]}-{month}-{date[:4]}"


def get_working_days(start_date, end_date, num_days, exchange, weekday=""):
    holidays = get_holidays( exchange )
    days = []
    if( start_date != "-1" and end_date != "-1" ):
        start_date = get_prev_working_day(start_date, holidays)
        end_date = get_next_working_day(end_date, holidays)
        end_date = get_prev_working_day(end_date, holidays)
        while( start_date != end_date ):
            start_date = get_next_working_day(start_date, holidays)
            days.append(start_date)
    if( start_date != "-1" and num_days != "-1" ):
        start_date = get_prev_working_day(start_date, holidays)
        for num in range(int(num_days)):
            start_date = get_next_working_day(start_date, holidays)
            days.append(start_date)
    if( end_date != "-1" and num_days != "-1" ):
        end_date = get_next_working_day(end_date, holidays)
        for num in range(int(num_days)):
            end_date = get_prev_working_day(end_date, holidays)
            days.insert(0,end_date)

    if weekday == "":
        return days
    else:
        return [day for day in days if get_weekday_name(day).lower() == weekday.strip().lower()]

        
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(" Usage :: ./dates_generator -s startdate -e enddate -n num_days")
        exit()
    parser = OptionParser()
    parser.add_option("-s", "--startdate", dest="sdate", default="-1")
    parser.add_option("-e", "--enddate", dest="edate", default="-1")
    parser.add_option("-n", "--numdays", dest="numdays", default="-1")
    parser.add_option("-w", "--weekday", dest="weekday", default="")
    (options, args) = parser.parse_args()
    dates = get_working_days(options.sdate, options.edate, options.numdays, "CME", options.weekday)
    for date in dates:
        print(date)

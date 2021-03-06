import os
import pandas as pd
from decimal import Decimal, ROUND_UP

files = [x for x in os.listdir() if x.endswith('.xlsx')]

def time_string_to_decimals(time_string):
  fields = time_string.split(":")
  hours = fields[0] if len(fields) > 0 else 0.0
  minutes = fields[1] if len(fields) > 1 else 0.0
  seconds = fields[2] if len(fields) > 2 else 0.0
  return float(hours) + (float(minutes) / 60.0) + float(seconds) / pow(60.0, 2)

for file in files:
  excel = pd.read_excel(file, header=None, skiprows=1, parse_dates=[1,2,3,4,5,6])\
  .rename(columns={0:'ID', 1:'IN', 2:'OUT1', 3:'IN1', 4:'OUT2', 5:'IN2', 6:'OUT', 7:'RATE'})

  times = excel.iloc[:, 1:7]
  hours = []
  for i in range(0,len(times)):
    hours.append(str(excel.OUT[i] - (excel.IN1[i] - excel.OUT1[i]) - (excel.IN2[i] - excel.OUT2[i]) - excel.IN[i])[-8:])

  hours_worked = [time_string_to_decimals(x) for x in hours]
  excel["HOURS"] = hours_worked
  excel['PAY'] = excel.RATE * excel.HOURS
  excel['PAY'] = excel["PAY"].apply(
      lambda x: float(Decimal(str(x)).quantize(Decimal('.01'), rounding=ROUND_UP))
  )

  for column in excel.iloc[:, 1:7].columns:
    excel[column] = excel[column].dt.strftime('%H:%M')

  excel.to_excel(f'automated_{file}', startcol=0, startrow=0, index=False)

#task1
from datetime import datetime, timedelta

# Get the current date
current_date = datetime.now()

# Subtract 5 days
result_date = current_date - timedelta(days=5)

print("Current Date:", current_date.strftime("%Y-%m-%d"))
print("5 Days Ago:", result_date.strftime("%Y-%m-%d"))

#task2
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print(f"Yesterday: {yesterday}")
print(f"Today:     {today}")
print(f"Tomorrow:  {tomorrow}")

#task3
from datetime import datetime

# Current time with microseconds
dt_with_ms = datetime.now()

# Replace microsecond with 0
dt_no_ms = dt_with_ms.replace(microsecond=0)

print("Original:", dt_with_ms)
print("Stripped:", dt_no_ms)

#task4
from datetime import datetime

# Example dates
date1 = datetime(2026, 2, 27, 12, 0, 0)
date2 = datetime(2026, 2, 28, 14, 30, 0)

# Calculate difference
duration = date2 - date1
seconds_diff = duration.total_seconds()

print(f"Difference: {seconds_diff} seconds")


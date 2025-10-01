from datetime import datetime, timedelta
import pytz





# def calculate_next_execution_time(repeat_days, time_str):
#     """
#     Calculate the next execution time based on repeat_days and time in IST.
#     """
#     # Define IST and UTC timezones
#     ist = pytz.timezone('Asia/Kolkata')
#     utc = pytz.utc

#     # Map days of the week to integers
#     days_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
#                     "Friday": 4, "Saturday": 5, "Sunday": 6}
#     repeat_days = [days_mapping[day] for day in repeat_days]

#     # Current time in UTC
#     now = datetime.now(utc)
#     current_day = now.weekday()
#     current_time = now.time()
#     current_date = datetime.now().strftime("%Y-%m-%d")

#     # Convert target time string (in IST) to UTC
#     target_time_ist = datetime.strptime(time_str, "%H:%M")
#     target_time_ist = datetime.strptime(f"{current_date} {time_str}", "%Y-%m-%d %H:%M")
#     target_time_utc = target_time_ist.astimezone(utc).time()
#     print(target_time_utc)

#     # Find the next valid day and time
#     days_until_next = None
#     for day in repeat_days:
#         day_difference = (day - current_day) % 7
#         if day == current_day and target_time_utc >= current_time:
#             days_until_next = day_difference
#             break
#         elif days_until_next is None or day_difference < days_until_next:
#             days_until_next = day_difference

#     # Calculate the next execution datetime
#     next_date = now + timedelta(days=days_until_next)
#     next_execution = datetime.combine(next_date.date(), target_time_utc, tzinfo=utc)

#     return next_execution


from datetime import datetime, timedelta
import pytz

# def calculate_next_execution_time(repeat_days, time_str):
#     """
#     Calculate the next execution time based on repeat_days and time in IST.
#     """
#     # Define IST and UTC timezones
#     ist = pytz.timezone('Asia/Kolkata')
#     utc = pytz.utc

#     # Map days of the week to integers
#     days_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
#                     "Friday": 4, "Saturday": 5, "Sunday": 6}
#     repeat_days = sorted([days_mapping[day] for day in repeat_days])  # Sort for easier lookup

#     # Current time in IST
#     now_ist = datetime.now(ist)
#     current_day = now_ist.weekday()
#     current_time = now_ist.time()

#     # Convert target time string to a datetime object in IST
#     today_date = now_ist.strftime("%Y-%m-%d")
#     target_time_ist = datetime.strptime(f"{today_date} {time_str}", "%Y-%m-%d %H:%M")
#     target_time_ist = ist.localize(target_time_ist)

#     # If today's execution is still in the future, select today
#     if current_day in repeat_days and current_time < target_time_ist.time():
#         next_execution = target_time_ist
#     else:
#         # Find the next available repeat day
#         days_until_next = None
#         for day in repeat_days:
#             day_difference = (day - current_day) % 7
#             if days_until_next is None or day_difference < days_until_next:
#                 days_until_next = day_difference

#         # Compute next execution date
#         next_execution_date = now_ist + timedelta(days=days_until_next)
#         next_execution = datetime.combine(next_execution_date.date(), target_time_ist.time(), tzinfo=ist)

#     # Convert to UTC before returning
#     return next_execution.astimezone(utc)


from datetime import datetime, timedelta
import pytz

# def calculate_next_execution_time(repeat_days, time_str):
#     """
#     Calculate the next execution time based on repeat_days and time in IST.
#     """
#     # Define IST and UTC timezones
#     ist = pytz.timezone('Asia/Kolkata')
#     utc = pytz.utc

#     # Map days of the week to integers
#     days_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
#                     "Friday": 4, "Saturday": 5, "Sunday": 6}
#     repeat_days = sorted([days_mapping[day] for day in repeat_days])  # Sort for easier lookup

#     # Current time in IST
#     now_ist = datetime.now(ist)
#     current_day = now_ist.weekday()
#     current_time = now_ist.time()

#     # Convert target time string to a datetime object in IST
#     today_date = now_ist.strftime("%Y-%m-%d")
#     target_time_ist = datetime.strptime(f"{today_date} {time_str}", "%Y-%m-%d %H:%M")
#     target_time_ist = ist.localize(target_time_ist)

#     # ✅ If today is a repeat day AND the current time is before the target time → Execute today
#     if current_day in repeat_days and current_time < target_time_ist.time():
#         next_execution = target_time_ist
#     else:
#         # ✅ If today's execution time has passed, find the NEXT repeat day
#         days_until_next = None
#         for day in repeat_days:
#             day_difference = (day - current_day) % 7
#             if day_difference == 0 and current_time >= target_time_ist.time():
#                 continue  # Skip today if the execution time has already passed
#             if days_until_next is None or day_difference < days_until_next:
#                 days_until_next = day_difference

#         # Compute next execution date
#         next_execution_date = now_ist + timedelta(days=days_until_next)
#         next_execution = datetime.combine(next_execution_date.date(), target_time_ist.time(), tzinfo=ist)

#     # Convert to UTC before returning
#     return next_execution.astimezone(utc)


from datetime import datetime, timedelta
import pytz

def calculate_next_execution_time_fixed(repeat_days, time_str):
    """
    Calculate the next execution time based on repeat_days and time in IST.
    """
    # Define IST and UTC timezones
    ist = pytz.timezone('Asia/Kolkata')
    utc = pytz.utc

    # Map days of the week to integers
    days_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                    "Friday": 4, "Saturday": 5, "Sunday": 6}

    # Ensure repeat_days is not empty
    if not repeat_days:
        raise ValueError("repeat_days cannot be empty")

    repeat_days = sorted([days_mapping[day] for day in repeat_days])  # Sort for easier lookup

    # Current time in IST
    now_ist = datetime.now(ist)
    current_day = now_ist.weekday()
    current_time = now_ist.time()

    # Convert target time string to a datetime object in IST
    today_date = now_ist.strftime("%Y-%m-%d")
    target_time_ist = datetime.strptime(f"{today_date} {time_str}", "%Y-%m-%d %H:%M")
    target_time_ist = ist.localize(target_time_ist)
    target_time_utc = target_time_ist.astimezone(utc).time()  # Convert to UTC time format

    # If today is a repeat day AND the current time is before the target time → Execute today
    if current_day in repeat_days and current_time < target_time_ist.time():
        next_execution_date = now_ist
    else:
        # Find the next available repeat day
        days_until_next = min(
            [(day - current_day) % 7 for day in repeat_days if (day - current_day) % 7 > 0],
            default=7  # Default to next week's first repeat day if all have passed
        )

        # Compute next execution date
        next_execution_date = now_ist + timedelta(days=days_until_next)

    # Combine date and UTC time in required format
    next_execution = datetime.combine(next_execution_date.date(), target_time_utc, tzinfo=utc)

    return next_execution

# Example usage:
repeat_days = ["Saturday","Monday"]
time_str = "15:10"  # IST time

next_time_fixed = calculate_next_execution_time_fixed(repeat_days, time_str)
print(next_time_fixed)




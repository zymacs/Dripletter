from datetime import datetime
from pathlib import Path

import config
from mailer import Mailer
from db_manager import DBManager




# -- algo
# check db
# get whats not sent
# send that

# update db

# -- updated algo
# check db
# check what is not sent that has send time set to now
# send that

def get_time_now():
    time_now = datetime.now()
    day,month,year,hour,minute = (time_now.day,time_now.month,time_now.year,time_now.hour,time_now.minute)
    return  hour, minute, '.'.join([str(day),str(month),str(year),str(hour),str(minute)])

mailer = Mailer(config.sender_email, config.sender_pass)
recepients = config.default_recepients

db_manager = DBManager(config.db_uri)

# loop through all tables and check if anything has to be sent.

table_tups = db_manager.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
tables = [table_tup[0] for table_tup in table_tups]



for table in tables:
    if '_table' not in table:
        continue
    hour, minute, time_now = get_time_now()
    time_str_24h = f'{hour}:{"0"+str(minute) if minute < 10 else minute}'
    print(time_str_24h)
    check_query = f"SELECT id,file_name,file_path from {table} WHERE send_date IS NULL AND planned_send_time='{time_str_24h}'"
    all_entries = db_manager.execute(check_query).fetchall()
    print(len(all_entries))
    num_entries = len(all_entries)
    file_id, file_name, file_path = all_entries[0] if num_entries > 0 else (None, None, None)

    if file_id is None:
        continue
    
    attachment_uri = Path(file_path) / Path(file_name)


    mail_body = """
       Filename: {file_name}\n
       Part: {part} of {total_parts}\n
       Attachment attached below\n\n
    """.format(file_name=file_name, part=file_id, total_parts=num_entries)

    raw_message = {"body":mail_body, "subject": f'CDS-plus-{file_name}'}

    # add status check
    mailer.send_mail(recepients, raw_message, attachment_uri)

    # update date for sent file with current date
    
    hour, minute, time_now = get_time_now()
    row_update_query = f'UPDATE {table} SET send_date = ?, send_status = ? WHERE id = ?'
    values = [time_now, 'sent', file_id]
    db_manager.execute(row_update_query, values)
    db_manager.commit()

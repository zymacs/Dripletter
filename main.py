import os
import time

from pathlib import Path

from splitter import Splitter
from scheduler import CronScheduler as Scheduler
from cronconverter import CronConverter
from file_manager import FileSearch
from db_manager import DBManager

import config

scheduler = Scheduler(config.user)
cronconverter = CronConverter()

def add_split_pdfs_to_db(split_pdfs, db_manager, table_name, broadcast_frequency):
    
    create_table(db_manager, table_name)
    
    planned_hour, planned_minute = cronconverter.convert_time(cronconverter.extract_time(broadcast_frequency))
    planned_send_time = f'{planned_hour}:{planned_minute}'

    for pdf in split_pdfs:
        insert_query = f"INSERT INTO {table_name} (file_name, file_path, broadcast_frequency, planned_send_time)  VALUES (?, ?, ?, ?)"
        db_manager.execute(insert_query, [Path(pdf).name, str(Path(pdf).parent), broadcast_frequency, planned_send_time])
    db_manager.commit()

    
    
def split_pdf(*args):
    splitter = Splitter(*args)
    return splitter.split_pdf()

def init_db():
    db_manager = DBManager(config.db_uri)
    return db_manager

def create_table(db_manager, table_name):
    if not table_name.replace('_', '').isalnum():
        raise ValueError(f"Invalid table name: {table_name}")
    
    db_manager.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    send_status TEXT,
    send_date TEXT,
    broadcast_frequency TEXT,
    planned_send_time TEXT
    )""")


def schedule_broadcast(comment, broadcast_frequency):
    command = f"cd {str(config.base_wdir)} && "
    command += "/usr/bin/python3 broadcaster.py"
    logs_file = str(config.logs_file)
    command += f" >> {logs_file}"

    scheduler.create_job(command)
    scheduler.annotate_all(comment)
    scheduler.set_schedule(broadcast_frequency)
    scheduler.enable_all()
    scheduler.write_all()


def get_user_input(input_type='string'):
    pass

def clean_table_name(name):
    name =  name.replace(' ','_').replace("(",'').replace(")",'').replace('-','_').replace(':','')
    if len(name) > 14:
        name = name[:14]
    return name

def main():
    # TODO:  check config to make sure all that is required is set before running anything.
    print("Searching for file to split")
    os.system('clear')
    search_term = input('Enter search term: ')
    pdf_file =   FileSearch.search(search_term)
    while pdf_file is None:
        print(f"{search_term} not found")
        search_term = input('Enter search term: ')
        pdf_file =   FileSearch.search(search_term)
    print("Opening the file so you can confirm start page and end page for section that'll be spliced")
    time.sleep(3)
    os.system(f'xdg-open "{pdf_file}"')
    from_page =  input("[+] Enter from page: ")
    to_page = input("[+] Enter to page: ") 
    if from_page is None:
        from_page = 1
    else:
        from_page = int(from_page)
    if to_page is not None:
        to_page = int(to_page)

    split_size = int(input("[+] Enter split size: ")) or config.default_split_size
    
    db_manager = init_db()
    out_folder = config.base_wdir / Path(pdf_file).stem
    if not out_folder.exists():
        out_folder.mkdir()
    split_pdfs = split_pdf(pdf_file, split_size, from_page, to_page, out_folder)
    table_name = input("Enter a short broadcast table alias: ") or str(Path(pdf_file).stem).lower()
    table_name = clean_table_name(table_name)
    broadcast_frequency = input("""Enter broadcast frequency:\n
      Sample: Every Saturday at 7:21pm\n
              Every Mon, Tue, Wed at 8:00pm \n
      Your input: """)
    add_split_pdfs_to_db(split_pdfs, db_manager, table_name + "_table", broadcast_frequency)
    schedule_broadcast(f'CDS: {table_name}', broadcast_frequency)

if __name__ == '__main__':
    os.system('clear')
    main()
    

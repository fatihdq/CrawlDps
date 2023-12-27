import time
import pandas as pd
from dotenv import load_dotenv
from pkg.googleSheet import GoogleSheet
from crawler.dpsCrawler import DpsCrawler
from pkg.progress import progress_bar
import os
import shutil

load_dotenv()

if __name__ == "__main__":
    try:
        SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    except:
        print("Error!!!: SPREADSHEET_ID not found in .env")
        exit()
    RESTART_ITTER = 25

    sheet_name = input("Sheet name: ")
    start_row = input("Start row: ")
    end_row = input("End row: ")

    if int(start_row) > int(end_row):
        print("Error!!!: End row must be higher than start row")
        exit()

    if os.path.exists('./ss/invalid'):
        shutil.rmtree('./ss/invalid')
    if os.path.exists('./ss/not_registered'):
        shutil.rmtree('./ss/not_registered')
    if os.path.exists('./ss/error_input'):
        shutil.rmtree('./ss/error_input')

    if not os.path.exists('./ss/invalid'):
        os.mkdir('./ss/invalid')
    if not os.path.exists('./ss/not_registered'):
        os.mkdir('./ss/not_registered')
    if not os.path.exists('./ss/error_input'):
        os.mkdir('./ss/error_input')

    gsheet = GoogleSheet(spreadsheet_id = SPREADSHEET_ID,
                         sheet_name=sheet_name,
                         start_range=start_row,
                         end_range=end_row)
    gsheet.createService()
    data = gsheet.read()

    start_time = time.time()
    print("Crawling Start...")
    crawl = DpsCrawler(headless=False)
    crawl.start()
    row = int(start_row)
    not_registered = 0

    for idx in range(len(data)):
        if not_registered == 2:
            crawl.quit()
            crawl = DpsCrawler(headless=False)
            crawl.start()
            not_registered = 0
            
        progress_bar(idx,len(data))
        if not data.loc[idx,'NIK'] == "" or not pd.isna(data.loc[idx,'NIK']):
            data = crawl.crawl(data,idx,row)
            if data.loc[idx,'DPT'] == "Not Registered":
                time.sleep(3)
                data = crawl.crawl(data,idx,row)
            if data.loc[idx,'DPT'] == "Not Registered":
                time.sleep(4)
                data = crawl.crawl(data,idx,row)
            if data.loc[idx,'DPT'] == "Not Registered":
                time.sleep(5)
                data = crawl.crawl(data,idx,row)

            if data.loc[idx,'DPT'] == "Not Registered":
                not_registered = not_registered + 1
            gsheet.writeRow(data.loc[idx,:],row)
        row = row + 1
        progress_bar(idx+1,len(data))
        time.sleep(3)
    
    print()
    print(f"{len(data)} Data Successfully Crawled:")
    
    end_time = time.time()
    print(f"Time taken: {((end_time-start_time)*10**3)/60000:.03f}m")

    data.to_excel('result.xlsx',index=False)


    
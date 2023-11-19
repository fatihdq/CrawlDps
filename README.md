# DPT Crawler

DPT Crawler is a crawl machine to retrieve information about the DPT (Daftar Pemilih Tetap) by the KPU. Integrated with Google Sheet so you can manage the NIK list and then in real time the information will be updated and you can select the sheet name and row range you want to crawl.

## Prerequites

To run this crawler, you need the following prerequisites:

- Python 3.9.0 or greater
- The pip package management tools (pip)[https://pypi.org/project/pip/]
- Git
- [A Google Cloud Project](https://developers.google.com/workspace/guides/create-project?hl=id)

# Start Guide

### A. Set Up Google Sheet Environment

### 1. Enable the API

You can turn on one or more APIs in a single Google Cloud project.

- In the Google Cloud console, enable the Google Sheets API.
  [Enable API](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com&hl=id)

### 2. Configure the OAuth consent screen

Configure the OAuth consent screen and add yourself as a test user. If you've already completed this step for your Cloud project, skip to the next section.
[Go to OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent?hl=id)

- Go to Menu > APIs & Services > OAuth consent screen
- Select the user type for your app, then click Create.
- Complete the app registration form, then click Save and Continue.
- For now, you can skip adding scopes and click Save and Continue. In the future, when you create an app for use outside of your Google Workspace organization, you must add and verify the authorization scopes that your app requires.
- If you selected External for user type, add test users
  - Under Test users, click Add users.
  - Enter your email address and any other authorized test users, then click Save and Continue.
- Review your app registration summary. To make changes, click Edit. If the app registration looks OK, click Back to Dashboard.

### 3. Authorize credentials for a desktop application

To authenticate as an end user and access user data in your app, you need to create one or more OAuth 2.0 Client IDs. A client ID is used to identify a single app to Google's OAuth servers.
[Go To Credentials](https://console.cloud.google.com/apis/credentials?hl=id)

- In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.
- Click Create Credentials > OAuth client ID.
- Click Application type > Desktop app.
- In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
- Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
- Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
- Save the downloaded JSON file as `GSCredentials.json`, and move the file to your working directory (Inside folder crawl machine).

### 4. Create Spreadshett

Create a new spreadsheet file or you can use an existing spreadsheet. You can only use columns A - H with their headers are [NIK, DPT, NAMA PEMILIH, TPS, ALAMAT TPS, KABUPATEN, KECAMATAN ,KELURAHAN] [Spreadsheet Template](https://docs.google.com/spreadsheets/d/1EgtiOvPg-F_ksB73HalcuQzM4xbiyyfE6_Edi1WPAjc/edit#gid=0)

### B. Get the crawl machine

### 1. Clone code from repository

```console
git clone https://github.com/fatihdq/CrawlDps.git
```

### 2. Setup .env

- Create file .env

```
touch .env
```

- Edit file .env

```
nano .env
```

- Then write like below:

```
SPREADSHEET_ID = [YOUR_SPREADSHEET_ID]
```

Example link: https://docs.google.com/spreadsheets/d/`1EgtiOvPg-F_ksB73HalcuQzM4xbiyyfE6_Edi1WPAjc`/edit#gid=0

```
SPREADSHEET_ID = 1EgtiOvPg-F_ksB73HalcuQzM4xbiyyfE6_Edi1WPAjc
```

- then ctrl+x -> Y -> Enter

### 3. Copy GSCredential.json to CrawlDps folder

The credentials for the Google account that you have renamed to `GSCredential.json`, you will need to copy them to the directory of crawl engine

### 4. install virtual env

- instal virtailenv package

```
pip install virtualenv
```

- Create the environment (creates a folder in your current directory)

```
virtualenv module_env
```

- in Linux or Mac, activate the new python environment

```
source module_env/bin/activate
```

- Or in Windows

```
.\module_env\Scripts\activate
```

- install requirement.txt (just 1 time)

```
pip install -r requirements.txt
```

- if you want to deactivate virtual env, then do:

```
deactivate
```

### 5. Running the code

```console
python main.py
```

then you should input the sheet name, start row ,and end row to identify which NIK list you want to crawl.

When you first time to using this crawl machine you will be directed to login with gmail account that have a access on your spreadsheet.

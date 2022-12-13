from config import *
import requests
import hmac
import hashlib
import time
import urllib.parse
import json
import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting  import *
import os
from threading import Thread
import telebot
from datetime import datetime
import schedule
re="\033[1;31m"
gr="\033[1;32m"
ye="\033[1;33m"
cy="\033[1;36m"
# os.system('clear') #linux
os.system('cls') # windows 
bot = telebot.TeleBot(bot_token)
print(f"""
{re}╔═╗{cy}┌─┐{re}═╦═
{re}╚═╗{cy}├─┤{re} ║
{re}╚═╝{cy}┴ ┴{re}═╩═
by https://github.com/foxius
""")
base_url = "https://testnet.binancefuture.com";
position_path = '/fapi/v2/positionRisk'
account_path = '/fapi/v1/account'
index_path = "/fapi/v1/premiumIndex"
headers= {
'Content-Type':'application/x-www-form-urlencoded',
'X-MBX-APIKEY': api_key
}
scopes = [
	'https://www.googleapis.com/auth/spreadsheets',
	'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file('creds.json',
	scopes=scopes)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(sheet_id)
worksheet = sheet.get_worksheet(0)
amountsheet = sheet.get_worksheet(1)
red = cellFormat(
	backgroundColor=color(1, 0, 0))
green = cellFormat(
	backgroundColor=color(0, 1, 0))
grey = cellFormat(
	backgroundColor=color(128, 128, 128))
white = cellFormat(
	backgroundColor=color(1, 1, 1))
usdfunding='=ОКРУГЛ(('
for i in range(2, len(symbols)+1):
	usdfundings = f"(Summ!B{i}*Summ!C{i})+"
	usdfunding += usdfundings
usdfundingform = str(usdfunding)
usdfundingl = len(usdfundingform)
usdfundingformula = usdfundingform[:usdfundingl-1]
usdfundingformula += ")*(-1);2)"
worksheet.update_cell(4, 5, usdfundingformula)
abssize = '='
for i in range(2, len(symbols)+1):
	abssizes = f'B{i}+'
	abssize += abssizes
abssizeform = str(abssize)
abssizel = len(abssizeform)
abssizeformula = abssizeform[:abssizel-1]
worksheet.update_cell(2, 5, abssizeformula)
worksheet.update_cell(10,5,ratiolimit)
def bot_sender():
	while True:
		timestamp = round(time.time()*1000)
		params = {
		"timestamp": timestamp
		}
		querystring = urllib.parse.urlencode(params)
		signature = hmac.new(api_secret.encode('utf-8'),msg = querystring.encode('utf-8'), digestmod = hashlib.sha256).hexdigest()
		payload = {}
		headers= {
		'Content-Type':'application/x-www-form-urlencoded',
		'X-MBX-APIKEY': api_key
		}
		account_url = base_url + account_path + '?' + querystring + '&signature='+ signature
		account_response = requests.request("GET", account_url, headers=headers, data = payload)
		account_data = json.loads(account_response.text)
		account_response = requests.request("GET", account_url, headers=headers, data = payload)
		account_data = json.loads(account_response.text)
		for i in account_data["assets"]:
			if i['asset'] == 'USDT':
				maint = float(i["maintMargin"])
				balance = float(i["marginBalance"])
				ratio = round(maint/balance*100 ,2)
				# print(ratio)
				if ratio >= ratiolimit:
					bot.send_message(RECIPIENT_ID, f'*Внимание*. Margin Ratio привысило лимит (*{ratiolimit}*). Текущее значение - *{ratio}*', parse_mode='Markdown')
					bot.send_message(adm_id, f'*Внимание*. Margin Ratio привысило лимит (*{ratiolimit}*). Текущее значение - *{ratio}*', parse_mode='Markdown')
		time.sleep(180)
def tables():	
	while True:
		try:
			timestamp = round(time.time()*1000)
			params = {
			"timestamp": timestamp
			}
			querystring = urllib.parse.urlencode(params)
			signature = hmac.new(api_secret.encode('utf-8'),msg = querystring.encode('utf-8'), digestmod = hashlib.sha256).hexdigest()
			payload = {}
			position_url = base_url + position_path + '?' + querystring + '&signature='+ signature
			position_response = requests.request("GET", position_url, headers=headers, data = payload)
			position_data = json.loads(position_response.text)
			account_url = base_url + account_path + '?' + querystring + '&signature='+ signature
			account_response = requests.request("GET", account_url, headers=headers, data = payload)
			account_data = json.loads(account_response.text)
			account_response = requests.request("GET", account_url, headers=headers, data = payload)
			account_data = json.loads(account_response.text)
			print('Запустил код')
			for i in account_data["assets"]:
				if i['asset'] == 'USDT':
					maint = float(i["maintMargin"])
					balance = float(i["marginBalance"])
					ratio = round(maint/balance*100 ,2)
					worksheet.update_cell(8,5, ratio)
			for d in symbols:
				time.sleep(4)
				index_payload = {"symbol": d}
				index_url = base_url + index_path
				index_response = requests.get(index_url,index_payload)
				index_data = json.loads(index_response.text)
				for i in position_data:
					if i["symbol"] == d:
						if float(i['notional']) != 0:
							size = round(float(i["notional"]))
							markprice = round(float(index_data["markPrice"]),4)
							indexprice = round(float(index_data["indexPrice"]),4)
							deviation = round((markprice - indexprice)/markprice * 100,4)
							funding = round(float(index_data["lastFundingRate"])*100,4) 
							dictionary = ([d, size, funding, deviation])
							cell = worksheet.find(d, in_column=0)
							amountcell = amountsheet.find(d, in_column=0)
							dictamount = ([d, size, float(index_data["lastFundingRate"])])
							if cell is None:
								worksheet.append_row(dictionary)
							else:
								if size < 0:
									clg = f'B{cell.row}'
									print(f"{re}[{cy}{d},{re}{size},{funding},{deviation}]")
									format_cell_range(worksheet,f'{clg}:{clg}',red)
									worksheet.update_cell(cell.row, 2, abs(size))
									worksheet.update_cell(cell.row, 3, funding)
									worksheet.update_cell(cell.row, 4, deviation)
									
								if size > 0:
									clg = f'B{cell.row}'
									print(f"{gr}[{cy}{d},{gr}{size},{funding},{deviation}]")
									format_cell_range(worksheet,f'{clg}:{clg}', green)
									worksheet.update_cell(cell.row, 2, abs(size))
									worksheet.update_cell(cell.row, 3, funding)
									worksheet.update_cell(cell.row, 4, deviation)
							if amountcell is None:
								amountsheet.append_row(dictamount)
							else:
								clg = f'B{cell.row}'
								amountsheet.update_cell(amountcell.row, 2, size)
								amountsheet.update_cell(amountcell.row, 3, float(index_data["lastFundingRate"]))
								
						else:
							size = 0
							markprice = round(float(index_data["markPrice"]),4)
							indexprice = round(float(index_data["indexPrice"]),4)
							deviation = round((markprice - indexprice)/markprice * 100,4)
							funding = round(float(index_data["lastFundingRate"])*100,4) 
							dictionary = ([d, size, funding, deviation])
							dictamount = ([d, size, float(index_data["lastFundingRate"])])
							print(f"{ye}[{cy}{d},{ye}{size},{funding},{deviation}]")
							cell = worksheet.find(d, in_column=0)
							amountcell = amountsheet.find(d, in_column=0)
							if cell is None:
								worksheet.append_row(dictionary)
							else:
								clg = f'B{cell.row}'
								format_cell_range(worksheet,f'{clg}:{clg}',grey)
								worksheet.update_cell(cell.row, 2, size)
								worksheet.update_cell(cell.row, 3, funding)
								worksheet.update_cell(cell.row, 4, deviation)
							if amountcell is None:
								amountsheet.append_row(dictamount)
							else:
								clg = f'B{cell.row}'
								amountsheet.update_cell(amountcell.row, 2, size)
								amountsheet.update_cell(amountcell.row, 3, float(index_data["lastFundingRate"]))
					
		except Exception as e:
			print(e)
			continue
def expiration():
	now = datetime.now()
	current_time = now.strftime("%H:%M")
	val = worksheet.acell('E4').value
	print(f"[{cy}GET expiration {gr}{val}]")
	worksheet.update_cell(11, 5, f"Значение в последнюю экспирацию ({current_time})")
	worksheet.update_cell(12, 5, val)
def expiration_check():
	schedule.every().day.at("01:00").do(expiration)
	schedule.every().day.at("09:00").do(expiration)
	schedule.every().day.at("21:36").do(expiration)
	while True:
		schedule.run_pending()
		time.sleep(1)
thread = Thread(target = bot_sender, args=(), daemon = True)
thread1 = Thread(target = expiration_check, args=(), daemon = True)
thread.start()
thread1.start()
tables()

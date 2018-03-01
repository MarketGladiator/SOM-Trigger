# INFO
#
# Version: 1.0.1
# Author: James Black (Discord @PsiliPharm)
# Credits: Based of SOM-Trigger_v1.3.ps1 Shell Script by Noel Stephenson (Discord @NoelS)
# Source Link: https://onedrive.live.com/?authkey=%21ANZv45qsSyq83p8&cid=D3BBC7F676E8898A&id=D3BBC7F676E8898A%21172135&parId=D3BBC7F676E8898A%21172134&o=OneUp
#
#
# API
#
# Uses Coindesk API to determine the current BTC price in Fiat (Default: USD)
# http://www.coindesk.com/api/
#
#
# DISCLAIMER
#
# This script is provided as is.  No warranty, Limited Support.
# To use the script. Place in your Profit Trailer program folder or wherever you want this script to live on your Linux/Mac or VPS box.
#
#
# USAGE
#
# Edit the script and alter the settings in the PARAMETERS SECTION below and save.
#
# Run the following in the terminal from the SOM-Trigger location:
#
# python SOM-Trigger.py
#
# PM2 Setup Instructions:
#
# npm install pm2@latest -g
#
# pm2 start pm2-SOM-Trigger.json
#
# To save as a startup script run:
#
# pm2 save
# pm2 startup
#
#
# CHANGELOG
#   - Initial Version based off of SOM-Trigger_v1.3.ps1
#   - Added Support to Configure the Base Coin a.k.a. Trading Market
#   - Added Support to Configure the Fiat Currency
#   - Fixed Issue with PM2 not logging output correctly
#
#
# DONATE
# If you find this script useful, please consider a small donation.
#
#   BTC address:  1EAZKnWwdgMWyRwHJxuM1x5Ue47CbFWz77
#   ETH address:  0x66e3062A31dFDA680aDc1555f1c646d6Bb1D3274
#   LTC address:  Li9MbeohmAjn1fcS15YR2f2hKs3oKDxZkB
#   NANO address: xrb_1mxdnmoszfq3je95aemcf7936s3gk5nuawkj3p5p69jcqczbgwegnonhhjjw
#

############ PARAMETERS SECTION ##############

# Base Trading Coin or Market set in Profit Trader.  Available Options (Default: "BTC"):
# Currently, only "BTC" and "ETH" supported.
base_coin = "BTC"
# Fiat currency to check the Base Coin (Default: "BTC") price against.  Available Options (Default: "USD"):
# "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "USD", "ZAR"
fiat_currency = "USD"
# The following line is the Number of hours between price checks.  Recommended to set to minimum of 2.
hours = 2
# Enable Sell Only Mode if Price hits Drop Trigger: Set to 'False' to disable.
trigger_drop = True
# Percentage decrease to check for.
trigger_drop_percent = 4
# Enable Sell Only Mode if Price hits Rise Trigger: Set to 'False' to disable.
trigger_rise = True
# Percentage increaase to check for.
trigger_rise_percent = 4
# Path to your PAIRS.properties file.
pf_path = "/ProfitTrailer/trading/PAIRS.properties"

############ END PARAMETERS SECTION ##############

import json, sys, time, urllib
from datetime import datetime, timedelta
from tempfile import mkstemp
from os import fdopen, path, remove
from shutil import move

# Force Sell Only Mode by Setting to 'True'
trigger_som = False

def check_pf_path():
  file_exists = path.isfile(pf_path)

  # Check if the PAIRS.properties file path is valid.
  if file_exists:
    print "\033[92mSuccess:\033[0m PAIRS.properties path validated."

    check_sell_only_mode()
  else:
    sys.exit("\033[91mError:\033[0m No PAIRS.properties path found. Configure the 'pf_path' variable in your script.\n")

def check_sell_only_mode():
  pairs_file = open(pf_path, 'r')

  valid_file = False
  sell_only_mode = "ALL_sell_only_mode"

  index = 0
  lines = pairs_file.readlines()

  # Validate 'ALL_sell_only_mode' is in the PAIRS.properties file.
  for line in lines:
    if sell_only_mode in line:
      print "\033[92mSuccess:\033[0m '%(line)s' found in pairs file at line number: %(line_number)s\n" % { 'line': line.rstrip(), 'line_number': index + 1 }

      valid_file = True

      break

    index += 1

  if not valid_file:
      print "\033[91mError:\033[0m Cannot find an entry for '%(line)s' in the pairs file." % { 'line': sell_only_mode }
      print "\033[93mWarning:\033[0m Please add '%(line)s = false' to the pairs file and restart the script." % { 'line': sell_only_mode }

def get_coin_price():
  url = "https://api.coinmarketcap.com/v1/ticker/%(base_coin)s/?convert=%(fiat)s" % { 'fiat': fiat_currency, 'base_coin': 'bitcoin' if base_coin == "BTC" else 'ethereum' }

  response = urllib.urlopen(url)
  data = json.loads(response.read())

  price_key = "price_%(fiat)s" % { 'fiat': fiat_currency.lower() } 
  price = data[0][price_key]
  change = data[0]['percent_change_1h']

  return price, change

def check_price_variation(base_price):
  fallen = False
  risen = False
  time_check = datetime.now()
  coin_price = get_coin_price()
  current_price = float(coin_price[0])
  hour_change = float(coin_price[1])
  diff = int((base_price - current_price) / base_price * 100)

  if diff < 0:
    # Number is negative - convert to positive for next logic.
    # Price has fallen.
    if diff > hour_change:
      diff = hour_change

    fallen = True
    risen = False

    diff = diff * -1
  else:
    # Price has risen.
    if diff < hour_change:
      diff = hour_change

    fallen = False
    risen = True

  print "Current Price: \033[36m%(current_price)s\033[0m" % { 'current_price': current_price }
  print "Last Price: \033[36m%(base_price)s\033[0m\n" % { 'base_price': base_price }

  if diff >= trigger_drop_percent or diff >= trigger_rise_percent or trigger_som == True:
    print "\033[91mPrice has changed by %(diff)s%% since last check.\033[0m\n" % { 'diff': diff }

    set_sell_only_mode(True)
  else:
    print "\033[92mPrice has changed within acceptable parameters %(diff)s%% since last check.\033[0m" % { 'diff': diff }
    print "Price has changed by %(hour_change)s%% in the past hour.\n" % { 'hour_change': hour_change }

    set_sell_only_mode(False)

  return current_price

def set_sell_only_mode(mode):
  sell_only_false = "ALL_sell_only_mode = false"
  sell_only_true = "ALL_sell_only_mode = true"

  if mode == True:
    replace = sell_only_false
    substution = sell_only_true
  else:
    replace = sell_only_true
    substution = sell_only_false

  # Create temp file for new PAIRS.properties file.
  file_handle, temp_path = mkstemp()

  with fdopen(file_handle,'w') as new_file:
    with open(pf_path) as old_file:
      for line in old_file:
        new_file.write(line.replace(replace, substution))

  # Remove old PAIRS.properties file.
  remove(pf_path)

  # Move new PAIRS.properties file.
  move(temp_path, pf_path)

  print "Sell Only Mode is: \033[93m%(sell_only_mode)s\033[0m\n" % { 'sell_only_mode': 'Enabled' if mode == True else 'Disabled' }

def run_script():
  # Get current coin price.
  coin_price = get_coin_price()
  base_price = float(coin_price[0]) - round(float(coin_price[0]) / 100 * float(coin_price[1]), 2)

  while True:
    time_check = datetime.now()
    current_price = check_price_variation(base_price)

    base_price = current_price
    last_time_check = time_check
    next_time_check = last_time_check + timedelta(hours = hours)

    print "- Last Checked Time: \033[36m%(last_time_check)s\033[0m" % { 'last_time_check': last_time_check.strftime('%m/%d/%Y %I:%M %p') }
    print "- Next Check Time: \033[36m%(next_time_check)s\033[0m" % { 'next_time_check': next_time_check.strftime('%m/%d/%Y %I:%M %p') }

    print "\n*** Press [Ctrl]+[C] to Quit ***\n"

    seconds = 3600 * hours

    time.sleep(seconds)

# Check PAIRS.properties file.
check_pf_path()

# Run script in a loop.
try:
  run_script()
except KeyboardInterrupt:
  # Quit
  sys.exit()
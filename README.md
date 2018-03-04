# SOM-Trigger

A script designed to check CoinMarketCap for extreme market conditions and put ProfitTrailer into Sell-Only Mode automatically.

  - Version: 1.0.1
  - Author: James Black (Discord @PsiliPharm)
  - Credits: Based of SOM-Trigger_v1.3.ps1 Shell Script by Noel Stephenson (Discord @NoelS)
  - Source Link: [https://1drv.ms/f/s!AoqJ6Hb2x7vTisBmy7icciJmrbhoRw](https://1drv.ms/f/s!AoqJ6Hb2x7vTisBmy7icciJmrbhoRw)


## API

Uses [Coindesk API](http://www.coindesk.com/api/) to determine the current BTC price in Fiat (Default: USD)


## DISCLAIMER

This script is provided as is.  No warranty, Limited Support.

To use the script. Place in your Profit Trailer program folder or wherever you want this script to live on your Linux/Mac or VPS box.


## USAGE

Edit the script and alter the settings in the PARAMETERS SECTION within the `SOM-Trigger.py` file and save.

Run the following in the terminal from the SOM-Trigger location:

    python SOM-Trigger.py

PM2 Setup Instructions:

    npm install pm2@latest -g

    pm2 start pm2-SOM-Trigger.json

To save as a startup script run:

    pm2 save
    pm2 startup


## CHANGELOG

  - Initial Version based off of `SOM-Trigger_v1.3.ps1`
  - Added Support to Configure the Base Coin a.k.a. Trading Market
  - Added Support to Configure the Fiat Currency
  - Fixed Issue with PM2 not logging output correctly


## DONATE

If you find this script useful, please consider a small donation.

  - BTC address:  1EAZKnWwdgMWyRwHJxuM1x5Ue47CbFWz77
  - ETH address:  0x66e3062A31dFDA680aDc1555f1c646d6Bb1D3274
  - LTC address:  Li9MbeohmAjn1fcS15YR2f2hKs3oKDxZkB
  - NANO address: xrb_1mxdnmoszfq3je95aemcf7936s3gk5nuawkj3p5p69jcqczbgwegnonhhjjw

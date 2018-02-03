import re

import aiohttp
from discord.ext import commands

try:
    from prettytable import PrettyTable
    requirementsSuccess = True
except:
    requirementsSuccess = False

class CryptoAUD:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cryptoaud(self, *currencies):
        """Fetch price data for cryptocurrencies provided to the command.
        If currency is omitted, will display top 5 by market cap."""    
        
        #set currencies to empty if none provided, and get 5 currencies.
        if len(currencies) == 0:
            currencies = [None]
            numCurrenciesLeft = 5
        else:
            numCurrenciesLeft = len(currencies)
            
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coinmarketcap.com/v1/ticker/?convert=AUD") as response:
                jsonData = await resp.json()
        for result in jsonData:
            if currencies[0] is None:
                results.append(result)
                numCurrenciesLeft -= 1
                if numCurrencies == 0:
                    break
            else:
                colSymbol = result['symbol']
                currencyName = result['name']
                if (colSymbol in [x.upper() for x in currencies]) or (currencyName.lower() in [x.lower() for x in currencies])::
                    results.append(result)
                    numCurrenciesLeft -=1
                    if numCurrenciesLeft == 0:
                        break
                
        if len(results) == 0:
            await self.bot.say("No currencies matched your query!")
            return
        else:
            text = await self.tableize(results)
        
        await self.bot.say("```" + text + "```")
        
    async def tableize(self, results):
        
        headers = ['Name', 'Symbol', 'Price (USD)', 'Price (AUD)', 'Change (24hr)']    
        x = PrettyTable(headers)
        
        ####
        #Old exchange rate code
        ####
        #rate = 0
        #url = 'http://api.fixer.io/latest?base=USD&symbols=AUD'
        #async with aiohttp.ClientSession() as session:
        #    async with session.get(url) as r:
        #        exch = await r.json()
        #rate = float(exch['rates']['AUD'])

        for row in results:
            column = []
            column.append(row['name'])
            column.append(row['symbol'])
            
            priceUSD = row['price_usd']
            flPriceUSD = float(priceUSD)
            priceAUD = row['price_aud']
            flPriceAUD = float(priceAUD)
            
            column.append('${0:.2f}'.format(flPriceUSD))
            column.append('${0:.2f}'.format(flPriceAUD))
            column.append('{}%'.format(row['percent_change_24h']))
            x.add_row(column)
        x.align["Change (24hr)"] = "r"
        x.align["Price (USD)"] = "r"
        x.align["Price (AUD)"] = "r"
        x.align["Name"] = "l"
        x.align["Symbol"] = "c"
        return x.get_string()


def setup(bot):
    if requirementsSuccess:
        bot.add_cog(CryptoAUD(bot))
    else:
        raise RuntimeError("You are missing requirements. Please run:\n"
                           "`pip3 install prettytable`")
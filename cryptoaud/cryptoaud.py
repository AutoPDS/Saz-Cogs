import re

import aiohttp
from discord.ext import commands

try:
    from bs4 import BeautifulSoup
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
        
        numColumns = 4
        results = []
        numCurrencies = 0
        text = ""
        
        if len(currencies) == 0:
            currencies = [None]
        for i in currencies:
            async with aiohttp.get("https://coinmarketcap.com") as response:
                marketsoup = BeautifulSoup(await response.text(), "html.parser")
            tds = marketsoup.find_all("tr", id=re.compile("id-"))
            for result in tds:
                if i is None:
                    results.append(result)
                    if numCurrencies == 4:
                        break
                    numCurrencies += 1
                else:
                    colSymbol = result.find("td", class_="circulating-supply").find("span", class_="hidden-xs").get_text().strip()
                    currencyName = result.find("a", class_="currency-name-container").get_text().strip().lower()
                    if (colSymbol == i.upper()) or (currencyName == i.lower()):
                        results.append(result)
                        break
                
        if len(results) == 0:
            await self.bot.say("No currencies matched your query!")
        else:
            text = await self.tableize(results)
        
        await self.bot.say("```" + text + "```")
        
    async def tableize(self, results):
        
        headers = ['Name', 'Symbol', 'Price (USD)', 'Price (AUD)', 'Change']    
        x = PrettyTable(headers)
        
        rate = 0
        url = 'http://api.fixer.io/latest?base=USD&symbols=AUD'
        async with aiohttp.request("GET", url) as r:
            exch = await r.json()
            rate = float(exch['rates']['AUD'])
    
        for row in results:
            column = []
            column.append(row.find("a", class_="currency-name-container").get_text().strip())
            column.append(result.find("td", class_="circulating-supply").find("span", class_="hidden-xs").get_text().strip())
            
            priceUSD = row.find("a", class_="price").get_text().strip().strip("$")
            flPriceUSD = float(priceUSD)
            flPriceAUD = float(rate * flPriceUSD)
            
            column.append('${0:.2f}'.format(flPriceUSD))
            column.append('${0:.2f}'.format(flPriceAUD))
            column.append(row.find("td", class_="percent-24h").get_text().strip())
            x.add_row(column)
            
        return x.get_string()


def setup(bot):
    if requirementsSuccess:
        bot.add_cog(CryptoAUD(bot))
    else:
        raise RuntimeError("You are missing requirements. Please run:\n"
                           "`pip3 install beautifulsoup4`\n"
"`pip3 install tabulate`")
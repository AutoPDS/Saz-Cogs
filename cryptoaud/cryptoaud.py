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
        self.url = "https://coinmarketcap.com/"

    @commands.command()
    async def cryptoaud(self, *currencies):
        """Fetch price data for cryptocurrencies matching your query.
        If currency is omitted, will display top 5 by market cap."""
        
        numColumns = 4
        results = []
        numCurrencies = 0
        if len(currencies) == 0:
            currencies = None
        
        for i in currencies:
            async with aiohttp.get("https://coinmarketcap.com/all/views/all/") as response:
                marketsoup = BeautifulSoup(await response.text(), "html.parser")
            tds = cryptosoup.find_all("tr", id=re.compile("id-"))
            for result in tds:
                colSymbol = result.find("td", class_="col-symbol").get_text().strip()
                currencyName = result.find("td", class_="currency-name").a.get_text().strip()
                if (colSymbol == i.upper()) or (currencyName == i.lower()):
                    results.append(result)
                else:
                    if currencies is None:
                        if numCurrencies < 5:
                            results.append(result)
                numCurrencies += 1
                
        if len(results) == 0:
            await self.bot.say("No currencies matched your query!")
        else:
            text = self.tableize(results)
        await self.bot.say("```" + text + "```")
        
    def tableize(self, results):
        
        headers = ['Name', 'Symbol', 'Price (USD)', 'Price (AUD)', 'Change']    
        x = PrettyTable(headers)
        
        for row in results:
            column = []
            column.append(row.find("td", class_="currency-name").a.get_text().strip())
            column.append(row.find("td", class_="col-symbol").get_text().strip)
            
            priceUSD = row.find("a", class_="price").get_text().strip()
            flPriceUSD = float(priceUSD)
            rate = 0
            url = 'http://api.fixer.io/latest?base=USD&symbols=AUD'
            async with aiohttp.request("GET", url) as r:
                exch = await r.json()
                rate = float(exch['rates']['AUD'])
            flPriceAUD = float(rate * flPriceUSD)
            
            column.append('${0:.2f}'.format(flPriceUSD))
            column.append('${0:.2f}'.format(flPriceAUD))
            column.append(row.find("td", class_="percent-24h").get_text().strip())
            x.add_row(column)
            
        return x


def setup(bot):
    if requirementsSuccess:
        bot.add_cog(CryptoAUD(bot))
    else:
        raise RuntimeError("You are missing requirements. Please run:\n"
                           "`pip3 install beautifulsoup4`\n"
"`pip3 install tabulate`")
import os
import json
from pathlib import Path

latest = 0
def example_context(language="English"):
    latest = 0
    path = Path(f"news_data/{language}")
    for path in path.iterdir():
        if ".gitignore" in path.name:
            continue
        name = int(path.name.split("/")[-1].split(".")[0])
        if name > latest:
            latest = name
            continue
        with open(f"{path}", "r", encoding="utf-8") as f:
            return json.loads(f.read())
    



def system_prompt(context_history):
    return f"""
    ABOUT YOU:
    You are a expert new anaylsist specializing particularly in financy and crypto currencies. You are present a news breif that summarizes all the news around particular tickers every day. 

    YOUR TASK:
    You need to take the breif presented to you and summarize the content as an output markdown string. Your response will be put directly into markdown and hosted on the sight so please just respond with the summary and nothing else. If you need to plan out your response you can wrap the non markdown response with <scratchpad> tags </scratchpad>.

    The following is an example breifing and an example response. 
    
    EXAMPLE CONTEXT:
    {context_history}

    EXAMPLE RESPONSE:
    markdown_content = '''
    ### GameStop (GME)
    1. **Recent Performance**: {{gme_recent_performance}}
    2. **Earnings Expectations**: {{gme_earnings_expectations}}
    3. **Market Reaction**: {{gme_market_reaction}}
    4. **Meme Stock Volatility**: {{gme_meme_stock_volatility}}

    ### Tesla (TSLA)
    1. **Investor Sentiment**: {{tsla_investor_sentiment}}
    2. **Earnings and Autonomy Focus**: {{tsla_earnings_autonomy}}
    3. **Political Impact**: {{tsla_political_impact}}
    4. **Stock Performance and Analyst Views**: {{tsla_stock_performance}}

    ### Bitcoin (BTC) and Ethereum (ETH)
    1. **Market Volatility**: {{btc_eth_market_volatility}}
    2. **ETF Impact**: {{btc_eth_etf_impact}}
    3. **Recent Trends**: {{btc_eth_recent_trends}}
    4. **Mining and Institutional Interest**: {{btc_eth_mining_institutional}}

    ### Solana (SOL)
    1. **Market Performance**: {{sol_market_performance}}
    2. **Investment Products**: {{sol_investment_products}}
    3. **Partnerships and Expansion**: {{sol_partnerships_expansion}}

    ### Wrap Technologies (WRAP)
    1. **Compliance Issues**: {{wrap_compliance_issues}}
    2. **Leadership Changes**: {{wrap_leadership_changes}}
    3. **Product Expansion**: {{wrap_product_expansion}}

    ### Miscellaneous
    1. **Bob Marley Biopic Success**: {{misc_bob_marley}}
    2. **Crypto Market Insights**: {{misc_crypto_insights}}
    '''.format(
        gme_recent_performance=news_data['GME']['https://finance.yahoo.com/news/know-beyond-why-gamestop-corp-130016722.html']['summary'],
        gme_earnings_expectations=news_data['GME']['https://finance.yahoo.com/news/gamestop-gme-stock-declines-while-214518882.html']['summary'],
        gme_market_reaction="Significant attention on its upcoming earnings report. Investors are interested in recent analyst estimate revisions.",
        gme_meme_stock_volatility="GameStop, known for its meme stock status, has seen substantial drops and some recovery.",
        tsla_investor_sentiment=news_data['TSLA']['https://finance.yahoo.com/news/berkshire-hathaways-massive-277m-cash-190030484.html']['summary'],
        tsla_earnings_autonomy=news_data['TSLA']['https://finance.yahoo.com/news/elon-musk-just-told-tesla-111500029.html']['summary'],
        tsla_political_impact=news_data['TSLA']['https://finance.yahoo.com/news/harris-buttigieg-could-beneficial-tesla-170008571.html']['summary'],
        tsla_stock_performance=news_data['TSLA']['https://finance.yahoo.com/news/tesla-stock-going-310-1-101500353.html']['summary'],
        btc_eth_market_volatility=news_data['BTC']['https://finance.yahoo.com/news/happened-crypto-today-bitcoins-least-101443588.html']['summary'],
        btc_eth_etf_impact=news_data['BTC']['https://finance.yahoo.com/news/crypto-etfs-actually-hurting-bitcoin-150827232.html']['summary'],
        btc_eth_recent_trends=news_data['BTC']['https://finance.yahoo.com/news/bitcoin-drops-below-59-000-235215498.html']['summary'],
        btc_eth_mining_institutional=news_data['BTC']['https://finance.yahoo.com/news/bitcoin-mining-difficulty-hits-record-062021957.html']['summary'],
        sol_market_performance=news_data['SOL']['https://finance.yahoo.com/news/sol-surges-faces-resistance-market-072344982.html']['summary'],
        sol_investment_products=news_data['SOL']['https://finance.yahoo.com/news/3iq-plans-north-america-first-174325896.html']['summary'],
        sol_partnerships_expansion=news_data['SOL']['https://finance.yahoo.com/news/solana-surges-ethereum-struggles-furrever-173000318.html']['summary'],
        wrap_compliance_issues=news_data['wTAO']['https://www.globenewswire.com/news-release/2024/05/24/2888112/0/en/Wrap-Technologies-Receives-Nasdaq-Notification-of-Non-Compliance-with-Listing-Rule-5250-c-1.html']['summary'],
        wrap_leadership_changes=news_data['wTAO']['https://www.globenewswire.com/news-release/2024/01/16/2809982/0/en/Wrap-Technologies-Inc-Appoints-Scot-Cohen-as-Chief-Executive-Officer.html']['summary'],
        wrap_product_expansion=news_data['wTAO']['https://www.globenewswire.com/en/news-release/2023/12/27/2801380/0/en/Wrap-Technologies-Inc-Announces-Largest-BolaWrap-Order-in-Company-History.html']['summary'],
        misc_bob_marley=news_data['wTAO']['https://www.yahoo.com/entertainment/elvis-elton-bob-marley-music-140000052.html']['summary'],
        misc_crypto_insights=news_data['BTC']['https://finance.yahoo.com/news/crypto-etfs-actually-hurting-bitcoin-150827232.html']['summary'],
    )
    
    NEW_CONTEXT:
    """
    
class Context:
    def __init__(self, context=None, context_history=None):
        self.context = context or system_prompt(context_history)
    def __name__(self):
        return self.context
    
def get_context(language="English"):
    context_history = example_context(language)
    return Context(context_history)
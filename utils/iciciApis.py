


def placeOptionsOrder(breeze, stock_code, expiry, strikePrice, right):

    breeze.get_quotes(stock_code=stock_code,
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right=right,
                    strike_price=strikePrice)
    
    breeze.place_order(stock_code=stock_code,
                    exchange_code="NFO",
                    product="options",
                    action="buy",
                    order_type="market",
                    stoploss="",
                    quantity="50",
                    price="",
                    validity="day",
                    validity_date="2022-08-30T06:00:00.000Z",
                    disclosed_quantity="0",
                    expiry_date="2022-09-29T06:00:00.000Z",
                    right="call",
                    strike_price="16600")

                    
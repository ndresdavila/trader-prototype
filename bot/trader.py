import MetaTrader5 as mt5
import json

# Cargar la orden desde Node.js
with open("server/orders/last_order.json", "r") as f:
    order = json.load(f)

symbol = order.get("symbol", "EURUSD")
volume = float(order.get("volume", 0.1))
action = order.get("action", "buy")

# Inicializar conexión
if not mt5.initialize():
    print("Fallo al iniciar MT5:", mt5.last_error())
    quit()

# Obtener precios actuales
symbol_info = mt5.symbol_info_tick(symbol)
price = symbol_info.ask if action == "buy" else symbol_info.bid
order_type = mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL

# Enviar orden
result = mt5.order_send({
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": volume,
    "type": order_type,
    "price": price,
    "deviation": 10,
    "magic": 123456,
    "comment": "TradingView -> MT5",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
})

# Resultado
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Fallo al enviar orden:", result)
else:
    print("Orden ejecutada:", result)

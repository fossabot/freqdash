import logging
from decimal import Decimal
from typing import Union

from freqdash.exchange.exchange import Exchange
from freqdash.exchange.utils import Intervals, Settle, send_public_request

log = logging.getLogger(__name__)


class Kucoin(Exchange):
    def __init__(self):
        super().__init__()
        log.info("Kucoin initialised")

    exchange = "kucoin"
    spot_api_url = "https://api.kucoin.com"
    spot_trade_url = "https://www.kucoin.com/trade/BASE-QUOTE"
    futures_api_url = "https://api-futures.kucoin.com"
    futures_trade_url = "https://www.kucoin.com/futures/trade/BASEQUOTE"
    max_weight = 600

    def get_spot_price(self, base: str, quote: str) -> Decimal:
        self.check_weight()
        params = {"symbol": f"{base}-{quote}"}
        header, raw_json = send_public_request(
            api_url=self.spot_api_url,
            url_path="/api/v1/market/orderbook/level1",
            payload=params,
        )
        if "data" in [*raw_json]:
            if "price" in [*raw_json["data"]]:
                return Decimal(raw_json["data"]["price"])
        return Decimal(-1.0)

    def get_spot_prices(self) -> list:
        self.check_weight()
        params: dict = {}
        header, raw_json = send_public_request(
            api_url=self.spot_api_url,
            url_path="/api/v1/market/allTickers",
            payload=params,
        )
        if "data" in [*raw_json]:
            if "ticker" in [*raw_json["data"]]:
                return [
                    {
                        "symbol": pair["symbol"].replace("-", ""),
                        "price": Decimal(pair["last"]),
                    }
                    for pair in raw_json["data"]["ticker"]
                ]
        return []

    def get_spot_kline(
        self,
        base: str,
        quote: str,
        interval: Intervals = Intervals.ONE_DAY,
        start_time: Union[int, None] = None,
        end_time: Union[int, None] = None,
        limit: int = 500,
    ) -> list:
        self.check_weight()
        custom_intervals = {
            "1m": "1min",
            "5m": "5min",
            "15m": "15min",
            "1h": "1hour",
            "4h": "4hour",
            "1d": "1day",
            "1w": "1week",
        }
        params: dict = {"symbol": f"{base}-{quote}", "type": custom_intervals[interval]}
        if start_time is not None:
            params["startAt"] = start_time
        if end_time is not None:
            params["endAt"] = end_time

        header, raw_json = send_public_request(
            api_url=self.spot_api_url, url_path="/api/v1/market/candles", payload=params
        )

        if "data" in [*raw_json]:
            if len(raw_json["data"]) > 0:
                return [
                    {
                        "timestamp": int(candle[0]),
                        "open": Decimal(candle[1]),
                        "high": Decimal(candle[3]),
                        "low": Decimal(candle[4]),
                        "close": Decimal(candle[2]),
                        "volume": Decimal(candle[5]),
                    }
                    for candle in raw_json["data"]
                ][:limit]
        return []

    def get_futures_price(self, base: str, quote: str) -> Decimal:
        self.check_weight()
        params = {"symbol": f"{base}{quote}"}
        header, raw_json = send_public_request(
            api_url=self.futures_api_url,
            url_path="/api/v1/ticker",
            payload=params,
        )
        if "data" in [*raw_json]:
            if "price" in [*raw_json["data"]]:
                return Decimal(raw_json["data"]["price"])
        return Decimal(-1.0)

    def get_futures_prices(self) -> list:
        self.check_weight()
        params: dict = {}
        header, raw_json = send_public_request(
            api_url=self.futures_api_url,
            url_path="/api/v1/contracts/active",
            payload=params,
        )
        if "data" in [*raw_json]:
            if len(raw_json["data"]) > 0:
                return [
                    {
                        "symbol": pair["symbol"],
                        "price": Decimal(pair["markPrice"]),
                    }
                    for pair in raw_json["data"]
                ]
        return []

    def get_futures_kline(
        self,
        base: str,
        quote: str,
        start_time: Union[int, None] = None,
        end_time: Union[int, None] = None,
        interval: Intervals = Intervals.ONE_DAY,
        limit: int = 500,
        settle: Union[Settle, None] = None,
    ) -> list:
        self.check_weight()
        custom_intervals = {
            "1m": 1,
            "5m": 5,
            "15m": 15,
            "1h": 60,
            "4h": 240,
            "1d": 1440,
            "1w": 10080,
        }
        params: dict = {
            "symbol": f"{base}{quote}",
            "granularity": custom_intervals[interval],
        }
        if start_time is not None:
            params["from"] = start_time
        if end_time is not None:
            params["to"] = end_time

        header, raw_json = send_public_request(
            api_url=self.futures_api_url, url_path="/api/v1/kline/query", payload=params
        )

        if "data" in [*raw_json]:
            if len(raw_json["data"]) > 0:
                return [
                    {
                        "timestamp": int(candle[0]),
                        "open": Decimal(candle[1]),
                        "high": Decimal(candle[2]),
                        "low": Decimal(candle[3]),
                        "close": Decimal(candle[4]),
                        "volume": Decimal(candle[5]),
                    }
                    for candle in raw_json["data"]
                ][:limit]
        return []

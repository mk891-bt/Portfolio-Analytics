
import pandas
import numpy


class StockPriceSimulator:

    def __init__(self):
        """
        Initialize the stock data simulator.
        """

    def __generate_unique_names(self, num_stocks:int) -> list[str]:
        """
        Generate a deterministic list of unique stock identifiers.

        This method creates a list of stock names in the format
        'stock_1', 'stock_2', ..., 'stock_N', where N equals
        the value of `num_stocks`.

        The naming is deterministic, contains no randomness,
        and guarantees uniqueness without relying on external
        libraries.

        Args:
            num_stocks (int):
                The total number of stock identifiers to generate.

        Returns:
            list[str]:
                A list of unique stock names of length `num_stocks`.
        """
        return [f"stock_{number}" for number in range(1, num_stocks + 1)]

    def __create_dates(self, interval: str, 
                       num_periods: int, 
                       starting_date: str) -> pandas.DatetimeIndex:
        """
        Generate a date index for the simulation based on the specified interval.

        Args:
            interval (str): "d" = daily, "w" = weekly, "m" = monthly
            num_periods (int): Number of periods to generate
            starting_date (str): Starting date of the index (YYYY-MM-DD)

        Returns:
            pd.DatetimeIndex: The generated date index
        """
        interval_map = {
            "d": "B",  # business days
            "w": "W",  # weekly
            "m": "BME",  # month end
        }

        if interval not in interval_map:
            raise ValueError("interval must be 'd', 'w', or 'm'")

        freq = interval_map[interval]
        dates = pandas.date_range(start=starting_date, periods=num_periods, freq=freq)
        return dates

    
    def create_stock_prices(self, num_stocks: int, num_periods: int,
                            starting_date: str = "2010-01-01", interval: str = "d") -> pandas.DataFrame:
        """
        Create simulated stock price data.

        Args:
            num_stocks (int): Number of stocks to simulate
            num_periods (int): Number of periods
            starting_date (str): Simulation start date
            interval (str): "d" = daily, "w" = weekly, "m" = monthly

        Returns:
            pd.DataFrame: DataFrame with simulated stock prices
        """
        # Generate date index
        dates = self.__create_dates(interval=interval, num_periods=num_periods, starting_date=starting_date)

        # Generate stock names
        name_list = self.__generate_unique_names(num_stocks=num_stocks)

        stock_df = pandas.DataFrame(index=dates)
        step_map = {"d": 1/252, "w": 1/52, "m": 1/12}
        step = step_map[interval]

        # Common market shocks
        market_shocks = numpy.random.randn(num_periods)
        jump_days = numpy.random.choice(a=num_periods, size=max(1, num_periods // 50), replace=False)
        market_shocks[jump_days] += numpy.random.normal(0, 0.05, size=len(jump_days))

        for name in name_list:
            start_day = numpy.random.randint(low=0, high=num_periods // 2)
            end_day = numpy.random.randint(low=start_day + 4, high=num_periods)
            days_active = end_day - start_day

            prices = numpy.zeros(shape=days_active)
            prices[0] = numpy.random.randint(low=10, high=200)

            group_choice = numpy.random.rand()
            if group_choice < 0.15:
                mu = numpy.random.normal(loc=0.18, scale=0.05)
            elif group_choice < 0.75:
                mu = numpy.random.normal(loc=0.04, scale=0.04)
            else:
                mu = numpy.random.normal(loc=-0.05, scale=0.05)

            sigma = numpy.random.uniform(low=0.10, high=0.30)

            for t in range(1, days_active):
                Z = 0.65 * market_shocks[start_day + t] + 0.35 * numpy.random.randn()
                prices[t] = prices[t - 1] * numpy.exp((mu - 0.5 * sigma ** 2) * step + sigma * numpy.sqrt(step) * Z)

            vector = numpy.full(num_periods, numpy.nan)
            vector[start_day:end_day] = prices
            stock_df[name] = vector

        return stock_df


simulator = StockPriceSimulator()
print(simulator.create_stock_prices(num_stocks=800, num_periods=50, interval="d"))
print(simulator.create_stock_prices(num_stocks=800, num_periods=50, interval="m"))
print(simulator.create_stock_prices(num_stocks=800, num_periods=50, interval="w"))


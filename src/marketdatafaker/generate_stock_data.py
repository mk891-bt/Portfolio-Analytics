
import pandas
import numpy
import random


class StockPriceSimulator:

    def __init__(self):
        """
        Initialize the stock data simulator.
        """

    def _generate_unique_names(self, num_stocks:int) -> list[str]:
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

    def _create_dates(self, interval: str, 
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
    
    def _assign_survivor_stocks(self,
                                name_list: list[str],
                                survivor_pct: float = 0,
                                use_random_interval: bool = True,
                                survivor_interval: tuple[float, float] = (0.5, 0.8)
                                ) -> list[str]:
        """
        Selects a subset of stocks to remain active for the full simulation duration.

        Logic:
        Calculates a survival percentage—either via a fixed value or a random 
        uniform range—and uses random sampling to select which stock names 
        will bypass delisting logic.

        Args:
            name_list: All unique stock identifiers.
            survivor_pct: Fraction (0-1) to keep if use_random_interval is False.
            use_random_interval: Toggles between fixed pct or random range.
            survivor_interval: Low/high bounds for random survival percentage.

        Returns:
            List of stock names designated as survivors.

        Edge Case Handling:
        # TODO: Validate interval bounds [0, 1], ensure low <= high, 
        # and clamp survivor_pct to prevent sampling errors.
        """

        #TODO fix for potential wrong arguments

        if use_random_interval is True:
            pct: float = numpy.random.uniform(low=survivor_interval[0], high=survivor_interval[1])
        else:
            pct: float = survivor_pct
        
        num_survivors: int = int(pct * len(name_list))

        survivor_names: list[str] = random.sample(population=name_list,
                                                  k=num_survivors)
        return survivor_names



    def create_stock_prices(self, num_stocks: int, 
                            num_periods: int,
                            starting_date: str = "2010-01-01", 
                            interval: str = "d") -> pandas.DataFrame:
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
        dates = self._create_dates(interval=interval, num_periods=num_periods, starting_date=starting_date)

        # Generate stock names
        name_list = self._generate_unique_names(num_stocks=num_stocks)
        # Assigns the survivor stocks which persist throughout the dataset
        #TODO add needed arguments to the function arguments to make this usable
        survivor_names = self._assign_survivor_stocks(name_list=name_list,
                                                      survivor_pct=0.5, 
                                                      use_random_interval=False)

        stock_df = pandas.DataFrame(index=dates)
        step_map = {"d": 1/252, "w": 1/52, "m": 1/12}
        step = step_map[interval]

        # Common market shocks
        market_shocks = numpy.random.randn(num_periods)
        jump_days = numpy.random.choice(a=num_periods, size=max(1, num_periods // 50), replace=False)
        market_shocks[jump_days] += numpy.random.normal(0, 0.05, size=len(jump_days))

        for name in name_list:

            if name in survivor_names:
                start_day: int = 0
                end_day: int = num_periods
            else:
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


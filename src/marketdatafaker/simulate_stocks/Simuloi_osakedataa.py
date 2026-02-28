
import faker
import pandas
import numpy

import faker
import pandas
import numpy


class StockDataSimulator:

    def __init__(self, num_stocks: int, num_dates: int,
                 starting_date: str = "2010-01-01"):
        """
        Initialize the stock data simulator.
        """
        if num_stocks <= 0:
            raise ValueError("Number of stocks can't be 0!")

        # Temporary logic for development
        # TODO: Improve this logic later
        if num_dates <= 10:
            raise ValueError("There must be a minimum of 10 days")

        self.faker: faker.Faker = faker.Faker()
        self.num_stocks: int = num_stocks
        self.num_days: int = num_dates
        self.starting_date: str = starting_date
        self.stock_names: list = self.generate_unique_names()

    def generate_unique_names(self) -> list[str]:
        """
        Generate a list of unique company names.

        The method creates a list whose length is exactly self.num_stocks.
        All names are unique and generated using the Faker library.
        Duplicates are removed using a set, ensuring the final list
        contains only distinct company names.

        Returns:
            list[str]: A list of unique company names of length num_stocks.
        """
        unique_names: set[str] = set()

        # Generate names until the set reaches the required size
        while len(unique_names) < self.num_stocks:
            unique_names.add(self.faker.company())

        return list(unique_names)

    def create_stock_data(self) -> pandas.DataFrame:
        """
        Create simulated stock price data.
        """
        dates: pandas.DatetimeIndex = pandas.date_range(
            start=self.starting_date,
            periods=self.num_days,
            freq="B"
        )

        stock_df: pandas.DataFrame = pandas.DataFrame(index=dates)
        step: float = 1 / 252

        # Common market factor to induce correlation
        market_shocks: numpy.ndarray = numpy.random.randn(self.num_days)

        for name in self.stock_names:
            # Randomly choose start and end dates
            start_day: int = numpy.random.randint(low=0, high=self.num_days // 2)
            end_day: int = numpy.random.randint(low=(start_day + 4), high=self.num_days)
            days_active: int = end_day - start_day

            prices = numpy.zeros(shape=days_active)
            prices[0] = numpy.random.randint(low=1, high=1000)

            # Random drift based on stock "group"
            group_choice: float = numpy.random.rand()

            # Super-winners: stocks that generate most of the returns
            if group_choice < 0.15:
                mu: float = numpy.random.normal(loc=0.18, scale=0.05)
            elif group_choice < 0.75:
                mu: float = numpy.random.normal(loc=0.04, scale=0.04)
            else:
                mu: float = numpy.random.normal(loc=-0.05, scale=0.05)

            # Annual volatility
            sigma: float = numpy.random.uniform(low=0.10, high=0.30)

            for t in range(1, days_active):
                Z = 0.65 * market_shocks[start_day + t] + 0.35 * numpy.random.randn()
                prices[t] = prices[t - 1] * numpy.exp(
                    (mu - 0.5 * sigma ** 2) * step + sigma * numpy.sqrt(step) * Z
                )

            vector = numpy.full(self.num_days, numpy.nan)
            vector[start_day:end_day] = prices

            stock_df[name] = vector

        return stock_df


simulator = StockDataSimulator(num_stocks=600, num_dates=25)
print(simulator.create_stock_data())



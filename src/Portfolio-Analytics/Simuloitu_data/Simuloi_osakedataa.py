
import faker

class Simuloi_Osakedataa:

    def __init__(self, osakkeiden_määrä: int, päivien_määrä: int):
        """
        
        """
        self.faker = faker.Faker()
        self.osakkeiden_määrä: int = osakkeiden_määrä
        self.päivien_määrä: int = päivien_määrä
        self.osakkeet_nimet: list = self.nimilista_uniikit(osakkeiden_määrä=self.osakkeiden_määrä)

    def nimilista_uniikit(self, osakkeiden_määrä: int) -> list:
        """
        """
        # Ratko tämä ongelma myöhemmin, miksi docstring ei näy
        return [self.faker.unique.company() for _ in range(osakkeiden_määrä)]



simulaattori = Simuloi_Osakedataa(osakkeiden_määrä=600, päivien_määrä=300)
print(simulaattori.osakkeet_nimet)

import faker

class Simuloi_Osakedataa:

    def __init__(self, osakkeiden_määrä: int, päivien_määrä: int):
        """
        
        """
        if osakkeiden_määrä <= 0:
            raise ValueError("Osakkeiden määrä 0!")
        if päivien_määrä <= 0:
            raise ValueError("Päivien määrän on oltava > 0")
         
        self.faker = faker.Faker()
        self.osakkeiden_määrä: int = osakkeiden_määrä
        self.päivien_määrä: int = päivien_määrä
        self.osakkeet_nimet: list = self.nimilista_uniikit()

    def nimilista_uniikit(self) -> list[str]:
        """
        Generoi listan uniikkeja yritysnimiä.

        Metodi luo listan, jonka pituus on täsmälleen self.osakkeiden_määrä.
        Kaikki nimet ovat uniikkeja, ja ne generoidaan Faker-kirjaston avulla.
        Duplikaatit suodatetaan setin avulla, joten lopullinen lista
        sisältää vain erilaisia yritysnimiä.

        Returns:
            list[str]: Lista uniikkeja yritysnimiä, jonka pituus vastaa osakkeiden_määrä.
        """
        # Käytetään settiä, jotta kaikki nimet ovat uniikkeja
        osakkeiden_nimet: set[str] = set()

        # Generoidaan nimiä kunnes setin koko vastaa tarvittavaa määrää
        while len(osakkeiden_nimet) < self.osakkeiden_määrä:
            osakkeiden_nimet.add(self.faker.company())

        return list(osakkeiden_nimet)



simulaattori = Simuloi_Osakedataa(osakkeiden_määrä=600, päivien_määrä=300)
print(simulaattori.osakkeet_nimet)
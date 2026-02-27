
import faker
import pandas
import numpy

class Simuloi_Osakedataa:

    def __init__(self, osakkeiden_määrä: int, päivien_määrä: int, 
                 aloitus_päivämäärä: str="2010-01-01"):
        """
        
        """
        if osakkeiden_määrä <= 0:
            raise ValueError("Osakkeiden määrä 0!")
        if päivien_määrä <= 10:
            raise ValueError("Päivien määrän on oltava > 10")
         
        self.faker = faker.Faker()
        self.osakkeiden_määrä: int = osakkeiden_määrä
        self.päivien_määrä: int = päivien_määrä
        self.aloitus_päivämäärä: str = aloitus_päivämäärä
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

    def luo_osakedata(self) -> pandas.DataFrame:
        """
        
        """
        päivämäärät: pandas.DatetimeIndex = pandas.date_range(start=self.aloitus_päivämäärä,
                                                              periods=self.päivien_määrä,
                                                              freq="B")
        osakedata_df: pandas.DataFrame = pandas.DataFrame(index=päivämäärät)
        askel: float = 1 / 252

        # Yhteinen markkinatekijä, luo korrelaatiota
        markkina_shokit: numpy.ndarray = numpy.random.randn(self.päivien_määrä)

        for nimi in self.osakkeet_nimet:
            # Arvotaan aloitus ja loeptusajat
            aloitus_päivä: int = numpy.random.randint(low=0, high=self.päivien_määrä // 2)
            lopetus_päivä: int = numpy.random.randint(low=(aloitus_päivä + 4), high=self.päivien_määrä)
            päiviä: int = lopetus_päivä - aloitus_päivä

            kurssit = numpy.zeros(shape=päiviä)
            kurssit[0] = numpy.random.randint(low=1, high=1000)

            # Arpoo driftin, ottaa huomioon
            ryhmä_valinta: float = numpy.random.rand()
            # Supervoittajat, osakkeet jotka tuottavat suurimman osan tuotoista
            if ryhmä_valinta < 0.15:
                mu: float = numpy.random.normal(loc=0.18,
                                            scale=0.05)
            elif ryhmä_valinta < 0.75:
                mu: float = numpy.random.normal(loc=0.04,
                                            scale=0.04)
            else:
                mu: float = numpy.random.normal(loc=-0.05,
                                            scale=0.05)
            
            # Volatiliteetti vuositasolla
            sigma: float = numpy.random.uniform(low=0.10, high=0.30)


            for t in range(1, päiviä):
                Z = 0.65 * markkina_shokit[aloitus_päivä + t] + 0.35 * numpy.random.randn()
                kurssit[t] = kurssit[t-1] * numpy.exp(
                    (mu - 0.5 * sigma ** 2) * askel + sigma * numpy.sqrt(askel) * Z
                )
            
            vektori = numpy.full(self.päivien_määrä, numpy.nan)
            vektori[aloitus_päivä:lopetus_päivä] = kurssit

            osakedata_df[nimi] = vektori
        
        return osakedata_df

simulaattori = Simuloi_Osakedataa(osakkeiden_määrä=600, päivien_määrä=20)
print(simulaattori.luo_osakedata())
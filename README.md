# KMO Map
Deze tool dient om data van Kruistpuntbank Ondernemingen (KBO) in kaart te brengen en om makkelijk inzicht te krijgen op een aantal bedrijven.

## Voorbereiding
Het project bestand momenteel KBO data voor postcodes 2060 en 2000. Als je de volledige data wil voor heel België kan je die [hier](https://economie.fgov.be/nl/themas/ondernemingen/kruispuntbank-van/diensten-voor-iedereen/hergebruik-van-publieke/kruispuntbank-van-0) downloaden.
**Als je een postcode wil toevoegen die niet in het project zit volg dan deze stappen**
1. Plaats de folder met csv-bestanden in de root van het project.
2. Voor het onderstaand commando uit voor je gekozen postcode
   ```
    python main.py <postcode>
   ```
3. Vervolgens moeten de adressen uit de KBO data worden omgezet naar hun respectievelijke coördinaten. Dit kan enige tijd duren.
  ```
    python geocody.py <postcode>
  ```

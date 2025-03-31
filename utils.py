from datetime import time

from customTypes import OpeningHours, Recommendation


def convertOpeningHoursStringToTime(openingHoursString: str) -> OpeningHours:
    #string is in format "10:00 - 22:00", so remove the spaces and the "-"
    openingHours = openingHoursString.split(" - ")
    openingHours = [time.fromisoformat(openingHour) for openingHour in openingHours]
    return OpeningHours(open=openingHours[0], close=openingHours[1])

def convertRecommendationToModel(recommendation: dict) -> Recommendation:
    return Recommendation(
        category=recommendation["Categorie"],
        name=recommendation["Naam"],
        priceClass=recommendation["Prijsklasse"],
        kitchen=recommendation["Keuken"],
        concept=recommendation["Type Concept"],
        atmosphere=recommendation["Sfeer"],
        style=recommendation["Stijl"],
        location=recommendation["Adres"],
        openingHours=convertOpeningHoursStringToTime(recommendation["Openingstijden"]),
        rating=float(recommendation["Beoordeling"])
    )

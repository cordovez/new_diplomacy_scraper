import json


def _get_dublin_missions():
    missions = []

    with open("data/foreign_missions_in_dublin.csv", "r") as file:
        for line in file:
            if country := line.strip().lower():
                missions.append(country)

    return missions


def _get_london_missions():
    missions = []

    with open("data/foreign_missions_in_london.csv", "r") as file:
        for line in file:
            if country := line.strip().lower():
                missions.append(country)

    return missions


def _get_accredited_countries():
    countries = []
    exceptions = ['european commission', 'european parliament',
                  'international organization for migration', 'japan (contd',
                  'mexico (contd', 'myanmar (cont)',
                  'united nations high commissioner for refugees']

    with open("data/missions_accredited_to_ireland.csv", "r") as file:
        for line in file:
            if country := line.strip().lower():
                countries.append(country)

    only_countries = [country for country in countries if country not in exceptions]
    return only_countries


def get_countries_scraped_as_list() -> list[str]:
    with open("data/scrape_results.json", "r") as file:
        json_data = json.load(file)

    objects = []
    terms_to_avoid = ["Palestinian", "Partnership", "Permanent Representation",
                      "Permanent Mission"]

    for item in json_data:
        for term in terms_to_avoid:
            if term not in item["accordion_title"] and item not in objects:
                objects.append(item)
    return [item["accordion_title"] for item in objects]


def correct_accredited_countries() -> list[str]:
    corrected_countries = []
    for country in accredited_countries:
        match country.lower():
            case 'andorra':
                corrected_countries.append("andorra, principality of")
            case 'antigua & barbuda':
                corrected_countries.append("antigua and barbuda")
            case 'kingdom of bahrain':
                corrected_countries.append("bahrain")
            case 'bosnia and herzegovina':
                corrected_countries.append("bosnia-herzegovina")
            case 'côte d’ivoire':
                corrected_countries.append("côte d'ivoire")
            case 'democratic republic of congo':
                corrected_countries.append("congo, democratic republic of")
            case 'gabonese republic':
                corrected_countries.append("gabon")
            case 'the gambia':
                corrected_countries.append("gambia, republic of the")
            case 'republic of guatemala':
                corrected_countries.append("guatemala")
            case 'republic of guinea':
                corrected_countries.append("guinea")
            case 'korea (democratic people’s republic of)':
                corrected_countries.append("korea, democratic republic of (north korea)")
            case 'korea (republic of)':
                corrected_countries.append("korea, republic of (south korea)")
            case 'lao':
                corrected_countries.append("laos")
            case 'republic of north macedonia':
                corrected_countries.append("north macedonia, republic of")
            case 'moldova':
                corrected_countries.append("moldova, republic of")
            case 'myanmar':
                corrected_countries.append("myanmar/burma")
            case 'palestinian mission':
                corrected_countries.append("palestinian authority")
            case 'russia':
                corrected_countries.append("russian federation")
            case 'saint vincent and the grenadines':
                corrected_countries.append("saint vincent and grenadines")
            case 'united kingdom':
                corrected_countries.append("great britain")
            case _:
                corrected_countries.append(country)

    return corrected_countries

def correct_dublin_missions() -> list[str]:
    dublin_missions = []
    for mission in missions_in_dublin:
        match mission.lower():
            case 'czechia':
                dublin_missions.append("czech republic")
            case 'moldova':
                dublin_missions.append("moldova, republic of")
            case 'russia':
                dublin_missions.append("russian federation")
            case 'south korea':
                dublin_missions.append("korea, republic of (south korea)")
            case 'turkey':
                dublin_missions.append("türkiye")
            case 'united kingdom':
                dublin_missions.append("great britain")
            case 'united states':
                dublin_missions.append("united states of america")
            case 'slovakia':
                dublin_missions.append("slovak republic")
            case _:
                dublin_missions.append(mission)
    return dublin_missions

def correct_london_missions() -> list[str]:
    london_missions = []
    for mission in missions_in_london:
        match mission.lower():
            case 'bosnia and herzegovina':
                london_missions.append("bosnia-herzegovina")
            case 'brunei':
                london_missions.append("brunei darussalam")
            case 'congo-kinshasa':
                london_missions.append("Congo, Democratic Republic of")
            case 'gambia':
                london_missions.append("gambia, republic of the")
            case 'ivory coast':
                london_missions.append("côte d'ivoire")
            case 'myanmar':
                london_missions.append("myanmar/burma")
            case 'north korea':
                london_missions.append("korea, democratic republic of (north korea)")
            case 'north macedonia':
                london_missions.append("north macedonia, republic of")
            case 'saint vincent and the grenadines':
                london_missions.append('saint vincent and grenadines')
            case _:
                london_missions.append(mission)
    return london_missions


def _get_cc():
    with open("data/country_codes_iso.json", "r") as file:
        return json.load(file)

def _get_countries_from_country_codes():
    with open("data/country_codes_iso.json", "r") as file:
        data = json.load(file)
    cc_countries = [item["name"] for item in data]
    scraped_countries = get_countries_scraped_as_list()

    unmatched = []
    for country in scraped_countries:
        for cc in cc_countries:
            if country.lower() in cc.lower():
                unmatched.append(cc)
    return unmatched

def correct_cc_countries():
    cc_countries = _get_cc()
    
    for country in cc_countries:
        match country["name"].lower():
            case 'bolivia, plurinational state of':
                country["name"] = "bolivia"
            case 'taiwan, province of china':
                country["name"] = "taiwan"
            case 'congo, democratic republic of the':
                country["name"] = "congo, democratic republic of"
            case 'south georgia and the south sandwich islands':
                country["name"] = "s. georgia and the s. sandwich islands"
            case 'united kingdom of great britain and northern ireland':
                country["name"] = "great britain"
            case 'guinea-bissau':
                country["name"] = "guinea bissau"
            case 'iran, islamic republic of':
                country["name"] = "iran"
            case 'netherlands, kingdom of the':
                country["name"] = "netherlands"
            case 'saint helena, ascension and tristan da cunha':
                country["name"] = "saint helena"
            case 'american samoa':
                country["name"] = "samoa"
            case 'sint maarten (dutch part)':
                country["name"] = "sint maarten"
            case 'syrian arab republic':
                country["name"] = "syria"
            case 'tanzania, united republic of':
                country["name"] = "tanzania"
            case 'venezuela, bolivarian republic of':
                country["name"] = "venezuela"
            case _:
                country["name"] = country["name"]
    return cc_countries


country_codes_countries = _get_countries_from_country_codes()
corrected_cc_countries = correct_cc_countries()
missions_in_dublin = _get_dublin_missions()
missions_in_london = _get_london_missions()
corrected_dublin_missions = correct_dublin_missions()
corrected_london_missions = correct_london_missions()
accredited_countries = _get_accredited_countries()
scraped_countries = get_countries_scraped_as_list()
correct_names = correct_accredited_countries()



def difference_from_two_lists() -> list[str]:
    lower_a = [x.lower() for x in corrected_cc_countries]
    # lower_a = [x.lower() for x in corrected_london_missions]
    # lower_a = [x.lower() for x in corrected_dublin_missions]
    # lower_a = [x.lower() for x in accredited_countries]
    lower_b = [x.lower() for x in scraped_countries]
    # return lower_b
    return [element for element in lower_a if element not in lower_b]


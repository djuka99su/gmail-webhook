


from datetime import date


text ="""logo
Hei Nemanja,
Tusen takk for hjelpen. Vi har mottatt ditt svar, og vi bekrefter at du er registrert på følgende vakter. Ta kontakt med oss hvis du har noen spørsmål.
100102 Helsefagarbeider
Ullern Helsehus, Avd 4
Ullernchausseen 111, 0284 Oslo, Norge
Fastvakt- kan være litt utagerende og si ting, så må tåle å stå i det. Har kastet vann på noen, men kan også være veldig rolig
From 4 des.
Schedule
w 49	4 des., ons.	07:30 – 15:00
5 des., tor.	07:30 – 15:00"""

def get_schedules(text: str) -> list[str]:
    """
    Extract date from schedule information in text
    
    Args:
        text (str): Input text containing schedule information
        
    Returns:
        date: Date object extracted from schedule text
    """
    # Find the position of 'Schedule' 
    schedule_index = text.find('Schedule')
    
    # If 'Schedule' is not found, return None
    if schedule_index == -1:
        return []
        
    # Get schedule text
    schedules = " ".join(text[schedule_index + len('Schedule'):].strip().replace("\t", " ").split(" ")[2:]).split("\n")
    # print(schedule_text.split("\n"))
    
    month_map = {
        "jan.": 1, "feb.": 2, "mar.": 3, "apr.": 4,
        "mai.": 5, "jun.": 6, "jul.": 7, "aug.": 8,
        "sep.": 9, "okt.": 10, "nov.": 11, "des.": 12
    }
    
    data = []
    for schedule in schedules:
        schedule_parts = schedule.split(" ")
        current_year = date.today().year
        day = schedule_parts[0]
        month = month_map[schedule_parts[1].replace(",", "")]
        start_time = schedule_parts[3]
        end_time = schedule_parts[5]
        data.append(f"{day}.{month}.{current_year} {start_time} - {end_time}")
    
    return data


print(get_schedules(text))

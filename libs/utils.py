from datetime import date


def get_schedules(text: str) -> list[dict]:
    """
    Extract date from schedule information in text

    Args:
        text (str): Input text containing schedule information

    Returns:
        list[dict]: List of dictionaries containing schedule information
    """
    # Find the position of 'Schedule'
    schedule_index = text.find("Schedule")

    # If 'Schedule' is not found, return None
    if schedule_index == -1:
        return []

    # Get schedule text
    schedules = " ".join(
        text[schedule_index + len("Schedule") :]
        .strip()
        .replace("\t", " ")
        .split(" ")[2:]
    ).split("\n")

    month_map = {
        "jan.": 1,
        "feb.": 2,
        "mar.": 3,
        "apr.": 4,
        "mai.": 5,
        "jun.": 6,
        "jul.": 7,
        "aug.": 8,
        "sep.": 9,
        "okt.": 10,
        "nov.": 11,
        "des.": 12,
    }

    data = []
    for schedule in schedules:
        schedule_parts = schedule.split(" ")
        current_year = date.today().year
        day = schedule_parts[0]
        month = month_map[schedule_parts[1].replace(",", "")]
        start_time = schedule_parts[3].replace("\r", "")
        end_time = schedule_parts[5].replace("\r", "")
        # data.append(f"{day}.{month}.{current_year} {start_time} - {end_time}")
        data.append(
            {
                "day": day,
                "month": str(month),
                "year": str(current_year),
                "start_time": start_time.replace(" – ", ":"),
                "end_time": end_time.replace(" – ", ":"),
            }
        )
    return data

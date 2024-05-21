from models import JobSeeker


def get_job_seeker_report(data: dict | JobSeeker, include_id: bool = False) -> str:
    if isinstance(data, JobSeeker):
        data, _data = {}, data
        for key in [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone_number",
            "experience",
            "skills",
        ]:
            data[key] = getattr(_data, key, "не вказано")
    experience = (
        str(data.get("experience", 0)) + " років"
        if data.get("experience", 0) > 0
        else "Без досвіду"
    )
    skills = ", ".join([str(s) for s in data.get("skills", [])]) or "не вказано"
    return (
        (f"#id{data.get('id', 'null')}\n" if include_id else "")
        + f"Ім'я: {data.get('first_name', 'не вказано')}\n"
        f"Прізвище: {data.get('last_name', 'не вказано')}\n"
        f"По-батькові: {data.get('middle_name', 'не вказано')}\n"
        f"Електронна адреса: {data.get('email', 'не вказано')}\n"
        f"Номер телефону: {data.get('phone_number', 'не вказано')}\n"
        f"Досвід роботи: {experience}\n"
        f"Навички: {skills}\n"
        # f"Освіта: {', '.join(data.get('educations', 'не вказано'))}\n"
    )

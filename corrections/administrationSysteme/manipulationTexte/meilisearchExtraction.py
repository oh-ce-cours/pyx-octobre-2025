import datetime
import re

ISO_DATE_REGEXP = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d*)?(-\d{2}:\d{2}|Z)?"


def match_iso_date(line):
    return re.compile(ISO_DATE_REGEXP).search(line)


def parse_http_port(line: str) -> str:
    return line.split("http://")[1].split(":")[1][:-1]


def parse_version(line):
    return line.split('"')[1]


def parse_date(line) -> datetime.date:
    date_str = re.search(ISO_DATE_REGEXP, line, re.IGNORECASE).group(0)
    return datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))


def output(version: str, port: str, date: datetime.datetime):
    print(f"La version utilisée est {version}")
    print("\t", end="")
    print(f"Le programme a été lancé un {date.strftime('%A')}, sur le port {port}")


def main():
    log_path = "../../../medias/administrationSysteme/analyseTexte/meilisearch.log"
    with open(log_path, encoding="utf8") as f:
        logs = f.readlines()

    version, port, date = "", "", None
    for line in logs:
        if line.startswith("Package version"):
            version = parse_version(line)
        if "Server listening on" in line:
            port = parse_http_port(line)
        if line.startswith("[") and line.startswith("[") and not date:
            date = parse_date(line)

    output(version, port, date)


if __name__ == "__main__":
    main()

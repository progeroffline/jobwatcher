from pathlib import Path

output_dir = Path(__file__).resolve().parent
output_dir.mkdir(exist_ok=True)
template_path = output_dir.joinpath("test.tpl")

with template_path.open("r") as template_file:
    test_template = template_file.read()

services = [
    {"service_package": "artstation", "service_class": "ArtStationParser"},
    {"service_package": "belmeta", "service_class": "BelmetaParser"},
    {"service_package": "jobsua", "service_class": "JobsUAParser"},
    {"service_package": "olx", "service_class": "OlxParser"},
    {"service_package": "rabotaua", "service_class": "RabotaUAParser"},
    {"service_package": "workua", "service_class": "WorkUAParser"},
]

for service in services:
    filename = f"services_{service['service_package']}.py"
    file_path = output_dir / filename

    file_content = test_template.format(
        service_package=service["service_package"],
        service_class=service["service_class"],
    )

    with file_path.open("w") as f:
        f.write(file_content)

    print(f"Generated file: {file_path}")

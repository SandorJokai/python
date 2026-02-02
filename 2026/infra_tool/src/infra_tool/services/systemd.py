import subprocess
import yaml
from importlib.resources import files

config_file = files("infra_tool.config").joinpath("data.yaml")


def read_from_yaml():
    with open(config_file, 'r') as file:
        parsed_data = yaml.safe_load(file)

    return parsed_data


def create_list(output):
    services = output.get("services")
    service_list = []

    for service in services:
        try:
            subprocess.run(
                    ["systemctl", "status", service],
                    text=True,
                    capture_output=True,
                    check=True
                )
        except subprocess.CalledProcessError as e:
            service_list.append(service)
        
    return service_list


def restart_svc(svc):
    print(f"{svc} service was stopped, restarting it now...")

    try:
        subprocess.run(
                ["sudo", "systemctl", "restart", svc],
                text=True,
                capture_output=True,
                check=True
            )
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")


output = read_from_yaml()
stopped_svc = create_list(output)

def service_check():
    for svc in stopped_svc:
        restart_svc(svc)

    if not stopped_svc:
        print("No services detected in a stopped state.")

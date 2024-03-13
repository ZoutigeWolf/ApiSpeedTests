import os
import requests
import socket
from statistics import stdev, mean
from subprocess import check_output, Popen, PIPE
from time import sleep

CONFIG = {
    "js": "node main.js",
    "python": "python3 main.py",
    "rust": "cargo run",
    "cs": "dotnet run",
    "java": "./gradlew run",
}

RUNS = 1000

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def measure(name: str) -> None:
    data = []
    
    for _ in range(RUNS):
        res = requests.get("http://localhost:8080")
        data.append(res.elapsed.total_seconds() * 1000)
        
    print(f"{round(mean(data), 3)} ± {round(stdev(data), 3)}")


def main() -> None:
    for dir, cmd in CONFIG.items():
        os.chdir(dir)
        
        # start server
        process = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        
        print(f"Starting: {dir}")
        
        # wait until server has started
        while not is_port_in_use(8080):
            sleep(0.1)
        
        print(f"Measuring...")
        measure(dir)
        
        process.terminate()
        os.chdir("..")
        
        # wait until server is stopped
        while is_port_in_use(8080):
            sleep(0.1)


if __name__ == "__main__":
    main()
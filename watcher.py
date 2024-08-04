import subprocess

from watchfiles import watch

# Path to the file for which we want to watch
WATCHED_FILE = "plugins/.plugins"


def rebuild_and_restart():
    print("Change detected. Rebuilding and restarting Docker Compose services...")
    try:
        subprocess.run(["docker", "compose", "build"], check=True)
        subprocess.run(["docker", "compose", "down"], check=True)
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        print("Docker Compose services restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


print(f"Watching {WATCHED_FILE} for changes...")

try:
    # Watch the file for changes
    for changes in watch(WATCHED_FILE):
        # Call the rebuild and restart function when a change is detected
        rebuild_and_restart()
except KeyboardInterrupt:
    print("Stopping watcher...")
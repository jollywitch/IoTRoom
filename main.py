import subprocess
import os
import signal
import time

def runMobius(scriptPath, workingDir):
    try:
        process = subprocess.Popen(
            ["node", scriptPath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=workingDir
        )
        
        print(f"Mobius server started. PID: {process.pid}")
        
        while True:
            output = process.stdout.readline()
            if output:
                print(f"[SERVER LOG]: {output.strip()}")
            if process.poll() is not None:
                print("Mobius server terminated.")
                break
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Terminating Mobius server...")
        process.send_signal(signal.SIGINT)
        process.wait()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if process and process.poll() is None:
            process.terminate()
            print("Force shutdown Mobius server.")

if __name__ == "__main__":
    workingDir = "./Mobius"
    scriptPath = "./Mobius/mobius.js"

    if not os.path.exists(workingDir):
        print("Can't locate file: {workingDir}")
    elif not os.path.exists(scriptPath):
        print(f"Can't locate file: {scriptPath}")
    else:
        runMobius(scriptPath, workingDir)

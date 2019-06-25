from subprocess import check_output
import time
from sys import stdout

if __name__ == "__main__":
    counter = 0
    loop_end = False
    while True:
        cmd = "ps -ef | grep \"wget -O\" | grep -v grep"
        result = check_output(cmd, shell=True).decode("utf-8")
        if "xml.bz2" in result:
            loop_end = False
            stdout.write("downloading...[{}]\r".format(counter))
            stdout.flush()
            time.sleep(1)
            counter += 1
        else:
            if loop_end:
                break
            else:
                time.sleep(100)
                loop_end = True
                continue
    time.sleep(60*60*4)

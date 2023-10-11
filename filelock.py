import os

class FileLock:
    def __init__(self, filename):
        self.filename = filename
        self.fd = None
        self.pid = os.getpid()

    def acquire(self):
        try:
            self.fd = os.open(self.filename, os.O_CREAT|os.O_EXCL|os.O_RDWR)
            # Only needed to let readers know who's locked the file
            os.write(self.fd, f"{self.pid}".encode('utf-8'))
            return True    
        except OSError:
            self.fd = None
            return False

    def release(self):
        if not self.fd:
            return False
        try:
            os.close(self.fd)
            os.remove(self.filename)
            return True
        except OSError:
            return False

    def __del__(self):
        self.release()

def main():
    lock = FileLock("lock.file")
    print(lock.acquire())
    # while 1:
    #     if lock.acquire():
    #         raw_input("acquired lock. Press ENTER to release:")
    #         lock.release()
    #         raw_input("released lock. Press ENTER to retry:")
    #     else:
    #         raw_input("Unable to acquire lock. Press ENTER to retry:")

if __name__ == "__main__":
    main()
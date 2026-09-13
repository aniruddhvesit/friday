import sys
import os

if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="127.0.0.1", port=8765, log_level="warning")

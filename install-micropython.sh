#!/usr/bin/env bash

cd /tmp
#git clone https://github.com/micropython/micropython.git
cd micropython/mpy-cross
make

cd ../ports/unix
echo "
freeze(
    \"\$(MPY_DIR)/extmod\",
    (
        \"uasyncio/__init__.py\",
        \"uasyncio/core.py\",
        \"uasyncio/event.py\",
        \"uasyncio/funcs.py\",
        \"uasyncio/lock.py\",
        \"uasyncio/stream.py\",
        \"uasyncio/task.py\",
    ),
    opt=3,
)
" >> variants/manifest.py
make submodules
make
sudo cp micropython /usr/local/bin

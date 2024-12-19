#!/bin/bash

BASE_DIR="$(dirname "$0")"

cd "$BASE_DIR/Mobius" || { echo "Can't find Mobius directory."; exit 1; }
echo "Running Mobius server..."
npm install
node mobius.js > mobius.log 2>&1 &
MOBIUS_PID=$!
echo "Mobius server started with (PID: $MOBIUS_PID)"
sleep 10

cd "../"

cd "$BASE_DIR/nCube" || { echo "Can't find nCube directory."; exit 1; }
echo "Running nCube server..."
npm install
node thyme.js > thyme.log 2>&1 &
NCUBE_PID=$!
echo "nCube server started with (PID: $NCUBE_PID)"
sleep 10

cd "../"

cd "$BASE_DIR/pythonServer" || { echo "Can't find pythonServer directory."; exit 1; }
echo "Running pythonServer..."
python server.py > pythonServer.log 2>&1 &
PSERVER_PID=$!
echo "pythonServer started with (PID: $PSERVER_PID)"

echo "All servers are successfully running."

wait $MOBIUS_PID $NCUBE_PID $PSERVER_PID

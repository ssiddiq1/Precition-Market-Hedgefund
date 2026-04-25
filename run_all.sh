#!/usr/bin/env bash
# run_all.sh — starts all quant-os agents and the dashboard

ROOT="$(cd "$(dirname "$0")" && pwd)"
LOGS="$ROOT/logs"
mkdir -p "$LOGS"

echo "[quant-os] Starting Kalshi collector..."
python3 "$ROOT/agents/collectors/collector.py" >> "$LOGS/collector.log" 2>&1 &
echo "  PID $! → logs/collector.log"

echo "[quant-os] Starting Polymarket collector..."
python3 "$ROOT/agents/collectors/polymarket_collector.py" >> "$LOGS/polymarket.log" 2>&1 &
echo "  PID $! → logs/polymarket.log"

echo "[quant-os] Starting analyst (runs every 6h)..."
python3 "$ROOT/agents/research/analyst.py" >> "$LOGS/analyst.log" 2>&1 &
echo "  PID $! → logs/analyst.log"

echo "[quant-os] Starting researcher (runs every 1h)..."
python3 "$ROOT/agents/research/researcher.py" >> "$LOGS/researcher.log" 2>&1 &
echo "  PID $! → logs/researcher.log"

echo "[quant-os] Starting dashboard..."
python3 "$ROOT/dashboard/app.py" >> "$LOGS/dashboard.log" 2>&1 &
echo "  PID $! → logs/dashboard.log"

echo ""
echo "[quant-os] All agents running. Dashboard → http://localhost:5050"
echo "           Ctrl+C kills this script but leaves agents running."
echo "           To stop all: kill \$(lsof -ti:5050) && pkill -f 'quant-os'"
echo ""

wait

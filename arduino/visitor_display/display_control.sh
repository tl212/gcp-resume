#!/bin/bash

# visitor display control 
# controls the python script that feeds data to arduino LCD

PID_FILE="visitor_feeder.pid"
LOG_FILE="visitor_feeder.log"
SCRIPT="visitor_feeder.py"

case "$1" in
    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "✅ Visitor display already running (PID: $PID)"
                exit 0
            fi
        fi
        
        echo "🚀 Starting visitor display..."
        nohup python3 "$SCRIPT" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        sleep 2
        
        if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
            echo "✅ Visitor display started successfully (PID: $(cat $PID_FILE))"
            echo "📝 Log file: $LOG_FILE"
        else
            echo "❌ Failed to start visitor display"
            rm -f "$PID_FILE"
            exit 1
        fi
        ;;
        
    stop)
        if [ ! -f "$PID_FILE" ]; then
            echo "⚠️  Visitor display is not running (no PID file)"
            exit 0
        fi
        
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "🛑 Stopping visitor display (PID: $PID)..."
            kill "$PID"
            rm -f "$PID_FILE"
            echo "✅ Visitor display stopped"
        else
            echo "⚠️  Process not found, cleaning up PID file"
            rm -f "$PID_FILE"
        fi
        ;;
        
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "✅ Visitor display is running (PID: $PID)"
                echo "📊 Latest updates:"
                tail -5 "$LOG_FILE" 2>/dev/null
            else
                echo "❌ Visitor display is not running (stale PID file)"
            fi
        else
            echo "❌ Visitor display is not running"
        fi
        ;;
        
    log)
        if [ -f "$LOG_FILE" ]; then
            echo "📋 Showing last 20 lines of log:"
            echo "─────────────────────────────────"
            tail -20 "$LOG_FILE"
        else
            echo "❌ No log file found"
        fi
        ;;
        
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
        
    *)
        echo "Usage: $0 {start|stop|status|log|restart}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the visitor display feeder"
        echo "  stop    - Stop the visitor display feeder"
        echo "  status  - Check if it's running"
        echo "  log     - View recent log entries"
        echo "  restart - Stop and start the service"
        exit 1
        ;;
esac
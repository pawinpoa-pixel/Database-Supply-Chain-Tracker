#!/bin/sh
set -eu

: "${PORT:=10000}"
export PORT

envsubst '$PORT' \
  < /app/render/nginx.conf.template \
  > /etc/nginx/conf.d/default.conf

python /app/backend/render_start.py &
BACKEND_PID=$!

nginx -g 'daemon off;' &
NGINX_PID=$!

terminate() {
  kill -TERM "$BACKEND_PID" "$NGINX_PID" 2>/dev/null || true
}
trap terminate INT TERM

while kill -0 "$BACKEND_PID" 2>/dev/null && kill -0 "$NGINX_PID" 2>/dev/null; do
  sleep 1
done

terminate
wait "$BACKEND_PID" 2>/dev/null || true
wait "$NGINX_PID" 2>/dev/null || true
exit 1

#!/bin/bash

set -e

INTERFACE="lo"

case "$1" in
    baseline)
        sudo tc qdisc del dev "$INTERFACE" root 2>/dev/null || true
        echo "Network profile: BASELINE"
        ;;

    latency100)
        sudo tc qdisc replace dev "$INTERFACE" root netem delay 100ms
        echo "Network profile: 100ms LATENCY"
        ;;

    latency200)
        sudo tc qdisc replace dev "$INTERFACE" root netem delay 200ms
        echo "Network profile: 200ms LATENCY"
        ;;

    bandwidth1mbps)
        sudo tc qdisc replace dev "$INTERFACE" root netem
        sudo tc qdisc replace dev "$INTERFACE" root tbf \
            rate 1mbit \
            burst 32kbit \
            latency 400ms
        echo "Network profile: 1 Mbps"
        ;;

    loss1)
        sudo tc qdisc replace dev "$INTERFACE" root netem loss 1%
        echo "Network profile: 1% PACKET LOSS"
        ;;

    mobile)
        sudo tc qdisc replace dev "$INTERFACE" root netem \
            delay 50ms 30ms \
            loss 0.5%
        echo "Network profile: MOBILE-LIKE"
        ;;

    status)
        sudo tc qdisc show dev "$INTERFACE"
        ;;

    *)
        echo "Usage:"
        echo "  $0 baseline"
        echo "  $0 latency100"
        echo "  $0 latency200"
        echo "  $0 bandwidth1mbps"
        echo "  $0 loss1"
        echo "  $0 mobile"
        echo "  $0 status"
        exit 1
        ;;
esac

echo
sudo tc qdisc show dev "$INTERFACE"

for x in /tmp/python-out-$1/*; do paste <(echo $x) <(cat $x | tail -1 | sed 's/[ ]\+//g' | cut -d= -f2); done | sort -nrk2 | head -1 | awk '{print $1}' | grep -o 'test\([0-9]\+\)' | grep -o '[0-9]\+'

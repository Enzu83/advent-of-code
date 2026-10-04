#!/usr/bin/env bash

help() {
    echo "Usage: solve.sh <YEAR> <DAY> <PART>"
}

solve_rust() {
    local PACKAGE="day-$DAY-$PART"
    cd "$YEAR_DIR" || exit 1
    cargo run -p $PACKAGE
    exit 0
}

solve_go() {
    cd "$YEAR_DIR/$(printf '%02d' $DAY)" || exit 1
    go run day$PART.go
    exit 0
}

solve_python() {
    local FILE
    FILE="$YEAR_DIR/$(printf '%02d' $DAY)/puzzle$PART.py"
    python3 "$FILE"
    exit 0
}

solve_c() {
    exit 0
}


# verify the number of passed args
if [ "$#" -ne 3 ]; then
    help
    exit 1
fi

YEAR_DIR="$(dirname "$0")/year-$(("$1"))"
DAY=$(("$2"))
PART=$(("$3"))

# rust | go | python | c
if [[ $(find "$YEAR_DIR" -name "*.rs" 2> /dev/null) ]]; then
    solve_rust
elif [[ $(find "$YEAR_DIR" -name "*.go" 2> /dev/null) ]]; then
    solve_go
elif [[ $(find "$YEAR_DIR" -name "*.py" 2> /dev/null) ]]; then
    solve_python
elif [[ $(find "$YEAR_DIR" -name "*.c" 2> /dev/null) ]]; then
    solve_c
else
    echo "Couldn't find language used in '$YEAR_DIR'"
    exit 1
fi

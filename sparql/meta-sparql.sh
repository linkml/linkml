#!/bin/sh
while getopts hi:s:q: flag
do
    case "${flag}" in
        h)
            echo "TODO"
            exit 0
            ;;
        i) input=${OPTARG};;
        s) schema=${OPTARG};;
        q) query=${OPTARG};;
    esac
done
OUT="$(mktemp)"
SCRIPT="$0"
SDIR="$(dirname $SCRIPT)"
DIR="$SDIR/.."
ARG_I=$([ $input ] && echo "-i $input" || echo  )
robot merge -i $DIR/meta.ttl -i $schema $ARG_I query -P $DIR/meta.context.jsonld -f tsv  --query $query $OUT
cat $OUT
rm $OUT

#!/bin/bash

# Bash script that pulls a bunch of SEC pdfs about company financials for analysis using RAG

REPO_URL="https://github.com/docugami/KG-RAG-datasets"
SUBDIR="sec-10-q"
DESTINATION="data"

mkdir $DESTINATION
git clone --no-checkout --depth 1 "$REPO_URL" $DESTINATION && cd $DESTINATION || exit
git sparse-checkout init --cone
git sparse-checkout set "$SUBDIR"
git checkout

echo "Cloned '$REPO_URL' from '$SUBDIR' into $DESTINATION."

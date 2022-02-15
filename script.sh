NAME=$(buildkite-agent meta-data get dt-name)
echo $NAME
export DT_NAME=$NAME
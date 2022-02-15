export NAME=$(buildkite-agent meta-data get dt-name)
echo $NAME
echo $NAME | buildkite-agent pipeline upload
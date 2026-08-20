# Snapshot the working container as a template
lxc snapshot test-agent-22 base
lxc publish test-agent-22/base --alias agent-template

# Launch 10 copies from the template
for i in {1..10}; do
    lxc launch agent-template turbine-$i
    lxc config set turbine-$i environment.KAFKA_BROKER 172.24.42.86:9094
    lxc config set turbine-$i environment.TURBINE_ID turbine-$i
    lxc exec turbine-$i -- systemctl enable --now agent
done

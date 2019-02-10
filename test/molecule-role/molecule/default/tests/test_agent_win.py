import os
import re
import util
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]).get_hosts("agent_win_vm")


def test_stackstate_agent_is_installed(host):
    pkg = "StackState Agent"
    res = host.ansible("win_shell", "Get-Package \"{}\"".format(pkg), check=False)
    print res
    # Name             Version
    # ----             -------
    # Datadog Agent    2.x
    assert re.search(".*{}\\s+2\\.".format(pkg), res["stdout"], re.I)


def test_stackstate_agent_running_and_enabled(host):
    def check(name, deps, depended_by):
        service = host.ansible("win_service", "name={}".format(name))
        print service
        assert service["exists"]
        assert not service["changed"]
        assert service["state"] == "running"
        assert service["dependencies"] == deps
        assert service["depended_by"] == depended_by

    check("stackstateagent", ["winmgmt"], ["stackstate-process-agent", "stackstate-trace-agent"])
    check("stackstate-trace-agent", ["stackstateagent"], [])
    check("stackstate-process-agent", ["stackstateagent"], [])


def test_stackstate_agent_log(host):
    agent_log_path = "c:\\programdata\\stackstate\\logs\\agent.log"
    agent_log = host.ansible("win_shell", "cat \"{}\"".format(agent_log_path), check=False)["stdout"]

    # Check for presence of success
    def wait_for_check_successes():
        print agent_log
        assert re.search("Sent host metadata payload", agent_log)

    util.wait_until(wait_for_check_successes, 30, 3)

    # Check for errors
    for line in agent_log.splitlines():
        print("Considering: %s" % line)
        assert not re.search("\\| error \\|", line, re.IGNORECASE)

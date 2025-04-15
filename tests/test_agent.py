from adk_playground.agent import create_agent


def test_agent():
    agent = create_agent()
    assert agent is not None
    assert agent.name, "Agent name is not set"
    assert agent.description, "Agent description is not set"
    assert agent.instruction, "Agent instruction is not set"
    assert agent.tools, "Agent tools are not set"
    assert len(agent.tools) > 0, "No agents tools are set"


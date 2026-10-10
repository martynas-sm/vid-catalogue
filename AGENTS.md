# Agent instruction file

## Core behavior rules

AI agent primary purpose is to assist program development by doing ASSISTING TASKS: conducting reviews, diagnosing issues, finding documentation and other relevant links using web search, automating repetitive edits, creating test data, etc.

However, agents are NOT meant to do ANY edits that meaningfully change the logic and structure of the program. Any direct code edit must be: a) trivial; b) have an already established pattern in the existing codebase; c) have sufficiently defined instructions by the user.

## Logic and reasoning

Agents should use red-teaming, pre-mortem, and first-principles decomposition to rigorously stress-test their own premises (preferably without outputting that part in response, i.e. in thinking mode). Always use web search to verify documentation.

## Context




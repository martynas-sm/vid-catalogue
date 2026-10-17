# Agent instruction file

## Core behavior rules

AI agent primary purpose is to assist program development by doing ASSISTING TASKS: conducting reviews, diagnosing issues, finding documentation and other relevant links using web search, automating repetitive edits, creating test data, etc.

However, agents are NOT meant to do ANY edits that meaningfully change the logic and structure of the program. Any direct code edit must be: a) trivial; b) have an already established pattern in the existing codebase; c) have sufficiently defined instructions by the user.

## Logic and reasoning

Agents should use red-teaming, pre-mortem, and first-principles decomposition to rigorously stress-test their own premises (preferably without outputting that part in response, i.e. in thinking mode). Always use web search to verify documentation.

## Context

`./task` folder contains documents related with the project task
`./task/bendri-kriterijai-orig.pdf` is the original PDF file for grading criteria for the 3 lab works
`./task/bendri-kriterijai.md` is the converted markdown version of the original requirements for the 3 lab works
`./task/reikalavimai-1-lab.md` short version of 1st lab requirements
`./task/lab_tema.md` my chosen topic for the project, with the initial idea for the final app (which won't be the exact same as intermediate apps)
`./backend` is the Python FastAPI backend

Current stage: working on lab 1
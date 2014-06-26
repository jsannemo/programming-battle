# Programming Battles

A service and web interface to support Programming Battles, a kind of programming competitions.

## What is a Programming Battle?

A Programming Battle is a team competition where teams compete, trying to solve programming tasks
and breaking the other teams' solutions.

Each team is partitioned into two sub-teams, the *solvers* and the *testers*. These two sub-teams
will have no communication between each other until the contest is over.

At the start of the contest, the teams are given a set of programming problems of various kinds.
The task of the solvers is to write a program which solves the problems and submit them in the
web interface. Solutions which are accepted generates points to the team until it is defeated
by a test case.

The tester, on the other hand, construct test cases for the problems and submit them to the
interface. Points are awarded to the tester if a test case manages to break a solution which
a solver has submitted.

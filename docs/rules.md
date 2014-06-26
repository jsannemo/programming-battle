# Rules

This document describes the rules of a programming battle.

## Solvers and testers

Before the competition start, each team must be partitioned into two subteams
called the *solvers* and *testers*. These two subteams must be separated from
each other during the contest.

## Competition

During the contest, the teams are given a set of programming challenges called
*problems*. The task of the solvers is to create programs which solve the
problems, while the testers will create test cases for the problems in an
attempt to find errors in the solverrs' solutions.

## Problems

A problem consists of:
* a *problem statement* which describes how a correct program should operate
  and a specification of the test case format
* at least one *input validator* which checks that the test cases constructed
  by the testers follow the test case format specified in the statement
* at least one *solution validator* which checks that a solution operates
  correctly given a certain test case
* at least one solution to the problem which must operate correctly on every
  test case that follows the specification.
* a *time limit* which specifies the maximum execution time of a correct
  program
* a *memory limit*  which specifies the maximum memory a correct program may
  use

The problem statement, time limit and memory limit are public to all the teams.

A problem may be set to be available only after a certain time after
competition start. In this case, the contestants are only shown the time before
the problem becomes available.

## Solving a test case

A solution is said to *solve* a test case if:
* its time usage does not exceed the time limit for the problem
* its memory usage does not exceed the memory limit for the problem
* it is considered by every solution validator to have operated correctly.

## Submitting

A solver can a solution to an available problem. The solution will then be run
on every test case previously submitted to the problem. If the solution solves
all of these test cases, it is considered *active*. If a team already had an
active solution to the problem, it becomes *inactive*. If a submitted solution
does not pass all existing test cases, it is considered *rejected*.

The time at which a solution becomes active is the time it arrived in the
judging system.

A tester can at any time during the competition submit a test case to an
available problem. All active solutions will then be run on the test case. If
an active solution fails the test case, the solution will instead become
*defeated* and the test case is said to have *defeated* the solution.

The time at which a test case defeat a solution is the time the test case arrived
in the judging system.

A problem may be set to have a limit on the number of submissions a certain
team is allowed to make.

A problem may be set to have a limit on the number of test cases a certain team
is allowed to submit.

## The scoring

Every problem *i* has a problem scoring value *P_i* and a  test case scoring
value of *T_i*

A period of *n* seconds is chosen, where *n* divides the total duration of the
contest. For every problem *i*, if a team has an active solution in the
interval [nk, n(k+1)) seconds since start of the contest for some non-negative
integer *k*, the team scores *P_i* points.

For example, if *n* = 4, one period would be the times 04:03:02.000 -
04:03:06.000. To get points in this interval, a submission must become active
no later than 04:03:02.000, and must not be defeated earlier than 04:03:06.000.

If a team's test case defeats a submission, the team is awarded *T_i* points.

The final score of a team is the sum of the submission score and test case
score.

## Tie breaking

If two teams have the same score, the teams are tied on their test case score.
If there is still a tie, the team which defeated the least number submissions
win. If there is still a tie, let *P_1j* >= *P_2j* >= ... >= *P_nj* be the
sorted sequence of problem scores for the *n* problems for team *j*. The team
with the largest lexicographical such sequence wins. If there is still a tie,
the teams are tied.

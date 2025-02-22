# 🎄🦹🏼‍♂️🤖 Jack Cheats at Advent of Code 2024 🤖🦹🏼‍♂️🎄

I've not yet caught the habit of using chat-style code assistants, so let's give it a go. I don't expect to do many days but I'll make sure I don't do the current day to try to avoid climbing leaderboards...

My goal is not to write any code myself and (in true Advent of Code spirit...) to spend as little time as possible understanding the problem/reading code to identify bugs.

My expectation: It will solve a lot of the early ones but get stuck later on?

Using ChatGPT-4o.

## Prompts

I started with a basic prompt along the lines of:

> Please write a Python script to solve the following problem:
>
> <copy-pasted part 1 problem text>

and then:

> Please update the solution for part 2 of the problem:
>
> <copy-pasted part 2 problem text>

After the first couple of days I realised I needed to tell it where to get the input data, so slightly updated the part 1 prompt to:

> Please write a Python script to solve the problem below. It should read the input from a file input.txt, which has the same format as the example.
>
> <copy-pasted part 1 problem text>

## Log

Attempts in December 2024 (attempting to solve one day later):

| Day    | Part 1 solved | Part 1 prompts | Part 2 solved | Part 2 prompts | Notes |
| ---- | ---- | ---- | ----| ---- |  ----------- |
| 1  | ✅ | 3 | ✅ | 1 | Had to prompt it to write something to load the input file, and then tell it the input file format. Otherwise solved it without issues. |
| 2  | ✅ | 3 | ✅ | 1 | Solved without additional prompting. Additional part 1 prompts were me hitting enter too soon and forgetting to tell it to load the input file again. |
| 3  | ✅ | 1 | ✅ | 3 | Had to read the task and the code to get it to solve part 2, what a drag. There was a logic issue that it was able to fix when I pointed out the problem. It didn't change anything between the first 2 prompts (when I only told it the output was wrong, not the potential cause). |
| 4  | ✅ | 1 | ✅ | 8 | Had to manually change the filename in the script for part 1. Was the biggest struggle so far to get it to understand part 2 correctly. It struggled to understand which MAS / SAM patterns were valid/invalid. The prompting was a lot of hand holding starting from the simplest possible example. |
| 5  | ✅ | 1 | ✅ | 1 | Over to the robot overlords today. Pretty sure this is one I would have spent a long time on myself as I doubt I would have immediately thought of topological sort/I would have implemented a broken version of it myself. ChatGPT commented the script to say it was using Kahn's algorithm, so it actually taught me something today. |
| 6  | ✅ | 1 | ✅ | 1 | Part 2 solution was slow (38s). |
| 7  | ✅ | 2 | ✅ | 2 | The first time the part 1 script was incorrect initially (other than issues with me specifying the input file on the first couple of days), but it was able to fix it after prompting it that it returned 0 for the example. The part 1 implementation took 34s to run. The first part 2 implementation was too slow, but asking it to make it more efficient worked - it added recursion and checking whether intermediate results had become too big. However, it mentioned memoization could make it more efficient but didn't add it to the script. |
| 8  | ✅ | 2 | ✅ | 4 | Part 1 incorrect initially, had not interpreted the antennas along a line logic correctly and had added some unused and unneeded variables too. I read the problem and the generated script to figure out how to prompt it to correct it with the 2nd prompt. Part 2 took me 4 prompts to correct the logic for finding antinode locations. The last prompt gave me two outputs to give a preference between - one gives the correct answer and the other is wrong. The one that gives the correct answer has a block of unused code using `gcd` which was used in previous incorrect answers. Our Slack channel had messages about the part 2 wording being difficult to understand. |
| 9  | ❌ | 13 | NA | NA | Gave up on part 1 after 13 prompts. I think I'm not helping by being tired and not understanding the problem fully myself. Last attempt pre-Christmas - remaining solutions may have additional caveats around whether ChatGPT has seen solutions in the training data/is using RAG to get them. |
| 10  | ✅ | 1 | ✅ | 1 |  |
| 11   | ✅ | 1 | ✅ | 7 | Part 2 it failed to come up with a more efficient solution itself. It suggested a numpy-based matrix multiplication approach that I haven't tried to understand but gave an answer much too large. I prompted it with a (strong) hint based on Radka's answer to get it to solve it. |
| 12  | ✅ | 1 | ❌ | 8 | First attempt for part 2 only renamed a variable from `perimeter` to `sides`. Later attempts tried to do something different but still fail to return a different answer to part 1. I may be contributing to the problem because the problem is something I often get wrong - it's caused by lines being drawn in-between grid points. |
| 13  | ✅ | 3 | ✅ | 14 | Part 1 took a few prompts to get it to parse the input correctly. Ended up in a big loop for part 2 of it failing to get a correct solution. I prompted it about simultaneous equations (again stealing a glance at other people's solution first) but it didn't actually update the script at first despite it telling me how the logic would work... It also switched to only returning updated portions of the script, rather than a whole updated script, for a while. |
| 14  | ✅ | 1 | ✅ | 5 | Came up with some crazy ideas for part 2 (that didn't work), including one using DBSCAN. After a few prompts to get it to try something different it tried something based on checking for densely populated sub-regions, which worked (and kind of blew my mind). |
| 15  | ✅ | 6 | ❌ | 7 | Took a lot of hand holding in part 1 to get the logic for moving multiple boxes correct. I then ran out of patience trying to get it to understand the movement rules for wide boxes. |
| 16  | ✅ | 1 | ❌ | 11 | Gave up trying to get it to solve part 2 but some of my prompts were likely misleading or unhelpful. |
| 17  | ✅ | 3 | ✅ | 12 | Part 2 only with a lot of effort and drawing from other people's solutions to tell ChatGPT the way to approach creating a more efficient solution. |
| 18  | ✅ | 3 | ✅ | 1 | Part 1 it initially failed due to assuming the grid size would be the same as the example. |
| 19  | ✅ | 3 | ✅ | 1 | Pretty smooth sailing - was able to fix a bug and then speed up part 1 without any hand holding. |
| 20  | ✅ | 11 | ❌ | 4 | First part 1 prompt gave up generating Python at the end and left some plain text hanging around. Got a very slow solution for part 1 after a lot of going round in loops with prompts that resulted in either a slow script or a script that returned 0. Quickly ran out of patience for part 2 after it was again much too slow or returning zero. |
| 21  |  |  |  |  |  |
| 22  |  |  |  |  |  |
| 23  |  |  |  |  |  |
| 24  |  |  |  |  |  |
| 25  |  |  |  |  |  |

## Misc

- Days 1 and 2 I have no idea what the problem or solution actually were, purely hands over to ChatGPT.
- I'm getting solutions quickly (for first few days) but it's frustrating when it doesn't work, more frustrating than if it's my programming/logic at fault. After 4 days I already doubt whether I could get it to solve a harder problem without telling it the solution. I think this is a big part of why I'm yet to embrace chat interfaces much - if I need to articulate the solution and review the generated code for errors would it have been easier to just write it myself (maybe, but probably slower too)?
  - but then day 5 gave me an existential crisis again.
- I'm not paying any attention to the explanations it gives after the script it generates. Maybe they would give clues for how to fix things/where there are issues in interpreting the problem.
- So far, just telling it the output is wrong doesn't seem to be enough for it to spot/correct the error.
  - but this did work for day 7 part 1.
- Sometimes it correctly articulates the problem in its descriptions around the code, but then the script itself misses some of the nuances in the problem/logic, doesn't implement what it said at all, or leaves the previous version of the script unchanged or mildly refactored. This get very frustrating.
- Can I be sure that ChatGPT isn't cheating itself? E.g. does it already have access to other people's answers? E.g. a "What was the problem for Advent of Code 2024, day 1?" prompt causes it to search the internet and return a summary and a link to a YouTube video of someone solving it...
- Sometimes it asks you to evaluate a new version of ChatGPT by giving two outputs and asking you which you prefer.
- Day 8 included unused code, but tricky to spot at a first glance.
- Feeling after day 8:
  - Can I solve the problems without writing code? **Yes**.
  - Can I solve the problems without understanding them or candidate code solutions? **No** (at least not always).
- A couple of the ones that needed more prompting involved some more complex 'spatial'-type logic, e.g. variations of things along diagonals.
- There might be a better way to prompt it to make edits, but prompts for small changes require generating the whole script (and any prose around it) again, which is pretty slow.
- On Day 9 it started giving me Chat GPT-4o with Canvas, which gives an editor like environment with a Python runtime and some other features. I'm going to mostly stick to conventional chat style prompting. It generates less text to explain the script in this mode.
- Sometimes it feels like trying to teach someone who just refuses to learn or is completely missing the point.
- Sometimes it returns updated functions rather than a whole updated script. More of an interface issue but it's quite annoying when what you're trying to lazily copy-paste is changing/moving around.
- Copy-pasting a traceback into a prompt worked _occasionally_.

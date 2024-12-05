# Jack cheats at Advent of Code

I've not yet caught the habit of using chat-style code assistants, so let's give it a go. I don't expect to do many days but I'll make sure I don't do the current day to try to avoid climbing leaderboards...

My goal is not to write any code myself and (in true Advent of Code spirit...) to spend as little time as possible understanding the problem/reading code to identify bugs.

Using ChatGPT-4o.

## Log

| Day    | Part 1 solved | Part 1 prompts | Part 2 solved | Part 2 prompts | Notes |
| ---- | ---- | ---- | ----| ---- |  ----------- |
| 1  | ✅ | 3 | ✅ | 1 | Had to prompt it to write something to load the input file, and then tell it the input file format. Otherwise solved it without issues. |
| 2  |  ✅ | 3 | ✅ | 1 | Solved without additional prompting. Additional part 1 prompts me hitting enter too soon and forgetting to tell it to load the input file again. |
| 3  | ✅ | 1 | ✅ | 3 | Had to read the task and the code to get it to solve part 2, what a drag. There was a logic issue that it was able to fix when I pointed out the problem. It didn't change anything between the first 2 prompts (when I only told it the output was wrong, not the potential cause). |
| 4  | ✅ | 1 | ✅ | 8 | Had to manually changed the filename in the script for part 1. Was the biggest struggle so far to get it to understand part 2 correctly. It struggled to understand which MAS / SAM patterns were valid/invalid. The prompting was a lot of hand holding starting from the simplest possible example. |
| 5  |  |  |  |  |  |
| 6  |  |  |  |  |  |
| 7  |  |  |  |  |  |
| 8  |  |  |  |  |  |
| 9  |  |  |  |  |  |
| 10  |  |  |  |  |  |
| 11   |  |  |  |  |  |
| 12  |  |  |  |  |  |
| 13  |  |  |  |  |  |
| 14  |  |  |  |  |  |
| 15  |  |  |  |  |  |
| 16  |  |  |  |  |  |
| 17  |  |  |  |  |  |
| 18  |  |  |  |  |  |
| 19  |  |  |  |  |  |
| 20  |  |  |  |  |  |
| 21  |  |  |  |  |  |
| 22  |  |  |  |  |  |
| 23  |  |  |  |  |  |
| 24  |  |  |  |  |  |
| 25  |  |  |  |  |  |

## Misc

- Days 1 and 2 I have no idea what the problem or solution actually were, purely hands over to ChatGPT.
- I'm getting solutions quickly (for first few days) but it's frustrating when it doesn't work, more frustrating than if it's my programming/logic at fault. After 4 days I already doubt whether I could get it to solve a harder problem without telling it the solution. I think this is a big part of why I'm yet to embrace chat interfaces much - if I need to articulate the solution and review the generated code for errors would it have been easier to just write it myself (maybe, but probably slower too)?
- I'm not paying any attention to the explanations it gives after the script it generates. Maybe they would give clues for how to fix things/where there are issues in interpreting the problem.
- So far, just telling it the output is wrong doesn't seem to be enough for it to spot/correct the error.
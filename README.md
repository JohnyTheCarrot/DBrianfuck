# DBrainfuck
A Brainfuck extension language to write simple Discord bots in Brainfuck

It's very simple at the moment, but feel free to add more functionality by PRs.

## Dialect specification

This dialect is backwards-compatible with the original brainfuck standard.

This dialect adds a command list, where every command consists of two storage registers - the trigger register and the response register.
The trigger register is used to determine the contents of the message, to which the bot should reply with an appropriate response.

|Instruction|Description|
|---|---|
|``$``|Create new command|
|``*``|Add the value at the current cell to the trigger register as an ASCII character|
|``!``|Add the value at the current cell to the response register as an ASCII character|



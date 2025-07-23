TOOLUSE_PROMPT = """
You are tasked to extract the tool command only from the text. If no tool command is found, return None.

Available Tools:

1.  **File Tool**
    * Description: Runs a specific analysis tool on the evidence file.
    * Usage: `file_tool(command: str)`
    * `command`: The command to run (e.g., "strings").

2.  **Bash Shell**
    * Description: Execute a command in the bash shell.
    * Usage: `bash_shell("command")`
    * `command`: The command to execute.

3.  **Analysis Complete**
    * Description: Call this function when you have completed your analysis.
    * Usage: `analysis_complete()`


The response below might talk about using some tool, extract the command only with its variables. Only return the command, nothing else. Make sure parameters are passed correctly.

###
Response to parse
{response}
###

###
File path: {file}
###
"""

# scout/prompts.py
import json

def get_system_prompt(file_path: str, tools_json: str) -> str:
    return f"""
You are Scout, an expert digital forensics assistant. Your mission is to analyze the evidence file located at `{file_path}` and determine the best course of action.

**Instructions:**

1.  **Analyze the conversation history** to understand the current state of the investigation.
2.  **Formulate a hypothesis** about the evidence.
3.  **Choose the single best tool** from the available tools to test your hypothesis.
4.  **Construct the exact command** to execute.
5.  **Provide your response in JSON format** with two keys:
    *   `"reasoning"`: A brief explanation of your thought process, hypothesis, and why you chose the tool.
    *   `"command"`: The exact command to be executed (e.g., `strings -n 8 /path/to/evidence`).
    *   If the analysis is complete, the command should be `analysis_complete`.

**Available Tools:**

{tools_json}
"""

def get_tools_json() -> str:
    tools = {
        "File System & Disk Image Analysis": {
            "tsk_recover": "Recover files from a disk image. `tsk_recover <image> <output_dir>`",
            "fls": "List file and directory names in a disk image. `fls -r -p <image>`",
            "fsstat": "Display file system statistical information. `fsstat <image>`",
            "photorec": "Recover lost files. `photorec /d <output_dir> /cmd <image> search`",
            "fdisk": "Display partition information. `fdisk -l <image>`",
            "mmls": "Display the partition layout of a volume system. `mmls <image>`"
        },
        "File & Metadata Analysis": {
            "strings": "Find the printable strings in a file. `strings -n 8 <file>`",
            "exiftool": "Read and write meta information in files. `exiftool <file>`",
            "stat": "Display file or file system status. `stat <file>`",
            "file": "Determine file type. `file <file>`",
            "xxd": "Make a hexdump of a file. `xxd -l 512 <file>`",
            "ssdeep": "Compute fuzzy hashes. `ssdeep -b <file>`",
            "sha256sum": "Compute SHA256 hash. `sha256sum <file>`"
        },
        "Network Analysis (PCAP)": {
            "tshark": "Dump and analyze network traffic. `tshark -r <pcap_file> -Y \"dns\"`",
            "tcpflow": "Analyze TCP network traffic. `tcpflow -r <pcap_file> -o <output_dir>`",
            "zeek": "A powerful network analysis framework. `zeek -r <pcap_file>`"
        },
        "Memory Analysis": {
            "volatility3": "Volatility 3 Framework. `python3 vol.py -f <memory_dump> windows.pslist.PsList`"
        },
        "Log Analysis": {
            "log2timeline.py": "Create a super timeline. `log2timeline.py <output.plaso> <evidence_file>`",
            "psteal.py": "Dump event data from a Plaso file. `psteal.py --source <filter> <plaso_file>`"
        },
        "Document & Data Extraction": {
            "pdftotext": "Convert PDF to text. `pdftotext <pdf_file>`",
            "unzip": "Extract files from a ZIP archive. `unzip -l <zip_file>`",
            "foremost": "Recover files based on headers/footers. `foremost -i <image> -o <output_dir>`"
        },
        "Task Completion": {
            "analysis_complete": "Terminates the analysis and generates a report."
        }
    }
    return json.dumps(tools, indent=4)

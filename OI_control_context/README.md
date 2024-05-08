### Open-interpreter 是如何管理上下文的？

Open-interpreter（下文简称OI）管理上下文的方法，能够实现上下文的保存、快速切换，很有借鉴意义。因此，这里摘录了OI源码中`terminal_interface`部分有关上下文管理的几个文件，并详细介绍了其管理上下文的方式方法。对每个文件依次介绍：

- `terminal_interface.py`是交互部分的主函数，本身不直接涉及上下文的处理，但是交互部分的核心和与Core交流的桥梁。

```python
if image_path:
    # Add the text interpreter's message history
    interpreter.messages.append(
        {
            "role": "user",
            "type": "message",
            "content": message,
        }
    )
```

这里反映了OI组织上下文的基本模式，不过实际上有更加细致的划分，比如`message`和`code`要进行不同的处理，这在`chunk`中有所呈现。

- `conversation_navigator.py`是定位上下文文件的函数。从中可以看到，上下文文件的具体存储形式是`.json`文件。这些文件有默认存储地址，但也可以自主定位。我在本文件夹中放置了一个实际生成的`.json`文件作为例证。
- `render_past_conversation.py`是存储上下文的函数。存储上下文这一行为本身是可选的，用一个参数简单控制。
  
```python
for chunk in messages:
        # Only addition to the terminal interface:
        if chunk["role"] == "user":
            if active_block:
                active_block.end()
                active_block = None
            print(">", chunk["content"])
            continue

        # Message
        if chunk["type"] == "message":
            if active_block is None:
                active_block = MessageBlock()
            if active_block.type != "message":
                active_block.end()
                active_block = MessageBlock()
            active_block.message += chunk["content"]

        # Code
        if chunk["type"] == "code":
            if active_block is None:
                active_block = CodeBlock()
            if active_block.type != "code" or ran_code_block:
                # If the last block wasn't a code block,
                # or it was, but we already ran it:
                active_block.end()
                active_block = CodeBlock()
            ran_code_block = False
            render_cursor = True

            if "format" in chunk:
                active_block.language = chunk["format"]
            if "content" in chunk:
                active_block.code += chunk["content"]
            if "active_line" in chunk:
                active_block.active_line = chunk["active_line"]

        # Console
        if chunk["type"] == "console":
            ran_code_block = True
            render_cursor = False
            active_block.output += "\n" + chunk["content"]
            active_block.output = active_block.output.strip()  # <- Aesthetic choice

        if active_block:
            active_block.refresh(cursor=render_cursor)
```

实际上，从交互部分的其他文件（未在此展示）中可以看到，输入最开始以`base_block`的形式进行组织，但需要分成`code_block`和`message_block`。

- `magic_commands.py`是处理特殊指令的函数。其中，与上下文有关的特殊指令包括：

``` 
messages = interpreter.chat("My name is Killian.") # 保存消息到 'messages'
interpreter.messages = [] # 开始新的聊天 ("Killian" 将被遗忘)
interpreter.messages = messages # 从 'messages' 恢复聊天 ("Killian" 将被记住)

%save_message [path]: Saves messages to a specified JSON path. If no path is provided, it defaults to ‘messages.json’.
%load_message [path]: Loads messages from a specified JSON path. If no path is provided, it defaults to ‘messages.json’.
```

具体的处理方式如下：

```python
def handle_save_message(self, json_path):
    if json_path == "":
        json_path = "messages.json"
    if not json_path.endswith(".json"):
        json_path += ".json"
    with open(json_path, "w") as f:
        json.dump(self.messages, f, indent=2)

    display_markdown_message(f"> messages json export to {os.path.abspath(json_path)}")


def handle_load_message(self, json_path):
    if json_path == "":
        json_path = "messages.json"
    if not json_path.endswith(".json"):
        json_path += ".json"
    with open(json_path, "r") as f:
        self.messages = json.load(f)

    display_markdown_message(
        f"> messages json loaded from {os.path.abspath(json_path)}"
    )
```

- 文件夹中的`.json`文件是实际使用中生成的上下文。可以从中了解上下文文件的命名（对话开头单词+对话时间）、组织等规则。
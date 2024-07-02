# 消息队列

该目录下的`main.c`与`task_queue.c`可编译形成了消息队列的可执行文件(task_queue)
执行`tq_gen.sh`脚本会完成编译并将该可执行文件放入/usr/local/bin目录下，并将其作为系统服务
> 可能需要先`chmod +x ./msg.sh`才能执行该脚本
对于`send.c`与`receive.c`中提供的`se_msg()`与`re_msg()`方法可通过以下方式调用这两个方法
```c
#include "send.c"
#include "receive.c"

// 即可使用 se_msg() 与 re_msg() 方法
```

需要使用python调用这两个函数时，需要`ctypes`库
```python
MAX_MSG_SIZE = 4096
from ctypes import CDLL, create_string_buffer

# 加载共享库
rec = CDLL('/usr/local/lib/libreceive.so')
sed = CDLL('/usr/local/lib/libsend.so')

# 注意在使用这两个函数时，其放回值或接受的参数都是C风格的字符串
msg = create_string_buffer(b"hello msg_queue")
sed.se_msg(msg, 0)
remsg = create_string_buffer(MAX_MSG_SIZE)
rec.re_msg(remsg)
# decode()是将c字符串转换为python字符串的方法，默认使用UTF-8解码
print(msg.value.decode())
```
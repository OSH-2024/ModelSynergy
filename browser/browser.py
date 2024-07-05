from PIL import Image
import torch
from transformers import AutoConfig, AutoModel, AutoTokenizer
from accelerate import init_empty_weights, infer_auto_device_map, load_checkpoint_in_model, dispatch_model
import os
from tqdm import tqdm
import argparse
import transformers
transformers.logging.set_verbosity(transformers.logging.CRITICAL)
parser = argparse.ArgumentParser()
parser.add_argument(
        "--folder",
        "-f",
        type=str,
        default="./test",
        help="folder path",
    )
parser.add_argument(
        "--descirbe",
        "-d",
        type=str,
        default="None",
        help="describe prompt",
    )
args = parser.parse_args()
folder_path = args.folder
describe_prompt = args.descirbe
files = []
for dirpath, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
        files.append(os.path.join(dirpath, filename))
MODEL_PATH = r'./MiniCPM-Llama3-V-2_5' # you can download in advance or use `openbmb/MiniCPM-Llama3-V-2_5`
max_memory_each_gpu = '10GiB' # Define the maximum memory to use on each gpu, here we suggest using a balanced value, because the weight is not everything, the intermediate activation value also uses GPU memory (10GiB < 16GiB)

gpu_device_ids = [0, 1] # Define which gpu to use (now we have two GPUs, each has 16GiB memory)

no_split_module_classes = ["LlamaDecoderLayer"]

max_memory = {
    device_id: max_memory_each_gpu for device_id in gpu_device_ids
}
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH, 
    trust_remote_code=True
)
# print(tokenizer.encode("yes no"))
config = AutoConfig.from_pretrained(
    MODEL_PATH, 
    trust_remote_code=True
)
with init_empty_weights():
    model = AutoModel.from_config(
        config, 
        torch_dtype=torch.float16, 
        trust_remote_code=True
    )

device_map = infer_auto_device_map(
    model,
    max_memory=max_memory, no_split_module_classes=no_split_module_classes
)

# print("auto determined device_map", device_map)

# Here we want to make sure the input and output layer are all on the first gpu to avoid any modifications to original inference script.

device_map["llm.model.embed_tokens"] = 0
device_map["llm.model.layers.0"] = 0
device_map["llm.lm_head"] = 0
device_map["vpm"] = 0
device_map["resampler"] = 0

load_checkpoint_in_model(
    model, 
    MODEL_PATH, 
    device_map=device_map)

model = dispatch_model(
    model, 
    device_map=device_map
)

torch.set_grad_enabled(False)

model.eval()



scores = []
for image_path in tqdm(files):
    response = model.chat(
        image=Image.open(image_path).convert("RGB"),
        msgs=[
            {
                "role": "user",
                "content": f"图片内容是否符合\'{describe_prompt}\'的描述?若符合则输出\'yes\',若不符合则输出\'no\',不要输出其他内容"
            }
        ],
        tokenizer=tokenizer
    )

    # print(response)
    # print(response.shape)
    prob = response[0, -1]
    prob = torch.nn.functional.log_softmax(prob, dim=0)
    # print(prob)
    # print(prob[9891], prob[912])
    scores.append((image_path, prob[9891].item()))
scores = sorted(scores, key=lambda x:-x[1])
# print(scores)
print(f"找到的图片:{scores[0][0]}")
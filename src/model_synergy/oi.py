import op_gen
from interpreter import interpreter

def main(args):
    prompt = op_gen(args)
    interpreter.chat("Please follow these prompts: " + prompt)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_model_args(parser)
    parser.add_argument(
        "--conv-template", type=str, default=None, help="Conversation prompt template."
    )
    parser.add_argument(
        "--conv-system-msg", type=str, default=None, help="Conversation system message."
    )
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--repetition_penalty", type=float, default=1.0)
    parser.add_argument("--top_k", type=int, default=-1)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--no-history", action="store_true")
    parser.add_argument(
        "--style",
        type=str,
        default="simple",
        choices=["simple", "rich", "programmatic"],
        help="Display style.",
    )
    parser.add_argument(
        "--multiline",
        action="store_true",
        help="Enable multiline input. Use ESC+Enter for newline.",
    )
    parser.add_argument(
        "--mouse",
        action="store_true",
        help="[Rich Style]: Enable mouse support for cursor positioning.",
    )
    parser.add_argument(
        "--judge-sent-end",
        action="store_true",
        help="Whether enable the correction logic that interrupts the output of sentences due to EOS.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print useful debug information (e.g., prompts)",
    )
    parser.add_argument(
        "--inf-llm-config-path",
        type=str, help="Inf LLM patch config",
        default=None
    )
    parser.add_argument(
        "--clear-kv-cache",
        action="store_true"
    )
    parser.add_argument(
        "--load-kv-cache-file",
        type=str, help="load kv cache from",
        default=None
    )
    parser.add_argument(
        "--store-kv-cache-file",
        type=str, help="store kv cache to",
        default=None
    )
    args = parser.parse_args()
    main(args)
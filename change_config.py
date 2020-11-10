#!/usr/bin/env python3

import argparse
import json
import os

from transformers.hf_api import HfApi


def convert_value(value_str):
    if value_str.replace("-", "").isdigit():
        return int(value_str)
    try:
        float(value_str)
        return float(value_str)
    except:  # noqa: E722
        return value_str


def main(args):
    api = HfApi()
    model_dict_list = api.model_list()

    if args.list is not None and args.search_key is not None:
        raise ValueError("Please define either `--search_key` OR `--list`, not both.")
    if args.list is not None:
        model_dict_list = [
            model_dict
            for model_dict in model_dict_list
            if model_dict.modelId in args.list
        ]
    elif args.search_key is not None:
        model_dict_list = [
            model_dict
            for model_dict in model_dict_list
            if args.search_key in model_dict.modelId
        ]
    else:
        raise ValueError("Either `--search_key` OR `--list` has to be defined.")

    for model_dict in model_dict_list:
        model_identifier = model_dict.modelId

        user, model = model_identifier.split("/")

        if os.path.exists(f"./{user}_{model}") and os.path.isdir(f"./{user}_{model}"):
            if args.rf:
                os.system(f"rm -rf ./{user}_{model}")
            else:
                print(
                    f"./{user}_{model} already exists. You should consider using `-rf` if "
                    f"./{user}_{model} is an old version of the model's repo."
                )

        os.system(f"git clone https://huggingface.co/{user}/{model} {user}_{model}")

        with open(f"./{user}_{model}/config.json") as f:
            config_json = json.load(f)

        sub_dict = config_json
        for value in args.key.split("/")[:-1]:
            sub_dict = config_json[value]

        sub_dict[args.key.split("/")[-1]] = convert_value(args.value)

        with open(f"./{user}_{model}/config.json", "w") as f:
            json.dump(config_json, f, indent=2, sort_keys=True)

        if args.upload:
            cd_cmd = f"cd ./{user}_{model} && "
            os.system(cd_cmd + f"git add .")
            os.system(cd_cmd + f"git commit -am 'Changed {args.key} to {args.value}'")
            os.system(cd_cmd + f"git push")

            os.system(f"rm -rf ./{user}_{model}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Change the configs of all models that match `search_key` or all models as defined in `list`."
    )
    parser.add_argument(
        "--search_key",
        type=str,
        help=(
            "A string that matches one or more model identifier names. E.g."
            " the `--search_key tiny-ran` matches all model identifiers shown when searching"
            " for `tiny-ran` online: https://huggingface.co/models?search=tiny-ran"
        ),
    )
    parser.add_argument(
        "--list",
        type=str,
        nargs="+",
        default=None,
        help="A list of complete model identifiers to change. By default this is an empty list and not used.",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Whether to upload the changes and delete all local files / repositories",
    )
    parser.add_argument(
        "--rf",
        action="store_true",
        help="Whether to force remove already existing repos under the name <user>_<model_name>."
    )
    parser.add_argument(
        "--key",
        type=str,
        help="The key to change. If key is nested use '', *e.g.* `task_specific_params/summarization/max_length`",
    )
    parser.add_argument(
        "--value", type=str, help="The value the key should be set to, *e.g.* 1024"
    )
    args = parser.parse_args()
    main(args)

#!/usr/bin/env python3
import argparse

from transformers.hf_api import HfApi


def main(args):
    hf_api = HfApi()
    token = hf_api.login(args.user, args.pw)
    url = hf_api.create_repo(token, name=args.model, organization=args.org)
    print(f"Succesfully created {url}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new repo."
    )
    parser.add_argument(
        "--user",
        type=str,
        help=(
            "Your username."
        ),
    )
    parser.add_argument(
        "--pw",
        type=str,
        help=(
            "Your password."
        ),
    )
    parser.add_argument(
        "--org",
        type=str,
        help=(
            "The name of the org to upload to. E.g. `google`."
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        help=(
            "Name of the model to upload. E.g.: `mt5-small`."
        ),
    )
    args = parser.parse_args()
    main(args)

import json
import argparse

from mosamaticdesktop.tasks.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(description="Run an image processing pipeline.")
    parser.add_argument("pipeline_config", help="JSON file defining the pipeline steps")
    args = parser.parse_args()

    with open(args.pipeline_config) as f:
        config = json.load(f)

    tasks = []
    for step in config["steps"]:
        cls = globals()[step["task"]]
        tasks.append(cls(step["input_dir"], step["output_dir"]))

    Pipeline(tasks).run()


if __name__ == "__main__":
    main()
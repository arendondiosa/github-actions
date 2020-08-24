# -*- coding: utf-8 -*-
# Copyright 2018 University of Groningen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import sys
from pylint import lint

def get_threshold(filename, current_threshold, service, version):
    """
    Get the threshold score
    :param filename: String, File that containes the best score. Ie, './path/file.py'
    :param current_threshold: Float, the latest score. Ie, 6.78
    :param service: String, Service to evaluate. Ie, 'originationservice'
    :param version: String, Python version to test. Ie, 'python_3'
    :return: Float, The last score to evaluate. Ie, 7.89
    """
    try:
        with open(filename) as f: file_data = f.read()
        file_object = json.loads(file_data)
        threshold = file_object[version][service]
    except:
        file_object = {}
        threshold = current_threshold

    return file_object, threshold

def store_threshold(file_source, filename, current_threshold, service, version):
    """
    Store/update the threshold score
    :param file_source: Dict, original score data. Ie, {'python_3': {'some_service': 0.0}}
    :param filename: String, File that containes the best score. Ie, './path/file.py'
    :param current_threshold: Float, the latest score. Ie, 6.78
    :param service: String, Service to evaluate. Ie, 'originationservice'
    :param version: String, Python version to test. Ie, 'python_3'
    """
    file_source[version] = file_source[version] if version in file_source else {} 
    file_source[version][service] = current_threshold

    with open(filename, 'w') as file:
        file.write(json.dumps(file_source, indent=4))

def main():
    DESC = (
        "PyLint wrapper that add the --fail-under option."
        " All other arguments are passed to pylint."
    )

    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument(
        "--path",
        dest="path",
        type=str,
        help="path where the pylint validation are going to run",
    )
    parser.add_argument(
        "--rcfile", dest="rcfile", type=str, help="path for pylint configuration"
    )
    parser.add_argument(
        "--fail-under",
        dest="threshold",
        type=float,
        default=8,
        help="If the final score is more than THRESHOLD, exit with"
        " exitcode 0, and pylint's exitcode otherwise.",
    )
    parser.add_argument(
        "--service", dest="service", type=str, help="service to evaluate"
    )
    parser.add_argument(
        "--version",
        dest="version",
        type=str,
        help="python version to test"
    )

    args, remaining_args = parser.parse_known_args()

    file_object, threshold = get_threshold('./private/pylint_score.json', args.threshold, args.service, args.version)
    path = args.path
    rcfile = args.rcfile

    run = lint.Run(["--rcfile=%s" % rcfile, path], exit=False)
    score = run.linter.stats["global_note"]

    print("score {}".format(score))
    print("threshold {}".format(threshold))
    print("msg_status {}".format(run.linter.msg_status))

    if score < threshold:
        sys.exit(run.linter.msg_status)
    else:
        store_threshold(file_object, './private/pylint_score.json', score, args.service, args.version)
        sys.exit(0)

if __name__ == "__main__":
    main()

import subprocess as sub
import os
import logging

def run_cmd(cmd):
    """Execute the command and return the output if successful. If
    unsuccessful, print the failed command and its output.
    """
    try:
        return sub.check_output(cmd, shell=True, stderr=sub.STDOUT)
    except sub.CalledProcessError as err:
        logging.error(f"The failed test setup command was [{err.cmd}].")
        logging.error(f"The output of the command was [{err.output}]")
        raise

CHECK_SPARK_HOME = """
if [ -z "$SPARK_HOME" ]; then
   echo "Error: SPARK_HOME is not set, can't run tests."
   exit -1
fi
"""
os.system(CHECK_SPARK_HOME)

# Dynamically load project root dir and jars.
project_root = f"{os.getcwd()}/../"
jars = run_cmd(f"ls {project_root}/target/sparkts*jar-with-dependencies.jar")

# Set environment variables.
os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = f"--jars {jars} --driver-class-path {jars} pyspark-shell"

os.environ["SPARK_CONF_DIR"] = f"{os.getcwd()}/test/resources/conf"


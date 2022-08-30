import os

from snakemake import shell


config = snakemake.config["sequana_taxonomy"]

outdir = snakemake.output.html.split("/",1)[0]
cmd = "sequana_taxonomy --file1 {snakemake.input[0]} "

confidence = config['confidence']
level = config['level']

if snakemake.params.paired:
    cmd += " --file2 {snakemake.input[1]} "

if confidence != 0:
    cmd += " --confidence {confidence} "

cmd += " --thread {snakemake.threads} --databases"
for this in config['databases']:
    if this != "toydb":
        assert os.path.exists(this), f"databases {this} does not exits"
    cmd += f" {this} "
cmd += " --output-directory {snakemake.wildcards.sample} --level {level}"

# we will save the unclassified files whatsover
if config['store_unclassified']:
    if snakemake.params.paired:
        cmd += " --unclassified-out unclassified#.fastq"  # this syntax replaces # with 1 and 2
    else:
        cmd += " --unclassified-out unclassified.fastq"
cmd += config['options']

# even tough we do not save the unclassified, we want to create a dummy 
# file since this ouptut file is expected.
cmd += f" && touch {snakemake.output.unclassified}"
shell(cmd)

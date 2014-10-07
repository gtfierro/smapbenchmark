sMAP Benchmark
==============

1. Quick/dirty scripts for sMAP benchmarking
2. (later) A better framework for benchmarking


## Setup

Currently, we assume that you've setup an archiver before hand. Setup scripts
to do this automatically are provided in the `setup/` directory. Running the
script as `. giles.sh` or `. archiver.sh` will install/start a Giles archiver
or UnitOfTime archiver respectively. The UnitOfTime archiver will still require
the user to create a superuser and a valid API key through the powerdb2
interface.

Once that's done, we can fillout a section in the configuration file
`config.ini` to setup a benchmark session.

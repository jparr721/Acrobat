# Stor v1.0.0
🦑 StÖr - A quick, lean ORM to store and analyze data trends from receipts CLI tool

## Usage
### Requirements
* Go version >= 1.9
* Postgres 10

### Running
To run, simply compile with `go build`, then run one of the following:

`./Stor -n` to generate your new database tables

`./Stor --reset` to drop and remake your tables for you

### Coming soon
* Goroutine support for concurrent receipt processing. Right now if you send more than 10 receipts at once the whole server throws a fit.

package main

import "flag"

const (
	databaseHost     = "localhost"
	databasPort      = 5432
	databaseUser     = "receipts"
	databasePassword = "receipts"
	databaseName     = "stor"
)

func main() {
	newInstall := flag.Bool("-n", false, "Generates a new instance of the database on this server.")
	resetInstall := flag.Bool("--reset", false, "Resets the existing instance (drops tables and remakes them)")
	s := Server{}
	s.Initialize(
		databaseUser,
		databasePassword,
		databaseName)

	flag.Parse()

	if *resetInstall {
		s.resetInstance()
		s.Run(":80")
	} else if *newInstall {
		s.newInstance()
		s.Run(":80")
	} else {
		s.Run(":80")
	}
}

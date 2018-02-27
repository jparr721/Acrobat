package main

const (
	databaseHost     = "localhost"
	databasPort      = 5432
	databaseUser     = "receipts"
	databasePassword = "receipts"
	databaseName     = "stor"
)

func main() {
	s := Server{}
	s.Initialize(
		databaseUser,
		databasePassword,
		databaseName)

	s.Run(":80")
}

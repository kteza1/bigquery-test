package main

import (
	"fmt"

	journal "github.com/coreos/go-systemd/sdjournal"
)

func main() {
	fmt.Println("Hello World")

	var err error
	j, err := journal.NewJournal()

	if err != nil {
		fmt.Println("Error creating journal handle")
		return
	}

	for {
		n, err := j.Next()

		if err != nil {
			fmt.Println("Error going to next record")
			return
		}

		if n == 0 {
			j.Wait(journal.IndefiniteWait)
			continue
		}

		r, err := j.GetEntry()

		if err != nil {
			fmt.Println("Error getting next record")
		}

		fmt.Println(r)
	}
}

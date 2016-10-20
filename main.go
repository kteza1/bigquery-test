package main

import (
	"fmt"

	journal "github.com/coreos/go-systemd/sdjournal"
	"github.com/kteza1/bigquery-test/sender"
)

func main() {
	var err error
	j, err := journal.NewJournal()

	if err != nil {
		fmt.Println("Error creating journal handle")
		return
	}

	var bqSender = sender.NewBQSender("crested-return-122311", "bq_testing", "can")

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

		var batch = sender.NewBatch("can")
		for i := 0; i < 50; i++ {
			batch.Append(r.Fields)
		}

		bqSender.Send(&batch)
	}
}

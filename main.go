package main

import (
	"fmt"
	"strings"
	"time"

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
		var batch = sender.NewBatch("can")
		for i := 0; i < 50; i++ {
			n, err := j.Next()

			if err != nil {
				fmt.Println("Error going to next record")
				return
			}

			if n == 0 {
				j.Wait(10 * time.Second)

				if batch.Timeout(10*time.Second) && batch.Len() > 0 {
					break
				}
				continue
			}

			record, err := j.GetEntry()

			if record.Fields["CHANNEL"] != "canFrame" {
				continue
			}

			// Creating a transformed record with all the requered fields
			var transRecord = make(map[string]string)
			for key, val := range record.Fields {
				transRecord[strings.ToLower(key)] = val
			}
			transRecord["bike_id"] = "s340-bq-test-1"
			transRecord["cursor_id"] = record.Cursor

			batch.Append(transRecord)
		}

		go bqSender.Send(&batch)
	}
}

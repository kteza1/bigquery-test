package sender

import "time"

// A Batch of messages to send
type Batch struct {
	Key         string
	Messages    []map[string]string
	LastUpdated time.Time
}

func NewBatch(key string) Batch {
	return Batch{
		Key:         key,
		Messages:    make([]map[string]string, 0),
		LastUpdated: time.Now(),
	}
}

func (batch *Batch) Append(record map[string]string) {
	batch.Messages = append(batch.Messages, record)
	batch.LastUpdated = time.Now()
}

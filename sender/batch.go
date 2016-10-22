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

func (batch *Batch) Timeout(timeout time.Duration) bool {
	if time.Since(batch.LastUpdated).Seconds() >= timeout.Seconds() {
		return true
	} else {
		return false
	}
}

func (batch *Batch) Len() int {
	return len(batch.Messages)
}

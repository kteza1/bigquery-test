package sender

import (
	"bytes"
	"errors"
	"net/http"
	"os"
	"time"

	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"

	"github.com/AtherEnergy/messaging-mqtt-client/helpers"
	log "github.com/Sirupsen/logrus"
	metrics "github.com/armon/go-metrics"
	bigquery "google.golang.org/api/bigquery/v2"
)

const (
	bqCallerKey = "bq_sender"
	insertIdKey = "cursor_id"
	bqScope     = bigquery.BigqueryInsertdataScope
)

// BQSender Sends data to BigQuery's tables directly using their HTTP API
type BQSender struct {
	service   *bigquery.Service
	datasetID string
	logger    *log.Entry
	projectID string
	name      string
}

// NewBQSender Create a new instance of the Sender
func NewBQSender(projectID string, datasetID string, table string) *BQSender {
	var err error
	var logFile *os.File
	logFile, err = os.OpenFile("/tmp/bq_test.log", os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)

	if err != nil {
		panic("Couldn't create log file")
	}

	// Output to stderr instead of stdout, could also be a file.
	log.SetOutput(logFile)
	// Only log the warning severity or above.
	log.SetLevel(log.WarnLevel)

	var service = GetBQService()
	return &BQSender{
		name:      "testing",
		projectID: projectID,
		datasetID: datasetID,
		logger: log.WithFields(log.Fields{
			"name":   "testing",
			"sender": "bigquery",
		}),
		service: service,
	}
}

// Send send a batch of messages to a single table
func (sender *BQSender) Send(batch *Batch) error {
	sender.logger.Infof("Sending batch with key %s and value %v", batch.Key, batch.Messages)
	start := time.Now()
	defer metrics.MeasureSince([]string{bqCallerKey, "send_batch_" + batch.Key}, start)
	var rows []*bigquery.TableDataInsertAllRequestRows
	for _, message := range batch.Messages {
		// Don't use unique insert id (cursor) for can parsed
		if batch.Key == "can_parsed" {
			rows = append(rows, sender.getInsertRow(message, ""))
		} else {
			rows = append(rows, sender.getInsertRow(message, message[insertIdKey]))
		}
	}
	request := &bigquery.TableDataInsertAllRequest{
		IgnoreUnknownValues: true,
		SkipInvalidRows:     false,
		Rows:                rows,
	}
	return sender.insertRows(batch.Key, request)
}

func (sender *BQSender) getInsertRow(msg map[string]string, insertID string) *bigquery.TableDataInsertAllRequestRows {
	jsonMessage := make(map[string]bigquery.JsonValue)
	for key, value := range msg {
		jsonMessage[key] = value
	}
	return &bigquery.TableDataInsertAllRequestRows{InsertId: insertID,
		Json: jsonMessage}
}

func (sender *BQSender) insertRows(tableName string, tableDataInsertAllRequest *bigquery.TableDataInsertAllRequest) error {
	sender.logger.Debugf("Inserting rows %v", tableDataInsertAllRequest.Rows)
	var insertResponse, err = sender.service.Tabledata.InsertAll(sender.projectID, sender.datasetID, tableName, tableDataInsertAllRequest).Do()
	if err != nil {
		sender.logger.Errorf("Unable to insert message in table %s. Error: %v", tableName, err)
		return err
	}
	if len(insertResponse.InsertErrors) != 0 {
		sender.logger.Errorln("Got errors when trying to insert into big query table", tableName)
		var buffer bytes.Buffer
		for _, insertErr := range insertResponse.InsertErrors {
			for _, protError := range insertErr.Errors {
				//return the last error
				sender.logger.Errorf("Insert error %s %s %s", protError.Message, protError.Reason, protError.DebugInfo)
				buffer.WriteString(protError.Message)
			}
		}
		return errors.New(buffer.String())
	}
	return nil
}

// GetBQService Returns a new instance of the BQ Service
func GetBQService() *bigquery.Service {
	var err error
	var client *http.Client
	var bqService *bigquery.Service

	client, err = google.DefaultClient(context.Background(), bqScope)
	helpers.Check(err)

	bqService, err = bigquery.New(client)
	helpers.Check(err)

	return bqService
}

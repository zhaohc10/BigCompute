package main

import (
	"log"
	"net/http"
	"strconv"
	"encoding/json"
	"math/rand"
)

const STATS_PORT = 3000

func main() {
	log.Println("stats server started, listening on port", STATS_PORT)

	http.HandleFunc("/stats/", func (res http.ResponseWriter, req *http.Request) {
		log.Println("incoming new stats request")

		if req.Method != http.MethodGet {
			res.WriteHeader(http.StatusNotImplemented)
			return
		}

		log.Println("handling new stats request")

		body, _ := json.Marshal(struct {
			Service string `json:"service"`
			Value float64 `json:"value"`
		}{
			"service",
			rand.Float64(),
		})

		log.Println("new stats: ", string(body))

		res.Write([]byte(body))
	})

	http.ListenAndServe(":" + strconv.Itoa(STATS_PORT), nil)
}
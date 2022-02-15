package main
import (
        "log"
        "net/http"
        "os"
        "os/exec"
)

func main() {
	log.Print("Starting server...")
	http.HandleFunc("/", scriptHandler)

	// Determine port for HTTP service.
	port := os.Getenv("PORT")
	if port == "" {
			port = "8080"
			log.Printf("Defaulting to port %s", port)
	}

	// Start HTTP server.
	log.Printf("Listening on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
			log.Fatal(err)
	}
}

func scriptHandler(w http.ResponseWriter, r *http.Request) {
	log.Print("Received a request...")
	cmd := exec.CommandContext(r.Context(), "/bin/bash", "dbt_script.sh")
	cmd.Stderr = os.Stderr
	out, err := cmd.Output()
	if err != nil {
			w.WriteHeader(500)
	}
	log.Print(string(out))
	w.Write(out)
}
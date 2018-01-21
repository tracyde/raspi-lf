package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"syscall"
)

const assets = "/assets"

// Status holds the global status of running programs
type Status struct {
	Running bool
	Status  string
	Program string
	Pid     int
}

// Page holds values required to fill in templates
type Page struct {
	Assets   string
	Language string
	Status   Status
}

// Helper functions
func runProg(program string, cmd string, args string, status *Status) {
	if status.Running {
		log.Printf("error: another program is running, unable to execute!\n")
		return
	}
	status.Running = true
	status.Program = program
	status.Status = "Starting"

	c := exec.Command(cmd, args)
	err := c.Start()
	if err != nil {
		log.Printf("error: problem occurred while starting %s, %s\n", program, err)
		status.Status = fmt.Sprintf("Error: %s", err)
		return
	}
	status.Pid = c.Process.Pid
	status.Status = "Running"
	log.Printf("info: running %s using pid %d\n", program, status.Pid)
	err = c.Wait()
	if err != nil {
		if status.Status == "Stopping" {
			return
		}
		log.Printf("error: problem occurred while running %s, %s\n", program, err)
		status.Status = fmt.Sprintf("Error: %s", err)
		return
	}
	status.Status = "Finished"
	status.Running = false
}

func killProg(program string, status *Status) {
	if !status.Running {
		log.Printf("error: no program is running, nothing to kill!\n")
		return
	}

	if status.Program != program {
		log.Printf("error: program is not running\n")
		return
	}

	log.Printf("info: killing program %s with pid %d\n", program, status.Pid)
	status.Status = "Stopping"

	p, err := os.FindProcess(status.Pid)
	if err != nil {
		log.Printf("error: unable to find process %d - %s\n", status.Pid, err)
		return
	}

	err = p.Signal(syscall.SIGINT)
	if err != nil {
		log.Printf("error: unable to send SIGINT to pid %d - %s\n", p.Pid, err)
		return
	}

	_, err = p.Wait()
	if err != nil {
		log.Printf("error: could not wait for program to exit - %s\n", err)
		return
	}

	status.Running = false
	status.Status = "Killed"
}

func main() {
	log.Printf("info: initializing server...")
	status := &Status{Running: false}

	// Handler for all static assets
	http.Handle("/assets/", http.StripPrefix("/assets/", http.FileServer(http.Dir("./assets"))))

	// Handler for '/run/{langauage}/{prog}'
	http.HandleFunc("/run/", func(w http.ResponseWriter, req *http.Request) {
		l := strings.Split(req.URL.Path, "/")[2]
		ext := ""
		interpreter := ""
		switch l {
		case "python":
			ext = ".py"
			interpreter = "/usr/bin/python"
		case "golang":
			ext = ".go"
			interpreter = "/usr/bin/python"
		default:
			http.NotFound(w, req)
			return
		}

		p := ""
		stop := false
		if len(strings.Split(req.URL.Path, "/")) >= 4 {
			p = strings.Split(req.URL.Path, "/")[3]
			if len(strings.Split(req.URL.Path, "/")) > 4 {
				stop = true
			}
		}

		if p != "" {
			prog := l + "/" + p
			switch p {
			case "follower":
				if stop {
					go killProg(prog, status)
				} else {
					go runProg(prog, interpreter, prog+ext, status)
				}
			case "motor_driver-test":
				if stop {
					go killProg(prog, status)
				} else {
					go runProg(prog, interpreter, prog+ext, status)
				}
			case "tracking_sensor-test":
				if stop {
					go killProg(prog, status)
				} else {
					go runProg(prog, interpreter, prog+ext, status)
				}
			default:
				http.NotFound(w, req)
				return
			}
			http.Redirect(w, req, fmt.Sprintf("/run/%s", l), 302)
		}

		// Load template file and display output
		t, _ := template.ParseFiles("templates/lang.html")
		t.Execute(w, &Page{Assets: assets, Language: l, Status: *status})
	})

	// Handler for web root
	http.HandleFunc("/", func(w http.ResponseWriter, req *http.Request) {
		// The "/" pattern matches everything, so we need to check
		// that we're at the root here.
		if req.URL.Path != "/" {
			http.NotFound(w, req)
			return
		}

		// Load template file and display output
		t, _ := template.ParseFiles("templates/index.html")
		t.Execute(w, &Page{Assets: assets})
	})

	log.Printf("info: starting server...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

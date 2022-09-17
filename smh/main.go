package main

import (
	"log"

	"golang.org/x/crypto/ssh"
	"golang.org/x/crypto/ssh/knownhosts"
)

func main() {
	// ssh config
	hostKeyCallback, err := knownhosts.New("/home/agriffin/.ssh/known_hosts")
	if err != nil {
		log.Fatal(err)
	}
	config := &ssh.ClientConfig{
		User: "agriffin",
		Auth: []ssh.AuthMethod{
			ssh.Password("Y*FNDrn8quNQ.Bq-"),
		},
		HostKeyCallback: hostKeyCallback,
	}
	// connect ot ssh server
	conn, err := ssh.Dial("tcp", "wea.smartaira360.com:22", config)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
}

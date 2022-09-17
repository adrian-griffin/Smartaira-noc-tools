package main

import (
	"log"

	"golang.org/x/crypto/ssh"
	"golang.org/x/crypto/ssh/knownhosts"
)

func main() {
	// ssh config
	hostKeyCallback, err := knownhosts.New("~/.ssh/known_hosts")
	if err != nil {
		log.Fatal(err)
	}
	config := &ssh.ClientConfig{
		User: "ubuntu",
		Auth: []ssh.AuthMethod{
			ssh.Password("password"),
		},
		HostKeyCallback: hostKeyCallback,
	}
	// connect ot ssh server
	conn, err := ssh.Dial("tcp", "wea.smartaira360.com", config)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
}

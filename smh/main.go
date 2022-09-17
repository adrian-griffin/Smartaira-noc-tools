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
		User: "root",
		Auth: []ssh.AuthMethod{
			ssh.Password("TfoK%55s2#&24%!a"),
		},
		HostKeyCallback: hostKeyCallback,
	}
	// connect ot ssh server
	conn, err := ssh.Dial("tcp", "137.184.3.254:22", config)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
}

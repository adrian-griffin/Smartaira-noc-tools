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

	session, err := conn.NewSession()
	if err != nil {
		log.Fatal(err)
	}
	defer session.Close()


	    // configure terminal mode
		modes := ssh.TerminalModes{
			ssh.ECHO:          0,     // supress echo
	
		}
		// run terminal session
		if err := session.RequestPty("xterm", 50, 80, modes); err != nil {
			log.Fatal(err)
		}
		// start remote shell
		if err := session.Shell(); err != nil {
			log.Fatal(err)
		}


	var buff bytes.Buffer
	session.Stdout = &buff
	if err := session.Run(“ls -la”); err != nil {
		log.Fatal(err)
	}
	fmt.Println(buff.String())

}

package models

import (
    _ "github.com/lib/pq"
    "database/sql"
)

type Database struct {
	*sql.DB
}

type Connection struct {
	host		string
	port		string
	user		string
	password	string
	dbname		string
}


type Accessor interface {
	PrepareConnection()
}

type Post struct {
	postID	string
	title	string
	body	string
}

type Visitor struct {
	visitorID		string
	Connection
}

func (v Visitor) PrepareConnection() {
	// TODO: use env vars, vault, or something else
	p.conn_string := `
		host = localhost
		port= 5432
		user = pseudoweb_visitor
		password = $$password$$
		dbname = pseudoweb`
}

func (a Accessor) Connect() (*Database, error) {
	db, err := sql.Open("postgres", a.conn_string)
	if err != nil {
		return nil, err
	}
	if err = db.Ping(); err != nil {
		return nil, err
	}
	return &Database{db}, nil
}

func PrepareStatement(command string, table string) (string) {
	statement := "none"
	statements := map[string]map[string]string{
		"insert": map[string]string{
			"users": `
				INSERT INTO users (userID, username, hashedPW)
				VALUES ($1, $2, $3, $4);`,
			"posts": `
				INSERT INTO posts (userID, post);`,
		},
		"select": map[string]string{
			"posts": `
				SELECT * FROM posts;`,
		},
	}
	for cmd, tbl := range statements {
		if cmd == command {
			for tbl, st := range tbl {
				if tbl == table {
					statement = st
				}
			}
		}
	}
	return statement
}

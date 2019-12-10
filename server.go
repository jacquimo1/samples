package main

import (
	"html/template"
	"net/http"
	"fmt"
	"log"

)


var userMessages []userMessage

type userMessage struct {
	handle		string
	body		string
} 
// ---	Form validation

type validity interface {
	validLength() 		bool
	invalidLength()		string
}

type field struct {
	value	string
	valid	bool
}

type username struct {
	field
}

type password struct {
	field
}

func (u username) validLength() bool {
	if len(u.field.value) > 2 && len(u.field.value) < 50 {
		return true
	}
	return false
}

func (u username) invalidLength() string {
	return "Username must be between three and fifty characters."
}

func (p password) validLength() bool {
	if len(p.field.value) > 8 && len(p.field.value) < 80 {
		return true
	}
	return false
}

func (p password) invalidLength() string {
	return "Password must be between nine and fifty characters."
}

func setMessages(field_name string, messages []string, v validity) {
	if !v.validLength() {
		messages = append(messages, v.invalidLength())
	}
}

func confirmPassword(p1 string, p2 string) bool {
	if p1 == p2 {
		return true
	}
	return false
}

func passwordMismatch() string {
	return "Passwords do not match."
}


func validate(form map[string][]string) []string {
	var (
		messages []string
		p string
	)
	for field_name, field_value := range form {
		switch field_name {
		case "username":
			setMessages(field_name, messages,  username{field{value: field_value[0]}})
		case "password":
			setMessages(field_name, messages,  password{field{value: field_value[0]}})
			p = field_value[0]
		case "password-confirmation":
			if !confirmPassword(p, field_value[0]) {
				messages = append(messages, passwordMismatch())
			}
		}
	}
	fmt.Println(messages)
	return messages
}

func register(w http.ResponseWriter, r *http.Request) {
	//data := map[string]string{}
	var data []string
	switch r.Method {
	case "POST":
		r.ParseForm()
		data = validate(r.Form)
		fallthrough
	case "GET":
		// if logged in redirect
		tmpl := template.Must(template.ParseFiles("register.html"))
		tmpl.Execute(w, data)
	default:
		fmt.Println("404: neither get nor post")
	}
}

func messenger(r *http.Request) []userMessage {
	var	(
		data 	[]userMessage
		message	userMessage
	)
	message.handle 	= r.FormValue("handle-field")
	message.body	= r.FormValue("chat-message-field")
	data = append(data, message)
	return data
}

func index(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		r.ParseForm()
		data := messenger(r)
		for _, m := range data {
			userMessages = append(userMessages, m)
			fmt.Println(m.handle, " -> ", m.body)
		}
		fallthrough
	case "GET":
		// if logged in redirect
		tmpl := template.Must(template.ParseFiles("index.html"))
		tmpl.Execute(w, userMessages)
	default:
		fmt.Println("404: neither get nor post")
	}
}

func main() {
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("static"))))
	http.HandleFunc("/register", register)
	http.HandleFunc("/", index)
	err := http.ListenAndServe(":4444", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

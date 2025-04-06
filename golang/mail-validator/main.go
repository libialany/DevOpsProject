package main

import (
    "fmt"
    "net/http"
    "strings"
    "net"
)

func main() {
    http.HandleFunc("/", homePage)
    http.ListenAndServe(":8080", nil)
}

func homePage(w http.ResponseWriter, r *http.Request) {
    if r.Method == http.MethodPost {
        r.ParseForm()
        name := r.FormValue("name")
        res := check_domain(name)
        if res == false {
            fmt.Fprintf(w, "Is not a valid email: %s", name) // Added %s for formatting
            return
        }
        fmt.Fprintf(w, "Congratulations! is a valid email: %s", name) // Added %s for formatting
        return
    }
    fmt.Fprintf(w, `
        <html>
            <body>
                <form method="POST">
                    Name: <input type="text" name="name">
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    `)
}

func isValidEmailDomain(email string) (bool, error) {
    // Split the email to get the domain
    parts := strings.Split(email, "@")
    if len(parts) != 2 {
        return false, fmt.Errorf("invalid email format")
    }
    domain := parts[1]
    mxRecords, err := net.LookupMX(domain)
    if err != nil {
        return false, err
    }

    return len(mxRecords) > 0, nil
}


func check_domain(email string) bool { // Added return type string
    valid, err := isValidEmailDomain(email)
    if err != nil {
        fmt.Println("Error:", err)
        return false
    }

    if valid {
        return true
    } else {
        return false
    }
}
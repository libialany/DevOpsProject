package main
import (
	"fmt"
	"log"
	"encoding/json"
	"math/rand"
	"net/http"
	"strconv"
	"github.com/gorilla/mux"
)

type Book struct {
	ID string `json:"id"`
	Title string `json:"title"`
	Category string `json:"category"`
	Author *Author `json:"author"`
}

type Author struct {
	ID string `json:"id"`
	Name string `json:"name"`
	Age int `json:"age"`
}

var books []Book

func setJSONContentType(w http.ResponseWriter){
	w.Header().Set("Content-Type", "application/json")
}

func getBooks(w http.ResponseWriter, r *http.Request){
	setJSONContentType(w)
	json.NewEncoder(w).Encode(books)
}

func deleteBook(w http.ResponseWriter, r *http.Request){
	setJSONContentType(w)
	params := mux.Vars(r)
	for index, item := range books {
		if item.ID == params["id"] {
			books = append(books[:index], books[index+1:]...)
			break
		}
	}
	json.NewEncoder(w).Encode(books)
}

func getBook(w http.ResponseWriter, r *http.Request){
	setJSONContentType(w)
	params := mux.Vars(r)
	for _, item := range books {
		if item.ID  == params["id"] {
			json.NewEncoder(w).Encode(item)
			return
		}
	}
}

func createBook(w http.ResponseWriter, r *http.Request){
	setJSONContentType(w)
	var book Book
	_ = json.NewDecoder(r.Body).Decode(&book)
	book.ID = strconv.Itoa(rand.Intn(100000000))
	books = append(books, book)
	json.NewEncoder(w).Encode(book)
}

func updateBook(w http.ResponseWriter, r *http.Request){
	setJSONContentType(w)
	params := mux.Vars(r)

	for index, item := range books {
		if item.ID == params["id"] {
			books = append(books[:index], books[index+1:]...)
			var book Book
			_ = json.NewDecoder(r.Body).Decode(&book)
			book.ID = params["id"]
			books = append(books, book)
			json.NewEncoder(w).Encode(book)
			return
		}
	}
}

func main(){
	r:= mux.NewRouter()

	r.HandleFunc("/books", getBooks).Methods("GET")
	r.HandleFunc("/books/{id}", getBook).Methods("GET")
	r.HandleFunc("/books", createBook).Methods("POST")
	r.HandleFunc("/books/{id}", updateBook).Methods("PUT")
	r.HandleFunc("/books/{id}", deleteBook).Methods("DELETE")
	
	fmt.Printf("Starting server at port 8080\n")
	log.Fatal(http.ListenAndServe(":8000",r))
}
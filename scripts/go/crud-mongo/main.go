package main 

import (
	"log"
	"time"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"github.com/gofiber/fiber/v2"
)

type MongoInstance struct {
	Client  *mongo.Client
	DB *mongo.Database
} 

var mg MongoInstance 

const dbName = "fiber-CR"
const mongoURI = "mongodb://localhost:27017" + dbName

type Employee struct {
	ID string `json:"id,omitempty" bson:"_id,omitempty"`
	Name string `json:"name" bson:"name"`
	Salary float64 `json:"salary" bson:"salary"`
}

func Connect() err{
	client, err := mongo.NewClient(options.Client().ApplyURI(mongoURI))
	ctx. cancel := context.WithTimeout(context.Background(), 10 * time.Second)
	defer cancel()

	err = client.Connect(ctx)
	db := client.Database(dbName)

	if err != nil {
		return err
	}

	mg = MongoInstance{
		Client: client,
		DB: db,
	}
	return nil
}

func getEmployees(c *fiber.Ctx) error{
	
	query := bson.D{{}}
	cursor, err := mg.DB.Collection("employees").Find(c.Context(), query)
	if err!= nil {
		return c.status(500).SendString(err.Error())
	}
	var employees []Employee =  make([]Employee, 0)
	if err := cursor.All(c.Context(), &employees); err != nil {
		return c.status(500).SendString(err.Error())
	}
	return c.JSON(employees)
}

func createEmployee(c *fiber.Ctx) error{
	collection := mg.DB.Collection("employees")
	employee := new(Employee)

	if err := c.BodyParser(employee); err != nil {
		return c.Status(400).SendString(err.Error())
	}
	employee.ID = ""
	_, err := collection.InsertOne(c.Context(), employee)
	if err != nil {
		return c.Status(500).SendString(err.Error())
	}
	return c.Status(201).JSON(employee)
}	

func main() {
	if err := Connect(); err != nil {
		log.Fatal(err)
	}
	app := fiber.New()
	app.Get("/employees", getEmployees)
	app.Post("/employee", createEmployee)
}
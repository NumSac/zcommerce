package types

import (
	"time"
)

// User represents a user with a shopping cart.
type User struct {
	Username     string             `json:"username"`
	PasswordHash string             `json:"password_hash"`
	SignUpDate   time.Time          `json:"sign_up_date"` // time.Time is the Go equivalent to Python's datetime
	FirstName    string             `json:"firstname"`
	LastName     string             `json:"lastname"`
	ShoppingCart []ShoppingCartItem `json:"shopping_cart"`
}

// Company represents company details.
type Company struct {
	RegistrationNumber     string `json:"registration_number"`
	CompanyName            string `json:"company_name"`
	CompanyEmail           string `json:"company_email"`
	CompanyBackgroundImage string `json:"company_background_image"`
	CompanyDescription     string `json:"company_description"`
}

// Product represents product details.
type Product struct {
	ProductID string `json:"product_id"`
	Category  string `json:"category"`
}

// ProductCategory represents a category of products.
type ProductCategory struct {
	Category string    `json:"category"`
	Products []Product `json:"products"`
}

// ShoppingCartItem represents an item in a shopping cart.
type ShoppingCartItem struct {
	ProductID string `json:"product_id"`
	Quantity  int    `json:"quantity"`
	// Add more fields as necessary, e.g., price, name, etc.
}

// ShoppingCart represents a user's shopping cart.
type ShoppingCart struct {
	Username string             `json:"username"` // Assuming this is the identifier linking the cart to a user
	Items    []ShoppingCartItem `json:"items"`
}
